import tcod


def handleKeys(key):
    action_dict = {  # Defines return values for single-key actions
        tcod.KEY_UP: {'move': (0, -1)},
        tcod.KEY_DOWN: {'move': (0, 1)},
        tcod.KEY_LEFT: {'move': (-1, 0)},
        tcod.KEY_RIGHT: {'move': (1, 0)},
        'y': {'move': (-1, -1)},
        'u': {'move': (1, -1)},
        'b': {'move': (-1, 1)},
        'n': {'move': (1, 1)},
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
