from ..gub_byte_array import GubByteArray

class WMBEntity:
    def __init__(self, obj):
        entity = obj.pogo_entity

        self.type = 7 # 7 is the ID for entity types
        self.origin = obj.matrix_world.to_translation().to_3d()
        self.angle = obj.matrix_world.to_euler() # TODO: check the rotation is right format
        self.scale = obj.matrix_world.to_scale().to_3d()
        self.name = obj.name
        self.filename = f"{obj.name}.mdl" # TODO: write real filename when converted to .mdl
        self.action = "" if entity.action == "ndef" else entity.action #TODO: figure out if all objects should just use two actions
        self.skills = entity.get_skills()
        self.flags = entity.get_flags()
        self.ambient = entity.ambient
        self.albedo = entity.albedo
        self.path = 0
        self.entity2 = 0
        self.material = entity.material
        self.string1 = ""
        self.string2 = ""

    def to_bytes(self):
        is_old = self.is_old() # 'old' entity types use less space

        bytes = GubByteArray()

        bytes.store_32(3 if is_old else self.type)
        bytes.store_vec3f(self.origin)
        bytes.store_vec3f(self.angle)
        bytes.store_vec3f(self.scale)
        bytes.store_string(self.name, 20 if is_old else 33)
        bytes.store_string(self.filename, 13 if is_old else 33)
        bytes.store_string(self.action, 20 if is_old else 34)
        if is_old: bytes.store_8s(0, 3) # unused
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
            bytes.store_8s(0, 33) # unused

        return bytes

    def is_old(self):
        return \
            self.albedo == 50.0 and \
            self.path == 0 and \
            self.entity2 == 0 and \
            self.material == "ndef" and \
            self.string1 == "" and \
            self.string2 == "" and \
            len(self.filename) <= 13 and \
            len(self.action) <= 20 and \
            self.is_skills_old()

    def is_skills_old(self):
        for i in range(8, min(len(self.skills), 20)):
            if self.skills[i] != 0.0:
                return False
        return True

class PogoSpawn(WMBEntity):
    def __init__(self, obj):
        self.type = 7 # 7 is the ID for entity types
        self.origin = obj.location
        self.angle = (0,0,0)
        self.scale = (1,1,1)
        self.name = "spawn1"
        self.filename = ""
        self.action = "spawn_act"
        self.skills = []
        self.flags = 1 << 8 | 1 << 17 | 1 << 9 # invisible, unlit and passable
        self.ambient = 0
        self.albedo = 50.0
        self.path = 0
        self.entity2 = 0
        self.material = "ndef"
        self.string1 = ""
        self.string2 = ""

class PogoStartLine(WMBEntity):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = "startLine"
        self.action = "skillset_act"
        self.flags |= 1 << 0 # flag_1
        self.skills = [1.0]
