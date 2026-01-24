import bpy


class ModifiersMenu(bpy.types.Menu):
    bl_label = "Modifiers"
    bl_idname = "OBJECT_MT_pogo_blend_modifiers_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("pogo_blend.add_pogo_edge_split")
        layout.operator("pogo_blend.add_pogo_bevel")
        layout.operator("pogo_blend.add_pogo_bevel_edge_split")


class PresetsMenu(bpy.types.Menu):
    bl_label = "Presets"
    bl_idname = "OBJECT_MT_pogo_blend_presets_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("pogo_blend.apply_ice_preset")
        layout.operator("pogo_blend.apply_sap_preset")
        layout.operator("pogo_blend.apply_pink_sap_preset")
        layout.operator("pogo_blend.apply_boost_juice_preset")
        layout.operator("pogo_blend.apply_background_preset")


class ObjectPogoMenu(bpy.types.Menu):
    bl_label = "PogoBlend"
    bl_idname = "OBJECT_MT_pogo_blend_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("pogo_blend.create_collider", text="Create a Pogostuck Collider")
        layout.menu(ModifiersMenu.bl_idname)
        layout.menu(PresetsMenu.bl_idname)


def draw_item(self, context):
    layout = self.layout
    layout.separator()
    layout.menu(ObjectPogoMenu.bl_idname)


def register():
    bpy.utils.register_class(ObjectPogoMenu)
    bpy.utils.register_class(ModifiersMenu)
    bpy.utils.register_class(PresetsMenu)
    bpy.types.VIEW3D_MT_object.append(draw_item)


def unregister():
    bpy.utils.unregister_class(ObjectPogoMenu)
    bpy.utils.unregister_class(ModifiersMenu)
    bpy.utils.unregister_class(PresetsMenu)
    bpy.types.VIEW3D_MT_object.remove(draw_item)
