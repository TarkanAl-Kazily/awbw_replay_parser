# Objectives

[X] Open a Replay (.zip) as input. Get out the metadata and list of actions performed.
[ ] Create a GameState object that contains the high-level stats of the game.
  - Number of units
  - Total funds
  - Total unit value
  - CO Power Meter
  - Income
[ ] Create a GameAction object that can be constructed using the info in the Replay list
[ ] Create a function (GameState, GameAction) -> GameState that updates a game with the given action
  -`From a Replay object, get a GameState object every turn. Do this by chaining the GameState with the given "next action" repeatedly
[ ] Use matplotlib to plot numbers from game state over time (actions)
[ ] P1: Open a map (.txt) as input. Get out a picture of the terrain.
[ ] P1: From a map id, download the text format for the terrain automatically.
[ ] P1: From a map id, create a matplotlib image with map assets pulled from awbw.
[ ] P1: Crawl the AWBW completed games page to get all the game IDs with replays available.
[ ] P1: Create a google collab / github interactive notebook for anyone to enter a replay ID and use Python to inspect state over time
[ ] P0: Purge files we don't want to commit from the Github repo
 - images that aren't ours
 - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
[ ] P1: Add a code linter to the github repo
[ ] P1: Add a contribution guide
