"""Classes and code to manage game state."""

import collections

# Base classes

class GameState():
    """
    Represents a single state in the game. Each game state is transitioned
    between using actions.
    """

    def __init__(self):
        pass

    def apply_action(self, action):
        """
        The main function defining a GameState. Applying an action to this game
        state produces a new game state.

        Arguments:
        - action: A GameAction

        Returns:
        - A new GameState
        """
        raise NotImplementedError()

class GameAction():
    """
    Represents a single action in the game. Used to transition between
    GameStates.
    """
    def __init__(self):
        pass

class DefaultDict(collections.UserDict):
    """
    An extension of UserDict that asserts the only constructed keys are the ones
    in ALLOWED_DATA, and assigns defaults according to the unassigned keys.
    """

    ALLOWED_DATA = {}

    def __init__(self, data=None, **kwargs):
        if data is None:
            data = {}

        data = data | kwargs

        # Check that only the supported keys are present
        for key in data:
            if key not in self.ALLOWED_DATA:
                raise KeyError(f"{key} is not supported for {self.__class__.__name__}")

        super().__init__({**self.ALLOWED_DATA, **data})
