import bpy

def register():
    bpy.utils.register_class(PogoEntity)
    bpy.types.Object.pogo_entity = bpy.props.PointerProperty(type=PogoEntity)

def unregister():
    bpy.utils.unregister_class(PogoEntity)
    del bpy.types.Object.pogo_entity

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

    action_config = {
        "mushroom_act": {
            "flags": [
                {
                    "identifier": "flag_5",
                    "name": "bounce_light",
                    "default": False,
                },
            ],
            "skills": [ ],
        },
        "mushroomFullObj_act": {
            "flags": [ ],
            "skills": [ ]
        },
        "execString12acts": {
            "disable": True,
            "flags": [ ],
            "skills": [ ]
        },
        "skillset_act": {
            "flags": [ ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "vecsk41",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "vecsk42",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "vecsk43",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_4",
                    "name": "vecsk44",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_5",
                    "name": "greyScale",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_6",
                    "name": "vecsk46",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_7",
                    "name": "vecsk47",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_8",
                    "name": "vecsk48",
                    "default": 0.0,
                },
            ]
        },
        "slime_act": {
            "flags": [ ],
            "skills": [ ]
        },
        "POI_act": {
            "flags": [
                {
                    "identifier": "flag_6",
                    "name": "scary",
                    "default": False,
                },
                {
                    "identifier": "flag_7",
                    "name": "mega",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "vecsk41",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "vecsk42",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "vecsk43",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_4",
                    "name": "vecsk44",
                    "default": 0.0,
                },
            ]
        },
        "monolithThorn_act": {
            "flags": [ ],
            "skills": [ ],
            "path": True
        },
        "coconutSlippery": {
            "flags": [ ],
            "skills": [ ]
        },
        "pinkSap_act": {
            "flags": [ ],
            "skills": [ ]
        },
        "boostjuice_act": {
            "flags": [ ],
            "skills": [ ]
        },
        "map3Wheel_act": {
            "flags": [
                {
                    "identifier": "flag_3",
                    "name": "continuousRotation",
                    "default": False,
                },
                {
                    "identifier": "flag_4",
                    "name": "sine_Rotation",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "rotateSpeed",
                    "default": 1.5,
                },
                {
                    "identifier": "skill_2",
                    "name": "sine_base",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "sine_amount",
                    "default": 45.0,
                },
            ]
        },
        "moveSine_act": {
            "flags": [
                {
                    "identifier": "flag_3",
                    "name": "y_changesAmbient",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "x_dist",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "z_dist",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "x_speedfac",
                    "default": 5.0,
                },
                {
                    "identifier": "skill_4",
                    "name": "z_speedfac",
                    "default": 5.0,
                },
                {
                    "identifier": "skill_5",
                    "name": "x_AngOffset",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_6",
                    "name": "z_AngOffset",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_7",
                    "name": "y_dist",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_8",
                    "name": "y_speedfac",
                    "default": 5.0,
                },
                {
                    "identifier": "skill_9",
                    "name": "y_AngOffset",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_11",
                    "name": "y_ambientEffect",
                    "default": 0.25,
                },
            ]
        },
        "moveLoop_act": {
            "flags": [ ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "x_dist",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "z_dist",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "speedfac",
                    "default": 5.0,
                },
                {
                    "identifier": "skill_5",
                    "name": "angOffset",
                    "default": 0.0,
                },
            ]
        },
        "toggleBlock_act": {
            "flags": [
                {
                    "identifier": "flag_3",
                    "name": "boost_toggle",
                    "default": False,
                },
                {
                    "identifier": "flag_4",
                    "name": "group_2",
                    "default": False,
                },
                {
                    "identifier": "flag_5",
                    "name": "turn_invisible",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "redBlueTintFac",
                    "default": 1.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "dither_scale",
                    "default": 1.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "dither_fac",
                    "default": 0.65,
                },
            ]
        },
        "customMapSetup_act": {
            "disable": True,
            "flags": [
                {
                    "identifier": "flag_3",
                    "name": "double_jump",
                    "default": False,
                },
                {
                    "identifier": "flag_4",
                    "name": "puzzle",
                    "default": False,
                },
                {
                    "identifier": "flag_5",
                    "name": "no_boost",
                    "default": False,
                },
                {
                    "identifier": "flag_6",
                    "name": "bonk_explode",
                    "default": False,
                },
                {
                    "identifier": "flag_7",
                    "name": "mushroom_power",
                    "default": False,
                },
                {
                    "identifier": "flag_8",
                    "name": "iceMode",
                    "default": False,
                },
            ],
            "skills": [ ]
        },
        "toggleSine_act": {
            "flags": [
                {
                    "identifier": "flag_3",
                    "name": "turn_background",
                    "default": False,
                },
                {
                    "identifier": "flag_5",
                    "name": "turn_invisible",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "speedFac",
                    "default": 5.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "offset",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "ambient_shift",
                    "default": -35.0,
                },
            ]
        },
        "bgObject_act": {
            "flags": [
                {
                    "identifier": "flag_6",
                    "name": "bottom_z",
                    "default": False,
                },
                {
                    "identifier": "flag_7",
                    "name": "fixed_x",
                    "default": False,
                },
                {
                    "identifier": "flag_8",
                    "name": "fixed_z",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "fac_x",
                    "default": 1.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "fac_z",
                    "default": 1.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "greyScale",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_5",
                    "name": "skill43",
                    "default": 0.0,
                },
            ]
        },
        "runStateToggle": {
            "flags": [
                {
                    "identifier": "flag_3",
                    "name": "show_start",
                    "default": False,
                },
                {
                    "identifier": "flag_4",
                    "name": "show_sun",
                    "default": False,
                },
                {
                    "identifier": "flag_5",
                    "name": "show_end",
                    "default": False,
                },
                {
                    "identifier": "flag_6",
                    "name": "turn_passable",
                    "default": False,
                },
                {
                    "identifier": "flag_7",
                    "name": "fade_scale",
                    "default": False,
                },
            ],
            "skills": [
                {
                    "identifier": "skill_1",
                    "name": "fade_speed",
                    "default": 10.0,
                },
                {
                    "identifier": "skill_2",
                    "name": "dofade_sk41",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_3",
                    "name": "dofade_alpha",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_4",
                    "name": "dosmoothstep",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_5",
                    "name": "doovershoot",
                    "default": 0.0,
                },
                {
                    "identifier": "skill_6",
                    "name": "overshoot_fac",
                    "default": 1.35,
                },
            ]
        }
    }

    actions = [("ndef", "", "")]
    for action, config in action_config.items():
        if "disable" in config and config["disable"] == True: continue
        actions.append((action, config["name"] if "name" in config else action, config["description"] if "description" in config else ""))
    action: bpy.props.EnumProperty(items=actions,name="Action", default="ndef")

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
