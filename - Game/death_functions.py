import tcod
from game_states import GameStates
from renderFunctions import RenderOrder
from gameMessages import Message


def kill_player(player):
    player.char = '%'
    player.colour = tcod.dark_red

    return Message('You explode in a fountain of gore!', tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message('The {0} explodes in a fountain of gore!'.format(monster.name.capitalize()), tcod.orange)

    monster.char = '%'
    monster.colour = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.corpse

    return death_message