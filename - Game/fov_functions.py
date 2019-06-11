import tcod

def initialize_fov(game_map):
    """Creates a new :obj:`GameMap` based on FOV calculations.

    Parameters
    ----------
    game_map : :obj:`GameMap`
        Game map over which to compute FOV."""
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(m=fov_map, x=x, y=y,
                                    isTrans=not game_map.tiles[x][y].block_sight,
                                    isWalk=not game_map.tiles[x][y].blocked)
    return fov_map


def recompute_fov(fov_map, x, y, radius=10, light_walls=True, algorithm=0):
    """Recomputes a FOV map

    Uses the player coordinates to update the fov map.

    Parameters
    ----------
    fov_map : :obj:`GameMap`
        old FOV map
    x : int
        player x-location
    y : int
        player y-location
    radius : int
        radius of vision around player
    light_walls : bool
        Whether or not to light the first block of the walls we see
    algorithm : int
        The integer identification of the algorithm we want to use
        for FOV computation."""

    tcod.map_compute_fov(m=fov_map, x=x, y=y, radius=radius,
                         light_walls=light_walls, algo=algorithm)
