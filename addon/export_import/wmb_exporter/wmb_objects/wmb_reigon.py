import bpy
from mathutils import Vector

from ...gub_byte_array import GubByteArray


class WMBReigon:
    def __init__(self, obj):
        self.type = 8  # 8 is the ID of the type for reigons

        self.name = obj.pogo_reigon.reigon_type
        match obj.pogo_reigon.reigon_type:
            case "gravityReg_":
                self.name += str(int(obj.pogo_reigon.gravity_angle))
                self.name += "_" + str(int(obj.pogo_reigon.gravity_power))

        self.min_pos = Vector((-1, -1, -1))
        self.max_pos = Vector((1, 1, 1))

        self.min_pos *= obj.matrix_world.to_scale().to_3d() * obj.empty_display_size
        self.max_pos *= obj.matrix_world.to_scale().to_3d() * obj.empty_display_size

        self.min_pos += obj.matrix_world.translation
        self.max_pos += obj.matrix_world.translation

        match obj.pogo_reigon.reigon_type:
            case (
                "modearea_double"
                | "modearea_puzzle"
                | "modearea_nobonk"
                | "moearea_noboost"
            ):
                self.min_pos.y = -384
                self.max_pos.y = -256
            case "kill" | "reg_finish" | "gravityReg_" | "gravityCircle":
                self.min_pos.y = -64
                self.max_pos.y = 64
            case "CP_":
                self.min_pos.y = 256
                self.max_pos.y = 384

    def to_bytes(self) -> GubByteArray:
        bytes = GubByteArray()

        bytes.store_32(self.type)
        bytes.store_vec3f(self.min_pos)
        bytes.store_vec3f(self.max_pos)
        bytes.store_8s(0, 8)  # unused... i think
        bytes.store_string(self.name, 20)

        return bytes
