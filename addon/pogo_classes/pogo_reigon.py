import bpy

from .. import pogo_blend_utils as pbu


class PogoReigon(bpy.types.PropertyGroup):
    reigon_types = [
        ("ndef", "", ""),
        ("kill", "Kill", ""),
        ("CP_", "Checkpoint", ""),
        ("modearea_double", "Double jump", ""),
        ("modearea_puzzle", "Puzzle", ""),
        ("modearea_nobonk", "No bonk", ""),
        ("modearea_noboost", "No boost", ""),
        ("gravityReg_", "Gravity", ""),
        ("reg_finish", "Finish", ""),
    ]

    def update_reigon_type(self, context):
        obj = context.object
        new_type = obj.pogo_reigon.reigon_type
        custom_map_collection = pbu.get_custom_map_collection()
        custom_map = pbu.get_custom_map()

        splits = {}
        for i, split in enumerate(custom_map.splits.values()):
            splits[split.split_reigon] = i

        if new_type == "CP_":
            if obj not in splits:
                split = custom_map.splits.add()
                split.split_reigon = obj
        else:
            if obj in splits:
                split = custom_map.splits.remove(splits[obj])

    reigon_type: bpy.props.EnumProperty(
        items=reigon_types, name="Reigon Type", update=update_reigon_type
    )

    def update_gravity_angle(self, context):
        if self.gravity_angle < 0 or self.gravity_angle >= 360:
            self.gravity_angle = self.gravity_angle % 360

    gravity_angle: bpy.props.IntProperty(
        name="Gravity angle", update=update_gravity_angle
    )  # 90 is -x 180 is +z
    gravity_power: bpy.props.IntProperty(
        name="Gravity power", default=100, min=0, max=999
    )


def register():
    bpy.utils.register_class(PogoReigon)
    bpy.types.Object.pogo_reigon = bpy.props.PointerProperty(type=PogoReigon)


def unregister():
    bpy.utils.unregister_class(PogoReigon)
    del bpy.types.Object.pogo_reigon
