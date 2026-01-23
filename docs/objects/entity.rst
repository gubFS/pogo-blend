Entities
========

Entities include:

- Models
- Sprites
- Blocks

All entities are just meshes. Models are regular meshes as you know them. Sprites are just a flat plane with a texture on it, and blocks are also flat planes with some pre defined settings.

.. seealso::

   :doc:`Modeling </modeling>` page for more information on how to make the meshes that entities use.

Entities have materials, actions, and flags.

Materials
---------

The material on an entity determines how it will look in-game. It currently has not effect on how it is displayed inside Blender. Some materials allows changing the brightness, and some other value (greyscale, transparency).

Below is an in-game image of the available materials, aswell as a list of their names and descriptions which is also available in the add-on by hovering your mouse over each material.

.. figure:: materials.png
   :align: center

   *In-game image of the available materials with a gradient texture applied. Note: the 'Sap', 'Pink Sap' and 'Boost Juice' materials have a bubbles texture instead. Also, the 'Normal Mapping' material is using a second texture, a normal map, and it will look different depedning on the normal map you are using.*

.. datatemplate:yaml:: ../../addon/pogo_classes/materials.yaml
    :template: ../objects/materials.tmpl

Actions
-------

Actions change the behavior of the entity. Some actions might have additional options that allow you to change the specifics of how the action should behave. An options is either a flag, an on or off option, or a 'skill' which is just a decimal number.

An entity can have a maximum of two actions. If you are using two actions please note that some of the options might overlap and that using two actions might give inconsistent behavior.

Below is a list of the avaiable actions. The descriptions for the actions will be available in the add-on, but unfortunately the descriptions for the options are not currently.

.. warning::

   Some flags in the action options might overlap with the 'Bonk' and 'Ice' flags.

.. datatemplate:yaml:: ../../addon/pogo_classes/actions.yaml
    :template: ../objects/actions.tmpl

.. _flags:

Flags
-----

Flags are on or off values, and change certain things about the entity.

**Invisible** makes the entity invisible.

**Shadow** gives a glow shadow around the entity. It does this by just adding a blurry version of it in the background, so this doesn't work if the background is blocked or the background flag is on.

**Background** places the entity in the background and blurs it.

**Collision** makes the entity collideable. See :ref:`collisions`.

The following flags only has an effect if the entity is collideable:

**Auto Collision** generates a collision that matches the entities sideview. See :ref:`collisions`.

**Kill** kills the player on contact with the entity.

**Ice** makes the player glide on the entity like ice.

**Bonk** makes the player bonk on contact with the entity, even if it's the pogostuck that makes contact.

.. _collisions:

Collisions
----------

You can enable collision on any entity. When collisions is enabled the player will collide with the entity. The collision happens where the Y-position is equal to 0, so make sure that you position collideable entities on the XZ-plane.

In case you just want the player to collide with an entity as it appears on it's sideview you can enable **Auto Collision** which will auto-generate a collider for the entity and place it correctly. If you want to preview or modify this collision you can generate the collision yourself by selecting the entity that you want to create a collider for and under the 'Object' panel you can select ``PogoBlend -> Create a Pogostuck Collider``.

.. note::

   Automatic colliders are not guarenteed correct so if your collisions are acting funky, try generating the collider manually and inspect it to look for any problems.

.. warning::

   Sometimes when colliding with a rotated entity, the player might fall straight through them. If this is the case, just rotate the mesh and not the entity, or use Auto Collision as that won't have any rotation on it.

.. _overrides:

Overrides
---------

The auto-generated assets from Pogostuck will have some overrides applied to them. Overrides just tells the add-on to build the entity in a certain way. For these assets it is the filename that is overriden, and that means that the mesh will not be exported to a model and the entity will instead use the file with the name given by the override. The same goes for just about any field on an entity, like materials. For normal usecases you won't have to set these overrides manually, but it's good to know what they are. You can enable viewing all overrides in the :doc:`preferences </preferences>`. If a field is overridden it will be shown no matter the option in your preferences.
