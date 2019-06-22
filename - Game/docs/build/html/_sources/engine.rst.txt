.. _engine:

Engine Components
=================

.. automodule:: entity
    :members:

The entity class is extremely broad, and used frequently throughout the game. Below are examples of the main use cases.

First, creating and using the player entity.
.. code-block:: python

    fighter_component = Fighter(15, 0, 3)
    # player = Entity(..., fighter=fighter_component, ...)
    entities = [player]

The creation of enemies is very similar.

Next, creating items.
.. code-block:: python

    item_component = Item(use_function=item_heal, amount=4)
    # item = Entity(..., item=item_component)
    entities.append(item)

.. automodule:: game_states
    :members:

An example case in which we need to know the game-state follows below.

.. code-block:: python

    if game_state == GameStates.PLAYERS_TURN:
        if player.move:
            # Move the player
            game_state = GameStates.ENEMIES_TURN