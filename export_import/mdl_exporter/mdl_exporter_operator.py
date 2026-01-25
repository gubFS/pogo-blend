# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
import bpy_extras

from ... import pogo_blend_utils as pbu
from .mdl_exporter import MDLExporter


def export_to_mdl(context, filepath, only_selected, scale):
    objects = context.scene.collection.all_objects
    if only_selected:
        objects = context.selected_objects

    objs = []
    for obj in objects:
        if obj.type == 'MESH':
            objs.append(obj)

    print(f"Exporting {len(objs)} objects to mdl")
    MDLExporter(filepath, objs, scale).export()


class MDLExporterOperator(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "pogo_blend.export_mdl"
    bl_label = "Export meshes to MDL (Gamestudio A8)"
    bl_description = "Exports meshes to MDL files."

    filename_ext = ".mdl"

    filter_glob: bpy.props.StringProperty(
        default="*.mdl",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    selected_only: bpy.props.BoolProperty(
        name="Export selected only",
        default=True,
    )

    global_scale: bpy.props.FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0,
        max=1000.0,
        default=50.0,
    )

    @classmethod
    def poll(cls, context):
        return pbu.get_preferences().mdl_exporter

    def execute(self, context):
        try:
            export_to_mdl(context, self.filepath, self.selected_only, self.global_scale)
        except Exception as e:
            self.report({'ERROR'}, str(e))
            return {'CANCELLED'}
        else:
            return {'FINISHED'}


def menu_func_export(self, context):
    if MDLExporterOperator.poll(context):
        self.layout.operator(MDLExporterOperator.bl_idname, text="MDL (.mdl)")


classes = (MDLExporterOperator,)


def register():
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
