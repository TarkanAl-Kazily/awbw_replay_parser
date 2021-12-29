"""Module for opening an AWBW replay file."""

import gzip
import json
import logging
from pathlib import Path
import sys
import typing
import zipfile

import parse
import phpserialize

# Replay files are .zip files, each of which are gzip compressed.
# Filenames are a{game_id} and {game_id}.
# a{game_id} file contains all the actions as csv style objects with JSON serialized
# contents for each turn.
# {game_id} file contains all the remaining metadata, including the initial player funds,
# initial buildings and units.

class RawTurn(typing.NamedTuple):
    """
    Contains all actions in a turn. The actual turn number is given by the
    placement in the action list.
    """
    playerId: int
    day: int
    actions: typing.List[typing.Dict]

def sanitize_phpobject(phpobj):
    """
    Recursively convert phpobj to a dict

    Also returns a list of all the phpobject class types found
    """

    found_types = []

    if isinstance(phpobj, phpserialize.phpobject):
        found_types.append(phpobj.__name__)
        phpobj, types = sanitize_phpobject(phpobj._asdict())
        found_types += types

    elif isinstance(phpobj, dict):
        for key, value in phpobj.items():
            phpobj[key], types = sanitize_phpobject(value)
            found_types += types

    elif isinstance(phpobj, list):
        for i, value in enumerate(phpobj):
            phpobj[i], types = sanitize_phpobject(value)
            found_types += types

    else: # primitive type
        pass

    return phpobj, set(found_types)

class AWBWReplay():
    """
    Usage:

    with AWBWReplay("52963.zip") as replay:
        ...
    """

    _ACTION_PARSE_STR = "p:{playerId:d};d:{day:d};a:{phpobj}"

    def __init__(self, file: str | Path):
        """
        Arguments:
        - file: str or Path object to open read-only to extract the replay.
        """
        self._path = file
        self.file = None
        # Replay archive name list
        self.namelist = []
        self.filedata = []

        self._turns = None
        self._game_data = None
        self._game = None

    def __enter__(self):
        logging.debug("Opening %s", self._path)
        self.file = zipfile.ZipFile(self._path)
        self.namelist = self.file.namelist()
        for name in self.namelist:
            self.filedata.append(gzip.decompress(self.file.read(name)))
            if "a" in name:
                # actions is a csv (sep = ;) of playerId, day, and php array of the actions made
                self._turns = self._parse_actions(self.filedata[-1])
            else:
                self._game_data = self._parse_game(self.filedata[-1])
                self._game, _ = sanitize_phpobject(self._game_data)

        return self

    def _parse_game(self, data): # pylint: disable=no-self-use
        """
        Arguments:
        - data: The decompressed contents of the (non-prefixed) {game_id} gzip file
        """
        return phpserialize.loads(data, object_hook=phpserialize.phpobject, decode_strings=True)

    def _parse_actions(self, data):
        """
        Arguments:
        - data: The decompressed contents of the a{game_id} gzip file
        """
        result = []
        for line in data.decode().strip().split("\n"):
            parsed = parse.parse(self._ACTION_PARSE_STR, line).named
            phpobj = phpserialize.loads(
                    bytes(parsed["phpobj"], encoding="utf-8"),
                    decode_strings=True)
            phpactions = phpobj[2]
            actions = []
            for jsonstr in phpactions.values():
                actions.append(json.loads(jsonstr))
            result.append(RawTurn(playerId=parsed["playerId"], day=parsed["day"], actions=actions))

        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def path(self):
        """Returns the filepath of the replay."""
        return self._path

    def game_info(self):
        """Returns the initial game info dictionary."""
        return self._game

    def turns(self):
        """Returns the list of turns in the game."""
        return self._turns

    def actions(self):
        """Generator over every action in the game."""
        for _turn in self.turns():
            yield from _turn.actions

    def action_summaries(self):
        """Generator over every action type in the game."""
        for _action in self.actions():
            yield _action["action"]

# Basic test code for opening a replay file
if __name__ == "__main__":
    import pprint
    with AWBWReplay(sys.argv[1]) as replay:

        print("Press enter to step through the replay")
        for action in replay.actions():
            if action["action"] == "Fire":
                pprint.pp(action)

        action_types = replay.action_summaries()
        print(f"The action types were {set(action_types)}")

        print(" ".join(replay.action_summaries()))
