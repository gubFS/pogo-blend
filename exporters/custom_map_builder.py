import os

import bpy
from PIL import Image

from .. import pogo_blend_utils as pbu
from .gub_byte_array import GubByteArray
from .mdl_exporter.mdl_exporter import MDLExporter
from .wmb_exporter.wmb_exporter import WMBExporter
from .wmb_exporter.wmb_objects.wmb_entity import (
    PogoModeSetup,
    PogoSpawn,
    PogoStartLine,
    WMBEntity,
)
from .wmb_exporter.wmb_objects.wmb_info import WMBInfo
from .wmb_exporter.wmb_objects.wmb_path import PogoPathProgress, WMBPath
from .wmb_exporter.wmb_objects.wmb_reigon import WMBReigon

used_names = set()


def build_custom_map(context, filepath, global_scale):
    custom_map_collection = pbu.get_custom_map_collection()
    custom_map = pbu.get_custom_map()

    spawn = custom_map.spawn
    if spawn == None:
        raise pbu.ContextError("You MUST choose a spawn on the 'CustomMap' collection")

    path_progress = custom_map.path_progress
    if path_progress == None:
        raise pbu.ContextError(
            "You MUST choose a progrees path on the 'CustomMap' collection"
        )

    start_line = custom_map.start_line
    if start_line == None:
        raise pbu.ContextError(
            "You MUST choose a starting line on the 'CustomMap' collection"
        )

    dirpath = os.path.dirname(filepath)
    used_names.clear()

    undo_map_scale_args = apply_map_scale(custom_map_collection, global_scale)
    try:
        wmb_objects = [
            WMBInfo(),
            PogoSpawn(spawn),
            PogoModeSetup(custom_map),
            PogoPathProgress(path_progress),
            PogoStartLine(start_line),
        ]
        meshes = {}
        textures = {}
        paths = [path_progress]
        paths_to_add = []
        splits_to_add = {}

        for obj in custom_map_collection.objects:
            if obj in [spawn, path_progress, start_line]:
                continue

            match obj.type:
                case "MESH":
                    if "pogo_entity" not in obj:
                        continue

                    entity = WMBEntity(obj)
                    mesh = obj.data
                    if obj.pogo_entity.filename_override == "":
                        if mesh not in meshes:
                            meshes[mesh] = (entity, obj)
                    if obj.pogo_entity.path != None:
                        paths_to_add.append((entity, obj.pogo_entity.path))
                    wmb_objects.append(entity)
                case "EMPTY":
                    if "pogo_reigon" not in obj:
                        continue
                    if obj.pogo_reigon.reigon_type == "ndef":
                        continue

                    reigon = WMBReigon(obj)
                    if obj.pogo_reigon.reigon_type == "CP_":
                        splits_to_add[obj] = reigon
                    wmb_objects.append(reigon)
                case "CURVE":
                    if "pogo_path" not in obj:
                        continue

                    paths.append(obj)
                    wmb_objects.append(WMBPath(obj))

        for entity, path in paths_to_add:
            entity.path = paths.index(path) + 1

        for entity, obj in meshes.values():
            filename = pbu.get_unique_name(obj.name, ".mdl", 33, used_names)
            if filename == None:
                print("WARNING: could not find a unique filename")
                continue

            entity.filename = filename
            mdlpath = os.path.join(dirpath, filename)
            if os.path.exists(mdlpath):
                print(f"WARNING: Overwriting '{mdlpath}'")
            mdl_exporter = MDLExporter(mdlpath, [obj], global_scale)
            for texture, slot_idx in mdl_exporter.skins.copy().items():
                if texture == "":
                    continue

                new_texture = None
                if texture in textures:
                    new_texture = textures[texture]
                else:
                    new_texture = pbu.get_unique_name(
                        os.path.splitext(os.path.basename(texture))[0],
                        ".tga",
                        255,
                        used_names,
                    )
                if new_texture == None:
                    print("WARNING: could not find a unique filename")
                    continue
                mdl_exporter.skins.pop(texture)
                mdl_exporter.skins[new_texture] = slot_idx
                textures[texture] = new_texture
            mdl_exporter.export()

        export_splits(dirpath, custom_map, splits_to_add)
        WMBExporter(filepath, wmb_objects).export()

        export_map_description(dirpath)
        export_map_image(dirpath, custom_map)
        for texture, new_texture in textures.items():
            export_texture(dirpath, new_texture, texture)
    finally:
        unapply_map_scale(*undo_map_scale_args)


def export_splits(dirpath, custom_map, splits):
    filepath = os.path.join(dirpath, "splitSetup.txt")
    bytes = GubByteArray()
    for i, split in enumerate(custom_map.splits.values()):
        split = split.split_reigon
        splits[split].name += str(i)
        bytes.store_string(f"{split.name}\n")
    with open(filepath, "wb") as f:
        f.write(bytes)


def export_map_description(dirpath):
    text = ""
    if "levelDescription.txt" in bpy.data.texts:
        text = bpy.data.texts["levelDescription.txt"].as_string()
    filepath = os.path.join(dirpath, "levelDescription.txt")
    with open(filepath, "wb") as f:
        f.write(0xFF.to_bytes())  # utf-16-le header aka 'BOM'
        f.write(0xFE.to_bytes())
        f.write(text.encode("utf-16-le"))


def export_map_image(dirpath, custom_map):
    img = Image.open(custom_map.map_image)
    img.save(os.path.join(dirpath, "workshopPreview.png"), format="PNG")


def export_texture(dirpath, image_name, image_path):
    img = Image.open(image_path)
    img.save(os.path.join(dirpath, image_name), format="TGA")


def apply_map_scale(custom_map_collection, scale):
    scale_root = bpy.data.objects.new(name="ScaleRoot", object_data=None)
    scale_root.location = (0, 0, 0)
    custom_map_collection.objects.link(scale_root)

    objects = custom_map_collection.objects.values()
    objects.remove(scale_root)

    for obj in objects:
        obj.parent = scale_root
    scale_root.scale *= scale
    bpy.context.evaluated_depsgraph_get().update()

    return (objects, scale_root)


def unapply_map_scale(objects, scale_root):
    for obj in objects:
        obj.parent = None
    bpy.data.objects.remove(scale_root, do_unlink=True)
