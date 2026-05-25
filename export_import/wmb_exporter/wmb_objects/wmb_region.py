# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

from mathutils import Vector

from ...gub_byte_array import GubByteArray


class WMBRegion:
    def __init__(self, obj, scale: float = 50.0):
        self.type = 8  # 8 is the ID of the type for regions

        region = obj.pogo_region

        if region.region_type != "ndef":
            self.name = region.region_type
            match region.region_type:
                case "gravityReg_":
                    self.name += str(int(region.gravity_angle))
                    self.name += "_" + str(int(region.gravity_power))
        elif region.name_override == "":
            self.name = obj.name
        else:
            self.name = region.name_override

        self.min_pos = Vector((-1, -1, -1))
        self.max_pos = Vector((1, 1, 1))

        self.min_pos *= obj.matrix_world.to_scale().to_3d() * obj.empty_display_size * scale
        self.max_pos *= obj.matrix_world.to_scale().to_3d() * obj.empty_display_size * scale

        self.min_pos += obj.matrix_world.translation * scale
        self.max_pos += obj.matrix_world.translation * scale

        self.min_pos.y = region.get_min_y()
        self.max_pos.y = region.get_max_y()

    def to_bytes(self) -> GubByteArray:
        bytes = GubByteArray()

        bytes.store_32(self.type)
        bytes.store_vec3f(self.min_pos)
        bytes.store_vec3f(self.max_pos)
        bytes.store_8s(0, 8)  # unused... i think
        bytes.store_string(self.name, 20)

        return bytes
