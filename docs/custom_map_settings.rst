Custom Map settings
===================

The Custom Map settings can be accessed in the Collection panel in the Properties Inspector whenever the Collection named 'CustomMap' is selected, or any of it's subcollections.

Map Information
---------------

Here you can select the name of your Custom Map.

You can edit the map description which will be displayed in-game and on the Steam Workshop page for your map when you :doc:`release <guides/releasing_a_map>` it.

You can select a map image which will be displayed in-game and on the Steam Workshop page for your map when you release it. It is recommended that the image file should be below 150KB. The in-game resolution is 490x200 pixels, but you can choose up to 1024 pixels in any dimension in case you want a higher resolution in the Steam Workshop.

Required Objects
----------------

There are some required objects that you need in order to get a working map.

The Spawn Location chooses where the player will spawn. This is just an empty object and only the location will be used.

The Progress Path is the path of progress in your map. This path will determine the percentage completion in the game.

The Start Line is a special object that will dissapear once the run is started. The run will start when the player leaves a circle around the Start Line location with a radius of roughly 475 pogo units in diameter.

Splits
------

Whenever you add a region with the region type of 'Split', it will be added to the list here. You can order the splits to choose in which order they will appear in-game. The name of any given split is the name of the Region.

.. warning::

  If you delete a split region this list might become desynced. Press the button with the refresh icon to resync.

Modes
-----

You can select which modes should be active on your map.

**Double Jump**, **Puzzle**, and **Ice** is like the ones from the main game.

**No Boost** disables boosting on the entire map. 

**No Bonk** kills the player whenever they bonk on anything.

**Mushroom Power** chooses whether or not mushrooms can have a custom power value. This is only relevant for entities that has the 'Mushroom Bones' action. I don't know why you would tick it off, but you can.

.. _static_files:

Static Files
------------

Here you can add a list of files you want to be added to the Custom Map folder. This could be if you have .mdl or texture files that the add-on cannot generate, or maybe you want to add a txt file with a note or lore.
