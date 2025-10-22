import bpy

class PogostuckPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Pogostuck"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj.type != 'MESH': return

        for property in [attr for attr in dir(obj.wmb_entity) if not attr.startswith("__") and not attr in ["bl_rna", "name", "rna_type"]]:
            row = layout.row()
            row.prop(obj.wmb_entity, property)
