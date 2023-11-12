import argparse
import configparser
import os


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

    def __str__(self) -> str:
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


def find_song_folders(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if "song.ini" in files and "notes.chart" in files:
            yield root


def scan_songs(base_folder):
    songs = []
    song_count = 0
    for song_folder in find_song_folders(base_folder):
        song_ini_path = os.path.join(song_folder, "song.ini")
        # notes_chart_path = os.path.join(song_folder, "notes.chart")
        try:
            print(f"Trying to scan song in {song_folder}")
            song_properties = extract_song_ini_properties(song_ini_path)
            print("INI file parsed successfully")

            song = Song(**song_properties)
            songs.append(song)
        except Exception as e:
            print(f"Could not parse song in folder {base_folder}")
            print(e)
        finally:
            song_count += 1

    # Now you have a list of Song objects
    print("\n\n".join([str(i) for i in songs]))
    print(f"Attempted to parse {song_count} songs")
    print(f"{len(songs)} songs successfully parsed")


def main():
    parser = argparse.ArgumentParser(description="Parser for Clone Hero songs.")
    parser.add_argument(
        "-b",
        "--base_folder",
        type=str,
        help="Path to the base folder containing song folders.",
    )
    args = parser.parse_args()
    base_folder = args.base_folder  # Change this to your folder path
    print(f"Scanning songs in {base_folder}\n")
    scan_songs(base_folder)


if __name__ == "__main__":
    main()
