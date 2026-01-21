import os

import bpy
from PIL import Image

from .. import pogo_blend_utils as pbu
from ..ui.operators import create_collider
from .gub_byte_array import GubByteArray
from .hash_cache import HashCache
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
from .wmb_exporter.wmb_objects.wmb_region import WMBRegion

used_names = set()


def build_custom_map(context, filepath, global_scale):
    custom_map_collection = pbu.get_custom_map_collection()
    custom_map = pbu.get_custom_map()
    custom_map.update_splits()

    spawn = custom_map.spawn
    if spawn is None:
        raise pbu.ContextError("You MUST choose a spawn on the 'CustomMap' collection")

    path_progress = custom_map.path_progress
    if path_progress is None:
        raise pbu.ContextError("You MUST choose a progrees path on the 'CustomMap' collection")

    start_line = custom_map.start_line
    if start_line is None:
        raise pbu.ContextError("You MUST choose a starting line on the 'CustomMap' collection")

    dirpath = os.path.dirname(filepath)
    cache = HashCache(os.path.join(dirpath, ".pogo_blend"))
    used_names.clear()

    wmb_objects = [
        WMBInfo(),
        PogoSpawn(spawn),
        PogoModeSetup(custom_map),
        PogoPathProgress(path_progress),
        PogoStartLine(start_line),
    ]
    meshes = {}
    if start_line.pogo_entity.filename_override == "":
        meshes[start_line.data] = ([wmb_objects[-1]], start_line, global_scale)
    textures = {}
    paths = [path_progress]
    paths_to_add = []
    splits_to_add = {}
    colliders = []
    used_files = set(
        [
            ".pogo_blend",
            "customMap.wmb",
            "levelDescription.txt",
            "splitSetup.txt",
            "workshopPreview.png",
        ]
    )

    for obj in custom_map_collection.all_objects:
        if obj in [spawn, path_progress, start_line]:
            continue

        match obj.type:
            case 'MESH':
                if "pogo_entity" not in obj:
                    continue

                entity = WMBEntity(obj, global_scale)
                mesh = obj.data
                path = None
                if obj.pogo_entity.filename_override == "":
                    if mesh not in meshes:
                        meshes[mesh] = ([entity], obj, global_scale)
                    else:
                        meshes[mesh][0].append(entity)
                    if obj.pogo_entity.flag_auto_collision and obj.pogo_entity.flag_polygon:
                        colliders.append((obj, entity))
                else:
                    used_files.add(obj.pogo_entity.filename_override)
                if obj.pogo_entity.path is not None and not obj.pogo_entity.flag_auto_collision:
                    paths_to_add.append((entity, obj.pogo_entity.path))
                wmb_objects.append(entity)
            case 'EMPTY':
                if "pogo_region" not in obj:
                    continue
                if obj.pogo_region.region_type == "ndef":
                    continue

                region = WMBRegion(obj, global_scale)
                if obj.pogo_region.region_type == "CP_":
                    splits_to_add[obj] = region
                wmb_objects.append(region)
            case 'CURVE':
                if "pogo_path" not in obj:
                    continue

                paths.append(obj)
                wmb_objects.append(WMBPath(obj, global_scale))

    # export meshes
    for entities, obj, scale in meshes.values():
        filename = pbu.get_unique_name(obj.name.replace(".", "_"), ".mdl", 33, used_names)
        if filename is None:
            print("WARNING: could not find a unique filename")
            continue
        used_files.add(filename)

        for entity in entities:
            entity.filename = filename
        mdlpath = os.path.join(dirpath, filename)

        for texture in pbu.get_textures(obj):
            if texture["image"] not in textures:
                new_texture = pbu.get_unique_name(
                    texture["name"].replace(".", "_"),
                    ".tga",
                    31,
                    used_names,
                )
                if new_texture is None:
                    print("WARNING: could not find a unique filename")
                    continue
                else:
                    used_files.add(new_texture)
                    texture["name"] = new_texture
                    textures[texture["image"]] = texture

        if not cache.update_entity(filename, obj):
            continue

        mdl_exporter = MDLExporter(mdlpath, [obj], scale)
        for texture, slot_idx in mdl_exporter.skins.copy().values():
            if texture["image"] in textures:
                new_texture = textures[texture["image"]]["name"]
                mdl_exporter.skins[texture["image"]][0]["name"] = new_texture
        mdl_exporter.export()

    # colliders
    with create_collider.CreateColliderContext() as ctx:
        for obj, entity in colliders:
            filename = pbu.get_unique_name(obj.name.replace(".", "_"), "_col.mdl", 33, used_names)
            if filename is None:
                print("WARNING: could not find a unique filename")
                continue
            used_files.add(filename)
            mdlpath = os.path.join(dirpath, filename)

            if cache.update_collider(filename, obj):
                collider = ctx.create_collider(obj, 64)
                MDLExporter(mdlpath, [collider], global_scale).export()
            else:
                collider = ctx.create_collider_object(obj)

            collider_entity = WMBEntity(collider, global_scale)
            collider_entity.filename = filename
            entity.flags &= ~(1 << 26)  # clear polygon
            entity.flags |= 1 << 9  # set passable
            if obj.pogo_entity.path is not None:
                paths_to_add.append((collider_entity, obj.pogo_entity.path))
            wmb_objects.append(collider_entity)

            # cleanup generated collider
            mesh = collider.data
            bpy.data.objects.remove(collider, do_unlink=True)
            if mesh is not None:
                bpy.data.meshes.remove(mesh, do_unlink=True)

    for entity, path in paths_to_add:
        entity.path = paths.index(path) + 1

    export_splits(dirpath, custom_map, splits_to_add)

    WMBExporter(filepath, wmb_objects).export()

    export_map_description(dirpath)
    export_map_image(dirpath, custom_map)
    for texture in textures.values():
        export_texture(dirpath, texture)

    files_in_dictionary = set([file for file in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, file))])
    unused_files = files_in_dictionary.difference(used_files)
    for file in unused_files:
        for extension in [".mdl", ".tga", ".png"]:
            if not file.startswith("_") and file.endswith(extension):
                fullpath = os.path.join(dirpath, file)
                os.remove(fullpath)

    cache.keep(used_files)
    cache.write()


def export_splits(dirpath, custom_map, splits):
    filepath = os.path.join(dirpath, "splitSetup.txt")
    bytes = GubByteArray()
    for i, split in enumerate(custom_map.splits.values()):
        split = split.split_region
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
    image_path = custom_map.map_image

    if image_path is None or image_path == "":
        return

    try:
        img = Image.open(custom_map.map_image)
        img.save(os.path.join(dirpath, "workshopPreview.png"), format='PNG')
    except Exception:
        print("Could not load or save map image!")


def export_texture(dirpath: str, texture: dict):
    image = texture["image"]
    image.reload()
    filepath = os.path.join(dirpath, texture["name"])

    old_format = image.file_format
    image.file_format = 'TARGA_RAW'
    image.save(filepath=filepath, save_copy=True)
    image.file_format = old_format
