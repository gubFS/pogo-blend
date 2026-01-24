import os
from pathlib import Path

import bpy

from . import pogo_blend_preferences as pbu
from .export_import import custom_map_builder_operator
from .export_import.mdl_exporter import mdl_exporter_operator
from .export_import.mdl_importer import mdl_importer
from .pogo_blend_asset_library import generate_pogo_assets
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
    presets,
)

# Uncomment the following for quick reloading of addon. Only for use in development.
# import importlib
# for root, dirs, files in os.walk(Path(__file__).parent):
#     root.replace("\\", "/")  # Windows >:(
#     if "__pycache__" in root or ".git" in root:
#         continue
#     for file in files:
#         filename = Path(file).stem
#         if Path(file).suffix != ".py":
#             continue
#         if file == "__init__.py":
#             continue
#         if filename in locals():
#             importlib.reload(locals()[filename])
#         else:
#             rel = root.split("/pogo_blend")[1].replace("/", ".")
#             rel = f"{rel}.{filename}"
#             locals()[filename] = importlib.import_module(rel, package=__name__)

modules = [
    pbu,
    custom_map_builder_operator,
    mdl_exporter_operator,
    mdl_importer,
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
    presets,
    generate_pogo_assets,
]


def install_app_template():
    bpy.ops.preferences.app_template_install(filepath=str(Path(__file__).parent.joinpath("app_template.zip")))


def register():
    for module in modules:
        for cls in module.classes:
            bpy.utils.register_class(cls)
        if hasattr(module, "register"):
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

    bpy.app.timers.register(install_app_template, first_interval=0.01)


def unregister():
    # delete any remaining real-time custom material files
    if pbu.get_preferences().custom_maps_path != "":
        for i in range(1, 6):
            path = Path(pbu.get_preferences().custom_maps_path).parent.joinpath(f"customMaterial{i}.fx")
            if path.exists():
                os.remove(path)

    asset_libraries = bpy.context.preferences.filepaths.asset_libraries
    lib_id = asset_libraries.find("PogoBlend")
    if lib_id != -1:
        asset_libraries.remove(asset_libraries[lib_id])

    for module in reversed(modules):
        if hasattr(module, "unregister"):
            module.unregister()
        for cls in reversed(module.classes):
            bpy.utils.unregister_class(cls)
