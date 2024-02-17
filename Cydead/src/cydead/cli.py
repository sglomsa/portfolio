import argparse

from . import commands as cmds

parser = argparse.ArgumentParser(prog="RDR2 Mod Profile Manager")
subparsers = parser.add_subparsers(dest="command")

print_game_dir_parser = subparsers.add_parser(
    "print-game-directory", help="prints out the path to the set RDR2 game directory"
)
print_game_dir_parser.set_defaults(func=cmds.print_game_dir)

set_game_dir_parser = subparsers.add_parser(
    "set-game-directory", help="specifies the RDR2 game directory"
)
set_game_dir_parser.add_argument(
    "path_to_game_directory", type=str, help="path to the game directory"
)
set_game_dir_parser.set_defaults(func=cmds.set_game_dir)

version_parser = subparsers.add_parser(
    "version", help="prints out the version of 'RDR2 Mod Profile Manager'"
)
version_parser.set_defaults(func=cmds.print_version)

list_commands_parser = subparsers.add_parser(
    "list-commands", help="list all commands")
list_commands_parser.set_defaults(func=cmds.list_commands)

create_profile_parser = subparsers.add_parser(
    "create-profile", help="create a new mod profile"
)
create_profile_parser.add_argument("profile_name", type=str)
create_profile_parser.add_argument(
    "-d", "--description", type=str, help="make a description of the profile"
)
create_profile_parser.set_defaults(func=cmds.create_profile)

list_profiles_parser = subparsers.add_parser(
    "list-profiles", help="list all existing profiles"
)
list_profiles_parser.set_defaults(func=cmds.list_profiles)

set_profiles_dir_parser = subparsers.add_parser(
    "set-profiles-directory", help="sets the directory where profiles will be stored"
)
set_profiles_dir_parser.add_argument(
    "path_to_profiles_directory",
    type=str,
    help="the path to where the profiles directory should be (where profiles and inactive mods stay)",
)
set_profiles_dir_parser.set_defaults(func=cmds.set_profiles_dir)

delete_profile_parser = subparsers.add_parser(
    "delete-profile", help="deletes a profile"
)
delete_profile_parser.add_argument(
    "profile_name", type=str, help="the name of the profile to delete"
)
delete_profile_parser.add_argument(
    "-y",
    "--yes",
    action="store_true",
    help="confirm the deletion of the profile and all contained mods without prompting",
)
delete_profile_parser.set_defaults(func=cmds.delete_profile)

print_profiles_dir_parser = subparsers.add_parser(
    "print-profiles-directory",
    help="prints out the path to the set profiles directory",
)
print_profiles_dir_parser.set_defaults(func=cmds.print_profiles_dir)

args = parser.parse_args()
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
