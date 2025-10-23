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

        entity = obj.pogo_entity

        layout.row().prop(obj, "name")
        layout.row().prop(obj, "location")
        layout.row().prop(obj, "rotation_euler", text="Rotation")
        layout.row().prop(obj, "scale")
        layout.row().prop(entity, "material")

        row = layout.row()
        row.prop(entity, "ambient")
        row.prop(entity, "albedo")

        row = layout.row()
        col = row.column()
        col.prop(entity, "flag_invisible")
        col.prop(entity, "flag_unlit")
        col.prop(entity, "flag_transparent")
        col.prop(entity, "flag_polygon")
        if entity.flag_polygon == True:
            col.prop(entity, "flag_auto_collision")

        col = row.column()
        col.prop(entity, "flag_shadow")
        col.prop(entity, "flag_cast")
        col.prop(entity, "flag_metal")
        col.prop(entity, "flag_7")

        layout.row().prop(entity, "action")
        if entity.action in entity.actions:
            currentConfig = entity.actions.get(entity.action)

            if "flags" in currentConfig:
                row = layout.row()
                colLeft = row.column()
                colRight = row.column()
                for i, flag in enumerate(currentConfig["flags"]):
                    col = colLeft if i % 2 == 0 else colRight
                    # entity[flag["identifier"]] = flag["default"] # TODO: change value to default when action is changed (not on every draw)
                    col.prop(entity, flag["identifier"], text=flag["name"])

            if "skills" in currentConfig:
                for i, skill in enumerate(currentConfig["skills"]):
                    layout.row().prop(entity, skill["identifier"], text=skill["name"])

            if "path" in currentConfig and currentConfig["path"] == True:
                layout.row().prop(entity, "path")
