import bpy

from ... import pogo_blend_utils as pbu


class AddPogoEdgeSplit(pbu.AltOperator):
    bl_idname = "pogo_blend.add_pogo_edge_split"
    bl_label = "Add Pogo Edge Split"
    bl_description = "Adds a Edge Split modifier that will make edges sharper in-game"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return obj.type == 'MESH'

    def execute_obj(self, obj):
        self.add_edge_split(obj)

    @classmethod
    def add_edge_split(cls, obj):
        mod = obj.modifiers.new("Edge Split", 'EDGE_SPLIT')
        mod.split_angle = 0.0


class AddPogoBevel(pbu.AltOperator):
    bl_idname = "pogo_blend.add_pogo_bevel"
    bl_label = "Add Pogo Bevel"
    bl_description = "Adds a Bevel modifier that will make sharp edges appears softer in-game"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return obj.type == 'MESH'

    def execute_obj(self, obj):
        self.add_bevel(obj)

    @classmethod
    def add_bevel(cls, obj):
        mod = obj.modifiers.new("Bevel", 'BEVEL')
        mod.width = 0.006
        mod.segments = 2
        mod.limit_method = 'NONE'


class AddPogoBevelEdgeSplit(pbu.AltOperator):
    bl_idname = "pogo_blend.add_pogo_bevel_edge_split"
    bl_label = "Add Pogo Bevel & Edge Split"
    bl_description = "Adds a Bevel and Edge Split modifier that will make soft edges in-game"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return obj.type == 'MESH'

    def execute_obj(self, obj):
        AddPogoBevel.add_bevel(obj)
        AddPogoEdgeSplit.add_edge_split(obj)


def register():
    bpy.utils.register_class(AddPogoEdgeSplit)
    bpy.utils.register_class(AddPogoBevel)
    bpy.utils.register_class(AddPogoBevelEdgeSplit)


def unregister():
    bpy.utils.unregister_class(AddPogoEdgeSplit)
    bpy.utils.unregister_class(AddPogoBevel)
    bpy.utils.unregister_class(AddPogoBevelEdgeSplit)
