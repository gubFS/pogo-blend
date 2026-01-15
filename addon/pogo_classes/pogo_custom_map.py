import bpy

from .. import pogo_blend_utils as pbu


class PogoSplit(bpy.types.PropertyGroup):
    split_region: bpy.props.PointerProperty(type=bpy.types.Object)


class ActiveSplitMove(bpy.types.Operator):
    bl_idname = "pogo_blend.active_split_move"
    bl_label = "Move active split"
    bl_description = "Moves the selected split"

    direction: bpy.props.StringProperty()

    def execute(self, context):
        custom_map = pbu.get_custom_map()
        current_idx = custom_map.active_split_idx

        new_idx = current_idx
        if self.direction == 'DOWN':
            new_idx = min(current_idx + 1, len(custom_map.splits) - 1)
        elif self.direction == 'UP':
            new_idx = max(current_idx - 1, 0)
        custom_map.splits.move(current_idx, new_idx)
        custom_map.active_split_idx = new_idx

        return {'FINISHED'}


class PogoCustomMap(bpy.types.PropertyGroup):
    map_name: bpy.props.StringProperty(name="Map Name", description="The name of the map")
    map_image: bpy.props.StringProperty(name="Map Image", description="The path to the image used for the map")

    splits: bpy.props.CollectionProperty(type=PogoSplit, name="Splits")
    active_split_idx: bpy.props.IntProperty(name="Active Split")

    def update_splits(self):
        custom_map_collection = pbu.get_custom_map_collection()
        actual_splits_set = set([obj for obj in custom_map_collection.all_objects if "pogo_region" in obj and obj.pogo_region.region_type == "CP_"])
        splits_set = set([split.split_region for split in self.splits])
        splits_to_remove = splits_set.difference(actual_splits_set)
        splits_to_add = actual_splits_set.difference(splits_set)
        for split in splits_to_remove:
            idx = -1
            for i, splt in enumerate(self.splits):
                if splt.split_region == split:
                    idx = i
                    break
            if idx != -1:
                self.splits.remove(idx)
        for split in splits_to_add:
            added_split = self.splits.add()
            added_split.split_region = split

    spawn: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Spawn",
        description="The location where the player will spawn",
        poll=lambda prop, obj: obj.type == 'EMPTY',
    )

    path_progress: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Progress Path",
        description="The path used to track progress through the map. Determines the percentage completion",
        poll=lambda prop, obj: "pogo_path" in obj,
    )
    start_line: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Start Line",
        description="The start line. This entity will dissapear once the run is started",
        poll=lambda prop, obj: "pogo_entity" in obj,
    )

    double_jump: bpy.props.BoolProperty(name="Double Jump", description="Enable Double Jump mode")
    puzzle: bpy.props.BoolProperty(name="Puzzle", description="Enable Puzzle mode")
    no_boost: bpy.props.BoolProperty(name="No boost", description="Enable No Boost mode")
    no_bonk: bpy.props.BoolProperty(name="No bonk", description="Enable No Bonk mode. The player will die when bonking on anything")
    mushroom_power: bpy.props.BoolProperty(
        name="Mushroom power",
        description="Enables mushrooms to have a bounce power. I don't know why you would turn this off...",
        default=True,
    )
    ice: bpy.props.BoolProperty(name="Ice", description="Enable Ice mode")


def register():
    bpy.utils.register_class(PogoSplit)
    bpy.utils.register_class(PogoCustomMap)
    bpy.utils.register_class(ActiveSplitMove)
    bpy.types.Collection.custom_map = bpy.props.PointerProperty(type=PogoCustomMap)


def unregister():
    bpy.utils.unregister_class(PogoSplit)
    bpy.utils.unregister_class(PogoCustomMap)
    bpy.utils.unregister_class(ActiveSplitMove)
    del bpy.types.Collection.custom_map
