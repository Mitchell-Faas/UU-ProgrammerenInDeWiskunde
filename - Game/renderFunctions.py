import tcod

def render_all(console, entities, game_map, fov_map, fov_recompute,
               screen_width, screen_height, colours):
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

                if visible:
                    if wall:
                        colour = colours.get('light_wall')
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
                else: # If unexplored, colour the area black
                    colour = colours.get('black')

                tcod.console_set_char_background(con=console,
                                                 x=x, y=y,
                                                 col=colour,
                                                 flag=tcod.BKGND_SET)


    # Draw all entities in the list
    for entity in entities:
        draw_entity(console, entity, fov_map)

    tcod.console_blit(src=console,
                      x=0, y=0,
                      w=screen_width,
                      h=screen_height,
                      dst=0,
                      xdst=0, ydst=0)

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