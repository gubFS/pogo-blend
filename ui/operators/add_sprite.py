# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy


class AddSprite(bpy.types.IMAGE_OT_import_as_mesh_planes):
    bl_idname = "pogo_blend.add_sprite"
    bl_label = "Add Pogo Sprite"
    bl_description = "Opens a file explorer to select an image. Then creates a plane and applies the image as a texture"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ret_code = super().execute(context)

        if ret_code == {'FINISHED'}:
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True)
            bpy.ops.object.editmode_toggle()
            for obj in context.selected_objects:
                entity = obj.pogo_entity
                entity.material = "cmUnlit"

        return ret_code


classes = (AddSprite,)
