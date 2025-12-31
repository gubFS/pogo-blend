import math

from ...gub_byte_array import GubByteArray


class WMBEntity:
    def __init__(self, obj):
        entity = obj.pogo_entity

        self.type = 7  # 7 is the ID for entity types
        self.origin = obj.matrix_world.to_translation().to_3d()
        rotation = obj.matrix_world.to_euler()
        self.angle = (
            math.degrees(rotation.z),
            math.degrees(-rotation.y),
            math.degrees(rotation.x),
        )
        self.scale = obj.scale.copy()  # if entity.filename_override == "" else (1, 1, 1)
        self.name = obj.name.replace(".", "_") if entity.name_override == "" else entity.name_override

        self.filename = (
            f"NOTSWITCHED"
            if entity.filename_override == ""
            else entity.filename_override
        )

        if entity.action_override != "":
            self.action = entity.action_override
            self.string1 = entity.string1_override
            self.string2 = entity.string2_override
        elif (
            entity.action2 == "ndef"
            or entity.string1_override != ""
            or entity.string2_override != ""
        ):
            self.action = entity.action1 if entity.action1 != "ndef" else ""
            self.string1 = entity.string1_override
            self.string2 = entity.string2_override
        else:
            self.action = "execString12acts"
            self.string1 = entity.action1 if entity.action1 != "ndef" else ""
            self.string2 = entity.action2 if entity.action2 != "ndef" else ""

        self.skills = entity.get_skills()
        self.flags = entity.get_flags()
        self.ambient = entity.ambient
        self.albedo = entity.albedo
        self.path = 0
        self.entity2 = 0
        self.material = (
            entity.material
            if entity.material_override == ""
            else entity.material_override
        )

    def to_bytes(self) -> GubByteArray:
        is_old = self.is_old()  # 'old' entity types use less space

        bytes = GubByteArray()

        bytes.store_32(3 if is_old else self.type)
        bytes.store_vec3f(self.origin)
        bytes.store_vec3f(self.angle)
        bytes.store_vec3f(self.scale)
        bytes.store_string(self.name, 20 if is_old else 33)
        bytes.store_string(self.filename, 13 if is_old else 33)
        bytes.store_string(self.action, 20 if is_old else 34)
        if is_old:
            bytes.store_8s(0, 3)  # unused
        bytes.store_float_buffer(self.skills, 8 if is_old else 20)
        bytes.store_32(self.flags)
        bytes.store_float(self.ambient)
        if not is_old:
            bytes.store_float(self.albedo)
            bytes.store_32(self.path)
            bytes.store_32(self.entity2)
            bytes.store_string(self.material, 33)
            bytes.store_string(self.string1, 33)
            bytes.store_string(self.string2, 33)
            bytes.store_8s(0, 33)  # unused

        return bytes

    def is_old(self) -> bool:
        return (
            self.albedo == 50.0
            and self.path == 0
            and self.entity2 == 0
            and self.material == "ndef"
            and self.string1 == ""
            and self.string2 == ""
            and len(self.filename) <= 12
            and len(self.action) <= 20
            and self.is_skills_old()
        )

    def is_skills_old(self) -> bool:
        for i in range(8, min(len(self.skills), 20)):
            if self.skills[i] != 0.0:
                return False
        return True


class PogoSpawn(WMBEntity):
    def __init__(self, obj):
        self.type = 7  # 7 is the ID for entity types
        self.origin = obj.location
        self.angle = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.name = "spawn1"
        self.filename = ""
        self.action = "spawn_act"
        self.skills = []
        self.flags = 1 << 8 | 1 << 17 | 1 << 9  # invisible, unlit and passable
        self.ambient = 0
        self.albedo = 50.0
        self.path = 0
        self.entity2 = 0
        self.material = "ndef"
        self.string1 = ""
        self.string2 = ""


class PogoModeSetup(WMBEntity):
    def __init__(self, custom_map):
        self.type = 7  # 7 is the ID for entity types
        self.origin = (0, 0, 0)
        self.angle = (0, 0, 0)
        self.scale = (1, 1, 1)
        self.name = "modeSetup"
        self.filename = ""
        self.action = "customMapSetup_act"
        self.string1 = ""
        self.string2 = ""
        self.skills = []

        flags = 1 << 8 | 1 << 9 | 1 << 17  # invis, passable, unlit
        if custom_map.double_jump:
            flags |= 1 << 2
        if custom_map.puzzle:
            flags |= 1 << 3
        if custom_map.no_boost:
            flags |= 1 << 4
        if custom_map.no_bonk:
            flags |= 1 << 5
        if custom_map.mushroom_power:
            flags |= 1 << 6
        if custom_map.ice:
            flags |= 1 << 7
        self.flags = flags

        self.ambient = 0.0
        self.albedo = 50.0
        self.path = 0
        self.entity2 = 0
        self.material = "ndef"


class PogoStartLine(WMBEntity):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = "startLine"
        self.action = "skillset_act"
        self.flags |= 1 << 0  # flag_1
        self.skills = [1.0]
