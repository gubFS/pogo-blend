Differences from WED
====================

If you've made Custom Maps before using WED, here is a list of things that might be noteably different when using PogoBlend. Otherwise ignore this page as it might not make a lot of sense.

- Your models are automatically converted to .mdl files.
- Your images are automatically converted to .tga files.
- Names that had to be exact no longer have to, such as startLine, spawn1 or modeSetup.
- You don't have to make an entity for picking the mode of the map. You can set this in the :doc:`Custom Map Settings <custom_map_settings>`.
- You don't have to make and name your own file for splits and description. You can edit these in the :doc:`Custom Map Settings <custom_map_settings>`.
- The map preview image will be automatically converted to a PNG-file and named correctly.
- You don't have to worry about the exact Y-position or naming of your regions, you can just pick a type.
- Flags, materials and actions go by different namings, and some of the unused ones are hidden entirely. Such as:

  - The albedo value, has changed name to 'Brightness', and will only be shown on materials that support it.
  - The ambient value, will only be shown on materials that support it, and will change name depending on what it does. This is either Greyscale or Transparency. It has a default value of 100 now.
  - Unlit, which will be on unless you are using no material.
  - Polygon is now called 'Collision'.
  - Passable is hidden and will be on unless collision is on.
  - Transparent will always be on, but everything has a default transparency of 100%.
  - Metal is now called 'Kill'.
  - Flag 7 is now called 'Bonk'.
  - Flag 8 is now called 'Ice'.
  - The way you would normally make background objects with the shadow and cast flags, are now just one flag, 'Background'. There is still a 'Shadow' flag though that can be used to create a glow shadow. See :ref:`flags`.
  - All the actions and materials have more saying names, i'm not going to list them here, but hopefully you should be able to make the connection.
- You can easily pick two actions, instead of having to use execString12acts. Also actions only show relevant flags and skills. These flags and skills also have more saying names.

There might be some other differences, but these should be the major ones. If I missed something big, let me know and I'll add it.
