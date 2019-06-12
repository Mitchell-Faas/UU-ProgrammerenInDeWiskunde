import tcod

def menu(console, header, options, width, screen_width, screen_height):
    """Sets up an interactive menu

    Menu displays options for interactive behaviour and pauses the game
    while it's being accessed.

    Parameters
    ----------
    console : tcod.Console
        Console window to draw to
    header : str
        Header text for the menu
    options : list
        List with available options to choose from
    width : int
        Width of menu screen
    screen_width : int
        Width of the entire game-screen (window)
    screen_height : int
        Height of the entire game-screen (window)"""

    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = tcod.console_get_height_rect(console, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)

    # print the header, with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(console, header, inventory, inventory_width, screen_width, screen_height):
    """Shows a menu which has the items stored in your inventory as options.
    For further information please look at the documentation for :obj:`menu`"""
    if len(inventory.items) == 0:
        options = ['You own nothing save the clothes on your back.']
    else:
        options = [item.name for item in inventory.items]

    menu(console, header, options, inventory_width, screen_width, screen_height)