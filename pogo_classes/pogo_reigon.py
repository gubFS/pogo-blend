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
            ("kill", "Kill", ""), 
            ("CP_", "Checkpoint", ""), 
            ("mode_double", "Double jump", ""), 
            ("mode_puzzle", "Puzzle", ""),
            ("mode_nobonk", "No bonk", ""),
            ("mode_noboost", "No boost", ""),
            ("gravity", "Gravity", ""),
            ("reg_finish", "Finish", "")
        ],
        name="Reigon Type"
    )
