"""
Basic unit tests for the replay module on select sample replays.

To run:
python -m unittest -v
"""

import os
import unittest
import tempfile

from awbw_replay.replay import AWBWReplay

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

if __name__ == "__main__":
    unittest.main()
