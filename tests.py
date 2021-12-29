# tests.py
#
# Basic unit tests for the library on select sample replays

import os
import unittest
import tempfile

from replay import AWBWReplay
from awbw import AWBWGameAction, AWBWGameState

TEST_REPLAYS_DIR = "replays"

class TestAWBWReplay(unittest.TestCase):

    def test_open(self):
        example_replay = os.path.join(TEST_REPLAYS_DIR, "test_open.zip")
        with AWBWReplay(example_replay) as replay:
            assert replay is not None
            assert replay._path == example_replay
            assert isinstance(replay.turns(), list)
            assert isinstance(replay.game_info(), dict)

    @unittest.expectedFailure
    def test_open_nonexistent(self):
        # Open a temporary directory, to ensure no files exist in it
        with tempfile.TemporaryDirectory() as tempdir:
            dne_file = os.path.join(tempdir, "does_not_exist.zip")
            with AWBWReplay(dne_file) as replay:
                assert replay._path == dne_file

if __name__ == "__main__":
    unittest.main()
