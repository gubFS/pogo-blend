# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import math
import os
import time
from pathlib import Path

import bpy
from bpy.app.handlers import persistent

from .. import pogo_blend_utils as pbu
from .custom_map_builder import build_custom_map


class CustomMapBuilder(bpy.types.Operator):
    bl_idname = "pogo_blend.build_custom_map"
    bl_label = "Export Project to a Pogostuck Map"
    bl_description = "Exports this project to a Pogostuck Custom Map"
    bl_options = {'BLOCKING'}

    filepath: bpy.props.StringProperty(name="File path")

    global_scale: bpy.props.FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0,
        max=1000.0,
    )

    def execute(self, context):
        context.window.cursor_set('WAIT')
        start_time = time.time()
        try:
            with pbu.BlenderModeContext():
                build_custom_map(context, self.filepath, self.global_scale, self)
            self.report(
                {'INFO'},
                f"Custom Map built in {math.floor((time.time() - start_time) * 1000)}ms",
            )
        except Exception as e:
            error_type = {'ERROR'}
            if isinstance(type, pbu.ContextError):
                error_type = {'ERROR_INVALID_CONTEXT'}
            self.report(error_type, str(e))
        context.window.cursor_set('DEFAULT')
        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            pbu.get_custom_map_collection()
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}

        self.filepath = pbu.get_preferences().custom_maps_path
        if self.filepath == "":
            self.report(
                {'ERROR'},
                "The Custom Maps folder is not defined. Select it and try again. It can be accessed manually in the preferences for the PogoBlend addon",
            )
            bpy.ops.pogo_blend.select_custom_maps_dir("INVOKE_DEFAULT")
            return {'CANCELLED'}
        if not Path(self.filepath).exists():
            self.report(
                {'ERROR'},
                "The Custom Maps folder does not exist. Select a valid folder in the preferences for the PogoBlend addon",
            )
            return {'CANCELLED'}
        if pbu.get_custom_map().map_name == "":
            self.report({'ERROR'}, "The map name cannot be empty")
            return {'CANCELLED'}

        self.filepath = str(Path(self.filepath, pbu.get_custom_map().map_name))
        if not Path(self.filepath).exists():
            os.mkdir(self.filepath)
            with open(Path(self.filepath, ".pogo_blend"), "w"):
                pass
        elif ".pogo_blend" not in os.listdir(self.filepath):
            self.report(
                {'ERROR'},
                f"The '{pbu.get_custom_map().map_name}' folder is not a PogoBlend folder. PogoBlend will delete files in the folder so either enter a new map name, safely delete the existing folder, or add a file named '.pogo_blend' in the folder.",
            )
            return {'CANCELLED'}
        self.filepath = str(Path(self.filepath, "customMap.wmb"))
        self.global_scale = pbu.get_preferences().map_scale
        return self.execute(context)


keymaps = []


@persistent
def post_save(file: str):
    try:
        bpy.ops.pogo_blend.build_custom_map('INVOKE_DEFAULT')
    except Exception:
        pass


def menu_func(self, context):
    self.layout.operator(CustomMapBuilder.bl_idname, text="Build Pogostuck Custom Map")


classes = (CustomMapBuilder,)


def register():
    bpy.types.TOPBAR_MT_file_export.append(menu_func)

    if pbu.get_preferences().build_on_save:
        bpy.app.handlers.save_post.append(post_save)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Window', space_type='EMPTY')
        kmi = km.keymap_items.new(CustomMapBuilder.bl_idname, 'F5', 'PRESS')
        keymaps.append((km, kmi))


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)

    if post_save in bpy.app.handlers.save_post:
        bpy.app.handlers.save_post.remove(post_save)

    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()
