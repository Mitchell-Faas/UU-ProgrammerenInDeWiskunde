import tcod
from game_states import GameStates
from renderFunctions import RenderOrder
from gameMessages import Message


def kill_player(player):
    """Executes all the actions required to kill the player.

    Parameters
    ----------
    player : :obj:`Entity`
        Player object

    Returns
    -------
    :obj:`Message`
        Message associated with killing the player"""
    player.char = '%'
    player.colour = tcod.dark_red

    return Message('You explode in a fountain of gore!', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    """Executes all the actions required to kill a monster

    Parameters
    ----------
    monster : :obj:`Entity`
        Monster Entity object

    Returns
    -------
    :obj:`Message`
        Message associated with the death of a monster.
    """
    death_message = Message('The {0} explodes in a fountain of gore!'.format(monster.name.capitalize()), tcod.orange)

    monster.char = '%'
    monster.colour = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.corpse

    return death_message
