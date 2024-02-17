# RDR2 Mod Profile Manager

Specification for the _RDR2 Mod Profile Manager_ project
by Sarlude

Start of development: 2024-01-28

### Description

A tool aimed at creating a streamlined,
CLI-based mod management tool specifically for Red Dead Redemption 2.
This tool is designed to simplify the process of managing
and switching between mod profiles, enhancing the user experience for modders.
It focuses on providing a hassle-free, efficient way to handle mods,
with an emphasis on compatibility and ease of use.

### Justification

None of the current mainstream mod managers offering such
functionality such as Vortex are compatible with RDR2
due to it being able to handle Lenny's Mod Loader

While custom mods outside of the LML ecosystem can be handled by it,
there is no functionality for seamlessly switching mod profiles.

My tool would solve this problem. It would easily be used,
and would not have any compatibility issues due to that it's just an automation
of moving files around.

> [!NOTE]
> Vortex does technically work with RDR2. It's just a **massive** hassle to
> set it up with Lenny's Mod Loader

---

## Functionaliy

The user should be able to create new profiles for a set of mods.
Once the user starts the tool, they will be able to start management.
They can create a profile through [various methods](#methods-to-create-profiles)
and configure their profiles to their hearts' contents.
It is allowed to have multiple profiles active at the same time,
to give the user the freedom to categorize their mods as they please.

There will also be included error handling
to make sure the tool cannot break in most circumstances.

### Methods to Create Profiles

- **Tracking New Files/Folders**: Start and stop tracking to define a new
  profile based on added files.
- **Direct Folder Addition**: Manually add mods to a specific folder within
  the tool for a new profile.
- **Manual Mod Addition**: Individually specify mods for inclusion in a profile.

### Command Structure

`set-gamedir <path-to-game-directory>` to specify the game directory for the tool.

`create-profile <profile-name>` to create a new mod profile

`start-tracking`, `stop-tracking` to begin and end tracking new files for a profile

`add-mod <profile-name> <mod-path>` for adding mods manually to a profile

`list-profiles` to display all existing profiles

`engage-profile <profile-name>` to activate a specific mod profile

`disengage-profile <profile-name>` to deactivate a specific mod profile

`disengage-all` to deactivate all active mod profiles

`delete-profile <profile-name>` to delete an existing profile

`update-profile <profile-name>` for updating an existing profile

`help` or `<command> --help` to display help information about commands

`--version` to display the current version of the tool.

---

## Technical

### Programming Language

**>Python 3.10**. The specific Python version to use has not been decided yet,
but it will be the latest available according to any dependencies.

### Data Storage

**JSON** will be used for data storage. Each profile will have it's own json file,
keeping track of all mod files and directories it contains, as well was whatever else-
This makes it easy to know what files to move in and out.

*Example of a profile's JSON file*
```json
{
  "profileName": "Immersion",
  "modFiles": ["mod1.asi", "mod2.asi"],
  "modDirectories": ["/lml/bettercrime/", "/huntenhance/"],
  "metadata": {
    "creationDate": "2024-01-28",
    "lastUpdated": "2024-02-15",
    "notes": "A collection of immersive mods."
  }
}

```

### Error Handling

There will need to be extensive error handling.
The user might delete a file when it's active, leading to confusion for the tool
when it wants to deactivate the profile. Such errors must be taken care of.

---

## Code Structure

- `main.py` is the entry point of the tool. It parses command line arguments
  and calls appropiate funcions and classes based on user input.
- `cli.py` handles all CLI-related functionalities.
  It contains functions to display help, parse command and command options.
- `profile_manager.py` contains the core logic for managing mod profiles.
  It contains classes or functions to create, update, delete, engage,
  and disengage mod profiles.
- `file_handler.py` deals with file operations. It contains functions for
  reading from and writing to JSON files, moving mod files around, etc.
- `error_handler.py` manages all error handling. It contains functions to
  catch and handle various errors, possibly logging them for debugging.
- `config.py` manages configuration settings or constants used throughout
  the project.