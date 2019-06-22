.. _auxiliary_functions:

Auxiliary Functions
===================

Input Handling
++++++++++++++

.. automodule:: inputHandlers
    :members:

Below follows an example of how inputs are recognized and handled.

.. code-block:: python

    action = inputHandlers.handleKeys(key, game_state)
    wait = action.get('wait')
    if wait:
        game_state = GameStates.ENEMIES_TURN

Rendering
+++++++++

.. automodule:: fov_functions
    :members:

.. automodule:: renderFunctions
    :members:

These renderfunctions are used together in engine.py to calculate what to put on the display.

.. code-block:: python

    if fov_recompute:
        recompute_fov(fov_map, player.x, player.y)

    # render.render_all(..., fov_map=fov_map, ...)
    fov_recompute = False
    tcod.console_flush()

Death Functions
++++++++++++++++++++++

.. automodule:: death_functions
    :members:

    Here we keep the functions necessary for killing various entities. For example, when player hp reaches zero, they die.

.. code-block:: python

    player.fighter.take_damage()

    dead_entity = enemy_turn_result.get('dead')
    if dead_entity == player
        kill_player(dead_entity)

Item Functions
++++++++++++++

Here we keep the functions our items have upon being used. Currently this consists only of a healing function.

.. automodule:: item_functions
    :members:
