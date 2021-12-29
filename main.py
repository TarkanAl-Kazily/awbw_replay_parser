"""Main CLI tool to use the AWBW Replay Parser libraries"""

import argparse
import sys
import matplotlib.pyplot as plt
import numpy as np

from awbw import AWBWGameAction, AWBWGameState
from replay import AWBWReplay

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# These are just random names for cleaner viewing.
PLAYER_NAMES = ["Andy", "Bob", "Colin", "Drake", "Eagle", "Flak", "Grit", "Hawke"]

def get_args(argv=None):
    """
    Handles argument parsing for main

    Arguments:
    - argv: List of string arguments, or None to use sys.argv (default)

    Returns:
    - namespace containing parsed arguments
    """

    parser = argparse.ArgumentParser(description="AWBW Replay Parser tool")

    parser.add_argument("file", help="Replay file to open", type=str)

    return parser.parse_args(argv)

def main(args):
    """Parses a replay to generate plots of data"""
    with AWBWReplay(args.file) as replay:
        states = [AWBWGameState(replay_initial=replay.game_info())]

        players = {}
        for i, p_id in enumerate(states[-1].players.keys()):
            players[p_id] = {"name": PLAYER_NAMES[i], "funds": []}

        # Generate all the states
        for action in replay.actions():
            action = AWBWGameAction(replay_action=action)
            states.append(states[-1].apply_action(action))

        # For each state, get the day. If it's the last state of the day, track both player's stats
        day = 1
        for i, state in enumerate(states):
            if i + 1 >= len(states) or states[i+1].game_info["day"] == day + 1:
                for p_id, player in players.items():
                    player["funds"].append(state.players[p_id]["funds"])
                day += 1

        x_vals = np.arange(1, day)
        x_offsets = np.linspace(-0.5, 0.5, num=len(players) + 2)
        x_width = 1.0 / (len(players) + 1)

        for i, p_id in enumerate(players.keys()):
            player = players[p_id]
            plt.bar(x_vals + x_offsets[i + 1], player["funds"], width=x_width, label=player["name"])

        plt.xlim([0, day])
        plt.xticks(x_vals)
        plt.legend()

        plt.show()

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main(get_args()))
