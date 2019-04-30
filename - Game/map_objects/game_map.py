from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]


        return tiles

    def create_map(self,max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x=x,y=y,w=w,h=h)
            # Check if the new room intersects any previous ones
            for other_room in rooms:
                if new_room.intersect(other_room):
                    # They intersect; don't add this room
                    break
            else:
                # There are no intersections with other rooms, it is valid

                # Carve out this room on the map
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_center_x, new_center_y) = new_room.center()

                if num_rooms == 0:
                    # This is the first room, where the player starts at
                    player.x = new_center_x
                    player.y = new_center_y
                else:
                    # This is not the first room. That means we need to connect it to the previous one using tunnels.

                    # Take the center coordinates of the previous room
                    (prev_center_x, prev_center_y) = rooms[num_rooms-1].center()

                    # Choose randomly whether to first dig vertically then horizontally, or vice versa
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_center_x, new_center_x, prev_center_y)
                        self.create_v_tunnel(prev_center_y, new_center_y, new_center_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_center_y, new_center_y, prev_center_x)
                        self.create_h_tunnel(prev_center_x, new_center_x, new_center_y)

                # Add the succesfully placed room to the list of rooms
                rooms.append(new_room)
                num_rooms += 1


    def create_room(self,room):
        # Go through each tile in the rectangle and make it passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self,x1,x2,y):
        for x in range (min(x1,x2),max(x1,x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self,y1,y2,x):
        for y in range (min(y1,y2),max(y1,y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False