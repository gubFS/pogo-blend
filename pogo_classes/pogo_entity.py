import json
import os

import bpy


def register():
    bpy.utils.register_class(PogoEntity)
    bpy.types.Object.pogo_entity = bpy.props.PointerProperty(type=PogoEntity)


def unregister():
    bpy.utils.unregister_class(PogoEntity)
    del bpy.types.Object.pogo_entity


class PogoEntity(bpy.types.PropertyGroup):
    name_override: bpy.props.StringProperty()
    filename_override: bpy.props.StringProperty()
    material_override: bpy.props.StringProperty()
    action_override: bpy.props.StringProperty()
    string1_override: bpy.props.StringProperty()
    string2_override: bpy.props.StringProperty()

    material_enums = [("ndef", "", "")]
    with open(os.path.join(os.path.dirname(__file__), "materials.json"), "r") as f_in:
        materials = json.load(f_in)
        for material, config in materials.items():
            if "disable" in config and config["disable"] == True:
                continue
            material_enums.append(
                (
                    material,
                    config["name"] if "name" in config else material,
                    config["description"] if "description" in config else "",
                )
            )
    material: bpy.props.EnumProperty(
        items=material_enums, name="Material", default="ndef"
    )

    flag_invisible: bpy.props.BoolProperty(name="Invisble")  # = 8,
    flag_passable: bpy.props.BoolProperty(name="Passable")  # = 9,
    flag_transparent: bpy.props.BoolProperty(name="Transparent")  # = 10,
    flag_unlit: bpy.props.BoolProperty(name="Unlit")  # = 17,
    flag_shadow: bpy.props.BoolProperty(name="Shadow")  # = 18, #
    flag_metal: bpy.props.BoolProperty(name="Kill")  # = 22, # kill
    flag_cast: bpy.props.BoolProperty(name="Cast")  # = 23, #
    flag_polygon: bpy.props.BoolProperty(
        name="Collision"
    )  # = 26, # collision. if polygon isn't set then its passable

    flag_overlay: bpy.props.BoolProperty()  # = 12,
    flag_flare: bpy.props.BoolProperty()  # = 15,
    flag_nofilter: bpy.props.BoolProperty()  # = 16,
    flag_nofog: bpy.props.BoolProperty()  # = 20,
    flag_bright: bpy.props.BoolProperty()  # = 21,
    flag_local: bpy.props.BoolProperty()  # = 25,
    flag_bbox: bpy.props.BoolProperty()  # = 29,

    ambient: bpy.props.FloatProperty(name="Ambient")
    albedo: bpy.props.FloatProperty(name="Albedo", default=50.0)

    action_enums = [("ndef", "", "")]
    with open(os.path.join(os.path.dirname(__file__), "actions.json"), "r") as f_in:
        actions = json.load(f_in)
        for action, config in actions.items():
            if "disable" in config and config["disable"] == True:
                continue
            action_enums.append(
                (
                    action,
                    config["name"] if "name" in config else action,
                    config["description"] if "description" in config else "",
                )
            )

    def on_action1_change(self, context):
        value = self.action1
        if value == "ndef" and self.action2 != "ndef":
            self.action1 = self.action2
            self.action2 = "ndef"

    action1: bpy.props.EnumProperty(
        items=action_enums, name="Action", default="ndef", update=on_action1_change
    )
    action2: bpy.props.EnumProperty(items=action_enums, name="Action2", default="ndef")

    flag_1: bpy.props.BoolProperty(name="flag_1")  # = 0,
    flag_2: bpy.props.BoolProperty(name="flag_2")  # = 1,
    flag_3: bpy.props.BoolProperty(name="flag_3")  # = 2,
    flag_4: bpy.props.BoolProperty(name="flag_4")  # = 3,
    flag_5: bpy.props.BoolProperty(name="flag_5")  # = 4,
    flag_6: bpy.props.BoolProperty(name="flag_6")  # = 5,
    flag_7: bpy.props.BoolProperty(name="Ice")  # = 6, # ICE
    flag_8: bpy.props.BoolProperty(name="Bonk")  # = 7,

    flag_auto_collision: bpy.props.BoolProperty(name="Auto Collision")

    path: bpy.props.PointerProperty(
        type=bpy.types.Object, name="Path", poll=lambda prop, obj: "pogo_path" in obj
    )

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
            | self.flag_transparent << 10
            | self.flag_overlay << 12
            | self.flag_flare << 15
            | self.flag_nofilter << 16
            | self.flag_unlit << 17
            | self.flag_shadow << 18
            | self.flag_nofog << 20
            | self.flag_bright << 21
            | self.flag_metal << 22
            | self.flag_cast << 23
            | self.flag_local << 25
            | self.flag_bbox << 27
            | 1 << (26 if self.flag_polygon else 9)  # 9 = passable
        )

        return flags
