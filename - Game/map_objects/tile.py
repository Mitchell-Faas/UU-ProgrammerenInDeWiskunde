class Tile:
    """
    A tile, may or may not be blocked, may block sight.
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked
        self.explored = False

        if not block_sight:
            block_sight = blocked

        self.block_sight = block_sight
