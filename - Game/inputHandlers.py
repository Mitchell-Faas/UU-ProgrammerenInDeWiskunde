import tcod
from game_states import GameStates

def handleKeys(key, game_state):
    """A function to interpret key inputs
    Returns a dictionary containing the relevant information for the game to react to key inputs.
    What keys have which effect is dependent on the gamestate. A dead player can't move for example,
    and when the inventory is opened there are different controls also.

    Parameters
    ----------
    key: int
        An integer representing the key that was pressed. Which keys correspond to what number is managed by tcod.
    game_state: int
        An integer representing the gamestate. This tells us whose turns it is, if the player is dead, etc.
        What integer corresponds to which state is kept track of in game_states.py.
    """
    # Controls available during player's turn
    if game_state == GameStates.PLAYERS_TURN:
        action_dict = {  # Defines return values for single-key actions
            tcod.KEY_UP: {'move': (0, -1)},
            tcod.KEY_DOWN: {'move': (0, 1)},
            tcod.KEY_LEFT: {'move': (-1, 0)},
            tcod.KEY_RIGHT: {'move': (1, 0)},
            tcod.KEY_KP1: {'move': (-1, 1)},
            tcod.KEY_KP2: {'move': (0, 1)},
            tcod.KEY_KP3: {'move': (1, 1)},
            tcod.KEY_KP4: {'move': (-1, 0)},
            tcod.KEY_KP5: {'wait': True},
            tcod.KEY_KP6: {'move': (1, 0)},
            tcod.KEY_KP7: {'move': (-1, -1)},
            tcod.KEY_KP8: {'move': (0, -1)},
            tcod.KEY_KP9: {'move': (1, -1)},
            'k': {'move': (0, -1)},
            'j': {'move': (0, 1)},
            'h': {'move': (-1, 0)},
            'l': {'move': (1, 0)},
            'y': {'move': (-1, -1)},
            'u': {'move': (1, -1)},
            'b': {'move': (-1, 1)},
            'n': {'move': (1, 1)},
            'g': {'pickup': True},
            'i': {'show_inventory': True},
            'd': {'drop_inventory': True},
            tcod.KEY_ESCAPE: {'exit': True}
        }
    # Controls available when player is dead
    elif game_state == GameStates.PLAYER_DEAD:
        action_dict = {
            'i': {'show_inventory': True},
            tcod.KEY_ESCAPE: {'exit': True}
        }
    # Controls available when inventory or drop menu is open
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        action_dict = {
        tcod.KEY_ESCAPE: {'exit': True}
        }
        # Give inventory index associated with each letter of the alphabet
        for letteridx in range(26):
            action_dict[chr(letteridx + 97)] = {'inventory_index': letteridx}

    # Multi-key actions
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    try:
        # Output the appropriate action
        if key.vk == tcod.KEY_CHAR:
            key_result = action_dict[chr(key.c)]
        else:
            key_result = action_dict[key.vk]
    except KeyError:
        key_result = {}
    return key_result
