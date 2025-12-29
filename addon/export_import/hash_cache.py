import hashlib
import json
import os
from collections.abc import Callable

import bpy

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

        hash = hashlib.new("sha256")
        hash.update(bytes)
        return hash.hexdigest()

    def hash_collider(self, obj) -> str:
        bytes = GubByteArray()
        mesh = obj.data

        self._store_verts(mesh, bytes)
        self._store_polygons(mesh, bytes)

        bytes.store_vec3f(obj.matrix_world.to_euler())
        bytes.store_vec3f(obj.matrix_world.to_scale())

        hash = hashlib.new("sha256")
        hash.update(bytes)
        return hash.hexdigest()

    def _store_verts(self, mesh, bytes: GubByteArray):
        for vert in mesh.vertices:
            bytes.store_vec3f(vert.co)
            bytes.store_vec3f(vert.normal)

    def _store_uvs(self, mesh, bytes: GubByteArray):
        for uv_layer in mesh.uv_layers:
            for uv in uv_layer.uv:
                bytes.store_float_buffer([uv.vector.x, uv.vector.y])

    def _store_edges(self, mesh, bytes: GubByteArray):
        for edge in mesh.edges:
            for i in range(2):
                bytes.store_32(edge.vertices[i])

    def _store_polygons(self, mesh, bytes: GubByteArray):
        for polygon in mesh.polygons:
            for i in range(3):
                bytes.store_32(polygon.vertices[i])
            bytes.store_32(polygon.material_index)

    def _store_textures(self, obj, bytes: GubByteArray):
        for texture in pbu.get_textures(obj):
            bytes.store_string(texture)
