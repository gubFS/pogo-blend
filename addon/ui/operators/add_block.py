import bpy


class AddBlock(bpy.types.Operator):
    bl_idname = "pogo_blend.add_block"
    bl_label = 'Add Pogo Block'
    bl_description = "Adds a square with settings for making quick geometry"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add()
        block = context.object

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True)
        bpy.ops.object.editmode_toggle()

        block.name = "PogoBlock"
        entity = block.pogo_entity
        entity.material = "cmUnlit"
        entity.flag_polygon = True
        entity.flag_auto_collision = True

        return {'FINISHED'}


def register():
    bpy.utils.register_class(AddBlock)


def unregister():
    bpy.utils.unregister_class(AddBlock)
