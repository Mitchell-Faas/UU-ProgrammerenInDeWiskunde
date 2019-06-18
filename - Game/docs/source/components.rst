.. _components:

Components
==========

Components contains a number of classes that are used to give certain properties and abilities to entities in the game. \
Examples of such entities are enemies, items, and the player themselves. Examples of properties are the ability to move, \
fight, carry items, etcetera.

AI
++

.. automodule:: components.ai
    :members: BasicMonster

The AI classes (just BasicMonster for now) employ one function: take_turn.
This function is called to elicit behaviour of an entity. Example:

.. code-block:: python

    AI = BasicMonster()
    AI.take_turn()

.. automodule:: components.fighter
    :members: Fighter

The fighter class gives us the functions we need to allow combat between entities.
It includes attacking, taking damage, healing, and other such functions.
Below follows a simplified example of combat.

.. code-block:: python

    fighter1 = Fighter(hp=5, defense=0, power=1)
    fighter2 = Fighter(hp=5, defense=0, power=1)
    # Entity1 = (..., fighter_component=fighter1)
    # Entity2 = (..., fighter_component=fighter2)
    fighter1.attack(Entity2)

    # As a result of this, Entity2 will take damage
    >>>fighter2.hp
    4

.. automodule:: components.inventory
    :members: Inventory

Below follows an example of how the inventory component is added to the player entity.

.. code-block:: python

    inventory_component = Inventory(26)
    # player = Entity(..., inventory=inventory_component)

.. automodule:: components.item
    :members: Item

Below follows an example of how the item component is added to an item entity.

.. code-block:: python

    item_component = Item(use_function=item_heal, amount=4)
    # item = Entity(..., item=item_component)