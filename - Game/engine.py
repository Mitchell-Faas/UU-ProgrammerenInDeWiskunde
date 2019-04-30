import tcod
import tcod.console
import inputHandlers

def main():
    screenWidth = 80
    screenHeight = 50

    # Create variables to store player location
    playerX = int(screenWidth / 2)
    playerY = int(screenHeight / 2)

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
        tcod.console_put_char(console, playerX, playerY, '@', tcod.BKGND_NONE)
        tcod.console_blit(console, x=0, y=0, w=screenWidth, h=screenHeight, dst=0, xdst=0, ydst=0)
        # Remove previous player position
        tcod.console_put_char(console, x=playerX, y=playerY, c=' ', flag=tcod.BKGND_NONE)
        tcod.console_flush()

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
            # move is a (dx, dy) tuple
            dx, dy = move
            playerX += dx
            playerY += dy
        if exit:
            return True
        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()
