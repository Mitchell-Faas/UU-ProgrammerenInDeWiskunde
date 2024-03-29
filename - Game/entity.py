import math
import tcod

from renderFunctions import RenderOrder

class Entity:
    """"A comprehensive object to represent any entity in the game.

    An entity is the main construct for things like monsters NPCs and items.
    This class provides all the options needed for a well functioning entity
    and is used for every entity in the game.

    Parameters
    ----------
    x : int
        Starting x coordinate of the entity.
    y : int
        Starting y coordinate of the entity.
    char : char
        Character (think !, ?, @, etc.) that represents this entity on the screen.
    colour : tcod.Color
        Render colour of the the entity's character.
    name : str
        Name of the entity.
    blocks : bool, optional
        Whether the player is able to walk through the entity or not.
        Defaults to False. (Meaning the player can walk through.)
    fighter : :obj:`Fighter`, optional
        Describes the stats used for fighting such as health, strength and defense.
        Also describes the available actions, such as different attacks.
        Defaults to None.
    ai : Class, optional
        A class that houses the AI logic of the entity. This class is required
        to have a `take_turn()` method.
        Defaults to None.
    render_order : int, optional
        Describes the order in which to render object (lowest first). Idiomatically
        used in conjunction with a `RenderOrder` class.
        Defaults to `RenderOrder.corpse`
    item : :obj:`Item`, optional
        An Item object.
        Defaults to None
    inventory: : :obj:`Inventory`, optional
        The inventory of this entity."""

    def __init__(self, x, y, char, colour, name, blocks=False,
                 fighter=None, ai=None, render_order=RenderOrder.corpse, item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self
        if self.item:
            self.item.owner = self
        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        """Moves the entity by some amount.

        Moves the entity by dx in the x direction and dy in the y direction.

        Parameters
        ----------
        dx : int
            Change in x direction
        dy : int
            Change in y direction"""
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        """Applies the entity-specific AI to move towards a target.

        Goes through the entire entity list and asks their AI to make
        a move towards a certain target based on its location and the
        game map.

        Parameters
        ----------
        target_x : int
            x-location of target
        target_y : int
            y-location of target
        game_map : :obj:`GameMap`
            Game map to apply the AI on
        entities : list
            List of all entities that need processing."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x+dx, self.y+dy) or
                get_blocking_entities_at(self.x + dx, self.y + dy, entities)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        """Uses A* algorithmic logic to move towards the target

        Parameters
        ----------
        target : :obj:`Entity`
            The target.
        entities : list
            List of entities to move
        game_map : :obj:`GameMap`
            Game Map to apply the algorithm on"""

        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        tcod.path_delete(my_path)

    def distance_to(self, other):
        """Calculates the distance from self to another entity

        Parameters
        ----------
        other : :obj:`Entity`
            Entity to which we need to calculate the distance"""
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx**2 + dy**2)


def get_blocking_entities_at(x, y, entity_list):
    """Checks if there are any movement-blocking entities at location

    Parameters
    ----------
    x : int
        x location
    y : int
        y location
    entity_list : list
        list of entities to check"""
    for entity in entity_list:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None
