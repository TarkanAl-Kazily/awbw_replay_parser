# AWBW Replay Parser

![pylint](https://github.com/TarkanAl-Kazily/awbw_replay_parser/actions/workflows/pylint.yml/badge.svg)
![unittest](https://github.com/TarkanAl-Kazily/awbw_replay_parser/actions/workflows/python-unittest.yml/badge.svg)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/TarkanAl-Kazily/awbw_replay_parser/blob/main/AWBW_Replays_Interactive_Notebook.ipynb)

This repository is home to the AWBW Replay Parser, a Python package to open and step through [AWBW](https://awbw.amarriner.com/) game replays. This project is unafilliated with AWBW or any related property.

To get started, click the __Open In Colab__ badge at the top of the README, or fork the repository to tinker with the package directly.

# Package Documentation

To open a replay file, use the `AWBWReplay` class:

```python
from awbw_replay.replay import AWBWReplay

with AWBWReplay("my_replay.zip") as replay:
    replay_actions = list(replay.actions())
    replay_turns = replay.turns()
    print(f"There are {len(replay_actions)} actions and {len(replay_turns)} turns in {replay.path()}")
```

The `AWBWReplay` class is the parser and general wrapper around the replay archive, but is generally not used directly.
Instead, we use the `game_info()` and `actions()` functions to get the necessary information to determine the game state between each action.

The `AWBWGameState` and `AWBWGameAction` classes take this information from the `AWBWReplay` instance and turn it into a consistent state format that can be analyzed over the course of a match.
Here's an example for how to generate all game states in a replay:

```python
from awbw_replay.replay import AWBWReplay
from awbw_replay.awbw import AWBWGameState, AWBWGameAction

# Read out all the game states
states = []
with AWBWReplay("my_replay.zip") as replay:
    states.append(AWBWGameState(replay_initial=replay.game_info()))

    for action in replay.actions():
        states.append(states[-1].apply_action(AWBWGameAction(action)))
```

Extract game information from the replay by examining the game states. `AWBWGameState` stores dictionaries for the following information:

- `game_info`: Global information including the game ID, the active player and the day.
- `players`: Player information given by player ID. Includes funds and CO power meter.
- `units`: Unit information given by unit ID. Includes hit points, cost and (x, y) coordinates
- `buildings` : Building information given by building ID. Includes capture values and (x, y) coordinates
- `game_map` (__PLANNED__): Map information including the map ID, map size and text representation of map

All of this information is stored in various dictionary types given by the classes `awbw.GameInfo`, `awbw.Player`, `awbw.Unit` and `awbw.Building`.
The `ALLOWED_DATA` dictionary of each of these classes provides the documentation for the present keys and expected types for parsing.

Here's an example of reading out players funds over the course of match:

```python
# Examine player funds over time
player_funds = {}
player_ids = states[0].players.keys()
for p_id in player_ids:
    player_funds[p_id] = []

for state in states:
    for p_id in player_ids:
        player_funds[p_id].append(state.players[p_id]["funds"])
```

# Contributing

This project is open source and welcomes contributions from the community.
Please review the [contribution guidelines](https://github.com/TarkanAl-Kazily/awbw_replay_parser/blob/main/CONTRIBUTING.md) for how to get involved.

Spoiler alert: Bugs probably exist in this repository. Please use Github's Issues system for reporting, and be as detailed as you can. Again, see the contributing guidelines for more information.
