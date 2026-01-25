import os
import shutil
from pathlib import Path

import bpy

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

    dirpath = Path(filepath).parent
    cache = HashCache(Path(dirpath, ".pogo_blend"))

    wmb_objects = [
        WMBInfo(),
        PogoSpawn(spawn, global_scale),
        PogoModeSetup(custom_map),
        PogoPathProgress(path_progress),
        PogoStartLine(start_line),
    ]
    entities = {}
    if start_line.pogo_entity.filename_override == "":
        entities[cache.hash_entity(start_line)] = ([wmb_objects[-1]], start_line)
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
    global used_names
    used_names = set(file for file in used_files)
    static_files = set()
    for file in custom_map.static_files:
        abspath = Path(bpy.path.abspath(file.filepath)).resolve()
        if not abspath.exists():
            continue
        if abspath.name in used_names:
            continue

        static_files.add(str(abspath))
        used_files.add(abspath.name)
        used_names.add(abspath.name)
    custom_materials = set()

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
                    hash = cache.hash_entity(obj)
                    if hash not in entities:
                        entities[hash] = ([entity], obj)
                    else:
                        entities[hash][0].append(entity)
                    if obj.pogo_entity.flag_auto_collision and obj.pogo_entity.flag_polygon:
                        colliders.append((obj, entity))
                else:
                    used_files.add(obj.pogo_entity.filename_override)
                if obj.pogo_entity.path is not None and not obj.pogo_entity.flag_auto_collision:
                    paths_to_add.append((entity, obj.pogo_entity.path))
                if entity.material.startswith("customMaterial"):
                    custom_materials.add(entity.material)
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
    for wmb_entities, obj in entities.values():
        filename = pbu.get_unique_name(obj.name.replace(".", "_"), ".mdl", 33, used_names)
        if filename is None:
            print("WARNING: could not find a unique filename")
            continue
        used_files.add(filename)

        for wmb_entity in wmb_entities:
            wmb_entity.filename = filename
        mdlpath = Path(dirpath, filename)

        for texture in pbu.get_textures(obj.data):
            if texture["image"] not in textures:
                new_texture = pbu.get_unique_name(
                    Path(texture["name"]).stem.replace(".", "_"),
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

        mdl_exporter = MDLExporter(mdlpath, [obj], global_scale)
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
            mdlpath = Path(dirpath, filename)

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

    # exporting

    export_splits(dirpath, custom_map, splits_to_add)

    WMBExporter(filepath, wmb_objects).export()

    export_map_description(dirpath)
    export_map_image(dirpath, custom_map)
    for texture in textures.values():
        export_texture(dirpath, texture)

    for static_file in static_files:
        shutil.copy(static_file, Path(dirpath, Path(static_file).name))

    for custom_material in custom_materials:
        filename = f"{custom_material}.fx"
        content = ""
        if filename in bpy.data.texts:
            text_obj = bpy.data.texts[filename]
            if not text_obj.is_dirty and text_obj.is_modified:
                with open(text_obj.filepath, "r") as f:
                    content = f.read()
            else:
                content = text_obj.as_string()
        elif Path(bpy.path.abspath(bpy.path.relpath(filename))).exists():
            with open(Path(bpy.path.abspath(bpy.path.relpath(filename))), "r") as f:
                content = f.read()
        else:
            continue

        filepath = Path(dirpath, f"{custom_material}.fx")
        with open(filepath, "wb") as f:
            f.write(content.encode())
        used_files.add(filename)
        pogostuck_path = Path(pbu.get_preferences().custom_maps_path).parent.joinpath(filename)
        shutil.copy(filepath, pogostuck_path)

    # cleanup

    files_in_dictionary = set([file for file in os.listdir(dirpath) if Path(dirpath, file).is_file()])
    unused_files = files_in_dictionary.difference(used_files)
    for file in unused_files:
        if not file.startswith("_"):
            fullpath = Path(dirpath, file)
            os.remove(fullpath)

    cache.keep(used_files)
    cache.write()


def export_splits(dirpath, custom_map, splits):
    filepath = Path(dirpath, "splitSetup.txt")
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
    filepath = Path(dirpath, "levelDescription.txt")
    with open(filepath, "wb") as f:
        f.write(0xFF.to_bytes())  # utf-16-le header aka 'BOM'
        f.write(0xFE.to_bytes())
        f.write(text.encode("utf-16-le"))


def export_map_image(dirpath, custom_map):
    image = custom_map.map_image
    if image is None:
        return

    old_format = image.file_format
    image.file_format = 'PNG'
    image.save(filepath=str(Path(dirpath, "workshopPreview.png")), save_copy=True)
    image.file_format = old_format


def export_texture(dirpath: str | Path, texture: dict):
    image = texture["image"]
    image.reload()
    filepath = str(Path(dirpath, texture["name"]))

    old_format = image.file_format
    image.file_format = 'TARGA_RAW'
    image.save(filepath=filepath, save_copy=True)
    image.file_format = old_format
