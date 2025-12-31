import json
import os
from collections.abc import Callable

import bpy
import xxhash

from .. import pogo_blend_utils as pbu
from .gub_byte_array import GubByteArray


class HashCache:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cache = {}
        self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, "r") as f:
            try:
                self.cache = json.load(f)
            except json.JSONDecodeError:
                pass

    def write(self):
        with open(self.filepath, "w") as f:
            json_string = json.dumps(self.cache)
            f.write(json_string)

    def _update(self, key: str, obj, hash_func: Callable) -> bool:
        hash = hash_func(obj)

        if key in self.cache and self.cache[key] == hash:
            return False

        self.cache.update({key: hash})
        return True

    def update_entity(self, key: str, obj) -> bool:
        return self._update(key, obj, self.hash_entity)

    def update_collider(self, key: str, obj) -> bool:
        return self._update(key, obj, self.hash_collider)

    def keep(self, keep_set: set):
        current = set(self.cache.keys())
        to_remove = current.difference(keep_set)
        for key in to_remove:
            del self.cache[key]

    def hash_entity(self, obj) -> str:
        bytes = GubByteArray()
        mesh = obj.data

        self._store_verts(mesh, bytes)
        self._store_uvs(mesh, bytes)
        # self._store_edges(mesh, bytes)
        self._store_polygons(mesh, bytes)
        self._store_textures(obj, bytes)
        self._store_modifiers(obj, bytes)

        return xxhash.xxh128_hexdigest(bytes)

    def hash_collider(self, obj) -> str:
        bytes = GubByteArray()
        mesh = obj.data

        self._store_verts(mesh, bytes)
        self._store_polygons(mesh, bytes)
        self._store_modifiers(obj, bytes)

        bytes.store_vec3f(obj.matrix_world.to_euler())
        bytes.store_vec3f(obj.matrix_world.to_scale())

        return xxhash.xxh128_hexdigest(bytes)

    def _store_verts(self, mesh, bytes: GubByteArray):
        verts = []
        for vert in mesh.vertices:
            verts.append(vert.co)
            verts.append(vert.normal)
        bytes.store_vec3f_buffer(verts)

    def _store_uvs(self, mesh, bytes: GubByteArray):
        floats = []
        for uv_layer in mesh.uv_layers:
            for uv in uv_layer.uv:
                floats.extend([uv.vector.x, uv.vector.y])
        bytes.store_float_buffer(floats)

    def _store_edges(self, mesh, bytes: GubByteArray):
        ints = []
        for edge in mesh.edges:
            for i in range(2):
                ints.append(edge.vertices[i])
        bytes.store_32_buffer(ints)

    def _store_polygons(self, mesh, bytes: GubByteArray):
        ints = []
        for polygon in mesh.polygons:
            for i in range(3):
                ints.append(polygon.vertices[i])
            ints.append(polygon.material_index)
        bytes.store_32_buffer(ints)

    def _store_textures(self, obj, bytes: GubByteArray):
        bytes.store_strings(pbu.get_textures(obj))

    def _store_modifiers(self, obj, bytes: GubByteArray):
        bytes.store_32(len(obj.modifiers))
        for modifier in obj.modifiers:
            bytes.store_bool(modifier.is_active)
            bytes.store_string(modifier.type)
            match(modifier.type):
                case 'ARRAY':
                    bytes.store_32(modifier.count)
                    bytes.store_bool(modifier.use_relative_offset)
                    if modifier.use_relative_offset:
                        bytes.store_vec3f(modifier.relative_offset_displace)
                    bytes.store_bool(modifier.use_constant_offset)
                    if modifier.use_constant_offset:
                        bytes.store_vec3f(modifier.constant_offset_displace)
                    bytes.store_bool(modifier.use_object_offset)
                    if modifier.use_object_offset:
                        if modifier.offset_object != None:
                            bytes.store_vec3f(modifier.offset_object.matrix_world.translation)
                case 'BEVEL':
                    bytes.store_string(modifier.affect)
                    bytes.store_string(modifier.offset_type)
                    if modifier.offset_type != 'PERCENT':
                        bytes.store_float(modifier.width)
                    else:
                        bytes.store_float(modifier.width_pct)
                    bytes.store_string(modifier.limit_method)
                    if modifier.limit_method == 'ANGLE':
                        bytes.store_float(modifier.angle_limit)
