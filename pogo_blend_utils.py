# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import webbrowser
from pathlib import Path
from string import ascii_lowercase

import bpy
import xxhash
import yaml


def get_preferences() -> bpy.types.AddonPreferences:
    return bpy.context.preferences.addons[__package__].preferences


class ContextError(Exception):
    pass


class AltOperator(bpy.types.Operator):
    objs: list

    def poll_obj(self, obj) -> bool:
        return True

    def execute_obj(self, obj):
        pass

    def execute(self, context):
        for obj in self.objs:
            self.execute_obj(obj)
        self.post_execute()
        return {'FINISHED'}

    def post_execute(self):
        pass

    def invoke(self, context, event):
        if event.alt:
            self.objs = context.selected_objects
        else:
            self.objs = [context.object]
        self.objs = [obj for obj in self.objs if self.poll_obj(obj)]
        return self.execute(context)


class LinkOperator(bpy.types.Operator):
    bl_idname = "pogo_blend.open_link"
    bl_label = "Open a link"
    bl_description = "Opens a link in the default browser"
    bl_options = {'REGISTER'}

    url: bpy.props.StringProperty(default="")

    def execute(self, context):
        webbrowser.open_new(self.url)
        return {'FINISHED'}


def get_custom_map_collection() -> bpy.types.Collection:
    try:
        return bpy.data.collections["CustomMap"]
    except KeyError:
        raise ContextError("No Custom Map found, please name a collection 'CustomMap'")


def get_custom_map() -> bpy.types.PropertyGroup:
    return get_custom_map_collection().custom_map


def get_generated_library_path() -> Path:
    return Path(__file__).parent.joinpath("pogo_blend_asset_library/pogostuck.blend")


def get_unique_name(suggestion, required_suffix, max_length, used_names):
    change_chars = "0123456789" + ascii_lowercase

    suggestion = suggestion.lower().replace(" ", "_")
    base_suggestion = suggestion
    suggestion = suggestion[: min(len(suggestion), max(0, max_length - len(required_suffix)))]
    name = suggestion + required_suffix
    if len(name) > max_length:
        return None

    change_array = [0]
    while name in used_names:
        if len(change_array) + len(required_suffix) > max_length:
            return None
        change = ""
        for change_idx in change_array:
            change += change_chars[change_idx]
        suggestion = (
            base_suggestion[
                : min(
                    len(base_suggestion),
                    max_length - len(required_suffix) - len(change),
                )
            ]
            + change
        )
        name = suggestion + required_suffix
        for i in range(len(change_array)):
            change_array[i] += 1
            if change_array[i] >= len(change_chars):
                change_array[i] = 0
                if i >= len(change_array) - 1:
                    change_array.append(0)
                    break
            else:
                break
    used_names.add(name)
    return name


def get_textures(mesh) -> list[dict]:
    textures = []
    for material in mesh.materials:
        if material is None:
            continue
        for node in material.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                image = node.image
                if image is None:
                    continue

                path = ""
                if image.filepath != "":
                    image_path = get_image_path(image)
                    if image_path.exists():
                        path = str(image_path)
                name = image.name
                if path != "":
                    name = Path(path).name
                textures.append({"image": image, "path": path, "name": name})
    return textures


def get_image_path(image) -> Path:
    return Path(bpy.path.abspath(image.filepath, library=image.library)).resolve()


def get_view_3d_context() -> tuple:
    context = next(((screen, area) for screen in bpy.data.screens for area in screen.areas if area.type == 'VIEW_3D'), None)
    if context is None:
        raise ContextError("Cannot find a VIEW_3D context")
    window = next((window for window in bpy.context.window_manager.windows if window.screen == context[0]), None)
    return (window, *context)


class BlenderModeContext:
    def __enter__(self):
        self.mode = bpy.context.mode
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except RuntimeError:
            pass
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.mode.startswith('EDIT') and self.mode != 'EDIT_GPENCIL':
            self.mode = 'EDIT'
        elif self.mode.startswith('PAINT'):
            self.mode = "_".join(reversed(self.mode.split("_")))
        elif self.mode == 'PARTICLE':
            self.mode = f"{self.mode}_EDIT"
        elif self.mode.endswith('GPENCIL') and self.mode != 'EDIT_GPENCIL':
            self.mode = self.mode.replace('GPENCIL', 'GREASE_PENCIL')
        try:
            bpy.ops.object.mode_set(mode=self.mode)
        except RuntimeError:
            pass


def open_temp_text_editor():
    bpy.ops.wm.window_new()

    # delete old editors
    _screen = bpy.context.screen
    try:
        screens_to_delete = (
            screen  #
            for screen in bpy.data.screens
            if screen.name.startswith("pogo_blend_text_editor") and screen not in (window.screen for window in bpy.context.window_manager.windows)
        )
        for screen in screens_to_delete:
            with bpy.context.temp_override(screen=screen):
                bpy.ops.screen.delete()  # this sometimes doesnt do anything, but over time it should purge most of the unused screens. i cant find a better method
    finally:
        bpy.context.window.screen = _screen

    bpy.context.window.screen.name = "pogo_blend_text_editor"
    area = bpy.context.area
    area.ui_type = 'TEXT_EDITOR'


def parse_yaml(filepath: str):
    yaml_obj = None
    with open(Path(__file__).parent.joinpath(Path(filepath)), "r") as f:
        yaml_obj = yaml.safe_load(f)
    return yaml_obj


def get_enum_list(filepath: str, show_all: bool) -> list[tuple]:
    yaml_obj = parse_yaml(filepath)
    enum_list = []
    for key, config in yaml_obj.items():
        if config is None:
            config = {}
        if not show_all and "hidden" in config and config["hidden"]:
            continue
        enum_list.append(
            (
                key,
                config["name"] if "name" in config else key,
                config["description"] if "description" in config else "",
                xxhash.xxh32_intdigest(key) & 0b0111_1111_1111_1111_1111_1111_0000_0000  # idk why the enums are weird but they are so this is the solution
                if "id" not in config
                else config["id"],
            )
        )
    return enum_list


def get_enum_key(obj, prop_name: str, enum_list: list[tuple]) -> str | None:
    if prop_name not in obj:
        return "ndef"
    key = [key for key, _, _, id in enum_list if id == obj[prop_name]]
    if len(key) == 0:
        return "ndef"
    else:
        return key[0]


classes = (LinkOperator,)
