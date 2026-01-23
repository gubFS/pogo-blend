"Building" Custom Maps
======================

Whenever the Blender file needs to be converted to a Pogostuck Custom Map it will be "built". Building the Map includes writing all the objects to a shared WMB-file, exporting model files, generating collisions, and moving/converting image files. 

Only objects in a collection called 'CustomMap' will be built.

Models and colliders can take some time to export, however after the first time they are exported, they will be saved and only re-exported when neccessary. 

.. tip::

  If you are experiencing slowdowns because of very large meshes, you could manualy generate the collision and .mdl files, and then use the filename :ref:`override <overrides>`. But hopefully this shouldn't be necessary.

The builder will only build into folders if there is a file named '.pogo_blend' present in the folder for the map. When the map is made for the first time, this file will automatically be created. This is in order to not accidentally delete or overwrite any unintenional files.

.. warning::

  When building a map, some files that are not used in the map but are in the map folder will automatically be delted. Currently any ``.mdl .tga .png`` files will be deleted. These files are usually auto-generated. Do **NOT** store project files in the map folder. If you do want to store a file in the map folder, any files that start with an underscore, will not be deleted.
