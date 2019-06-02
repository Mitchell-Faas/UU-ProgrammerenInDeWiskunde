import inputHandlers
import renderFunctions as render
import tcod
import tcod.console
from entity import Entity, get_blocking_entities_at
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from map_objects.game_map import GameMap
from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_player, kill_monster
from gameMessages import Message, MessageLog

# To do: Fix: player moving into a wall skips their turn, allowing enemies to move
# To do: Add: pressing '5' should skip player turn

"""
Created by Mitchell Faas and Pim te Rietmole
Heavily based on the python 3 roguelike tutorial at http://rogueliketutorials.com/tutorials/tcod/
"""

def main():
    screenWidth = 80
    screenHeight = 50

    barWidth = 20
    panelHeight = 7
    panelY = screenHeight-panelHeight

    messageX = barWidth + 2
    messageWidth = screenWidth - barWidth - 2
    messageHeight = panelHeight - 1

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2

    colours = {'dark_wall': tcod.Color(0, 0, 100),
               'dark_ground': tcod.Color(50, 50, 150),
               'light_wall': tcod.Color(130, 110, 50),
               'light_ground': tcod.Color(200, 180, 50),
               'black': tcod.Color(0, 0, 0)}

    fighter_component = Fighter(15,0,3)
    inventory_component = Inventory(26)
    # Create variables to store player location
    player = Entity(x=0, y=0, char='@', colour=tcod.white, name='Player',
                    blocks=True, fighter=fighter_component, render_order=render.RenderOrder.actor,
                    inventory=inventory_component)
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
                        max_items_per_room=max_items_per_room,
                        map_type='regular')

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    messageLog = MessageLog(messageX, messageWidth, messageHeight)

    # Define Key and Mouse objects
    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    # Initialise the console with some hardcoded data
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(w=screenWidth, h=screenHeight, title='Esc to exit')
    console = tcod.console.Console(width=screenWidth, height=screenHeight)
    # UI at bottom of screen
    panel = tcod.console.Console(screenWidth, panelHeight)

    # Start the game loop
    while True:
        #####################
        ## Key-press logic ##
        #####################
        # Check input from keyboard or mouse
        tcod.sys_check_for_event(mask=tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, k=key, m=mouse)

        # Compute fov if needed
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y)

        # Write current state to console
        render.render_all(console=console,
                          panel=panel,
                          entities=entities,
                          player=player,
                          game_map=game_map,
                          fov_map=fov_map,
                          fov_recompute=fov_recompute,
                          messageLog=messageLog,
                          screen_width=screenWidth,
                          screen_height=screenHeight,
                          barWidth=barWidth,
                          panelHeight=panelHeight,
                          panelY=panelY,
                          mouse=mouse,
                          colours=colours,
                          game_state=game_state)
        fov_recompute = False  # Keep on false until we move again
        tcod.console_flush()
        # Remove all entities so we can update
        render.clear_all(console=console, entities=entities)

        # Translate keypress in to action
        action = inputHandlers.handleKeys(key, game_state)

        # dict.get returns None if key doesn't exist
        move = action.get('move')
        exit = action.get('exit')
        pickup = action.get('pickup')
        wait = action.get('wait')
        show_inventory = action.get('show_inventory')
        inventory_index = action.get('inventory_index')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            dest_x = player.x + dx
            dest_y = player.y + dy
            if not game_map.is_blocked(x=dest_x, y=dest_y):
                enemy = get_blocking_entities_at(dest_x, dest_y, entity_list=entities)
                if enemy:
                    attack_results = player.fighter.attack(enemy)
                    player_turn_results.extend(attack_results)
                else:
                    # move is a (dx, dy) tuple
                    player.move(*move)
                    fov_recompute = True
                game_state = GameStates.ENEMIES_TURN
            else:
                player_turn_results.extend([{'message': Message('The wall stubbornly refuses to move.',tcod.sky)}])
        elif wait and game_state == GameStates.PLAYERS_TURN:
            game_state = GameStates.ENEMIES_TURN
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                player_turn_results.extend([{'message': Message('There is nothing to pick up.',tcod.sky)}])
        # Take necessary steps to display inventory
        elif show_inventory:
            # Sets what state to go back to after exiting the inventory
            if game_state != GameStates.SHOW_INVENTORY: # Exit state can't also be inventory
                previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        # Take necessary steps to select item from inventory
        elif inventory_index != None and previous_game_state != GameStates.PLAYER_DEAD \
                and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            player_turn_results.extend(player.inventory.use(item))


        if exit:
            if game_state == GameStates.SHOW_INVENTORY:
                game_state = previous_game_state
            else:
                return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
        # Look at the results of the player's turn and print the appropriate messages
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')

            if message:
                messageLog.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                messageLog.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMIES_TURN

            if item_consumed:
                game_state = GameStates.ENEMIES_TURN

        if game_state == GameStates.ENEMIES_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    if enemy_turn_results:
                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')

                            if message:
                                messageLog.add_message(message)

                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                messageLog.add_message(message)

                                if game_state == GameStates.PLAYER_DEAD:
                                    break # Ignore further results of this enemy's turn
                        if game_state == GameStates.PLAYER_DEAD:
                            break # Skip other enemies' turns

            else: # If the for-loop was broken, dont give player their turn back
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
