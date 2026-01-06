import os
from pathlib import Path
from string import ascii_lowercase

import bpy
import xxhash
import yaml

from .pogo_blend_preferences import get_preferences as gp


def get_preferences() -> bpy.types.AddonPreferences:
    return gp()


class ContextError(Exception):
    pass


def get_custom_map_collection() -> bpy.types.Collection:
    try:
        return bpy.data.collections["CustomMap"]
    except KeyError:
        raise ContextError("No Custom Map found, please name a collection 'CustomMap'")


def get_custom_map() -> bpy.types.PropertyGroup:
    return get_custom_map_collection().custom_map


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


def get_textures(obj) -> list[str]:
    textures = []
    for mat_slot in obj.material_slots:
        if mat_slot.material and mat_slot.material.node_tree:
            for node in mat_slot.material.node_tree.nodes:
                if node.type == 'TEX_IMAGE':
                    image = node.image
                    full_path = bpy.path.abspath(image.filepath, library=image.library)
                    image_path = os.path.normpath(full_path)
                    textures.append(image_path)
    return textures


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
                xxhash.xxh32_intdigest(key) & 0b1111_1111_1111_1111_1111_1111_0000_0000  # idk why the enums are weird but they are so this is the solution
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
