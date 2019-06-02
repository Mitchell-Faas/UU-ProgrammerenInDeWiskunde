from random import randint

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from renderFunctions import RenderOrder

import tcod
from entity import Entity
from map_objects.rectangle import Rect
from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(blocked=True) for y in range(self.height)]
                 for x in range(self.width)]
        return tiles

    def create_map(self, max_rooms, room_min_size, room_max_size, width, height,
                   player, entities, max_monsters_per_room, max_items_per_room, map_type='regular'):
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
        # Go through each tile in the rectangle and make it passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room, max_items_per_room):
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

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_component = Item()
                item = Entity(x, y, '!', tcod.violet, 'Blood Crystal',
                              render_order=RenderOrder.item, item=item_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
