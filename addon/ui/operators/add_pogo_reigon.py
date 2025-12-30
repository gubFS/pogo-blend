import bpy


class AddPogoReigon(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_reigon"
    bl_label = "Reigon"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.object.empty_add(type="CUBE")
        empty = context.object

        empty.name = "PogoReigon"
        empty.scale.y = 0
        for i in range(3):
            empty.lock_rotation[i] = True
        empty.pogo_reigon

        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(AddPogoReigon.bl_idname, text="Add Pogo Reigon")


def register():
    bpy.utils.register_class(AddPogoReigon)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddPogoReigon)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)
