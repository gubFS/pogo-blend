import os

import bpy
from mathutils import Vector

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
        self.filepath = filepath
        if len(objs) == 0:
            raise Exception("No objects selected")
        self.objs = objs

        center = Vector((0, 0, 0))
        if not bake_location:
            sum = Vector((0, 0, 0))
            for obj in objs:
                sum += obj.matrix_world.translation * scale
            center = sum / len(objs)

        self.skins = {"": 0}
        self.uvs = []
        self.tris = []
        self.verts = []
        self.vert_normals = []

        obj_verts_index = 0
        uv_index = 0
        skin_dict = {}
        for obj in self.objs:
            mesh = obj.data

            has_skin = False
            # Goes through every node on every material on the object
            for mat_slot in obj.material_slots:
                if mat_slot.material and mat_slot.material.node_tree:
                    for node in mat_slot.material.node_tree.nodes:
                        if node.type == "TEX_IMAGE":
                            image = node.image
                            full_path = bpy.path.abspath(
                                image.filepath, library=image.library
                            )
                            image_path = os.path.normpath(full_path)
                            if image_path in self.skins:
                                skin_dict[mat_slot.slot_index] = self.skins[image_path]
                            else:
                                self.skins[image_path] = len(self.skins)
                                skin_dict[mat_slot.slot_index] = self.skins[image_path]
                            has_skin = True

            # y-axis is flipped in A8
            if has_skin:
                for uv in mesh.uv_layers[0].uv:
                    self.uvs.append(Vector((uv.vector.x, 1 - uv.vector.y)))

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
                self.vert_normals.append(normal)

            total_uvs = 0
            uvkeys = {}
            for poly in mesh.polygons:
                uvkeys[poly.index] = {}
                for vert_idx in poly.vertices:
                    uv_idx = total_uvs
                    uvkeys[poly.index][vert_idx] = uv_idx
                    total_uvs += 1

            for i, tri in enumerate(mesh.loop_triangles):
                poly_idx = mesh.loop_triangle_polygons[i].value
                skin_idx = 0
                if has_skin and tri.material_index in skin_dict:
                    skin_idx = skin_dict[tri.material_index]

                vert_indecies = []
                uv_indecies = []
                for i in range(
                    2, -1, -1
                ):  # loop in reverse because the normals are flipped in mdl files compared to blend
                    vert_indecies.append(obj_verts_index + tri.vertices[i])
                for vert_idx in tri.vertices:
                    uv_indecies.append(uv_index + uvkeys[poly_idx][vert_idx])
                uv_indecies.reverse()
                self.tris.append((vert_indecies, uv_indecies, skin_idx))

            obj_verts_index = len(self.verts)
            uv_index = len(self.uvs)

    # See MDLFormat.txt for documentation
    def export(self):  # see MDL7Format.txt
        mdl = GubByteArray()

        mdl.store_string("MDL7")
        mdl.store_32(0)
        mdl.store_32(0)
        mdl.store_32(
            1
        )  # group num may need to update but imma just do one group for now
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
        mdl.store_32(len(self.skins))
        mdl.store_32(len(self.uvs))
        mdl.store_32(len(self.tris))
        mdl.store_32(len(self.verts))
        mdl.store_32(0)

        # Skin
        for texture, skin_idx in self.skins.items():
            texture = os.path.basename(texture)
            mdl.store_8(7)  # type?
            mdl.store_8s(0, 3)  # unused
            mdl.store_32(len(texture) + 1)
            mdl.store_32(1)
            mdl.store_string(f"Skin{skin_idx + 1}", 16)
            mdl.store_string(texture)
            mdl.store_8(0)

        for uv in self.uvs:
            for i in range(2):
                mdl.store_float(uv[i])

        for tri, uv, skin_idx in self.tris:
            for i in range(3):
                mdl.store_16(tri[i])
            for i in range(3):
                mdl.store_16(uv[i])
            mdl.store_32(skin_idx)
            mdl.store_8s(0xFF, 6)
            mdl.store_8s(0xFF, 4)

        for vert_idx in range(len(self.verts)):
            for i in range(3):
                mdl.store_float(self.verts[vert_idx][i])
            mdl.store_16(0xFFFF)
            for i in range(3):
                mdl.store_float(self.vert_normals[vert_idx][i])

        mdl.store_32_at(mdl.get_position(), file_size_pos)
        mdl.store_32_at(mdl.get_position() - group_pos, group_size_pos)

        with open(self.filepath, "wb") as f:
            f.write(mdl)
