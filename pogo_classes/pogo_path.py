import bpy


class PogoPath(bpy.types.PropertyGroup):
    pass


classes = (PogoPath,)


def register():
    bpy.types.Object.pogo_path = bpy.props.PointerProperty(type=PogoPath)


def unregister():
    del bpy.types.Object.pogo_path
