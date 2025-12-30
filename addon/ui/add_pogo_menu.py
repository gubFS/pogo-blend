import bpy


class AddPogoMenu(bpy.types.Menu):
    bl_label = "Pogo Blend"
    bl_idname = "OBJECT_MT_pogo_blend_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("pogo_blend.add_block", text="Block", icon="CUBE")
        layout.operator("pogo_blend.add_sprite", text="Sprite", icon="IMAGE_DATA")
        layout.operator("pogo_blend.add_pogo_reigon", text="Reigon", icon="MESH_PLANE")
        layout.operator("pogo_blend.add_pogo_path", text="Path", icon="CON_FOLLOWPATH")


def draw_item(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(AddPogoMenu.bl_idname)


def register():
    bpy.utils.register_class(AddPogoMenu)
    bpy.types.VIEW3D_MT_add.append(draw_item)


def unregister():
    bpy.utils.unregister_class(AddPogoMenu)
    bpy.types.VIEW3D_MT_add.remove(draw_item)
