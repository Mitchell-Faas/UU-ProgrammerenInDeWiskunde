import tcod
import tcod.console
import inputHandlers
from entity import Entity
import renderFunctions as render
from map_objects.game_map import GameMap

def main():
    screenWidth = 80
    screenHeight = 50
    map_width = 80
    map_height =45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    colours = {
               'dark_wall': tcod.Color(0,0,100),
               'dark_ground': tcod.Color(50,50,150)}

    # Create variables to store player location
    player = Entity(
                    x=int(screenWidth / 2),
                    y=int(screenHeight / 2),
                    char='@',
                    colour=tcod.white)
    npc = Entity(
                 x=int(screenWidth / 2 - 5),
                 y=int(screenHeight / 2),
                 char='@',
                 colour=tcod.yellow)

    entities = [npc, player]

    game_map = GameMap(map_width, map_height)
    game_map.create_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    # Define Key and Mouse objects
    key = tcod.Key()
    mouse = tcod.Mouse()

    # Initialise the console with some hardcoded data
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(w=screenWidth, h=screenHeight, title='Esc to exit')
    console = tcod.console.Console(width=screenWidth, height=screenHeight)

    # Start the game loop
    while True:
        # Write current state to console
        render.render_all(console=console,
                          entities=entities,
                          game_map = game_map,
                          screen_width=screenWidth,
                          screen_height=screenHeight,
                          colours=colours)
        tcod.console_flush()
        # Remove all entities so we can update
        render.clear_all(console=console, entities=entities)

        #####################
        ## Key-press logic ##
        #####################
        # Check input from keyboard or mouse
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # Translate keypress in to action
        action = inputHandlers.handleKeys(key)

        # dict.get returns None if key doesn't exist
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            if not game_map.is_blocked(player.x + move[0], player.y + move[1]):
                # move is a (dx, dy) tuple
                player.move(*move)
        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
