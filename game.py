"""Classes and code to manage game state."""

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
