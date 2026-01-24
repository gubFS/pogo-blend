import bpy

from .. import pogo_blend_utils as pbu


class PogoRegion(bpy.types.PropertyGroup):
    region_types = [("ndef", "", "No region type", 0)]
    region_types.extend(pbu.get_enum_list("pogo_classes/region_types.yaml", True))

    def update_region_type(self, context):
        custom_map = pbu.get_custom_map()
        custom_map.update_splits()

    region_type: bpy.props.EnumProperty(items=region_types, name="Region Type", update=update_region_type)

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
