Getting Started
===============

.. admonition:: Video
   :class: video

   There is a video of the Getting Started guide `here <https://www.youtube.com/watch?v=RjmvBSbCaFo>`__. This video is meant to be supplementary, and not a substitution, to the guide, so I suggest you still read it through.

Before making your first Map, here is some basic information that you should know:

Pogostucks coordinate systems looks toward the positive Y-axis. So to look in the Blender file as you would in Pogostuck, position the Camera to look into the Y-axis with a orthographic view, to simulate how it would look in-game. You can do this by clicking on the '-Y' on the Gimbal in the top right of the main view, or with a shortcut (default is NUMPAD1).

.. tip::

   If you have made Custom Maps before using WED, please first check out the page for :doc:`differences from WED<wed_differences>`, as this add-on attempts to be more streamlined, so many things you would do in WED are no longer neccesary.

Custom Maps are built using regular Blender objects. Only objects that are in a Collection named 'CustomMap' and has 'PogoData' will be included in the map. You can add, remove and edit PogoData in the Properties Inspector.

Regular meshes can be :doc:`Entities <objects/entity>` and are the main building blocks of a Custom Map. Entities has materials, flags and actions, aswell as regular data such as location, rotation and scale. The most important flag on an entity is the 'Collision' flag. If enabled the Pogo Dude will be able to collide with the entity. Collision only occur where y=0, so make sure to position your objects on the XZ plane. PogoBlend also offers the **Auto Collision** flag, which will create a collider that matches the entities sideview. Read more about collisions :ref:`here <collisions>`

:doc:`Regions <objects/region>` are areas that will affect the Pogo Dude while they are in it. You can create a region from the regular add menu under "PogoBlend". Regions have types that will have different effects.

:doc:`Paths <objects/path>` are only used for the 'ProgressPath' and Thorn paths. The progress path is the path of progress in the map and will be used for the percentage completion in the map. If an entity is using the Thorns action, you can pick a Path and the Pogo Dude will be sent to the closest point on the Path on contact with the Entity. You can also create Paths from the regular add menu.

.. seealso::

   The :doc:`Objects <objects/object>` page for more information on entities, regions and paths.

Making a Map
------------

To start making a Map, open Blender and make a new project. I recommend using the provided Application Template, under ``File -> New -> PogoBlend``. Save the Blender file to a folder where you will store all your project files, e.g ``Desktop/CustomMapProjects/MyMap/MyMap.blend``.

To make a custom map there is 3 required objects. A Spawn Position, a Start Line, and a Progress Path. The provided Application Template, will automatically create and set these.

These objects will need to be set in the CustomMap collection. Select the 'CustomMap' collection and switch the Properties Inspector to show Collections. Here you will see a tab for configuring the settings of the Custom Map. Here you can change the Map Name, Description, Image, Splits and Modes. The Map will need a name, and the earlier mentioned required objects.

.. seealso::

   The :doc:`Custom Map settings <custom_map_settings>` page for more information on the available settings here.

Once the map has all the minimum requirements you can :doc:`build <building>` it from the Collection Inspector using the "Build Custom Map" button, or use F5 as a shortcut.

Inside Pogostuck you can now go to your local Custom Maps and there should be a map with the name you chose! Edit your map in Blender, build it and hit F1 in Pogostuck and your changes will apply.

.. tip::

   You can fly in local Custom Maps by pressing and holding T.

Add a cube under the Spawn Position and mark it as an Entity, using the Property Inspector. Turn on the collision flag, and build the Map again. You should now have a platform that the player can stand on.

If you want to quickly add more platforms to outline your map, you can use ``Add -> PogoBlend -> Block`` to create a Block, which is just a flat plane that is an Entity with auto-collision turned on, that you can easily edit in edit mode.

You can now continue making the your own Map by adding Entities, Regions and Paths.

I **highly** recommend that you read the other guides mentioned here on this page, and in the documentation.

Otherwise, enjoy making maps!

.. toctree::
  :hidden:

  wed_differences
