import bpy

from ... import pogo_blend_utils as pbu


def redraw_properties():
    for area in [area for area in bpy.context.screen.areas if area.type == 'PROPERTIES']:
        area.tag_redraw()


class ApplyIcePreset(pbu.AltOperator):
    bl_idname = "pogo_blend.apply_ice_preset"
    bl_label = "Ice"
    bl_description = "Ice preset"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_entity" in obj

    def execute_obj(self, obj):
        entity = obj.pogo_entity
        entity.material = "iceSnow_mat"
        entity.flag_polygon = True
        entity.flag_7 = True
        entity.flag_metal = False
        entity.flag_8 = False
        entity.action2 = "ndef"
        entity.action1 = "ndef"

    def post_execute(self):
        redraw_properties()


class ApplySapPreset(pbu.AltOperator):
    bl_idname = "pogo_blend.apply_sap_preset"
    bl_label = "Sap"
    bl_description = "Sap preset"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_entity" in obj

    def execute_obj(self, obj):
        entity = obj.pogo_entity
        entity.material = "slime_mat"
        entity.flag_polygon = True
        entity.flag_metal = False
        entity.flag_7 = False
        entity.flag_8 = False
        entity.action2 = "ndef"
        entity.action1 = "slime_act"

    def post_execute(self):
        redraw_properties()


class ApplyPinkSapPreset(pbu.AltOperator):
    bl_idname = "pogo_blend.apply_pink_sap_preset"
    bl_label = "Pink Sap"
    bl_description = "Pink Sap preset"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_entity" in obj

    def execute_obj(self, obj):
        entity = obj.pogo_entity
        entity.material = "pinkSap_mat"
        entity.flag_polygon = True
        entity.flag_metal = False
        entity.flag_7 = False
        entity.flag_8 = False
        entity.action2 = "ndef"
        entity.action1 = "pinkSap_act"

    def post_execute(self):
        redraw_properties()


class ApplyBoostJuicePreset(pbu.AltOperator):
    bl_idname = "pogo_blend.apply_boost_juice_preset"
    bl_label = "Boost Juice"
    bl_description = "Boost Juice preset"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_entity" in obj

    def execute_obj(self, obj):
        entity = obj.pogo_entity
        entity.material = "map3GoldSlime_mat"
        entity.flag_polygon = True
        entity.flag_metal = False
        entity.flag_7 = False
        entity.flag_8 = False
        entity.action2 = "ndef"
        entity.action1 = "boostjuice_act"

    def post_execute(self):
        redraw_properties()


class ApplyBackgroundPreset(pbu.AltOperator):
    bl_idname = "pogo_blend.apply_background_preset"
    bl_label = "Background"
    bl_description = "Background preset"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return "pogo_entity" in obj

    def execute_obj(self, obj):
        entity = obj.pogo_entity
        entity.flag_polygon = False
        entity.flag_metal = False
        entity.flag_7 = False
        entity.flag_8 = False
        entity.action2 = "ndef"
        entity.action1 = "bgObject_act"

    def post_execute(self):
        redraw_properties()


def register():
    bpy.utils.register_class(ApplyIcePreset)
    bpy.utils.register_class(ApplySapPreset)
    bpy.utils.register_class(ApplyPinkSapPreset)
    bpy.utils.register_class(ApplyBoostJuicePreset)
    bpy.utils.register_class(ApplyBackgroundPreset)


def unregister():
    bpy.utils.unregister_class(ApplyIcePreset)
    bpy.utils.unregister_class(ApplySapPreset)
    bpy.utils.unregister_class(ApplyPinkSapPreset)
    bpy.utils.unregister_class(ApplyBoostJuicePreset)
    bpy.utils.unregister_class(ApplyBackgroundPreset)
