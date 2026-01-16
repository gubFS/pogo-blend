from pathlib import Path

import bpy

from . import make_asset_library
from . import pogo_blend_preferences as pbu
from .export_import import custom_map_builder_operator
from .export_import.mdl_exporter import mdl_exporter_operator
from .export_import.mdl_importer import mdl_importer_operator
from .pogo_classes import pogo_custom_map, pogo_entity, pogo_path, pogo_region
from .ui import (
    add_pogo_menu,
    object_pogo_menu,
    pogo_collection_panel,
    pogo_object_panel,
)
from .ui.gizmos import gravity_gizmo
from .ui.operators import (
    add_block,
    add_pogo_path,
    add_pogo_region,
    add_sprite,
    create_collider,
    modifiers,
)

# Uncomment the following for quick reloading of addon. Only for use in development.
# import importlib
# import os
# for root, dirs, files in os.walk(os.path.dirname(__file__)):
#     root.replace("\\", "/")  # Windows >:(
#     if "__pycache__" in root or ".git" in root:
#         continue
#     for file in files:
#         filename, file_extension = os.path.splitext(file)
#         if file_extension != ".py":
#             continue
#         if file == "__init__.py":
#             continue
#         if filename in locals():
#             importlib.reload(locals()[filename])
#         else:
#             rel = root.split("/pogo_blend")[1].replace("/", ".")
#             rel = f"{rel}.{filename}"
#             locals()[filename] = importlib.import_module(rel, package=__name__)

to_register = [
    pbu,
    custom_map_builder_operator,
    mdl_exporter_operator,
    mdl_importer_operator,
    pogo_custom_map,
    pogo_entity,
    pogo_path,
    pogo_region,
    add_pogo_menu,
    object_pogo_menu,
    pogo_collection_panel,
    pogo_object_panel,
    gravity_gizmo,
    add_block,
    add_pogo_path,
    add_pogo_region,
    add_sprite,
    create_collider,
    modifiers,
    make_asset_library,
]


def register():
    for module in to_register:
        module.register()

    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    lib_id = asset_libraries.find("PogoBlend")
    if lib_id == -1:
        al = asset_libraries.new(
            name="PogoBlend",
            directory=str(Path(__file__).parent.joinpath("pogo_blend_asset_library")),
        )
        al.import_method = 'APPEND_REUSE'
        al.use_relative_path = True


def unregister():
    for module in to_register:
        module.unregister()

    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    lib_id = asset_libraries.find("PogoBlend")
    if lib_id != -1:
        asset_libraries.remove(asset_libraries[lib_id])
