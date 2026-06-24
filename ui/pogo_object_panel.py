# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import bpy

from .. import pogo_blend_utils as pbu


class AddPogoPathData(pbu.AltOperator):
    bl_idname = "pogo_blend.add_pogo_path_data"
    bl_label = "Add Pogo Data"
    bl_description = "Adds Pogo Data to the curve, allowing it to be used in the map"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return obj.type == 'CURVE'

    def execute_obj(self, obj):
        obj.pogo_path


class RemovePogoPathData(pbu.AltOperator):
    bl_idname = "pogo_blend.remove_pogo_path_data"
    bl_label = "Remove Pogo Data"
    bl_description = "Removes Pogo Data from the curve, turning it back into a regular Blender Curve that will not be included in the map"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_path" in obj

    def execute_obj(self, obj):
        del obj["pogo_path"]


class AddPogoEntityData(pbu.AltOperator):
    bl_idname = "pogo_blend.add_pogo_entity_data"
    bl_label = "Add Pogo Data"
    bl_description = "Adds Pogo Data to the object, turning it into an entity that will be included in the map"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return obj.type == 'MESH'

    def execute_obj(self, obj):
        obj.pogo_entity


class RemovePogoEntityData(pbu.AltOperator):
    bl_idname = "pogo_blend.remove_pogo_entity_data"
    bl_label = "Remove Pogo Data"
    bl_description = "Removes Pogo Data from the object, turning it back into a regular Blender Object that will not be included in the map"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_entity" in obj

    def execute_obj(self, obj):
        del obj["pogo_entity"]


class EditCustomMaterial(bpy.types.Operator):
    bl_idname = "pogo_blend.edit_custom_material"
    bl_label = "Edit Custom Material"
    bl_description = "Opens the Custom Material shader code in a text editor"
    bl_options = {'REGISTER'}

    def get_templates(self, context):
        templates = pbu.get_custom_material_templates()
        return [(str(template.filepath.resolve().absolute()), template.name, template.description) for template in templates if template.filepath is not None]

    material_idx: bpy.props.IntProperty(default=-1)
    template: bpy.props.EnumProperty(items=get_templates)

    def execute(self, context):
        if self.material_idx < 0 or self.material_idx > 5:
            return {'CANCELLED'}

        filename = f"customMaterial{self.material_idx}.fx"

        pbu.open_temp_text_editor()

        if filename not in bpy.data.texts:
            filepath = Path(bpy.path.abspath(bpy.path.relpath(filename)))
            if filepath.exists():
                bpy.ops.text.open(filepath=str(filepath))
            else:
                bpy.ops.text.new()
                context.space_data.text.name = filename
                content = pbu.read_file(Path(self.template))
                bpy.data.texts[filename].from_string(content)

        text_obj = bpy.data.texts[filename]
        context.space_data.text = text_obj
        if not text_obj.is_dirty and text_obj.is_modified:
            with open(text_obj.filepath, "r") as f:
                text_obj.from_string(f.read())
            bpy.ops.text.save()

        bpy.ops.text.move(type='FILE_TOP')

        return {'FINISHED'}


