from typing import Any

import bpy

from .. import pogo_blend_utils as pbu


class PogoEntity(bpy.types.PropertyGroup):
    name_override: bpy.props.StringProperty()
    filename_override: bpy.props.StringProperty()
    material_override: bpy.props.StringProperty()
    action_override: bpy.props.StringProperty()
    string1_override: bpy.props.StringProperty()
    string2_override: bpy.props.StringProperty()

    material_enums = []
    material_enums.extend(pbu.get_enum_list("pogo_classes/materials.yaml", False))  # pbu.get_preferences().show_all_materials))

    materials = pbu.parse_yaml("pogo_classes/materials.yaml")
    for key, config in materials.items():
        if config is None:
            config = {}
            materials[key] = config
        config.setdefault("name", key)
        config.setdefault("description", "")
        # config.setdefault("id", -1)
        config.setdefault("ambient", None)
        config.setdefault("albedo", None)
        config.setdefault("transparent", None)

    material: bpy.props.EnumProperty(items=material_enums, name="Material", description="The material on the entity. Changes the look of the entity", default="appAGeoDefault_mat")

    flag_invisible: bpy.props.BoolProperty(name="Invisble", description="Makes the entity invisible")  # = 8,
    flag_transparent: bpy.props.BoolProperty(name="Transparent", description="Makes the entity transparent. Albedo changes the transparency percentage. Does not work with most materials", default=True)  # = 10,
    flag_unlit: bpy.props.BoolProperty(name="Unlit", description="Makes entity ignore lighting and appear \"flat\". Only relevant without any material", default=True)  # = 17,
    flag_shadow: bpy.props.BoolProperty(name="Shadow", description="Add a glow shadow to the entity")  # = 18, #
    flag_metal: bpy.props.BoolProperty(name="Kill", description="Kills the player on contact. (looks metallic if there's no material and it's not unlit)")  # = 22, # kill
    flag_cast: bpy.props.BoolProperty(name="Background", description="Blurs the entity and places it in the background")
    flag_polygon: bpy.props.BoolProperty(name="Collision", description="Enable collsion with the entity. Collides where it's Y-position is 0")  # = 26, # collision. if polygon isn't set then its passable

    flag_auto_collision: bpy.props.BoolProperty(name="Auto Collision", description="Create a collider for the entity that matches it's sideview no matter the Y-position")

    flag_passable: bpy.props.BoolProperty()  # = 9,
    flag_overlay: bpy.props.BoolProperty()  # = 12,
    flag_flare: bpy.props.BoolProperty()  # = 15,
    flag_nofilter: bpy.props.BoolProperty()  # = 16,
    flag_nofog: bpy.props.BoolProperty()  # = 20,
    flag_bright: bpy.props.BoolProperty()  # = 21,
    flag_local: bpy.props.BoolProperty()  # = 25,
    flag_bbox: bpy.props.BoolProperty()  # = 29,

    ambient: bpy.props.FloatProperty(name="Brightness", description="The brightness of the entity between -100% and 100% (does not work on some materials)", min=-100.0, max=100.0)
    albedo: bpy.props.FloatProperty(name="Albedo", description="General purpose percentage slider. The effect changes depending on other settings", default=100.0, min=0.0, max=100.0)

    action_enums = [("ndef", "", "No action", 0)]
    action_enums.extend(pbu.get_enum_list("pogo_classes/actions.yaml", False))  # pbu.get_preferences().show_all_actions))

    actions = pbu.parse_yaml("pogo_classes/actions.yaml")
    for key, config in actions.items():
        if config is None:
            config = {}
            actions[key] = config
        config.setdefault("name", key)
        config.setdefault("description", "")
        config.setdefault("flags", {})
        config.setdefault("skills", {})
        config.setdefault("path", False)

        flags_to_delete = set()
        for flag, flag_config in config["flags"].items():
            if "hidden" in flag_config and flag_config["hidden"]:
                flags_to_delete.add(flag)
                continue
            flag_config.setdefault("name", flag)
            flag_config.setdefault("description", "")
            flag_config.setdefault("default", False)
        for flag in flags_to_delete:
            del config["flags"][flag]

        skills_to_delete = set()
        for skill, skill_config in config["skills"].items():
            if "hidden" in skill_config and skill_config["hidden"]:
                skills_to_delete.add(skill)
                continue
            skill_config.setdefault("name", skill)
            skill_config.setdefault("description", "")
            skill_config.setdefault("default", 0.0)
        for skill in skills_to_delete:
            del config["skills"][skill]

    def on_action1_change(self, context):
        value = self.action1
        if value == "ndef" and self.action2 != "ndef":
            self.action1 = self.action2
            self.action2 = "ndef"
        else:
            if context.area and context.area.type == 'PROPERTIES':
                self.set_action_defaults(context, True)

    def on_action2_change(self, context):
        if context.area.type == 'PROPERTIES':
            self.set_action_defaults(context, False)

    def set_action_defaults(self, context, is_action1: bool) -> None:
        other_action_name = ""
        if ("action1" if not is_action1 else "action2") in self:
            other_action_name = self.action1 if not is_action1 else self.action2
        new_action_name = self.action1 if is_action1 else self.action2

        all_values = set()
        all_values.update(f"flag_{i}" for i in range(1, 9))
        all_values.update(f"skill_{i}" for i in range(1, 21))

        in_use = set()
        if other_action_name in self.actions:
            config = self.actions[other_action_name]
            in_use.update(flag for flag in config["flags"].keys())
            in_use.update(skill for skill in config["skills"].keys())
        all_values = all_values.difference(in_use)

        new_action_values = {}
        if new_action_name in self.actions:
            config = self.actions[new_action_name]
            new_action_values.update({flag: flag_config["default"] for flag, flag_config in config["flags"].items()})
            new_action_values.update({skill: skill_config["default"] for skill, skill_config in config["skills"].items()})

        for id, value in new_action_values.items():
            if id in in_use:
                continue
            default = value
            self[id] = default
        all_values = all_values.difference(new_action_values)
        for value in all_values:
            self.property_unset(value)

    action1: bpy.props.EnumProperty(items=action_enums, name="Action", description="Changes the behavior of the entity", default="ndef", update=on_action1_change)
    action2: bpy.props.EnumProperty(items=action_enums, name="Action2", description="Changes the secondary behavior of the entity", default="ndef", update=on_action2_change)

    flag_1: bpy.props.BoolProperty(name="flag_1")  # = 0,
    flag_2: bpy.props.BoolProperty(name="flag_2")  # = 1,
    flag_3: bpy.props.BoolProperty(name="flag_3")  # = 2,
    flag_4: bpy.props.BoolProperty(name="flag_4")  # = 3,
    flag_5: bpy.props.BoolProperty(name="flag_5")  # = 4,
    flag_6: bpy.props.BoolProperty(name="flag_6")  # = 5,
    flag_7: bpy.props.BoolProperty(name="Ice", description="Makes the entity have ice physics (may overlap with some actions flags)")  # = 6, # ICE
    flag_8: bpy.props.BoolProperty(name="Bonk", description="Bonks the player on contact no matter what (may overlap with some action flags)")  # = 7, # NO BONK

    path: bpy.props.PointerProperty(type=bpy.types.Object, name="Path", description="Attached path", poll=lambda prop, obj: "pogo_path" in obj)

    skill_1: bpy.props.FloatProperty(name="skill_1")
    skill_2: bpy.props.FloatProperty(name="skill_2")
    skill_3: bpy.props.FloatProperty(name="skill_3")
    skill_4: bpy.props.FloatProperty(name="skill_4")
    skill_5: bpy.props.FloatProperty(name="skill_5")
    skill_6: bpy.props.FloatProperty(name="skill_6")
    skill_7: bpy.props.FloatProperty(name="skill_7")
    skill_8: bpy.props.FloatProperty(name="skill_8")
    skill_9: bpy.props.FloatProperty(name="skill_9")
    skill_10: bpy.props.FloatProperty(name="skill_10")
    skill_11: bpy.props.FloatProperty(name="skill_11")
    skill_12: bpy.props.FloatProperty(name="skill_12")
    skill_13: bpy.props.FloatProperty(name="skill_13")
    skill_14: bpy.props.FloatProperty(name="skill_14")
    skill_15: bpy.props.FloatProperty(name="skill_15")
    skill_16: bpy.props.FloatProperty(name="skill_16")
    skill_17: bpy.props.FloatProperty(name="skill_17")
    skill_18: bpy.props.FloatProperty(name="skill_18")
    skill_19: bpy.props.FloatProperty(name="skill_19")
    skill_20: bpy.props.FloatProperty(name="skill_20")

    def compare_material_config(self, key: str, comparision: Any = True) -> bool:
        return self.material in self.materials and self.materials[self.material][key] == comparision

    def copy_from(self, other) -> None:
        self.name_override = other.name_override
        self.filename_override = other.filename_override
        self.material_override = other.material_override
        self.action_override = other.action_override
        self.string1_override = other.string1_override
        self.string2_override = other.string2_override
        self.material = other.material if other.material != "" else "ndef"
        self.flag_invisible = other.flag_invisible
        self.flag_passable = other.flag_passable
        self.flag_transparent = other.flag_transparent
        self.flag_unlit = other.flag_unlit
        self.flag_shadow = other.flag_shadow
        self.flag_metal = other.flag_metal
        self.flag_cast = other.flag_cast
        self.flag_polygon = other.flag_polygon
        self.flag_overlay = other.flag_overlay
        self.flag_flare = other.flag_flare
        self.flag_nofilter = other.flag_nofilter
        self.flag_nofog = other.flag_nofog
        self.flag_bright = other.flag_bright
        self.flag_local = other.flag_local
        self.flag_bbox = other.flag_bbox
        self.ambient = other.ambient
        self.albedo = other.albedo
        self.action1 = other.action1 if other.action1 != "" else "ndef"
        self.action2 = other.action2 if other.action2 != "" else "ndef"
        self.flag_1 = other.flag_1
        self.flag_2 = other.flag_2
        self.flag_3 = other.flag_3
        self.flag_4 = other.flag_4
        self.flag_5 = other.flag_5
        self.flag_6 = other.flag_6
        self.flag_7 = other.flag_7
        self.flag_8 = other.flag_8
        self.flag_auto_collision = other.flag_auto_collision
        self.path = other.path
        self.skill_1 = other.skill_1
        self.skill_2 = other.skill_2
        self.skill_3 = other.skill_3
        self.skill_4 = other.skill_4
        self.skill_5 = other.skill_5
        self.skill_6 = other.skill_6
        self.skill_7 = other.skill_7
        self.skill_8 = other.skill_8
        self.skill_9 = other.skill_9
        self.skill_10 = other.skill_10
        self.skill_11 = other.skill_11
        self.skill_12 = other.skill_12
        self.skill_13 = other.skill_13
        self.skill_14 = other.skill_14
        self.skill_15 = other.skill_15
        self.skill_16 = other.skill_16
        self.skill_17 = other.skill_17
        self.skill_18 = other.skill_18
        self.skill_19 = other.skill_19
        self.skill_20 = other.skill_20

    def get_skills(self) -> list[bpy.props.FloatProperty]:
        skills = []
        for i in range(1, 21):
            skills.append(getattr(self, f"skill_{i}"))
        return skills

    def get_flags(self) -> int:
        flags = (
            self.flag_1 << 0
            | self.flag_2 << 1
            | self.flag_3 << 2
            | self.flag_4 << 3
            | self.flag_5 << 4
            | self.flag_6 << 5
            | self.flag_7 << 6
            | self.flag_8 << 7
            | self.flag_invisible << 8
            | ((self.flag_transparent & self.compare_material_config("albedo", "Transparency")) | self.compare_material_config("transparent")) << 10
            | self.flag_overlay << 12
            | self.flag_flare << 15
            | self.flag_nofilter << 16
            | (self.flag_unlit & (self.material != "ndef")) << 17
            | (self.flag_shadow | self.flag_cast) << 18
            | self.flag_nofog << 20
            | self.flag_bright << 21
            | self.flag_metal << 22
            | self.flag_cast << 23
            | self.flag_local << 25
            | self.flag_bbox << 27
            | 1 << (26 if self.flag_polygon else 9)  # 9 = passable
        )

        return flags


def register():
    bpy.utils.register_class(PogoEntity)
    bpy.types.Object.pogo_entity = bpy.props.PointerProperty(type=PogoEntity)


def unregister():
    bpy.utils.unregister_class(PogoEntity)
    del bpy.types.Object.pogo_entity
