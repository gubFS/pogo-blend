Map Bounds
==========

Once you reach a certain distance you will exit the bounds of the map, and the rendering in Pogostuck will freak out and you won't be able to see.

I don't have the exact details but the general gist is this:

The bounds have a fixed minimum size to start with, and then they will expand just beyond the origin of the closest object to the bounds. So if you are hitting the bounds of the map, try placing a dummy object further out.

