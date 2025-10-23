import bpy
from .wmb_classes import PogoEntity

def register():
    bpy.utils.register_class(AddPogoEntityData)
    bpy.utils.register_class(PogoObjectPanel)

def unregister():
    bpy.utils.unregister_class(AddPogoEntityData)
    bpy.utils.unregister_class(PogoObjectPanel)

class AddPogoEntityData(bpy.types.Operator):
    bl_idname = "object.add_pogo_entity_data"
    bl_label = "Add pogo data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object.pogo_entity
        return {'FINISHED'}

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

        match obj.type:
            case 'MESH':
                self.draw_mesh_panel(obj, layout)
            case _:
                layout.label(text="This object type has no relevant pogo data")
                return

    def draw_mesh_panel(self, obj, layout):
        try: obj["pogo_entity"]
        except KeyError:
            layout.operator("object.add_pogo_entity_data")
            return

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

            if "flags" in currentConfig and len(currentConfig.get("flags")) != 0:
                row = layout.row()
                colLeft = row.column()
                colRight = row.column()
                for i, flag in enumerate(currentConfig["flags"]):
                    col = colLeft if i % 2 == 0 else colRight
                    # entity[flag["identifier"]] = flag["default"] # TODO: change value to default when action is changed (not on every draw)
                    col.prop(entity, flag.get("identifier"), text=flag.get("name", flag.get("identifier")))

            if "skills" in currentConfig and len(currentConfig.get("skills")) != 0:
                for i, skill in enumerate(currentConfig["skills"]):
                    layout.row().prop(entity, skill.get("identifier"), text=skill.get("name", skill.get("identifier")))

            if "path" in currentConfig and currentConfig.get("path") == True:
                layout.row().prop(entity, "path")

