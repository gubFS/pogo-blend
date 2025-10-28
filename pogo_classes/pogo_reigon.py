import bpy

def register():
    bpy.utils.register_class(PogoReigon)
    bpy.types.Object.pogo_reigon = bpy.props.PointerProperty(type=PogoReigon)

def unregister():
    bpy.utils.unregister_class(PogoReigon)
    del bpy.types.Object.pogo_reigon

class PogoReigon(bpy.types.PropertyGroup):
    reigon_type: bpy.props.EnumProperty(
        items=[
            ("ndef", "", ""),
            ("kill", "Kill", ""), 
            ("CP_", "Checkpoint", ""), 
            ("modearea_double", "Double jump", ""), 
            ("modearea_puzzle", "Puzzle", ""),
            ("modearea_nobonk", "No bonk", ""),
            ("modearea_noboost", "No boost", ""),
            ("gravityReg_", "Gravity", ""),
            ("reg_finish", "Finish", "")
        ],
        name="Reigon Type"
    )

    gravity_angle: bpy.props.FloatProperty(name="Gravity angle") # 90 is -x 180 is +z
    gravity_power: bpy.props.FloatProperty(name="Gravity power", default=100.0)