class PogoObjectPanel(bpy.types.Panel):
    bl_label = "PogoBlend"
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
            case 'EMPTY':
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

        if entity.action_override == "egg_act":
            layout.row().operator("pogo_blend.open_link", text="Open Egg Documentation").url = "https://gubfs.github.io/pogo-blend/guides/egg.html"

        row = layout.row()
        if entity.name_override == "":
            row.prop(obj, "name")
        else:
            row = layout.row()
            row.column().label(text="Name: ")
            override_text = row.column()
            override_text.scale_x = 1.74
            override_text.enabled = False
            override_text.label(text=entity.name_override)
        row.operator("pogo_blend.remove_pogo_entity_data", text="", icon="X")
        layout.prop(obj, "location")
        layout.prop(obj, "rotation_euler", text="Rotation")
        layout.prop(obj, "scale")

        if entity.material_override == "":
            row = layout.row()
            if not entity.material.startswith("customMaterial"):
                row.prop(entity, "material")
            else:
                material_idx = int(entity.material[-1])
                custom_material = pbu.CustomMaterial.from_index(material_idx)

                if custom_material is None or custom_material.name == "":
                    row.prop(entity, "material")
                else:
                    idk = row.column()
                    idk.label(text="Material: ")
                    idk.scale_x = 0.34
                    match material_idx:
                        case 1:
                            icon = "IPO_SINE"
                        case 2:
                            icon = "IPO_QUAD"
                        case 3:
                            icon = "IPO_CUBIC"
                        case 4:
                            icon = "IPO_QUART"
                        case 5:
                            icon = "IPO_QUINT"
                        case _:
                            icon = "NONE"
                    row.prop(entity, "material", icon=icon, icon_only=True)

                if custom_material is not None:
                    row.operator("pogo_blend.edit_custom_material", text=custom_material.name, icon='GREASEPENCIL').material_idx = material_idx
                else:
                    row.operator_menu_enum("pogo_blend.edit_custom_material", "template", text="", icon="DOCUMENTS").material_idx = material_idx
        else:
            row = layout.row()
            row.column().label(text="Material: ")
            override_text = row.column()
            override_text.scale_x = 1.8
            override_text.enabled = False
            override_text.label(text=entity.material_override)

        row = layout.row()
        if entity.material_override == "" and entity.material in entity.materials:
            ambient = entity.materials[entity.material]["ambient"]
            if ambient is not None:
                row.prop(entity, "ambient", text=ambient)
            albedo = entity.materials[entity.material]["albedo"]
            if albedo is not None:
                row.prop(entity, "albedo", text=albedo)

        row = layout.row()
        col = row.column()
        col.prop(entity, "flag_invisible")
        col.prop(entity, "flag_polygon")
        if entity.flag_polygon:
            col.prop(entity, "flag_auto_collision")
            col.prop(entity, "flag_metal")

        col = row.column()
        col.prop(entity, "flag_shadow")
        col.prop(entity, "flag_cast")
        if entity.flag_polygon:
            col.prop(entity, "flag_7")
            col.prop(entity, "flag_8")

        if entity.action_override == "":
            layout.row().prop(entity, "action1")
            if entity.action1 in entity.actions:
                self.draw_action_panel(entity, entity.action1, layout)
                layout.row().prop(entity, "action2")
                if entity.action2 in entity.actions:
                    self.draw_action_panel(entity, entity.action2, layout)
        else:
            row = layout.row()
            row.column().label(text="Action: ")
            override_text = row.column()
            override_text.scale_x = 1.76
            override_text.enabled = False
            override_text.label(text=entity.action_override)

        if entity.filename_override != "":
            layout.label(text=f"Using \"{entity.filename_override}\". Model may appear different in game.", icon="WARNING_LARGE")

    def draw_action_panel(self, entity, action, layout):
        action_config = entity.actions[action]

        if len(action_config["flags"]) != 0:
            row = layout.row()
            colLeft = row.column()
            colRight = row.column()
            for i, (flag, flag_config) in enumerate(action_config["flags"].items()):
                col = colLeft if i % 2 == 0 else colRight
                col.prop(
                    entity,
                    flag,
                    text=flag_config["name"],
                )

        if len(action_config["skills"]) != 0:
            for i, (skill, skill_config) in enumerate(action_config["skills"].items()):
                if action != "skillset_act" or not entity.material.startswith("customMaterial"):
                    layout.prop(
                        entity,
                        skill,
                        text=skill_config["name"],
                    )
                else:
                    material_idx = int(entity.material[-1])
                    custom_material = pbu.CustomMaterial.from_index(material_idx)
                    if custom_material is not None and len(custom_material.skills) != 0:
                        skill_renamed = skill.replace("_", "")
                        if skill_renamed in custom_material.skills:
                            layout.prop(
                                entity,
                                skill,
                                text=custom_material.skills[skill_renamed][0],
                                placeholder=custom_material.skills[skill_renamed][1],
                            )
                    else:
                        layout.prop(
                            entity,
                            skill,
                            text=skill_config["name"],
                        )

        if action_config["path"]:
            layout.prop(entity, "path", placeholder="Path", icon='OUTLINER_OB_CURVE')

    def draw_empty_panel(self, obj, layout):
        if "pogo_region" not in obj:
            self.draw_not_relevant(layout)
            return
        layout.prop(obj.pogo_region, "region_type")
        if obj.pogo_region.region_type == "gravityReg_":
            layout.prop(obj.pogo_region, "gravity_angle")
            layout.prop(obj.pogo_region, "gravity_power")


