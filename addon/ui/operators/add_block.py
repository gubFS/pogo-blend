import bpy


class AddBlock(bpy.types.Operator):
    bl_idname = "pogo_blend.add_block"
    bl_label = "Block"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add()
        block = context.object

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X')
        bpy.ops.object.editmode_toggle()

        block.name = "PogoBlock"
        entity = block.pogo_entity
        entity.flag_unlit = True
        entity.flag_polygon = True
        entity.flag_auto_collision = True

        return {"FINISHED"}


def register():
    bpy.utils.register_class(AddBlock)


def unregister():
    bpy.utils.unregister_class(AddBlock)
