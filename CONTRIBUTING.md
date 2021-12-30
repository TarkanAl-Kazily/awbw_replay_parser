# Contributing to this repository

Thank you for your interest! In the interest of enabling the community to suggest and contribute back improvements and features to this repository to benefit all users, please read these guidelines.

Please make bug reports or feature requests through the [Issues](https://github.com/TarkanAl-Kazily/awbw_replay_parser/issues) page. Please comment in detail the problem, including a way to reproduce it if possible. Issues specific to a replay file should include the replay file artifact as an upload.

If you are comfortable with Python, make actual code changes through a [Pull Request](https://github.com/TarkanAl-Kazily/awbw_replay_parser/pulls). This will require making a fork of the repository in order to develop your change, and then code review before being merged.

Issues and Pull Requests will be engaged with as the maintainers have time available. If you are interested in becoming an authorized maintainer (to review and merge pull requests), please contact the owner of this repo directly.

## Unit testing and code quality

This repository is configured with some basic Github Actions which will automatically run Pylint and Python's built in `unittest` module. All pull requests must have these jobs pass before being merged.

When making a pull request fixing a bug, please add a unit test to verify the bug doesn't regress with your pull request. Example replay data can be checked in to the `replays` directory. However, it is preferred to use an external file hosting solution (like Google Drive) to store these replay archives to keep the overal repository size small.

A good unit test will verify that the given feature or replay file is loaded properly, and ideally will test some known facts about the replay file loaded - it's game ID, the players involved, the number of turns or the winner. Most important, the test should be kept short and to the point, focused on the bug or feature being tested.
