import bpy

def register():
    bpy.utils.register_class(PogoPath)
    bpy.types.Object.pogo_path = bpy.props.PointerProperty(type=PogoPath)

def unregister():
    bpy.utils.unregister_class(PogoPath)
    del bpy.types.Object.pogo_path

class PogoPath(bpy.types.PropertyGroup):
    pass
