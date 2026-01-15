import bpy


class AddPogoRegion(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_region"
    bl_label = "Add Pogo Region"
    bl_description = "Adds a Pogo Region"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.empty_add(type='CUBE')
        empty = context.object

        empty.name = "PogoRegion"
        empty.scale.y = 0
        for i in range(3):
            empty.lock_rotation[i] = True
        empty.pogo_region

        return {'FINISHED'}


def register():
    bpy.utils.register_class(AddPogoRegion)


def unregister():
    bpy.utils.unregister_class(AddPogoRegion)
