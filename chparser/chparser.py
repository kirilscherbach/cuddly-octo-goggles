import argparse
import configparser
import os
import json

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
        intensity_bass=-1,
        intensity_bass_real=-1,
        intensity_bassghl=-1,
        intensity_drums=-1,
        intensity_drums_real=-1,
        intensity_drums_phase_shift=-1,
        intensity_guitar=-1,
        intensity_guitar_coop=-1,
        intensity_guitar_coop_ghl=-1,
        intensity_guitar_real=-1,
        intensity_guitarghl=-1,
        intensity_keys=-1,
        intensity_keys_real=-1,
        intensity_keys_phase_shift=-1,
        intensity_rhythm=-1,
        intensity_rhythm_ghl=-1,
    ):
        self.song_title = song_title
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year
        self.song_length = song_length
        self.charter = charter
        self.intensity_bass = intensity_bass
        self.intensity_bass_real = intensity_bass_real
        self.intensity_bassghl = intensity_bassghl
        self.intensity_drums = intensity_drums
        self.intensity_drums_real = intensity_drums_real
        self.intensity_drums_phase_shift = intensity_drums_phase_shift
        self.intensity_guitar = intensity_guitar
        self.intensity_guitar_coop = intensity_guitar_coop
        self.intensity_guitar_coop_ghl = intensity_guitar_coop_ghl
        self.intensity_guitar_real = intensity_guitar_real
        self.intensity_guitarghl = intensity_guitarghl
        self.intensity_keys = intensity_keys
        self.intensity_keys_real = intensity_keys_real
        self.intensity_keys_phase_shift = intensity_keys_phase_shift
        self.intensity_rhythm = intensity_rhythm
        self.intensity_rhythm_ghl = intensity_rhythm_ghl

    def __repr__(self):
        return f"Song(title={self.song_title}, artist={self.artist})"

    def __str__(self) -> str:
        return f"Song(title={self.song_title}, artist={self.artist})"
    
    def to_json(self):
        return json.dumps(self.__dict__, indent=2)

def convert_int(s):
    try:
        i = int(s)
    except ValueError:
        i = -1
    return i

def extract_song_ini_properties(filepath):
    parser = configparser.ConfigParser(strict=False)
    parser.read(filepath)
    song_properties = {}

    if parser.has_section("Song"):
        section = parser["Song"]
    else:
        section = parser["song"]

    # Extract mandatory and optional properties
    song_properties["song_title"] = section["name"]
    optional_keys = ["artist", "album", "genre", "year", "song_length", "charter"]
    intensity_keys = {
        "diff_bass": "intensity_bass",
        "diff_bass_real": "intensity_bass_real",
        "diff_bass_real_22": "intensity_bass_real",
        "diff_bassghl": "intensity_bassghl",
        "diff_drums": "intensity_drums",
        "diff_drums_real": "intensity_drums_real",
        "diff_drums_real_ps": "intensity_drums_phase_shift",
        "diff_guitar": "intensity_guitar",
        "diff_guitar_coop": "intensity_guitar_coop",
        "diff_guitar_coop_ghl": "intensity_guitar_coop_ghl",
        "diff_guitar_real": "intensity_guitar_real",
        "diff_guitar_real_22": "intensity_guitar_real",
        "diff_guitarghl": "intensity_guitarghl",
        "diff_keys": "intensity_keys",
        "diff_keys_real": "intensity_keys_real",
        "diff_keys_real_ps": "intensity_keys_phase_shift",
        "diff_rhythm": "intensity_rhythm",
        "diff_rhythm_ghl": "intensity_rhythm_ghl"
        #"diff_vocals": 2676,
        #"diff_vocals_harm": 2599,
    }





    for key in optional_keys:
        if key in section:
            song_properties[key] = section[key]

    for ini_key, intensity_key in intensity_keys.items():
        if ini_key in section:
            song_properties[intensity_key] = convert_int(section[ini_key])
    return song_properties, section.keys()


def find_song_folders(base_folder):
    for root, dirs, files in os.walk(base_folder):
        if "song.ini" in files:
            yield root


def scan_songs(base_folder):
    songs = []
    song_count = 0
    key_frequency = {}      
    for song_folder in find_song_folders(base_folder):
        song_ini_path = os.path.join(song_folder, "song.ini")
        try:
            #print(f"Trying to scan song in {song_folder}")
            song_properties, keys = extract_song_ini_properties(song_ini_path)
            #print("INI file parsed successfully")
            song = Song(**song_properties)
            songs.append(song.__dict__)
            for key in keys:
                key_frequency[key] = key_frequency.get(key, 0) + 1
        except Exception as e:
            print(f"Could not parse song in folder {song_folder}")
            raise e
        finally:
            song_count += 1

    # Now you have a list of Song objects
    print(f"Attempted to parse {song_count} songs")
    print(f"{len(songs)} songs successfully parsed")
    print(key_frequency)
    with open("output.json", "w") as file:
        file.write(json.dumps(songs, indent=2))
        print("Written songs to output.json")


def main():
    parser = argparse.ArgumentParser(description="Parser for Clone Hero songs.")
    parser.add_argument(
        "-b",
        "--base_folder",
        type=str,
        help="Path to the base folder containing song folders.",
    )
    args = parser.parse_args()
    base_folder = args.base_folder
    print(f"Scanning songs in {base_folder}\n")
    scan_songs(base_folder)


if __name__ == "__main__":
    main()
