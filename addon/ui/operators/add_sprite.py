import bpy


class AddSprite(bpy.types.IMAGE_OT_import_as_mesh_planes):
    bl_idname = "pogo_blend.add_sprite"
    bl_label = "Sprite"

    def execute(self, context):
        ret_code = super().execute(context)

        if ret_code == {"FINISHED"}:
            sprite = context.object
            sprite.name = "PogoSprite"
            sprite.rotation_euler[0] = 1.570796

            entity = sprite.pogo_entity
            entity.flag_unlit = True

        return ret_code


def menu_func(self, context):
    self.layout.operator(AddSprite.bl_idname, text="Add Pogo Sprite")


def register():
    bpy.utils.register_class(AddSprite)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(AddSprite)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)
