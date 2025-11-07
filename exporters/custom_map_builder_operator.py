import math
import os
import time

import bpy

# ExportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper

from .. import pogo_blend_utils as pbu
from .custom_map_builder import build_custom_map


class CustomMapBuilderFile(bpy.types.Operator, ExportHelper):
    bl_idname = "pogo_blend.build_custom_map_file"
    bl_label = "Export Project to a Pogostuck Map"
    bl_description = "Exports this project to a Pogostuck Custom Map"

    filename_ext = ".wmb"

    filter_glob: bpy.props.StringProperty(
        default="*.wmb",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    global_scale: bpy.props.FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0,
        max=1000.0,
    )

    def execute(self, context):
        return bpy.ops.pogo_blend.build_custom_map(
            filepath=self.filepath, global_scale=self.global_scale
        )

    def invoke(self, context, event):
        self.global_scale = pbu.get_preferences().map_scale
        return ExportHelper.invoke(self, context, event)


class CustomMapBuilder(bpy.types.Operator):
    bl_idname = "pogo_blend.build_custom_map"
    bl_label = "Export Project to a Pogostuck Map"
    bl_description = "Exports this project to a Pogostuck Custom Map"

    filepath: bpy.props.StringProperty(name="File path")

    global_scale: bpy.props.FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0,
        max=1000.0,
    )

    def execute(self, context):
        start_time = time.time()
        try:
            build_custom_map(context, self.filepath, self.global_scale)
        except BaseException as e:
            error_type = {"ERROR"}
            if isinstance(type, pbu.ContextError):
                error_type = {"ERROR_INVALID_CONTEXT"}
            self.report(error_type, str(e))
            raise e  # NOTE: For debugging purposes, should not be here
            return {"CANCELLED"}
        else:
            self.report(
                {"INFO"},
                f"Custom Map built in {math.floor((time.time() - start_time) * 1000)}ms",
            )
            return {"FINISHED"}

    def invoke(self, context, event):
        self.filepath = pbu.get_preferences().custom_maps_path
        if self.filepath == "":
            self.report(
                {"INFO"},
                "The Custom Maps directory is not defined. Select it and try again. It can be accessed manually in the preferences for the Pogo Blend addon",
            )
            bpy.ops.pogo_blend.select_custom_maps_dir("INVOKE_DEFAULT")
            return {"CANCELLED"}
        if not os.path.exists(self.filepath):
            self.report(
                "ERROR",
                "The Custom Maps directory does not exist. Select a valid directory in the preferences for the Pogo Blend addon",
            )
            return {"CANCELLED"}
        self.filepath = os.path.join(
            self.filepath, bpy.data.collections["CustomMap"].custom_map.map_name
        )
        if not os.path.exists(self.filepath):
            os.mkdir(self.filepath)
        self.filepath = os.path.join(self.filepath, "customMap.wmb")
        self.global_scale = pbu.get_preferences().map_scale
        return self.execute(context)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(CustomMapBuilderFile.bl_idname, text="Pogostuck Custom Map")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(CustomMapBuilder)
    bpy.utils.register_class(CustomMapBuilderFile)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(CustomMapBuilder)
    bpy.utils.unregister_class(CustomMapBuilderFile)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
