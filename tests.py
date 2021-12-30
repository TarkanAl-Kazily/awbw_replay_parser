"""
Basic unit tests for the library on select sample replays.

To run:
python -m unittest -v
"""


import os
import unittest
import tempfile

from replay import AWBWReplay
from awbw import AWBWGameAction, AWBWGameState

# pylint: disable=no-self-use

TEST_REPLAYS_DIR = "replays"

class TestAWBWReplay(unittest.TestCase):
    """Tests for the AWBWReplay class"""

    def test_open(self):
        """Test that we can open a file, and that the basic functions return valid results"""
        example_replay = os.path.join(TEST_REPLAYS_DIR, "test_open.zip")
        with AWBWReplay(example_replay) as replay:
            assert replay is not None
            assert replay.path() == example_replay
            assert isinstance(replay.turns(), list)
            assert isinstance(replay.game_info(), dict)

    @unittest.expectedFailure
    def test_open_nonexistent(self):
        """Test that an error is raised when a nonexistent file is opened"""
        # Open a temporary directory, to ensure no files exist in it
        with tempfile.TemporaryDirectory() as tempdir:
            dne_file = os.path.join(tempdir, "does_not_exist.zip")
            with AWBWReplay(dne_file) as _replay:
                # We don't expect to get here
                pass

class TestAWBWGameState(unittest.TestCase):

    def test_short_replay(self):
        """Test a basic short replay."""
        example_replay = os.path.join(TEST_REPLAYS_DIR, "short_replay.zip")
        with AWBWReplay(example_replay) as replay:
            states = [AWBWGameState(replay_initial=replay.game_info())]
            
            for action in replay.actions():
                states.append(states[-1].apply_action(AWBWGameAction(action)))

            assert len(replay.turns()) == states[-1].game_info["turn"] + 1
            assert all([len(state.players) == 2 for state in states])

    def test_basic_replay(self):
        """Test a medium length replay."""
        example_replay = os.path.join(TEST_REPLAYS_DIR, "basic_replay.zip")
        with AWBWReplay(example_replay) as replay:
            states = [AWBWGameState(replay_initial=replay.game_info())]
            
            for action in replay.actions():
                states.append(states[-1].apply_action(AWBWGameAction(action)))

            assert len(replay.turns()) == states[-1].game_info["turn"] + 1
            assert all([len(state.players) == 2 for state in states])

if __name__ == "__main__":
    unittest.main()
