.. _map_objects:

Map Objects
===========

.. automodule:: map_objects.game_map
    :members:

.. automodule:: map_objects.tile
    :members:

A tile has several kinds of important attributes. For example, we need to know whether a tile is bloody or not \
to determine what colour to use when rendering it.

.. code-block:: python

    bled_on_tile = turn_results.get('bled_on_tile')
    if bled_on_tile:
        game_map.tiles[bled_on_tile[0]][bled_on_tile[1]].bloody = True

.. automodule:: map_objects.rectangle
    :members:

Rectangles are used to create rooms during procedural level generation.

.. code-block:: python

    room_width = randint(room_min_size, room_max_size)
    room_height = randint(room_min_size, room_max_size)
    x = randint(0, width - room_width - 1)
    y = randint(0, height - room_height - 1)

    new_room = Rect(x=x, y=y, width=room_width, height=room_height)

