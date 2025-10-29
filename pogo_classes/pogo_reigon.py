import bpy

def register():
    bpy.utils.register_class(PogoReigon)
    bpy.types.Object.pogo_reigon = bpy.props.PointerProperty(type=PogoReigon)

def unregister():
    bpy.utils.unregister_class(PogoReigon)
    del bpy.types.Object.pogo_reigon

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
            ("reg_finish", "Finish", "")
        ]

    def update_reigon_type(self, context):
        obj = context.object
        new_type = obj.pogo_reigon.reigon_type
        custom_map_collection = bpy.data.collections["CustomMap"]
        custom_map = custom_map_collection.custom_map

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
        items=reigon_types,
        name="Reigon Type",
        update=update_reigon_type
    )

    gravity_angle: bpy.props.FloatProperty(name="Gravity angle", update=update_reigon_type) # 90 is -x 180 is +z
    gravity_power: bpy.props.FloatProperty(name="Gravity power", default=100.0)
