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

"""
Created by Mitchell Faas and Pim te Rietmole
Heavily based on the python 3 roguelike tutorial at http://rogueliketutorials.com/tutorials/tcod/
"""


def main():

    screenWidth = 80
    screenHeight = 50

    barWidth = 20
    panelHeight = 7
    panelY = screenHeight - panelHeight

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

    colours = {'dark_wall': tcod.Color(0, 0, 50),
               'dark_ground': tcod.Color(25, 25, 60),
               'light_wall': tcod.Color(70, 70, 70),
               'light_ground': tcod.Color(120, 120, 120),
               'bloody_ground': tcod.Color(130, 30, 30),
               'black': tcod.Color(0, 0, 0)}

    fighter_component = Fighter(15, 0, 3)
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
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        # This section tells the game how to respond to various inputs
        if game_state == GameStates.PLAYERS_TURN:
            # Player moved
            if move:
                dx, dy = move
                dest_x = player.x + dx
                dest_y = player.y + dy

                # Check if destination is blocked
                if not game_map.is_blocked(x=dest_x, y=dest_y):
                    enemy = get_blocking_entities_at(dest_x, dest_y, entity_list=entities)
                    # Attack if we try to move on to an enemy
                    if enemy:
                        attack_results = player.fighter.attack(enemy)
                        player_turn_results.extend(attack_results)
                    else:
                        player.move(*move) # move is a (dx, dy) tuple
                        fov_recompute = True

                    game_state = GameStates.ENEMIES_TURN
                else:
                    # The destination is blocked
                    player_turn_results.extend([{'message': Message('The wall stubbornly refuses to move.', tcod.sky)}])

            # Player picked something up
            elif pickup:
                # Check if there's an item to be picked up, and pick up all such items
                for entity in entities:
                    if entity.item and entity.x == player.x and entity.y == player.y:
                        pickup_results = player.inventory.add_item(entity)
                        player_turn_results.extend(pickup_results)
                else:
                    player_turn_results.extend([{'message': Message('The ground growls at you for touching it!', tcod.sky)}])

            # Player decided to wait a turn
            elif wait:
                game_state = GameStates.ENEMIES_TURN

        # Take necessary steps to display inventory
        elif show_inventory:
            # Sets what state to go back to after exiting the inventory
            if game_state != GameStates.SHOW_INVENTORY:  # Exit state can't also be inventory
                previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        # Take necessary steps to select item from inventory
        elif inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD \
                and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop(item))

        # Take necessary steps to allow the player to drop items
        elif drop_inventory:
            if game_state != GameStates.DROP_INVENTORY:  # Exit state can't also be drop menu
                previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY
        # On pressing escape, exits the current menu. If not in a menu, exits the game
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                # Exit the menu to the previous state
                game_state = previous_game_state
            else:
                # Exit the game
                return True
        # If the relevant keys are pressed, enters full-screen mode
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


        # Look at the results of the player's turn and print the appropriate
        # Also implement the consequences of various turn results
        # E.g. dropping an item places it in the list of entities
        # E.g. places blood on a tile after the entity on it was attacked
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            enemy_item_dropped = player_turn_result.get('enemy_item_dropped')
            item_dropped = player_turn_result.get('item_dropped')
            bled_on_tile = player_turn_result.get('bled_on_tile')

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

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMIES_TURN

            if enemy_item_dropped:
                entities.append(enemy_item_dropped)

            if bled_on_tile:
                game_map.tiles[bled_on_tile[0]][bled_on_tile[1]].bloody = True

        # This section goes through the list of entities and tells them to take their turns
        if game_state == GameStates.ENEMIES_TURN:
            for entity in entities:
                if entity.ai:
                    # The enemy is an intelligent actor, and can thus take a turn
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
                    if enemy_turn_results:
                        # If there are any results of enemy actions we need to handle, we do so here
                        for enemy_turn_result in enemy_turn_results:
                            message = enemy_turn_result.get('message')
                            dead_entity = enemy_turn_result.get('dead')
                            bled_on_tile = enemy_turn_result.get('bled_on_tile')

                            # Add any messages to the messagelog
                            if message:
                                messageLog.add_message(message)

                            # Spray blood where necessary
                            if bled_on_tile:
                                game_map.tiles[bled_on_tile[0]][bled_on_tile[1]].bloody = True

                            # Make sure to properly kill any dead entities
                            if dead_entity:
                                if dead_entity == player:
                                    message, game_state = kill_player(dead_entity)
                                else:
                                    message = kill_monster(dead_entity)

                                messageLog.add_message(message)

                                # If the player died, break out of the loop
                                if game_state == GameStates.PLAYER_DEAD:
                                    break  # Ignore further results of this enemy's turn

                        if game_state == GameStates.PLAYER_DEAD:
                            break  # Skip other enemies' turns

            else:  # If the for-loop was broken, dont give player their turn back
                game_state = GameStates.PLAYERS_TURN

# Run the game
if __name__ == '__main__':
    main()
