# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from pathlib import Path
from string import ascii_uppercase

import bpy

from . import pogo_blend_utils as pbu


class SelectCustomMapsDir(bpy.types.Operator):
    bl_idname = "pogo_blend.select_custom_maps_dir"
    bl_label = "Select the Custom Maps folder"
    bl_options = {'REGISTER'}

    directory: bpy.props.StringProperty(
        name="Custom Maps folder",
        description="New maps will be created in the selected folder",
        subtype='DIR_PATH',
    )

    # Filters folders
    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})

    def execute(self, context):
        get_preferences().custom_maps_path = self.directory
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class PogoBlendPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    mdl_importer: bpy.props.BoolProperty(
        default=False,
        name="MDL Importer",
        description="Add the MDL-impoterter to importers",
    )

    mdl_exporter: bpy.props.BoolProperty(
        default=False,
        name="MDL Exporter",
        description="Add the MDL-exporter to exporters",
    )

    custom_maps_path: bpy.props.StringProperty(
        default="",
        name="Custom Maps folder",
        description="The path to the folder where custom maps will be put",
    )

    map_scale: bpy.props.FloatProperty(
        default=50.0,
        name="Map Scale",
        description="The default map scale. 50 means the default Cube is roughly half the size of the Pogo Dude",
    )

    show_overrides: bpy.props.BoolProperty(
        default=False,
        name="Enable Overrides",
        description="Adds a panel to entities that shows all editiable fields. Not relevant in most normal use cases",
    )

    build_on_save: bpy.props.BoolProperty(
        default=False,
        name="Build on save",
        description="Builds the Custom Map whenever the Blender file is saved. Reload Blender to apply",
    )

    debug_mode: bpy.props.BoolProperty(
        default=False,
        name="Debug Mode",
        description="Enables more verbose outputs and options, allowing for easier debugging and development. Not relevant for casual use cases",
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "custom_maps_path")
        row.operator("pogo_blend.select_custom_maps_dir", text="", icon='FILE_FOLDER')

        row = layout.row()
        row.prop(self, "build_on_save")
        row.prop(self, "map_scale")

        row = layout.row()
        row.prop(self, "mdl_importer")
        row.prop(self, "mdl_exporter")

        row = layout.row()
        row.prop(self, "show_overrides")
        row.prop(self, "debug_mode")
        if bpy.ops.pogo_blend.make_asset_library.poll():
            layout.operator("pogo_blend.make_asset_library", text=f"{'Reg' if pbu.get_generated_library_path().exists() else 'G'}enerate Pogostuck Asset Library")


def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences


def _get_custom_maps_path() -> str:
    roots = []
    places_to_search = []
    match os.name:
        case 'posix':
            roots.extend(["/"])
            roots.extend(str(path) for path in Path("/").glob("home/*/Drives/*"))
            roots.extend(str(path) for path in Path("/").glob("home/*/Storage/*"))
            roots.extend(str(path) for path in Path("/").glob("mnt/*"))
            places_to_search.extend(["home/*/.local/share/Steam", "home/*/Library/Application Support/Steam"])
        case 'nt':
            roots.extend(f"{letter}:\\" for letter in ascii_uppercase if Path(f"{letter}:\\").exists())
            places_to_search.extend(["Program Files (x86)/Steam"])
    places_to_search.extend(["Steam", "Games", "SteamLibrary"])

    cmp = ""
    for root in roots:
        for path in places_to_search:
            path = Path(root).joinpath(path)
            if not path.exists():
                continue
            cmp = str(next(path.rglob("steamapps/common/Pogostuck/CustomMaps"), ""))
            if cmp != "":
                break
    return cmp


classes = (
    SelectCustomMapsDir,
    PogoBlendPreferences,
)


def register():
    cmp = get_preferences().custom_maps_path
    if cmp is None or cmp == "":
        try:
            get_preferences().custom_maps_path = _get_custom_maps_path()
        except Exception as e:
            print(f"WARNING: Exception while searching for Custom Maps path: {e}")
