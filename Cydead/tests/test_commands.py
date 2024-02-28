import json
from argparse import Namespace
from unittest.mock import patch

from cydead import commands as cmds
from cydead import utils


def test_create_profile_success(tmp_path):
    """Tests the profile creation function with valid arguments"""
    args = Namespace(profile_name="test_profile", description="A test profile")

    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    cmds.create_profile(args, test=True, test_dir=test_profiles_path)

    expected_dir = test_profiles_path / args.profile_name
    assert expected_dir.exists()
    assert (expected_dir / "profile.json").exists()


def test_create_profile_duplicate(tmp_path):
    """Tests the profile creation when it is attempting to
    create a profile with an already existing name
    """
    args = Namespace(
        profile_name="duplicate_profile",
        description="This profile is duplicated",
        )

    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    cmds.create_profile(args, test=True, test_dir=test_profiles_path)
    assert (test_profiles_path / args.profile_name).exists()

    cmds.create_profile(args, test=True, test_dir=test_profiles_path)
    assert len(list(test_profiles_path.iterdir())) == 1


def test_list_profiles(tmp_path):
    """Tests if it can list profiles in the
    `profiles` folder properly
    """
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    for i in range(1, 4):
        args = Namespace(
            profile_name=f"test_profile_{i}", description=f"Test profile {i}"
            )
        cmds.create_profile(args, test=True, test_dir=test_profiles_path)

    args = Namespace()

    with patch("builtins.print") as mocked_print:
        cmds.list_profiles(args, test=True, test_dir=test_profiles_path)

        expected_calls = [
            (("YOUR PROFILES:",), {}),
            (("\nName: test_profile_1",), {}),
            (("Description: Test profile 1",), {}),
            (("\nName: test_profile_2",), {}),
            (("Description: Test profile 2",), {}),
            (("\nName: test_profile_3",), {}),
            (("Description: Test profile 3",), {}),
            ]

        mocked_print.assert_has_calls(expected_calls, any_order=True)


def test_list_profiles_empty(tmp_path):
    """Tests if it will respond properly when `list-profiles` is run
    with an empty `profiles` folder
    """
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    args = Namespace()

    with patch("builtins.print") as mocked_print:
        cmds.list_profiles(args, test=True, test_dir=test_profiles_path)
        expected_calls = [
            (("You do not have any profiles!",), {}),
            ]
        mocked_print.assert_has_calls(expected_calls)


def test_list_profiles_missing_json(tmp_path):
    """Tests how it will react when a profile folder
    is missing a profile.json file
    """
    test_profiles_path = tmp_path / "profiles"
    profile_name = "test_profile"
    args = Namespace(profile_name=profile_name, description="A test profile")
    cmds.create_profile(args, True, test_profiles_path)

    profile_json_path = test_profiles_path / profile_name / "profile.json"
    profile_json_path.unlink(missing_ok=True)

    with patch("builtins.print") as mocked_print:
        cmds.list_profiles(args, test=True, test_dir=test_profiles_path)
        expected_calls = [
            (("\nThe profile.json file was not found in the profile",), {}),
            (("Creating a recovery file...",), {}),
            ]
        mocked_print.assert_has_calls(expected_calls)


def test_delete_profile_yes_flag(tmp_path):
    """Tests the deletion of a profile with the `yes` flag"""
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_name = "test_profile"
    profile_path = test_profiles_path / profile_name
    profile_path.mkdir(parents=True, exist_ok=True)

    args = Namespace(profile_name=profile_name, description="A test profile",
                     yes=True)
    assert profile_path.exists()

    cmds.delete_profile(args, test=True, test_dir=test_profiles_path)
    assert not profile_path.exists()


def test_delete_profile_confirmation_yes(tmp_path):
    """Tests the deletion of a profile with confirmation 'yes'"""
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_name = "test_profile"
    args = Namespace(profile_name=profile_name, description="A test profile",
                     yes=False)

    with patch("builtins.input", return_value="yes"):
        cmds.delete_profile(args, True, test_profiles_path)

    assert not (test_profiles_path / profile_name).exists()


def test_delete_profile_confirmation_no(tmp_path):
    """Tests the cancellation of profile deletion with confirmation 'no'"""
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_name = "test_profile"
    profile_path = test_profiles_path / profile_name
    profile_path.mkdir(parents=True, exist_ok=True)

    args = Namespace(profile_name=profile_name, description="A test profile",
                     yes=False)

    with patch("builtins.input", return_value="no"):
        cmds.delete_profile(args, True, test_profiles_path)

    assert profile_path.exists()


def test_delete_profile_invalid_confirmation(tmp_path):
    """Tests the handling of invalid confirmation input"""
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_name = "test_profile"
    profile_path = test_profiles_path / profile_name
    profile_path.mkdir(parents=True, exist_ok=True)

    args = Namespace(profile_name=profile_name, description="A test profile",
                     yes=False)

    with patch("builtins.input", side_effect=["invalid", "no"]):
        cmds.delete_profile(args, True, test_profiles_path)

    assert profile_path.exists()


def test_delete_profile_not_found(tmp_path):
    """Tests the handling of a profile that does not exist"""
    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_name = "nonexistent_profile"
    args = Namespace(profile_name=profile_name,
                     description="A nonexistent profile", yes=True)

    with patch("builtins.print") as mocked_print:
        cmds.delete_profile(args, True, test_profiles_path)

        mocked_print.assert_called_with(f"'{profile_name}' does not exist.")


def test_update_profile_success(tmp_path):
    """Tests the profile update function with valid arguments"""
    args = Namespace(profile_name="test_profile")

    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_path = test_profiles_path / args.profile_name
    profile_path.mkdir(parents=True, exist_ok=True)

    test_file_path = profile_path / "test_file.txt"
    test_file_path.touch()

    cmds.update_profile(args, test=True, test_dir=test_profiles_path)

    profile_json_path = profile_path / "profile.json"
    assert profile_json_path.exists()

    with open(profile_json_path, "r") as file:
        data = json.load(file)
        assert data["modFiles"] == ["test_file.txt"]


def test_update_profile_subdirectories(tmp_path):
    """Tests the profile update function with files in subdirectories"""
    args = Namespace(profile_name="test_profile")

    test_profiles_path = tmp_path / "profiles"
    test_profiles_path.mkdir(parents=True, exist_ok=True)

    profile_path = test_profiles_path / args.profile_name
    profile_path.mkdir(parents=True, exist_ok=True)

    subdirectory_path = profile_path / "subdirectory"
    subdirectory_path.mkdir(parents=True, exist_ok=True)

    test_file_path = subdirectory_path / "test_file.txt"
    test_file_path.touch()

    cmds.update_profile(args, test=True, test_dir=test_profiles_path)

    profile_json_path = profile_path / "profile.json"
    assert profile_json_path.exists()

    with open(profile_json_path, "r") as file:
        data = json.load(file)
        assert data["modFiles"] == ["subdirectory/test_file.txt"]
