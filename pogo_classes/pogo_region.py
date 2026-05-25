# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

from .. import pogo_blend_utils as pbu


class PogoRegion(bpy.types.PropertyGroup):
    region_types = [("ndef", "", "No region type", 0)]
    region_types.extend(pbu.get_enum_list("pogo_classes/region_types.yaml", True))

    regions = pbu.parse_yaml("pogo_classes/region_types.yaml")

    def update_region_type(self, context):
        custom_map = pbu.get_custom_map()
        custom_map.update_splits()

    region_type: bpy.props.EnumProperty(items=region_types, name="Region Type", update=update_region_type)
    name_override: bpy.props.StringProperty(default="")

    def get_min_y(self):
        if self.region_type == "ndef":
            return self.min_y_override
        config = self.regions[self.region_type]
        if config is None or "min_y" not in config:
            return self.min_y_override
        return config["min_y"]

    def get_max_y(self):
        if self.region_type == "ndef":
            return self.max_y_override
        config = self.regions[self.region_type]
        if config is None or "max_y" not in config:
            return self.max_y_override
        return config["max_y"]

    min_y_override: bpy.props.FloatProperty(default=0.0)
    max_y_override: bpy.props.FloatProperty(default=0.0)

    def update_gravity_angle(self, context):
        if self.gravity_angle < 0 or self.gravity_angle >= 360:
            self.gravity_angle = self.gravity_angle % 360

    gravity_angle: bpy.props.IntProperty(name="Gravity angle", update=update_gravity_angle)  # 90 is -x 180 is +z
    gravity_power: bpy.props.IntProperty(name="Gravity power", default=100, min=0, max=999)


classes = (PogoRegion,)


def register():
    bpy.types.Object.pogo_region = bpy.props.PointerProperty(type=PogoRegion)


def unregister():
    del bpy.types.Object.pogo_region
