class Tile:
    """A class for tiles in the game-map

    A tile in the game-map. It may or may not be passable, and it may or may not block sight.

    Parameters
    ----------
    blocked : bool
        A boolean which determines whether this tile can be walked through.
    block_sight : bool, optional
        A boolean which determines whether this tile can be seen through.
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        if not block_sight:
            block_sight = blocked

        self.block_sight = block_sight
