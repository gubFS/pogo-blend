import json
import os
from collections.abc import Callable

import xxhash

from .. import pogo_blend_utils as pbu
from .gub_byte_array import GubByteArray


class HashCache:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cache = {}
        self.temp_cache = {}
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
        self.temp_cache.clear()

    def _update(self, key: str, obj, hash_func: Callable) -> bool:
        hash = hash_func(obj)

        if key in self.cache and self.cache[key] == hash:
            return False

        self.cache[key] = hash
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

        self._store_buffer(mesh, self._store_verts, bytes)
        self._store_buffer(mesh, self._store_uvs, bytes)
        # self._store_buffer(mesh, self._store_edges, bytes)
        self._store_buffer(mesh, self._store_polygons, bytes)
        self._store_buffer(obj, self._store_textures, bytes)
        self._store_buffer(obj, self._store_modifiers, bytes)

        return self._hash_bytearray(bytes)

    def hash_collider(self, obj) -> str:
        bytes = GubByteArray()
        mesh = obj.data

        self._store_buffer(mesh, self._store_verts, bytes)
        self._store_buffer(mesh, self._store_polygons, bytes)
        self._store_buffer(obj, self._store_modifiers, bytes)

        bytes.store_vec3f(obj.matrix_world.to_euler())
        bytes.store_vec3f(obj.matrix_world.to_scale())

        return self._hash_bytearray(bytes)

    def _hash_bytearray(self, bytes: bytearray) -> str:
        return xxhash.xxh128_hexdigest(bytes)

    def _store_buffer(self, value, store_func: Callable, bytes: GubByteArray):
        buffer = self.temp_cache.get(value, {}).get(store_func, None)
        if buffer is None:
            buffer = GubByteArray()
            store_func(value, buffer)
            # hash = self._hash_bytearray(bytes_to_hash)
            self.temp_cache.setdefault(value, {})
            self.temp_cache[value][store_func] = buffer
        bytes.store_buffer(buffer)

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
        bytes.store_strings([texture["name"] for texture in pbu.get_textures(obj)])

    def _store_modifiers(self, obj, bytes: GubByteArray):
        bytes.store_32(len(obj.modifiers))
        for modifier in obj.modifiers:
            bytes.store_bool(modifier.is_active)
            bytes.store_string(modifier.type)
            match modifier.type:
                case "ARRAY":
                    bytes.store_32(modifier.count)
                    bytes.store_bool(modifier.use_relative_offset)
                    if modifier.use_relative_offset:
                        bytes.store_vec3f(modifier.relative_offset_displace)
                    bytes.store_bool(modifier.use_constant_offset)
                    if modifier.use_constant_offset:
                        bytes.store_vec3f(modifier.constant_offset_displace)
                    bytes.store_bool(modifier.use_object_offset)
                    if modifier.use_object_offset:
                        if modifier.offset_object is not None:
                            bytes.store_vec3f(modifier.offset_object.matrix_world.translation)
                case "BEVEL":
                    bytes.store_string(modifier.affect)
                    bytes.store_string(modifier.offset_type)
                    if modifier.offset_type != "PERCENT":
                        bytes.store_float(modifier.width)
                    else:
                        bytes.store_float(modifier.width_pct)
                    bytes.store_string(modifier.limit_method)
                    if modifier.limit_method == "ANGLE":
                        bytes.store_float(modifier.angle_limit)
                case "EDGE_SPLIT":
                    bytes.store_bool(modifier.use_edge_angle)
                    if modifier.use_edge_angle:
                        bytes.store_float(modifier.split_angle)
                    bytes.store_bool(modifier.use_edge_sharp)
