import tcod
from enum import Enum
from game_states import GameStates
from menus import inventory_menu

class RenderOrder(Enum):
    """Static data on render order"""
    corpse = 1
    item = 2
    actor = 3

def get_names_under_mouse(mouse, entities, fov_map):
    """Finds the name of whichever entity is located below the cursor

    Parameters
    ----------
    mouse : tcod.Mouse
        Mouse object which gives coordinates
    entities : list
        List of entities on the map
    fov_map : :obj:`GameMap`
        Mapobject which gives the FOV (Don't want to show
        objects which we can't see.)

    Returns
    -------
    str
        Name of the entity your cursor is positioned above"""
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()

def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    """"""
    barWidth = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if barWidth > 0:
        tcod.console_rect(panel, x, y, barWidth, 1, False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_all(console, panel, entities, player, game_map, fov_map, fov_recompute, messageLog,
               screen_width, screen_height, barWidth, panelHeight, panelY, mouse, colours, game_state):
    """Renders all given entities on the screen.

    params
    -------------
    console: console object
    entities: list of entity objects
    game_map: nested list containing all tiles on the map
    screen_width: horizontal length of the screen in number of tiles
    screen_height: vertical length of the screen in number of tiles
    colours: dictionary containing the colours of different map tiles
    returns
    -------------
    None
    """
    if fov_recompute:
        # Draw the tiles in game_map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                bloody = game_map.tiles[x][y].bloody

                if visible:
                    if wall:
                        colour = colours.get('light_wall')
                    elif bloody:
                        colour = colours.get('bloody_ground')
                    else:
                        colour = colours.get('light_ground')
                    # We've now explored this tile
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    # Only render walls and ground that's explored
                    if wall:
                        colour = colours.get('dark_wall')
                    else:
                        colour = colours.get('dark_ground')
                else:  # If unexplored, colour the area black
                    colour = colours.get('black')

                tcod.console_set_char_background(con=console,
                                                 x=x, y=y,
                                                 col=colour,
                                                 flag=tcod.BKGND_SET)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(console, entity, fov_map)


    tcod.console_blit(src=console,
                      x=0, y=0,
                      w=screen_width,
                      h=screen_height,
                      dst=0,
                      xdst=0, ydst=0)
    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 1
    for message in messageLog.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, messageLog.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, barWidth, 'BLOOD', player.fighter.hp, player.fighter.max_hp,
               tcod.light_red, tcod.darker_red)

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    # Blit UI bar
    tcod.console_blit(src=panel,
                      x=0, y=0,
                      w=screen_width,
                      h=panelHeight,
                      dst=0,
                      xdst=0, ydst=panelY)

    # Display inventory
    if game_state in (GameStates.SHOW_INVENTORY,GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'
        inventory_menu(console, inventory_title, player.inventory, 50, screen_width, screen_height)

def clear_all(console, entities):
    """Removes all given entities from screen.
    params
    -------------
    console: console object
    entities: list of entity objects
    returns
    -------------
    None"""
    for entity in entities:
        clear_entity(console, entity)


def draw_entity(console, entity, fov_map):
    """Renders a given entity on the screen.

    params
    -------------
    console: console object
    entity: entity object

    returns
    -------------
    None
    """
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y):
        tcod.console_set_default_foreground(con=console, col=entity.colour)
        tcod.console_put_char(con=console,
                              x=entity.x, y=entity.y,
                              c=entity.char,
                              flag=tcod.BKGND_NONE)


def clear_entity(console, entity):
    """Removes a given entity from the screen.

    params
    -------------
    console: console object
    entity: entity object

    returns
    -------------
    None
    """
    # erase the character that represents this object
    tcod.console_put_char(con=console,
                          x=entity.x, y=entity.y,
                          c=' ',
                          flag=tcod.BKGND_NONE)
