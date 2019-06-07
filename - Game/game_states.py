from enum import Enum


class GameStates(Enum):
    """A class that keeps track of the state of the game
    This class inherits from Enum. It allows us to keep track of the state the game is in.
    This is used to check whose turn it is, whether the player is dead or not,
    whether the inventory menu is opened, etc.
    This helps us keep track of which inputs are allowed, what their consequences are, and what actions are possible.
    """
    PLAYERS_TURN = 1
    ENEMIES_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVENTORY = 4
