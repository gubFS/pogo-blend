import bpy

def register():
    bpy.utils.register_class(AddPogoEntityData)
    bpy.utils.register_class(AddPogoPathData)
    bpy.utils.register_class(PogoObjectPanel)
    bpy.utils.register_class(PogoObjectPanelOverrides)


def unregister():
    bpy.utils.unregister_class(AddPogoEntityData)
    bpy.utils.unregister_class(AddPogoPathData)
    bpy.utils.unregister_class(PogoObjectPanel)
    bpy.utils.unregister_class(PogoObjectPanelOverrides)

class AddPogoPathData(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_path_data"
    bl_label = "Add pogo data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object.pogo_path
        return {'FINISHED'}

class AddPogoEntityData(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_entity_data"
    bl_label = "Add pogo data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object.pogo_entity
        return {'FINISHED'}

class PogoObjectPanel(bpy.types.Panel):
    bl_label = "Pogo Blend"
    bl_idname = "OBJECT_PT_object_pogo_blend"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        match obj.type:
            case 'MESH':
                self.draw_mesh_panel(obj, layout)
            case 'CURVE':
                self.draw_curve_panel(obj, layout)
            case _:
                layout.label(text="This object type has no relevant pogo data")
                return

    def draw_curve_panel(self, obj, layout):
        try: obj["pogo_path"]
        except KeyError:
            layout.operator("pogo_blend.add_pogo_path_data")
            return
        layout.label(text="This curve is a Pogo Path")

    def draw_mesh_panel(self, obj, layout):
        try: obj["pogo_entity"]
        except KeyError:
            layout.operator("pogo_blend.add_pogo_entity_data")
            return

        entity = obj.pogo_entity

        layout.prop(obj, "name")
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
                    layout.prop(entity, skill.get("identifier"), text=skill.get("name", skill.get("identifier")))

            if "path" in currentConfig and currentConfig.get("path") == True:
                layout.prop(entity, "path")

class PogoObjectPanelOverrides(bpy.types.Panel):
    bl_label = "Overrides"
    bl_idname = "OBJECT_PT_object_pogo_blend_override"
    bl_parent_id = "OBJECT_PT_object_pogo_blend"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        try: obj["pogo_entity"]
        except KeyError: return

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

