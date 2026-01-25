# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

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


class StaticFile(bpy.types.PropertyGroup):
    filepath: bpy.props.StringProperty()


class StaticFileAdd(bpy.types.Operator):
    bl_idname = "pogo_blend.static_file_add"
    bl_label = "Add Static File"
    bl_description = "Adds the selected Static Files"

    allowed_formats: list[str] = ["mdl", "tga", "png", "jpg", "jpeg", "txt", "blend", "fx"]

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')
    files: bpy.props.CollectionProperty(type=bpy.types.OperatorFileListElement)

    filter_glob: bpy.props.StringProperty(default=''.join(f"*.{format};" for format in allowed_formats), options={'HIDDEN'})

    def execute(self, context):
        custom_map = pbu.get_custom_map()
        dirpath = Path(self.filepath).parent
        current_statics = set(static.filepath for static in custom_map.static_files)

        for file in self.files:
            abs_path = Path(dirpath).joinpath(file.name).absolute()
            if not Path(abs_path).exists():
                continue
            if file.name.split(".")[-1] not in self.allowed_formats:
                continue

            rel_path = bpy.path.relpath(str(abs_path))
            if rel_path in current_statics:
                continue

            new_file = custom_map.static_files.add()
            new_file.filepath = rel_path

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class StaticFileRemove(bpy.types.Operator):
    bl_idname = "pogo_blend.static_file_remove"
    bl_label = "Removes Static File"
    bl_description = "Remove the active Static File"

    @classmethod
    def poll(cls, context):
        custom_map = pbu.get_custom_map()
        current_idx = custom_map.active_static_file_idx
        return current_idx < len(custom_map.static_files) and current_idx >= 0

    def execute(self, context):
        custom_map = pbu.get_custom_map()
        current_idx = custom_map.active_static_file_idx

        if self.poll(context):
            custom_map.static_files.remove(current_idx)

        return {'FINISHED'}


class PogoCustomMap(bpy.types.PropertyGroup):
    map_name: bpy.props.StringProperty(name="Map Name", description="The name of the map")
    map_image: bpy.props.PointerProperty(type=bpy.types.Image, name="Map Image", description="The image used for the map thumbnail")

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
        description="The start line. This entity will dissapear once the run is started. The run will start once the player leaves a circle of roughly 475 pogo units in diameter, from the origin of this object",
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

    static_files: bpy.props.CollectionProperty(type=StaticFile, name="Static Files")
    active_static_file_idx: bpy.props.IntProperty(name="Active Static File")


classes = (
    PogoSplit,
    StaticFile,
    PogoCustomMap,
    ActiveSplitMove,
    StaticFileAdd,
    StaticFileRemove,
)


def register():
    bpy.types.Collection.custom_map = bpy.props.PointerProperty(type=PogoCustomMap)


def unregister():
    del bpy.types.Collection.custom_map
