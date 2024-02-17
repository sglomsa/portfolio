import json
from pathlib import Path


def read_json_data(file_path):
    """Reads and returns the contents of a JSON file"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def write_json_data(file_path, data):
    """Writes data to a JSON file"""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_game_dir_path() -> str:
    """Gets the user-set path for the
    Red Dead Redemption 2 game directory
    """
    data = read_json_data(get_root() / "directories.json")
    return data["gameDirectory"]


def get_profiles_dir_path() -> str:
    """Gets the user-set path for the profiles directory"""
    data = read_json_data(get_root() / "directories.json")
    return data["profilesDirectory"]


def get_root() -> Path:
    """Gets the root directory"""
    return Path(__file__).parent.parent.parent
