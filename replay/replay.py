# replay.py
#
# Module for opening an awbw replay file

import sys
import parse
import typing
import logging
from pathlib import Path
import zipfile
import gzip
import phpserialize

from io import StringIO
from collections import OrderedDict

# Replay files are .zip files, each of which are gzip compressed
# Filenames are a{game_id} and {game_id}

class TurnObj(typing.NamedTuple):
    """
    Used in the awbw codebase to query the gamestate of a given turn
    """
    gameId: int # int value, must correspond to a real game in the awbw server
    turn: int # int value, the turn number it is. Not the day value - there are two turns per day (p1 and p2). 0 indexed
    turnPId: int # int value, indicates which is the active player. Game state "players" array makes lookup from turnPId to real awbw users_id
    turnDay: int # int value, the maximum number of days in the replay ???
    initial: bool # bool value, indicates it's the first turn of the game or not

class TurnAction(typing.NamedTuple):
    """
    Contains all actions in a turn. The actual turn number is given by the placement in the action list.
    """
    playerId: int
    day: int
    action: dict # TODO: Unpack this fully, including the JSON inside

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

class Replay():
    """
    Usage:

    with Replay("52963.zip") as replay:
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

        self._actions = None
        self._game = None

    def __enter__(self):
        logging.debug(f"Opening {self._path}")
        self.file = zipfile.ZipFile(self._path)
        self.namelist = self.file.namelist()
        for name in self.namelist:
            self.filedata.append(gzip.decompress(self.file.read(name)))
            if "a" in name:
                # actions is a csv (sep = ;) of playerId, day, and php array of the actions made
                self._actions = self._parse_actions(self.filedata[-1])
            else:
                self._game_data = self._parse_game(self.filedata[-1])
                self._game = self._game_data._asdict()

        #self._setup_properties()

        return self

    def _parse_game(self, data):
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
            phpobj = phpserialize.loads(bytes(parsed["phpobj"], encoding="utf-8"), decode_strings=True)
            result.append(TurnAction(playerId=parsed["playerId"], day=parsed["day"], action=phpobj))

        return result

    def _setup_properties(self):
        """
        Inherit all the attributes from self._game as top level attributes
        """
        def generic_getter(data, name):
            """
            Returns a callable that returns data[name]
            """
            def _getter():
                return data[name]
            return _getter

        for key in self._game.keys():
            setattr(self, key, generic_getter(self._game, key))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    # TODO: Remove debug tools
    def print(self):
        print(self._game)

if __name__ == "__main__":
    with Replay(sys.argv[1]) as replay:
        replay.print()

        data, types = sanitize_phpobject(replay._game_data)
        print(types)
        print(data)
