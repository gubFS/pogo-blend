# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

from .. import pogo_blend_utils as pbu


class CustomMaterialTemplatesMenu(bpy.types.Menu):
    bl_label = "PogoBlend Custom Materials"
    bl_idname = "CUSTOM_MATERIALS_MT_pogo_blend_menu"

    def add_custom_material(self, layout, custom_material: pbu.CustomMaterial):
        if custom_material.filepath is None:
            return
        opts = layout.operator("text.open", text=custom_material.name)
        opts.filepath = str(custom_material.filepath.resolve().absolute())
        opts.internal = True

    def draw(self, context):
        layout = self.layout

        custom_material_templates = pbu.get_custom_material_templates()

        for custom_material in custom_material_templates:
            self.add_custom_material(layout, custom_material)


def draw_item(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(CustomMaterialTemplatesMenu.bl_idname)


classes = (CustomMaterialTemplatesMenu,)


def register():
    bpy.types.TEXT_MT_templates.append(draw_item)


def unregister():
    bpy.types.TEXT_MT_templates.remove(draw_item)
