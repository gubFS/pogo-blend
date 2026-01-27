# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

# PogoBlend Blender Add-on
# Copyright (C) 2026 gubFS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

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


def manual_map():
    map = (
        # entity
        ("bpy.types.pogoentity.material", "/objects/entity.html#materials"),
        ("bpy.types.pogoentity.action*", "/objects/entity.html#actions"),
        ("bpy.types.pogoentity.skill*", "/objects/entity.html#actions"),
        ("bpy.types.pogoentity.flag*", "/objects/entity.html#flags"),
        ("bpy.types.pogoentity.*_override", "/objects/entity.html#overrides"),
        ("bpy.types.pogoentity.*", "/objects/entity.html"),
        ("bpy.ops.pogo_blend.*pogo_entity*", "/objects/entity.html"),
        # region
        ("bpy.types.pogoregion.*", "/objects/region.html"),
        ("bpy.ops.pogo_blend.*pogo_region*", "/objects/region.html"),
        # path
        ("bpy.types.pogopath.*", "/objects/entity.html"),
        ("bpy.ops.pogo_blend.*pogo_path*", "/objects/path.html"),
        # custom map
        ("bpy.ops.pogo_blend.build_custom_map", "/building.html"),
        ("bpy.types.pogocustommap.*", "/custom_map_settings.html"),
        ("bpy.ops.pogo_blend.*custom_map*", "/custom_map_settings.html"),
        # object tools
        ("bpy.ops.pogo_blend.create_collider", "/objects/object_tools.html"),
        ("bpy.ops.pogo_blend.add*", "/objects/object_tools.html#modifiers"),
        ("bpy.ops.pogo_blend.apply*", "/objects/object_tools.html#presets"),
        # catch all
        ("bpy.ops.pogo_blend.*", "/"),
    )

    return "https://gubfs.github.io/pogo-blend", map


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

    bpy.utils.register_manual_map(manual_map)


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

    bpy.utils.unregister_manual_map(manual_map)
