import bpy
import os
import json

def register():
    bpy.utils.register_class(PogoEntity)
    bpy.types.Object.pogo_entity = bpy.props.PointerProperty(type=PogoEntity)
    bpy.utils.register_class(PogoCustomMap)
    bpy.types.Collection.custom_map = bpy.props.PointerProperty(type=PogoCustomMap)

def unregister():
    bpy.utils.unregister_class(PogoEntity)
    del bpy.types.Object.pogo_entity
    bpy.utils.unregister_class(PogoCustomMap)
    del bpy.types.Collection.custom_map

class PogoCustomMap(bpy.types.PropertyGroup):
    map_name: bpy.props.StringProperty(name="Map Name")
    map_image: bpy.props.StringProperty(name="Map Image")

    spawn: bpy.props.PointerProperty(type=bpy.types.Object, name="Spawn", poll=lambda prop, obj: obj.type == 'EMPTY')
    path_progress: bpy.props.PointerProperty(type=bpy.types.Object, name="Progress Path", poll=lambda prop, obj: obj.type == 'CURVE')
    start_line: bpy.props.PointerProperty(type=bpy.types.Object, name="Start Line", poll=lambda prop, obj: obj.type == 'MESH')

class PogoEntity(bpy.types.PropertyGroup):
    material: bpy.props.EnumProperty(items=[
        ("ndef", "", ""),
        ("appAGeoDefault_mat", "appAGeoDefault_mat", ""), # albedo changes greyscale of object, 50 albedo is 50% greyscale. 100 albedo is no greyscale
        ("appAGeoXRay_mat", "appAGeoXRay_mat", ""),
        ("anvil_mat", "anvil_mat", ""),
        ("mat_bug", "mat_bug", ""), # similar to traffic cone
        ("characterSimple_mat", "characterSimple_mat", ""),
        ("cloud_mat", "cloud_mat", ""),
        ("coconut_mat", "coconut_mat", ""),
        ("cmFruitTex_mat", "cmFruitTex_mat", ""), # this is the same material as map3FruitTex_mat, except that texture coordinates are not mirrored when they leave the 0..1 square area
        ("egg_mat", "egg_mat", ""),
        ("fruit_mat", "fruit_mat", ""), # map 1 main material, uses gradientTest mostly
        ("fruitTex_mat", "fruitTex_mat", ""), # map 1 main material but uses custom textures, such as for the red mushrooms
        ("iceSnow_mat", "iceSnow_mat", ""), 
        ("map3Carrots_mat", "map3Carrots_mat", ""), 
        ("map3Chain_mat", "map3Chain_mat", ""), 
        ("map3ClothBee_mat", "map3ClothBee_mat", ""), 
        ("map3Eggplants_mat", "map3Eggplants_mat", ""), 
        ("map3FruitDefault_mat", "map3FruitDefault_mat", ""), # see map 1 notes
        ("map3FruitTex_mat", "map3FruitTex_mat", ""), 
        ("map3GoldSlime_mat", "map3GoldSlime_mat", ""), 
        ("mymetal_mat", "mymetal_mat", ""),
        ("monoSpikes_mat", "monoSpikes_mat", ""),
        ("monoWheel_mat", "monoWheel_mat", ""),
        ("mountain_mat", "mountain_mat", ""),
        ("pencil_mat", "pencil_mat", ""),
        ("pinkSap_mat", "pinkSap_mat", ""),
        ("pogostick_mat", "pogostick_mat", ""),
        ("pogostickGold_mat", "pogostickGold_mat", ""),
        ("slime_mat", "slime_mat", ""), 
        ("toggleBlock_mat", "toggleBlock_mat", ""), 
        ("mat_trafficCone", "mat_trafficCone", ""), 
        ("mat_ushanka", "mat_ushanka", ""),
        ("viking_mat", "viking_mat", ""),
        ("wood_mat", "wood_mat", ""),
        ("cmNormalmapping", "cmNormalmapping", ""),
        ("cmUnlit", "cmUnlit", ""),
        ("cmPixelated", "cmPixelated", ""),
    ], name="Material", default="ndef")

    flag_invisible: bpy.props.BoolProperty(name="Invisble") # = 8,
    flag_passable: bpy.props.BoolProperty(name="Passable") # = 9,
    flag_transparent: bpy.props.BoolProperty(name="Transparent") # = 10,
    flag_unlit: bpy.props.BoolProperty(name="Unlit") # = 17,
    flag_shadow: bpy.props.BoolProperty(name="Shadow") # = 18, # 
    flag_metal: bpy.props.BoolProperty(name="Kill") # = 22, # kill
    flag_cast: bpy.props.BoolProperty(name="Cast") # = 23, # 
    flag_polygon: bpy.props.BoolProperty(name="Collision") # = 26, # collision. if polygon isn't set then its passable
    ambient: bpy.props.FloatProperty(name="Ambient")
    albedo: bpy.props.FloatProperty(name="Albedo", default=50.0)

    action_enums = [("ndef", "", "")]
    with open(os.path.join(os.path.dirname(__file__), "actions.json"), 'r') as f_in: 
        actions = json.load(f_in)
        for action, config in actions.items():
            if "disable" in config and config["disable"] == True: continue
            action_enums.append((action, config["name"] if "name" in config else action, config["description"] if "description" in config else ""))
    action: bpy.props.EnumProperty(items=action_enums,name="Action", default="ndef")

    flag_1: bpy.props.BoolProperty(name="flag_1") # = 0,
    flag_2: bpy.props.BoolProperty(name="flag_2") # = 1,
    flag_3: bpy.props.BoolProperty(name="flag_3") # = 2,
    flag_4: bpy.props.BoolProperty(name="flag_4") # = 3,
    flag_5: bpy.props.BoolProperty(name="flag_5") # = 4,
    flag_6: bpy.props.BoolProperty(name="flag_6") # = 5,
    flag_7: bpy.props.BoolProperty(name="Ice") # = 6, # ICE
    flag_8: bpy.props.BoolProperty(name="flag_8") # = 7,

    flag_auto_collision: bpy.props.BoolProperty(name="Auto Collision")

    path: bpy.props.PointerProperty(type=bpy.types.Curve, name="Path")

    skill_1: bpy.props.FloatProperty(name="skill_1")
    skill_2: bpy.props.FloatProperty(name="skill_2")
    skill_3: bpy.props.FloatProperty(name="skill_3")
    skill_4: bpy.props.FloatProperty(name="skill_4")
    skill_5: bpy.props.FloatProperty(name="skill_5")
    skill_6: bpy.props.FloatProperty(name="skill_6")
    skill_7: bpy.props.FloatProperty(name="skill_7")
    skill_8: bpy.props.FloatProperty(name="skill_8")
    skill_9: bpy.props.FloatProperty(name="skill_9")
    skill_10: bpy.props.FloatProperty(name="skill_10")
    skill_11: bpy.props.FloatProperty(name="skill_11")
    skill_12: bpy.props.FloatProperty(name="skill_12")
    skill_13: bpy.props.FloatProperty(name="skill_13")
    skill_14: bpy.props.FloatProperty(name="skill_14")
    skill_15: bpy.props.FloatProperty(name="skill_15")
    skill_16: bpy.props.FloatProperty(name="skill_16")
    skill_17: bpy.props.FloatProperty(name="skill_17")
    skill_18: bpy.props.FloatProperty(name="skill_18")
    skill_19: bpy.props.FloatProperty(name="skill_19")
    skill_20: bpy.props.FloatProperty(name="skill_20")

class PogoPath(bpy.types.PropertyGroup):
    pass

class PogoArea(bpy.types.PropertyGroup):
    area_type: bpy.props.EnumProperty(["KILL", "CHECKPOINT", "MODE_DOUBLE", "MODE_PUZZLE", "MODE_NOBONK", "MODE_NOBOOST", "GRAVITY"])
