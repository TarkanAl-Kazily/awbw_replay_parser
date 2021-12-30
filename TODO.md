# Objectives

- [X] Open a Replay (.zip) as input. Get out the metadata and list of actions performed.
- [X] Create a GameState object that contains the high-level stats of the game.
  - Number of units
  - Total funds
  - Total unit value
  - CO Power Meter
  - Income
- [X] Create a GameAction object that can be constructed using the info in the Replay list
- [X] Create a function (GameState, GameAction) -> GameState that updates a game with the given action
  - From a Replay object, get a GameState object every turn. Do this by chaining the GameState with the given "next action" repeatedly
- [X] P0: Purge files we don't want to commit from the Github repo
 - images that aren't ours
 - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- [X] P1: Add a code linter to the github repo
  - Also added unit tests!
- [X] P0: Use matplotlib to plot numbers from game state over time (actions)
- [X] P0: Support tracking which day it is
- [X] P1: Add a contribution guide
- [X] P1: Add batch testing for multiple replay files

# Up next

- [ ] P0: Update the README with common actions / workflows
- [ ] P0: Expand main.py to output a summary of all the tested replay files.
  - CSV format
  - Include the exception replay parsing failed on, if any
  - P1: Find a way to tell if any warnings were logged during the replay (usually indicates a bad replay)
- [ ] P1: Continue adding support for more action types
  - Resign
  - Powers
  - Launch
  - Hide / Reveal / Dive / Rise ?
- [ ] P1: Create a google collab / github interactive notebook for anyone to enter a replay ID and use Python to inspect state over time
  - https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb#scrollTo=8J3NBxtZpPcK
  - Find a workaround for Python 3.8 not being supported (typing.TypedDict)

# Low-Pri ideas

- [ ] P1: Pull replay files from an external file hosting solution (GDrive)
- [ ] P1: Open a map (.txt) as input. Get out a picture of the terrain.
- [ ] P1: From a map id, download the text format for the terrain automatically.
- [ ] P1: From a map id, create a matplotlib image with map assets pulled from awbw.
- [ ] P1: Add helper functions to go right from a game ID to a game analysis (by downloading the replay directly from awbw)
- [ ] P2: Crawl the AWBW completed games page to get all the game IDs with replays available.
  - We can't download replays without login credentials...
