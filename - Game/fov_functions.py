import tcod

def initialize_fov(game_map):
    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(m=fov_map, x=x, y=y,
                                    isTrans=not game_map.tiles[x][y].block_sight,
                                    isWalk=not game_map.tiles[x][y].blocked)
    return fov_map


def recompute_fov(fov_map, x, y, radius=10, light_walls=True, algorithm=0):
    tcod.map_compute_fov(m=fov_map, x=x, y=y, radius=radius,
                         light_walls=light_walls, algo=algorithm)
