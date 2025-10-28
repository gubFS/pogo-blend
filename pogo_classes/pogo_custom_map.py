import bpy

def register():
    bpy.utils.register_class(PogoCustomMap)
    bpy.types.Collection.custom_map = bpy.props.PointerProperty(type=PogoCustomMap)

def unregister():
    bpy.utils.unregister_class(PogoCustomMap)
    del bpy.types.Collection.custom_map

class PogoCustomMap(bpy.types.PropertyGroup):
    map_name: bpy.props.StringProperty(name="Map Name")
    map_image: bpy.props.StringProperty(name="Map Image")

    spawn: bpy.props.PointerProperty(type=bpy.types.Object, name="Spawn", poll=lambda prop, obj: obj.type == 'EMPTY')
    path_progress: bpy.props.PointerProperty(type=bpy.types.Object, name="Progress Path", poll=lambda prop, obj: obj.type == 'CURVE')
    start_line: bpy.props.PointerProperty(type=bpy.types.Object, name="Start Line", poll=lambda prop, obj: obj.type == 'MESH')