class PogoObjectPanelOverrides(bpy.types.Panel):
    bl_label = "Overrides"
    bl_idname = "OBJECT_PT_object_pogo_blend_override"
    bl_parent_id = "OBJECT_PT_object_pogo_blend"
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return ("pogo_entity" in context.object or "pogo_path" in context.object or "pogo_region" in context.object) and cls.is_overridden(context.object)

    @classmethod
    def is_overridden(cls, obj) -> bool:
        if "pogo_entity" in obj:
            entity = obj.pogo_entity
            return (
                pbu.get_preferences().show_overrides  #
                or entity.name_override != ""
                or entity.filename_override != ""
                or entity.material_override != ""
                or entity.action_override != ""
                or entity.string1_override != ""
                or entity.string2_override != ""
            )
        if "pogo_path" in obj:
            path = obj.pogo_path
            return (
                pbu.get_preferences().show_overrides  #
                or path.name_override != ""
            )
        if "pogo_region" in obj:
            region = obj.pogo_region
            return (
                region.region_type == "ndef"  #
                and (pbu.get_preferences().show_overrides or region.name_override != "")
            )
        return False

    def draw(self, context):
        layout = self.layout
        obj = context.object

        match obj.type:
            case 'MESH':
                self.draw_mesh_override(obj, layout)
            case 'CURVE':
                self.draw_curve_panel(obj, layout)
            case 'EMPTY':
                self.draw_empty_override(obj, layout)

    def draw_mesh_override(self, obj, layout):
        if "pogo_entity" not in obj:
            return

        show_override = pbu.get_preferences().show_overrides

        entity = obj.pogo_entity

        if show_override or entity.name_override != "":
            layout.prop(entity, "name_override")
        if show_override or entity.filename_override != "":
            layout.prop(entity, "filename_override")
        if show_override or entity.material_override != "":
            layout.prop(entity, "material_override")

        if show_override:
            row = layout.row()
            row.prop(entity, "ambient", text="ambient")
            row.prop(entity, "albedo", text="albedo")

        if show_override:
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

        if show_override or entity.action_override != "":
            layout.prop(entity, "action_override")

        if show_override:
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

        if show_override:
            layout.prop(entity, "path")

        if show_override or entity.string1_override != "":
            layout.prop(entity, "string1_override", text="string1")
        if show_override or entity.string2_override != "":
            layout.prop(entity, "string2_override", text="string2")

        if show_override:
            for i in range(1, 21):
                layout.prop(entity, f"skill_{i}", text=f"skill_{i}")

    def draw_curve_panel(self, obj, layout):
        if "pogo_path" not in obj:
            return

        path = obj.pogo_path

        layout.prop(path, "name_override")

    def draw_empty_override(self, obj, layout):
        if "pogo_region" not in obj:
            return

        region = obj.pogo_region

        layout.prop(region, "name_override")
        layout.prop(region, "min_y_override")
        layout.prop(region, "max_y_override")


classes = (
    AddPogoEntityData,
    RemovePogoEntityData,
    AddPogoPathData,
    RemovePogoPathData,
    EditCustomMaterial,
    PogoObjectPanel,
    PogoObjectPanelOverrides,
)
