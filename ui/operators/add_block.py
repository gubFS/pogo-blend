import bpy


class AddBlock(bpy.types.Operator):
    bl_idname = "pogo_blend.add_block"
    bl_label = "Block"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add()
        block = context.object

        block.name = "PogoBlock"
        block.rotation_euler[0] = 1.570796
        entity = block.pogo_entity
        entity.flag_unlit = True
        entity.flag_polygon = True
        entity.flag_auto_collision = True

        return {"FINISHED"}


def register():
    bpy.utils.register_class(AddBlock)


def unregister():
    bpy.utils.unregister_class(AddBlock)
