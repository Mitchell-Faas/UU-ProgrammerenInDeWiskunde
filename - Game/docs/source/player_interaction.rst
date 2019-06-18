.. _player_interaction:

User Interface
==================

.. automodule:: gameMessages
    :members:

Sometimes we want to let the player know something important. Such as the fact that an enemy has already died, and that \
there is really no point in continuing to beat their bloody corpse. In such cases, a message is sent to the message log.

.. code-block:: python

    player_turn_result = {'message': Message("Stop! Stop! He's already dead!")}
    message = player_turn_result.get('message')
    messageLog.add_message(message)

.. automodule:: menus
    :members:

.. code-block:: python

    if game_state == GameStates.SHOW_INVENTORY
                inventory_menu(console, inventory_title, player.inventory, 50, screen_width, screen_height)