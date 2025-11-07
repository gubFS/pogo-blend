import bpy

from .. import pogo_blend_preferences as pbu


class AddPogoPathData(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_path_data"
    bl_label = "Add pogo data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object.pogo_path
        return {"FINISHED"}


class RemovePogoPathData(bpy.types.Operator):
    bl_idname = "pogo_blend.remove_pogo_path_data"
    bl_label = "Remove pogo data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        del context.object["pogo_path"]
        return {"FINISHED"}


class AddPogoEntityData(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_entity_data"
    bl_label = "Add pogo data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        context.object.pogo_entity
        return {"FINISHED"}


class RemovePogoEntityData(bpy.types.Operator):
    bl_idname = "pogo_blend.remove_pogo_entity_data"
    bl_label = "Remove pogo data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        del context.object["pogo_entity"]
        return {"FINISHED"}


class PogoObjectPanel(bpy.types.Panel):
    bl_label = "Pogo Blend"
    bl_idname = "OBJECT_PT_object_pogo_blend"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        match obj.type:
            case "MESH":
                self.draw_mesh_panel(obj, layout)
            case "CURVE":
                self.draw_curve_panel(obj, layout)
            case "EMPTY":
                self.draw_empty_panel(obj, layout)
            case _:
                self.draw_not_relevant(layout)
                return

    def draw_not_relevant(self, layout):
        layout.label(text="This object type has no relevant pogo data")

    def draw_curve_panel(self, obj, layout):
        if "pogo_path" not in obj:
            layout.operator("pogo_blend.add_pogo_path_data")
            return
        row = layout.row()
        row.label(text="This curve is a Pogo Path")
        row.separator_spacer()
        row.operator("pogo_blend.remove_pogo_path_data", text="", icon="X")

    def draw_mesh_panel(self, obj, layout):
        if "pogo_entity" not in obj:
            layout.operator("pogo_blend.add_pogo_entity_data")
            return

        entity = obj.pogo_entity

        row = layout.row()
        row.prop(obj, "name")
        row.operator("pogo_blend.remove_pogo_entity_data", text="", icon="X")
        layout.prop(obj, "location")
        layout.prop(obj, "rotation_euler", text="Rotation")
        layout.prop(obj, "scale")
        layout.prop(entity, "material")

        row = layout.row()
        row.prop(entity, "ambient")
        row.prop(entity, "albedo")

        row = layout.row()
        col = row.column()
        col.prop(entity, "flag_invisible")
        col.prop(entity, "flag_unlit")
        col.prop(entity, "flag_transparent")
        col.prop(entity, "flag_polygon")
        # if entity.flag_polygon == True:
        #     col.prop(entity, "flag_auto_collision")

        col = row.column()
        col.prop(entity, "flag_shadow")
        col.prop(entity, "flag_cast")
        col.prop(entity, "flag_metal")
        col.prop(entity, "flag_7")
        col.prop(entity, "flag_8")

        layout.row().prop(entity, "action1")
        if entity.action1 in entity.actions:
            self.draw_action_panel(entity, entity.action1, layout)
            layout.row().prop(entity, "action2")
            if entity.action2 in entity.actions:
                self.draw_action_panel(entity, entity.action2, layout)

    def draw_action_panel(self, entity, action, layout):
        currentConfig = entity.actions.get(action)

        if "flags" in currentConfig and len(currentConfig.get("flags")) != 0:
            row = layout.row()
            colLeft = row.column()
            colRight = row.column()
            for i, flag in enumerate(currentConfig["flags"]):
                col = colLeft if i % 2 == 0 else colRight
                # entity[flag["identifier"]] = flag["default"] # TODO: change value to default when action is changed (not on every draw)
                col.prop(
                    entity,
                    flag.get("identifier"),
                    text=flag.get("name", flag.get("identifier")),
                )

        if "skills" in currentConfig and len(currentConfig.get("skills")) != 0:
            for i, skill in enumerate(currentConfig["skills"]):
                layout.prop(
                    entity,
                    skill.get("identifier"),
                    text=skill.get("name", skill.get("identifier")),
                )

        if "path" in currentConfig and currentConfig.get("path") == True:
            layout.prop(entity, "path", placeholder="Path", icon="OUTLINER_OB_CURVE")

    def draw_empty_panel(self, obj, layout):
        if "pogo_reigon" not in obj:
            self.draw_not_relevant(layout)
            return
        layout.prop(obj.pogo_reigon, "reigon_type")
        if obj.pogo_reigon.reigon_type == "gravityReg_":
            layout.prop(obj.pogo_reigon, "gravity_angle")
            layout.prop(obj.pogo_reigon, "gravity_power")


class PogoObjectPanelOverrides(bpy.types.Panel):
    bl_label = "Overrides"
    bl_idname = "OBJECT_PT_object_pogo_blend_override"
    bl_parent_id = "OBJECT_PT_object_pogo_blend"
    bl_options = {"DEFAULT_CLOSED"}
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return pbu.get_preferences().show_overrides and "pogo_entity" in context.object

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if "pogo_entity" not in obj:
            return

        entity = obj.pogo_entity
        layout.prop(entity, "name_override")
        layout.prop(entity, "filename_override")
        layout.prop(entity, "material_override")

        row = layout.row()
        col = row.column()
        col.prop(entity, "flag_invisible", text="flag_invisible")
        col.prop(entity, "flag_unlit", text="flag_unlit")
        col.prop(entity, "flag_transparent", text="flag_transparent")
        col.prop(entity, "flag_overlay", text="flag_overlay")
        col.prop(entity, "flag_shadow", text="flag_shadow")
        col.prop(entity, "flag_cast", text="flag_cast")
        col.prop(entity, "flag_metal", text="flag_metal")

        col = row.column()
        col.prop(entity, "flag_flare", text="flag_flare")
        col.prop(entity, "flag_bright", text="flag_bright")
        col.prop(entity, "flag_nofilter", text="flag_nofilter")
        col.prop(entity, "flag_nofog", text="flag_nofog")
        col.prop(entity, "flag_passable", text="flag_passable")
        col.prop(entity, "flag_bbox", text="flag_bbox")
        col.prop(entity, "flag_polygon", text="flag_polygon")
        col.prop(entity, "flag_local", text="flag_local")

        layout.prop(entity, "action_override")
        row = layout.row()
        col = row.column()
        col.prop(entity, "flag_1", text="flag_1")
        col.prop(entity, "flag_2", text="flag_2")
        col.prop(entity, "flag_3", text="flag_3")
        col.prop(entity, "flag_4", text="flag_4")

        col = row.column()
        col.prop(entity, "flag_5", text="flag_5")
        col.prop(entity, "flag_6", text="flag_6")
        col.prop(entity, "flag_7", text="flag_7")
        col.prop(entity, "flag_8", text="flag_8")

        layout.prop(entity, "string1_override", text="string1")
        layout.prop(entity, "string2_override", text="string2")


def register():
    bpy.utils.register_class(AddPogoEntityData)
    bpy.utils.register_class(RemovePogoEntityData)
    bpy.utils.register_class(AddPogoPathData)
    bpy.utils.register_class(RemovePogoPathData)
    bpy.utils.register_class(PogoObjectPanel)
    bpy.utils.register_class(PogoObjectPanelOverrides)


def unregister():
    bpy.utils.unregister_class(AddPogoEntityData)
    bpy.utils.unregister_class(RemovePogoEntityData)
    bpy.utils.unregister_class(AddPogoPathData)
    bpy.utils.unregister_class(RemovePogoPathData)
    bpy.utils.unregister_class(PogoObjectPanel)
    bpy.utils.unregister_class(PogoObjectPanelOverrides)
