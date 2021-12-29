import sys
import argparse

from replay import AWBWReplay
from awbw import AWBWGameAction, AWBWGameState
import matplotlib.pyplot as plt
import numpy as np

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# These are just random names for cleaner viewing.
PLAYER_NAMES = ["Andy", "Bob", "Colin", "Drake", "Eagle", "Flak", "Grit", "Hawke"]

def get_args(argv=None):
    parser = argparse.ArgumentParser(description="AWBW Replay Parser tool")

    parser.add_argument("file", help="Replay file to open", type=str)

    return parser.parse_args(argv)

def main(args):
    with AWBWReplay(args.file) as replay:
        state = AWBWGameState(replay_initial=replay.game_info())

        players = {}
        for i, p_id in enumerate(state.players.keys()):
            players[p_id] = {"name": PLAYER_NAMES[i], "funds": [state.players[p_id]["funds"]]}

        action_number = 0
        # Keep track of what actions turns changed on, to draw vertical lines with
        turns = []
        for action in replay.actions():
            action = AWBWGameAction(replay_action=action)
            state = state.apply_action(action)
            if state.game_info["turn"] == len(turns):
                turns.append(action_number)
            for p_id, player in state.players.items():
                players[p_id]["funds"].append(player["funds"])

            action_number += 1

        # TODO: Instead of using turns for this data, use days
        turns.append(action_number)

        # Convert actions to proportionally where they fall in the turn
        x_vals = np.array([])
        for i, (t, next_t) in enumerate(zip(turns[:-1], turns[1:])):
            x_vals = np.append(x_vals, np.linspace(i, i+1, num=next_t - t, endpoint=False))

        # Edge case due to using Endpoint = False, we miss the very last action value
        # which would be at the start of the next turn
        x_vals = np.append(x_vals, [len(turns) - 1])

        for p_id, player in players.items():
            plt.plot(x_vals, player["funds"], label=player["name"])

        plt.show()

    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main(get_args()))
