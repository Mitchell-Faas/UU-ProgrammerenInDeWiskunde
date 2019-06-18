.. _components:

Components
==========

Components contains a number of classes that are used to give certain properties and abilities to entities in the game. \
Examples of such entities are enemies, items, and the player themselves. Examples of properties are the ability to move, \
fight, carry items, etcetera.

.. automodule:: components.ai
    :members: BasicMonster

.. automodule:: components.fighter
    :members: Fighter

Below follows an example of how the ai and fighter components are used when creating an entity.

.. codeblock:: python

    fighter_component = Fighter(hp=5, defense=0, power=1)
    ai_component = BasicMonster()
    monster = Entity(x, y, 'o', tcod.Color(0, 80, 0), 'orc', blocks=True, fighter=fighter_component, ai=ai_component, render_order=RenderOrder.actor)

.. automodule:: components.inventory
    :members: Inventory

Below follows an example of how the inventory component is added to the player entity.

.. codeblock:: python

    inventory_component = Inventory(26)
    player = Entity(x=0, y=0, char='@', colour=tcod.white, name='Player',
                    blocks=True, fighter=fighter_component, render_order=render.RenderOrder.actor,
                    inventory=inventory_component)

.. automodule:: components.item
    :members: Item

Below follows an example of how the item component is added to an item entity.

.. codeblock:: python

    item_component = Item(use_function=item_heal, amount=4)
    item = Entity(self.owner.x, self.owner.y, '!', tcod.Color(147, 113, 230), 'Blood Crystal',
                              render_order=RenderOrder.item, item=item_component)