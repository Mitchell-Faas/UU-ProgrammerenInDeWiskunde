import inputHandlers
import renderFunctions as render
import tcod
import tcod.console
from entity import Entity, get_blocking_entities_at
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from components.fighter import Fighter


def main():
    screenWidth = 80
    screenHeight = 50
    map_width = screenWidth
    map_height = screenHeight  # -5 to fill add room at the bottom

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colours = {'dark_wall': tcod.Color(0, 0, 100),
               'dark_ground': tcod.Color(50, 50, 150),
               'light_wall': tcod.Color(130, 110, 50),
               'light_ground': tcod.Color(200, 180, 50),
               'black': tcod.Color(0, 0, 0)}

    fighter_component = Fighter()
    # Create variables to store player location
    player = Entity(x=0, y=0, char='@', colour=tcod.white, name='Player',
                    blocks=True, fighter=fighter_component)
    entities = [player]

    game_map = GameMap(width=map_width, height=map_height)
    game_map.create_map(max_rooms=max_rooms,
                        room_min_size=room_min_size,
                        room_max_size=room_max_size,
                        width=map_width,
                        height=map_height,
                        player=player,
                        entities=entities,
                        max_monsters_per_room=max_monsters_per_room,
                        map_type='regular')

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    # Define Key and Mouse objects
    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # Initialise the console with some hardcoded data
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(w=screenWidth, h=screenHeight, title='Esc to exit')
    console = tcod.console.Console(width=screenWidth, height=screenHeight)

    # Start the game loop
    while True:
        #####################
        ## Key-press logic ##
        #####################
        # Check input from keyboard or mouse
        tcod.sys_check_for_event(mask=tcod.EVENT_KEY_PRESS, k=key, m=mouse)

        # Compute fov if needed
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)

        # Write current state to console
        render.render_all(console=console,
                          entities=entities,
                          game_map=game_map,
                          fov_map=fov_map,
                          fov_recompute=fov_recompute,
                          screen_width=screenWidth,
                          screen_height=screenHeight,
                          colours=colours)
        fov_recompute = False  # Keep on false until we move again
        tcod.console_flush()
        # Remove all entities so we can update
        render.clear_all(console=console, entities=entities)

        # Translate keypress in to action
        action = inputHandlers.handleKeys(key)

        # dict.get returns None if key doesn't exist
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            dest_x = player.x + dx
            dest_y = player.y + dy
            if not game_map.is_blocked(x=dest_x, y=dest_y):
                enemy = get_blocking_entities_at(dest_x, dest_y, entity_list=entities)
                if enemy:
                    print('You make weird faces to the ' + enemy.name + '.\n',
                          'It stares blankly at you, then makes one back')
                else:
                    # move is a (dx, dy) tuple
                    player.move(*move)
                    fov_recompute = True

            game_state = GameStates.ENEMIES_TURN

        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        if game_state == GameStates.ENEMIES_TURN:
            for entity in entities:
                if entity.ai:
                    entity.ai.take_turn(player, fov_map, game_map)
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
