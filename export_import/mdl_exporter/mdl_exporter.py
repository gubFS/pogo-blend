# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import bmesh
import bpy
from mathutils import Vector

from ... import pogo_blend_utils as pbu
from ..gub_byte_array import GubByteArray


class MDLExporter:
    def __init__(
        self,
        filepath,
        objs,
        scale=1.0,
        bake_location=False,
        bake_rotation=False,
        bake_scale=False,
    ):
        self.filepath = str(filepath)
        if len(objs) == 0:
            raise Exception("No objects selected")
        self.objs = objs

        with pbu.BlenderModeContext():
            center = Vector((0, 0, 0))
            if not bake_location:
                sum = Vector((0, 0, 0))
                for obj in objs:
                    sum += obj.matrix_world.translation * scale
                center = sum / len(objs)

            self.skins = {}
            self.uvs = []
            self.tris = []
            self.verts = []
            self.vert_normals = []

            obj_verts_index = 0
            uv_index = 0
            skin_dict = {}
            dg = bpy.context.evaluated_depsgraph_get()
            for obj in self.objs:
                mesh = obj.to_mesh()
                bm = bmesh.new()
                bm.from_object(obj, dg)
                bmesh.ops.triangulate(bm, faces=bm.faces)
                bm.to_mesh(mesh)
                bm.free()

                textures = pbu.get_textures(mesh)
                for i, texture in enumerate(textures):
                    if texture["name"] in self.skins:
                        skin_dict[i] = self.skins[texture["name"]]
                    else:
                        self.skins[texture["name"]] = (texture, len(self.skins))
                        skin_dict[i] = self.skins[texture["name"]]
                has_skin = len(textures) != 0
                self.has_skin = has_skin

                # y-axis is flipped in A8
                uv_hash_map = {}
                uv_idx_lookup = []
                if has_skin:
                    for uv in [uv for uv_layer in mesh.uv_layers[:2] for uv in uv_layer.uv]:
                        uv = Vector((uv.vector.x, 1 - uv.vector.y))
                        uv.freeze()
                        idx = len(uv_hash_map)
                        if uv in uv_hash_map:
                            idx = uv_hash_map[uv]
                        else:
                            uv_hash_map[uv] = idx
                            self.uvs.append(uv)
                        uv_idx_lookup.append(idx)
                self.has_second_uv_set = len(mesh.uv_layers) >= 2

                loc = obj.matrix_world.translation
                rot = obj.matrix_world.to_euler()
                scl = obj.matrix_world.to_scale()
                for vert in mesh.vertices:
                    normal = vert.normal.copy()
                    vert = vert.co.copy()
                    vert *= scale
                    if bake_rotation:
                        vert.rotate(rot)
                        normal.rotate(rot)
                    if bake_scale:
                        vert *= scl

                    self.verts.append((loc * scale - center) + vert)
                    self.vert_normals.append(normal * -1)  # GSA8 uses flipped normals or something

                uvkeys = {}
                if has_skin:
                    uv_idx = 0
                    for poly in mesh.polygons:
                        uvkeys[poly.index] = {}
                        for vert_idx in poly.vertices:
                            uvkeys[poly.index][vert_idx] = uv_idx
                            uv_idx += 1

                for i, tri in enumerate(mesh.loop_triangles):
                    poly_idx = mesh.loop_triangle_polygons[i].value
                    skin_idx = 0
                    if has_skin and tri.material_index in skin_dict:
                        skin_idx = skin_dict[tri.material_index][1]

                    vert_indecies = []
                    uv_indecies = []
                    for i in range(2, -1, -1):  # loop in reverse because the normals are flipped in mdl files compared to blend
                        vert_indecies.append(obj_verts_index + tri.vertices[i])
                    if has_skin:
                        for vert_idx in tri.vertices:
                            uv_indecies.append(uv_index + uv_idx_lookup[uvkeys[poly_idx][vert_idx]])
                        uv_indecies = uv_indecies[::-1]
                        if self.has_second_uv_set:
                            for vert_idx in tri.vertices:
                                uv_indecies.append(uv_index + uv_idx_lookup[uvkeys[poly_idx][vert_idx] + len(uv_idx_lookup) // 2])
                            uv_indecies[3:6] = uv_indecies[3:6][::-1]
                    self.tris.append((vert_indecies, uv_indecies, skin_idx))

                obj_verts_index = len(self.verts)
                uv_index = len(self.uvs)

    # See MDL7Format.txt for documentation
    def export(self):
        mdl = GubByteArray()

        mdl.store_string("MDL7")
        mdl.store_32(0)
        mdl.store_32(0)
        mdl.store_32(1)  # group num may need to update but imma just do one group for now
        file_size_pos = mdl.get_position()
        mdl.store_32(0)  # file size, update at the end
        mdl.store_32(0)
        mdl.store_32(0)

        mdl.store_16(0x24)
        mdl.store_16(0x1C)
        mdl.store_16(0x10)
        mdl.store_16(0x44)
        mdl.store_16(0x08)
        mdl.store_16(0x1A)
        mdl.store_16(0x1A)
        mdl.store_16(0x1A)
        mdl.store_16(0x44)
        mdl.store_16(0x14)

        group_pos = mdl.get_position()
        mdl.store_8(1)  # 1 is triangle based
        mdl.store_8s(0, 3)  # unused
        group_size_pos = mdl.get_position()
        mdl.store_32(0)  # size of group, store later
        mdl.store_string("Group", 16)
        mdl.store_32(len(self.skins) if self.has_skin else 0)
        mdl.store_32(len(self.uvs) if self.has_skin else 0)
        mdl.store_32(len(self.tris))
        mdl.store_32(len(self.verts))
        mdl.store_32(0)

        # Skin
        if self.has_skin:
            for texture, skin_idx in self.skins.values():
                if len(texture["name"]) > 31:
                    print(f"WARNING: While MDL files can have skins with long filenames, it will crash when loaded in the A8 Engine if the filename is longer than 31 characters. Please use a shorter name than {texture}")
                mdl.store_8(7)  # type?
                mdl.store_8s(0, 3)  # unused
                mdl.store_32(len(texture["name"]) + 1)
                mdl.store_32(1)
                mdl.store_string(f"Skin{skin_idx + 1}", 16)
                mdl.store_string(texture["name"])
                mdl.store_8(0)

        if self.has_skin:
            for uv in self.uvs:
                mdl.store_float_buffer(uv)  # vec2f

        for tri, uv, skin_idx in self.tris:
            for tri_idx in tri[:3]:
                mdl.store_16(tri_idx)
            if self.has_skin:
                for uv_idx in uv[:3]:
                    mdl.store_16(uv_idx)
                mdl.store_32(skin_idx)
                if self.has_second_uv_set:
                    for uv_idx in uv[3:6]:
                        mdl.store_16(uv_idx)
                    mdl.store_32(skin_idx)
                else:
                    mdl.store_8s(0, 10 * 1)
            else:
                mdl.store_8s(0, 10 * 2)

        for vert_idx in range(len(self.verts)):
            mdl.store_vec3f(self.verts[vert_idx])
            mdl.store_16(0xFFFF)
            mdl.store_vec3f(self.vert_normals[vert_idx])

        mdl.store_32_at(mdl.get_position(), file_size_pos)
        mdl.store_32_at(mdl.get_position() - group_pos, group_size_pos)

        with open(self.filepath, "wb") as f:
            f.write(mdl)
