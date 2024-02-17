import datetime
import json
import os
import shutil
from pathlib import Path

from . import utils


def set_game_dir(args):
    """Saves the path for the RDR2 game directory into 'directories.json'
    for use by other commands
    """
    path = Path(utils.get_root() / "directories.json")
    data = utils.read_json_data(path)
    data["gameDirectory"] = args.path_to_game_directory
    utils.write_json_data(path, data)


def print_game_dir():
    """Prints out the saved path for the RDR2 game directory,
    and provides instructions if it hasn't been set yet
    """
    try:
        print(utils.get_game_dir_path())
    except FileNotFoundError:
        print("The path to the RDR2 game directory has not been set!")
        print("Use 'set-game-directory' to set it.")


def create_profile(args, test=False, test_dir=""):
    """Creates a new profile in the 'profiles' folder
    with the given name and description
    """
    if test:
        profiles_dir_path = Path(test_dir)
    else:
        profiles_dir_path = Path(utils.get_profiles_dir_path())

    profile_path = profiles_dir_path / args.profile_name

    try:
        profile_path.mkdir(parents=True)
    except FileExistsError:
        print(f"There is already a profile called '{args.profile_name}'!")
    else:
        # fmt: off
        initial_data = {
            "profileName": args.profile_name,
            "metadata": {
                "creationDate": str(datetime.date.today()),
                "lastUpdated": str(datetime.date.today()),
                "description": args.description
                },
            "modDirectories": [],
            "modFiles": []
            }
        # fmt: on

        json_file_path = profile_path / "profile.json"
        with json_file_path.open("w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)


def list_profiles(test=False, test_dir=""):
    """Lists all the profiles in the 'profiles' folder"""
    if test:
        profiles_dir_path = Path(test_dir)
    else:
        profiles_dir_path = Path(utils.get_profiles_dir_path())
    profiles = os.listdir(profiles_dir_path)

    if profiles:
        print("YOUR PROFILES:")
        for profile in profiles:
            profile_json_path = Path(profiles_dir_path / profile / "profile.json")
            try:
                with profile_json_path.open("r") as file:
                    contents = file.read()
            except FileNotFoundError:
                print("\nThe profile.json file was not found in the profile")
                print("Creating a recovery file...")
                # Will create a recovery file
            else:
                profile_data = json.loads(contents)

                name = profile_data["profileName"]
                description = profile_data["metadata"]["description"]

                print(f"\nName: {name}")
                if description:
                    print(f"Description: {description}")
    else:
        print("You do not have any profiles!")


def print_version():
    """Prints the version of 'RDR2 Mod Profile Manager'"""
    print("Development stage")


def set_profiles_dir(args):
    """Saves the path to the directory where profiles should be saved"""
    path = Path(utils.get_root() / "directories.json")
    data = utils.read_json_data(path)
    data["profilesDirectory"] = args.path_to_profiles_directory
    utils.write_json_data(path, data)


def delete_profile(args, test=False, test_dir=""):
    """Deletes a profile, including all mods within it.
    It will request confirmation unless a flag is used (-y/--yes)
    """
    if test:
        profiles_path = test_dir
    else:
        profiles_path = utils.get_profiles_dir_path()
    if args.yes:
        try:
            shutil.rmtree(f"{profiles_path}/{args.profile_name}")
        except FileNotFoundError:
            print(f"'{args.profile_name}' does not exist.")
        else:
            print(f"Successfully deleted '{args.profile_name}'")
    else:
        prompt = "Are you sure you want to delete "
        prompt += f"'{args.profile_name}' including all its mods? (yes/no)\n> "
        confirmation = input(prompt)
        while confirmation.lower() != "yes" and confirmation.lower() != "no":
            prompt = "Invalid input. Please write either 'yes' or 'no'\n> "
            confirmation = input(prompt)
        if confirmation.lower() == "yes":
            try:
                shutil.rmtree(f"{profiles_path}/{args.profile_name}")
            except FileNotFoundError:
                print(f"'{args.profile_name}' does not exist.")
            else:
                print(f"Successfully deleted '{args.profile_name}'")
        else:
            print("Deletion cancelled")


def print_profiles_dir():
    """Prints out the saved path for the 'profiles' directory,
    and provides instructions if it hasn't been set yet
    """
    try:
        print(utils.get_profiles_dir_path())
    except FileNotFoundError:
        print("The path to the 'profiles' directory has not been set!")
        print("Use 'set-profiles-directory' to set it.")


def list_commands():
    """Lists all commands along with some help text"""
    commands = {
        "set-game_dir <path-to-game-directory>": "sets the RDR2 game directory",
        "list-profiles                       ": "list all profiles",
        "version                             ": "prints out the version of 'RDR2 Mod Profile Manager'",
        "...                                 ": "...",
    }
    for command, help in commands.items():
        print(f"{command}\t\t{help}")
