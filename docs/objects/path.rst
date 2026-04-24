Paths
=====

Paths are a series of points connected by lines. 

The only uses for paths are for the progress path, and the paths used with the thorns action.

To create a Path open the add menu and under PogoBlend you can select Path. 

You can create branching paths, by placing points on top of eachother but it's not really supported in Blender or Pogostuck (for the progress on the Progress Path), so it's best to just make a non-branching linear path.

.. caution::

   Any Curve Object in Blender can become a Pogo Path but the builder only uses the points to create the path, so curves like Bezier Curves can have deceptive visuals that don't convey what the path will actually look like in-game. So use the provided way of making paths in the ``Add -> PogoBlend -> Path`` or change the spline type of your Curve to 'Poly'.
