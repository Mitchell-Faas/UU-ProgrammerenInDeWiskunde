import tcod


def render_all(console, entities, game_map, screen_width, screen_height, colours):
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
    # Draw the tiles in game_map
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                tcod.console_set_char_background(console, x, y, colours.get('dark_wall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(console, x, y, colours.get('dark_ground'), tcod.BKGND_SET)

    # Draw all entities in the list
    for entity in entities:
        draw_entity(console, entity)

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


def draw_entity(console, entity):
    """Renders a given entity on the screen.

    params
    -------------
    console: console object
    entity: entity object

    returns
    -------------
    None
    """

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