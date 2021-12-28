# replay.py
#
# Module for opening an awbw replay file

import pdb

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
    action: OrderedDict

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

        self.actions = None
        self.game = None

    def __enter__(self):
        logging.debug(f"Opening {self._path}")
        self.file = zipfile.ZipFile(self._path)
        self.namelist = self.file.namelist()
        pdb.set_trace()
        for name in self.namelist:
            self.filedata.append(gzip.decompress(self.file.read(name)))
            if "a" in name:
                # actions is a csv (sep = ;) of playerId, day, and php array of the actions made
                self.actions = self._parse_actions(self.filedata[-1])
            else:
                self.game = self._parse_game(self.filedata[-1])

        return self

    def _parse_game(self, data):
        """
        Arguments:
        - data: The decompressed contents of the (non-prefixed) {game_id} gzip file
        """
        return phpserialize.loads(self.filedata[-1], object_hook=phpserialize.phpobject)

    def _parse_actions(self, data):
        """
        Arguments:
        - data: The decompressed contents of the a{game_id} gzip file
        """
        result = []
        for line in data.decode().strip().split("\n"):
            parsed = parse.parse(self._ACTION_PARSE_STR, line).named
            phpobj = phpserialize.loads(bytes(parsed["phpobj"], encoding="utf-8"))
            result.append(TurnAction(playerId=parsed["playerId"], day=parsed["day"], action=phpobj))

        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

    def print(self):
        print()

        print(self.actions)
        print(self.game)

    def id(self):
        pass

    def map(self):
        pass

    def players(self):
        pass

if __name__ == "__main__":
    with Replay("ignore/526302.zip") as replay:
        replay.print()
