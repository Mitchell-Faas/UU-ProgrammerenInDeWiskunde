from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from renderFunctions import RenderOrder

import tcod
from entity import Entity
from item_functions import item_heal
from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    """A class to represent information about the game map

    This class is used to save information about the game map. This mainly involves the different types of tiles
    (walkable, non-walkable, transparent or opaque) in different positions.

    Parameters
    ----------
    width : int
        The horizontal number of tiles in the map
    height : int
        The vertical number of tiles in the map
    tiles : list
        This is a nested list which serves as an array, to keep track of what tiles are walls, and which are not.
        We start out with a game-map fully consisting of walls, and then dig out rooms and corridors.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        """A function to construct the initial game-map

        This function allows us to create an array of tiles, the width and height of the game-map.
        We return this array. This array is initially completely filled with walls.
        It is later altered by digging out rooms and corridors, so it can serve as a map
        the player can maneuver through.
        """
        tiles = [[Tile(blocked=True) for _ in range(self.height)]
                 for _ in range(self.width)]
        return tiles

    def create_map(self, max_rooms, room_min_size, room_max_size, width, height,
                   player, entities, max_monsters_per_room, max_items_per_room, map_type='regular'):
        """A function that constructs a playable version of the game-map

        This function takes the initial game-map, which consists of only walls. It digs out rooms, connects
        them via corridors, and places entities and items.

        Parameters
        ----------
        max_rooms : int
            The maximum number of rooms in a game-map. This is the number of times this function will attempt
            to place a room before finishing.
        room_min_size: int
            The minimum width and height allowed for rooms that are placed procedurally, in number of tiles.
        room_max_size: int
            The maximum width and height allowed for rooms that are placed procedurally, in number of tiles.
        width : int
            The horizontal number of tiles in the map.
        height : int
            The vertical number of tiles in the map.
        player : :obj:`Entity`
            The instance of the Entity class representing the player. It is handed to the create_map function so
            it can be placed to initially start in a room.
        entities : list
            A list of instances of the Entity class. When handed to this function, it normally only contains the player.
            Other entities such as enemies are added to this list during procedural map generation.
        max_monsters_per_room : int
            The maximum number of enemies allowed to be placed in a single procedurally generated room.
        max_items_per_room : int
            The maximum number of items allowed to be placed in a single procedurally generated room.
        map_type : str, optional
            A string indicating what type of map to generate. Setting it to anything other than 'regular' allows
            for the creation of non-standard maps, such as boss-rooms, using a different generation procedure.
        """
        if map_type == 'regular':
            rooms = []
            num_rooms = 0

            for r in range(max_rooms):
                # random room_width and room_height
                room_width = randint(room_min_size, room_max_size)
                room_height = randint(room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = randint(0, width - room_width - 1)
                y = randint(0, height - room_height - 1)

                new_room = Rect(x=x, y=y, width=room_width, height=room_height)
                # Check if the new room intersects any previous ones
                for other_room in rooms:
                    if new_room.intersects_with(other_room):
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
                        (prev_center_x, prev_center_y) = rooms[num_rooms - 1].center()

                        # Choose randomly whether to first dig vertically then horizontally, or vice versa
                        if randint(0, 1) == 1:
                            self.create_h_tunnel(prev_center_x, new_center_x, prev_center_y)
                            self.create_v_tunnel(prev_center_y, new_center_y, new_center_x)
                        else:
                            # first move vertically, then horizontally
                            self.create_v_tunnel(prev_center_y, new_center_y, prev_center_x)
                            self.create_h_tunnel(prev_center_x, new_center_x, new_center_y)

                    # Place some monsters
                    self.place_entities(new_room, entities, max_monsters_per_room, max_items_per_room)

                    # Add the succesfully placed room to the list of rooms
                    rooms.append(new_room)
                    num_rooms += 1

        if map_type == 'boss1':
            entry_room = Rect(x=10, y=21, width=6, height=6)
            self.create_room(entry_room)
            (player.x, player.y) = entry_room.center()
            boss_hall = Rect(x=20, y=9, width=40, height=30)
            self.create_room(boss_hall)
            self.create_h_tunnel(5, player.x, player.y)
            self.create_v_tunnel(player.y - 8, player.y + 8, 5)
            self.create_h_tunnel(5, 30, player.y + 8)
            self.create_h_tunnel(5, 30, player.y - 8)



    def create_room(self, room):
        """A function for digging out rooms.

        This function digs out a room in the game-map, of a certain size and at a certain position.

        Parameters
        ----------
        room : :obj:`Rect`
            An instance of the rectangle class, used for the position and proportions of the room to be placed.
        """
        # Go through each tile in the rectangle and make it passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        """A function for digging out horizontal corridors.

        This function digs out a horizontal corridor in the game-map, of a certain length and at a certain position.

        Parameters
        ----------
        x1 : int
            This integer indicates the horizontal coordinate of one end of the corridor.
        x2 : int
            This integer indicates the horizontal coordinate of the other end of the corridor.
        y : int
            This integer indicates the vertical coordinate of the corridor.
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        """A function for digging out vertical corridors.

        This function digs out a vertical corridor in the game-map, of a certain length and at a certain position.

        Parameters
        ----------
        y1 : int
            This integer indicates the vertical coordinate of one end of the corridor.
        y2 : int
            This integer indicates the vertical coordinate of the other end of the corridor.
        x : int
            This integer indicates the horizontal coordinate of the corridor.
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    @staticmethod
    def place_entities(room, entities, max_monsters_per_room, max_items_per_room):
        """A static function that places enemies and items

        This function is used to populate a single room with both items and enemies.

        Parameters
        ----------
        room : :obj:`Rect`
            An instance of the Rectangle class. This is the room we place things in.
        entities : list
            The list of entities on the floor. Any items or enemies that are placed, are appended to this list.
        max_monsters_per_room : int
            The maximum number of enemies allowed to be placed in a single procedurally generated room.
        max_items_per_room : int
            The maximum number of items allowed to be placed in a single procedurally generated room.
        """
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # One-liner to say: If there's not already an entity at this location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # Add some variety in monsters
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=5, defense=0, power=1)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'orc', blocks=True,
                                     fighter=fighter_component, ai=ai_component, render_order=RenderOrder.actor)
                else:
                    fighter_component = Fighter(hp=10, defense=1, power=1)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', tcod.darker_green, 'troll', blocks=True,
                                     fighter=fighter_component, ai=ai_component, render_order=RenderOrder.actor)

                entities.append(monster)

    def is_blocked(self, x, y):
        """A function to check if a tile is blocked

        This function checks the game-map's tile array, to see whether a tile can be moved through or not.

        Parameters
        ----------
        x : int
            The horizontal coordinate of the tile to be checked
        y : int
            The vertical coordinate of the tile to be checked
        """
        if self.tiles[x][y].blocked:
            return True

        return False
