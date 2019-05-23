import tcod


def handleKeys(key):
    action_dict = {  # Defines return values for single-key actions
        tcod.KEY_UP: {'move': (0, -1)},
        tcod.KEY_DOWN: {'move': (0, 1)},
        tcod.KEY_LEFT: {'move': (-1, 0)},
        tcod.KEY_RIGHT: {'move': (1, 0)},
        tcod.KEY_KP1: {'move': (-1, 1)},
        tcod.KEY_KP2: {'move': (0, 1)},
        tcod.KEY_KP3: {'move': (1, 1)},
        tcod.KEY_KP4: {'move': (-1, 0)},
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
        tcod.KEY_ESCAPE: {'exit': True}
    }

    # Multi-key actions
    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}

    try:
        # Return the appropriate action
        return action_dict[key.vk]
    except KeyError:
        # Key is unkown.
        return {}
