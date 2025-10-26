from mathutils import *
from ..gub_byte_array import GubByteArray

class MDLExporter:
    def __init__(self, filepath, objs, scale=1.0):
        self.filepath = filepath
        if len(objs) == 0: raise Exception("No objects selected")
        self.objs = objs

        sum = Vector((0,0,0))
        for obj in objs:
            sum += obj.matrix_world.translation * scale
        center = sum / len(objs)

        self.verts = []
        self.vert_normals = []
        self.tris = []
        obj_verts_index = 0
        for obj in self.objs:
            mesh = obj.to_mesh()
            for vert in mesh.vertices:
                self.verts.append((obj.matrix_world.translation * scale - center) + vert.co * scale)
                self.vert_normals.append(vert.normal)

            for tri in mesh.loop_triangles:
                vert_indecies = []
                for i in range(2, -1, -1): # loop in reverse because the normals are flipped in mdl files compared to blend
                    vert_indecies.append(obj_verts_index + tri.vertices[i])
                self.tris.append(vert_indecies)

            obj_verts_index += len(mesh.vertices)


    # See MDLFormat.txt for documentation
    def export(self):	# see MDL7Format.txt
        mdl = GubByteArray()

        mdl.store_string("MDL7")
        mdl.store_32(0)
        mdl.store_32(0)
        mdl.store_32(1) # group num may need to update but imma just do one group for now
        file_size_pos = mdl.get_position()
        mdl.store_32(0) # file size, update at the end
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
        mdl.store_8(1) # 1 is triangle based
        mdl.store_8s(0, 3) # unused
        group_size_pos = mdl.get_position()
        mdl.store_32(0) # size of group, store later
        mdl.store_string("Group", 16)
        mdl.store_32(0) # num of skins, currently not supported TODO: do this
        mdl.store_32(0) # num of uv points, TODO: do this
        mdl.store_32(len(self.tris))
        mdl.store_32(len(self.verts))
        mdl.store_32(0)

        # TODO: skin and UV points

        for tri in self.tris:
            for i in range(3):
                mdl.store_16(tri[i])
            mdl.store_8s(0xFF, 20)

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

