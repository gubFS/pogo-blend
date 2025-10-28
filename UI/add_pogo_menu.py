import bpy

class AddPogoMenu(bpy.types.Menu):
    bl_label = "Pogo Blend"
    bl_idname = "OBJECT_MT_pogo_blend_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("pogo_blend.add_pogo_reigon", icon='CUBE')


def draw_item(self, context):
    layout = self.layout
    layout.menu(AddPogoMenu.bl_idname)


def register():
    bpy.utils.register_class(AddPogoMenu)

    # lets add ourselves to the main header
    bpy.types.VIEW3D_MT_add.append(draw_item)


def unregister():
    bpy.utils.unregister_class(AddPogoMenu)

    bpy.types.VIEW3D_MT_add.remove(draw_item)
