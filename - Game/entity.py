class Entity:
    """"An object representing entities"""

    def __init__(self, x, y, char, colour, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


def get_blocking_entities_at(x, y, entity_list):
    for entity in entity_list:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None
