"""
Basic unit tests for the awbw module on select sample replays.

To run:
python -m unittest -v
"""


import os
import unittest

from replay import AWBWReplay
from awbw import AWBWGameAction, AWBWGameState

# pylint: disable=no-self-use

TEST_REPLAYS_DIR = "replays"

class TestAWBWGameState(unittest.TestCase):
    """Tests for the AWBWGame* classes"""

    def test_short_replay(self):
        """Test a basic short replay."""
        example_replay = os.path.join(TEST_REPLAYS_DIR, "short_replay.zip")
        with AWBWReplay(example_replay) as replay:
            states = [AWBWGameState(replay_initial=replay.game_info())]

            for action in replay.actions():
                states.append(states[-1].apply_action(AWBWGameAction(action)))

            assert len(replay.turns()) == states[-1].game_info["turn"] + 1
            assert all((len(state.players) == 2 for state in states))

    def test_basic_replay(self):
        """Test a medium length replay."""
        example_replay = os.path.join(TEST_REPLAYS_DIR, "basic_replay.zip")
        with AWBWReplay(example_replay) as replay:
            states = [AWBWGameState(replay_initial=replay.game_info())]

            for action in replay.actions():
                states.append(states[-1].apply_action(AWBWGameAction(action)))

            assert len(replay.turns()) == states[-1].game_info["turn"] + 1
            assert all((len(state.players) == 2 for state in states))

    def test_standard_replay(self):
        """Test a non Fog replay."""
        example_replay = os.path.join(TEST_REPLAYS_DIR, "standard_replay.zip")
        with AWBWReplay(example_replay) as replay:
            states = [AWBWGameState(replay_initial=replay.game_info())]

            for action in replay.actions():
                states.append(states[-1].apply_action(AWBWGameAction(action)))

            assert len(replay.turns()) == states[-1].game_info["turn"] + 1
            assert all((len(state.players) == 2 for state in states))

if __name__ == "__main__":
    unittest.main()
