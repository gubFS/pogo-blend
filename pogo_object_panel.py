import bpy

def register():
    bpy.utils.register_class(PogoObjectPanel)

def unregister():
    bpy.utils.unregister_class(PogoObjectPanel)

class PogoObjectPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Pogo Blend"
    bl_idname = "OBJECT_PT_pogo_blend"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj.type != 'MESH': return

        layout.row().prop(obj, "name")
        layout.row().prop(obj, "location")
        layout.row().prop(obj, "rotation_euler", text="Rotation")
        layout.row().prop(obj, "scale")
        layout.row().prop(obj.pogo_entity, "material")

        row = layout.row()
        row.prop(obj.pogo_entity, "ambient")
        row.prop(obj.pogo_entity, "albedo")

        row = layout.row()
        col = row.column()
        col.prop(obj.pogo_entity, "flag_invisible")
        col.prop(obj.pogo_entity, "flag_unlit")
        col.prop(obj.pogo_entity, "flag_transparent")
        col.prop(obj.pogo_entity, "flag_polygon")
        if obj.pogo_entity.flag_polygon == True:
            col.prop(obj.pogo_entity, "flag_auto_collision")

        col = row.column()
        col.prop(obj.pogo_entity, "flag_shadow")
        col.prop(obj.pogo_entity, "flag_cast")
        col.prop(obj.pogo_entity, "flag_metal")
        col.prop(obj.pogo_entity, "flag_7")

        layout.row().prop(obj.pogo_entity, "action")

        # for property in [attr for attr in dir(obj.pogo_entity) if not attr.startswith("__") and not attr in ["bl_rna", "name", "rna_type"]]:
        #     row = layout.row()
        #     row.prop(obj.pogo_entity, property)
