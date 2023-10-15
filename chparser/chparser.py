import os
import hashlib
import configparser


class Song:
    def __init__(
        self,
        song_title,
        artist=None,
        album=None,
        genre=None,
        year=None,
        song_length=None,
        charter=None,
        intensity={},
        difficulty={},
    ):
        self.song_title = song_title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year
        self.song_length = song_length
        self.charter = charter
        self.intensity = intensity
        self.difficulty = difficulty

    def __repr__(self):
        return f"Song(title={self.song_title}, artist={self.artist}, intensity={self.intensity}, difficulty={self.difficulty})"


def extract_song_ini_properties(filepath):
    parser = configparser.ConfigParser()
    parser.read(filepath)
    song_properties = {}

    # Extract mandatory and optional properties
    song_properties["song_title"] = parser["Song"]["name"]
    optional_keys = ["artist", "album", "genre", "year", "song_length", "charter"]
    intensity_keys = {
        "diff_guitar": "guitar",
        "diff_rhythm": "rhythm",
        "diff_bass": "bass",
        "diff_guitar_coop": "guitar_coop",
        "diff_drums": "drums",
        "diff_drums_real": "drums_real",
        "diff_guitarghl": "guitarghl",
        "diff_bassghl": "bassghl",
        "diff_rhythm_ghl": "rhythm_ghl",
        "diff_guitar_coop_ghl": "guitar_coop_ghl",
        "diff_keys": "keys",
    }

    for key in optional_keys:
        if key in parser["Song"]:
            song_properties[key] = parser["Song"][key]

    intensity = {}
    for ini_key, intensity_key in intensity_keys.items():
        if ini_key in parser["Song"]:
            intensity[intensity_key] = int(parser["Song"][ini_key])
    song_properties["intensity"] = intensity

    return song_properties


def extract_chart_difficulties(filepath):
    difficulty_mapping = {
        "ExpertSingle": "guitar_expert",
        "HardSingle": "guitar_hard",  # ... add all other mappings here ...
    }

    with open(filepath, "r") as f:
        content = f.read().split("[")

    difficulties = {}
    for section in content:
        for tag, difficulty in difficulty_mapping.items():
            if section.startswith(tag):
                instrument, level = difficulty.split("_")
                data = section.split("]")[1].strip()
                md5_hash = hashlib.md5(data.encode()).hexdigest()
                if instrument not in difficulties:
                    difficulties[instrument] = {}
                difficulties[instrument][level] = md5_hash

    return {"difficulty": difficulties}


def find_song_folders(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if "song.ini" in files and "notes.chart" in files:
            yield root


def main():
    base_folder = "/path/to/your/folder"  # Change this to your folder path
    songs = []

    for song_folder in find_song_folders(base_folder):
        song_ini_path = os.path.join(song_folder, "song.ini")
        notes_chart_path = os.path.join(song_folder, "notes.chart")

        song_properties = extract_song_ini_properties(song_ini_path)
        song_properties.update(extract_chart_difficulties(notes_chart_path))

        song = Song(**song_properties)
        songs.append(song)

    # Now you have a list of Song objects
    for song in songs:
        print(song)


if __name__ == "__main__":
    main()
