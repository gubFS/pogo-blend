import bpy

class WMBEntity(bpy.types.PropertyGroup):
    action: bpy.props.StringProperty(name="Action")
    #skills: bpy
    FLAG1: bpy.props.BoolProperty(name="FLAG1") # = 0,
    FLAG2: bpy.props.BoolProperty(name="FLAG2") # = 1,
    FLAG3: bpy.props.BoolProperty(name="FLAG3") # = 2,
    FLAG4: bpy.props.BoolProperty(name="FLAG4") # = 3,
    FLAG5: bpy.props.BoolProperty(name="FLAG5") # = 4,
    FLAG6: bpy.props.BoolProperty(name="FLAG6") # = 5,
    FLAG7: bpy.props.BoolProperty(name="FLAG7") # = 6, # ICE
    FLAG8: bpy.props.BoolProperty(name="FLAG8") # = 7,
    INVISIBLE: bpy.props.BoolProperty(name="INVISIBLE") # = 8,
    PASSABLE: bpy.props.BoolProperty(name="PASSABLE") # = 9,
    TRANSPARENT: bpy.props.BoolProperty(name="TRANSPARENT") # = 10,
    UNLIT: bpy.props.BoolProperty(name="UNLIT") # = 17,
    SHADOW: bpy.props.BoolProperty(name="SHADOW") # = 18, # 
    METAL: bpy.props.BoolProperty(name="METAL") # = 22, # kill
    CAST: bpy.props.BoolProperty(name="CAST") # = 23, # 
    POLYGON: bpy.props.BoolProperty(name="POLYGON") # = 26, # collision. if polygon isn't set then its passable
    ambient: bpy.props.FloatProperty(name="Ambient")
    albedo: bpy.props.FloatProperty(name="Albedo")
    material: bpy.props.StringProperty(name="Material")
