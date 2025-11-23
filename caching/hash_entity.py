import hashlib
import struct

import bpy


def hash_entity(obj) -> str:
    mesh = obj.data

    hash = hashlib.new("sha256")

    # mesh
    for vert in mesh.vertices:
        hash.update(get_vector_bytes(vert.co))
        hash.update(get_vector_bytes(vert.normal))

    for uv_layer in mesh.uv_layers:
        for uv in uv_layer.uv:
            hash.update(struct.pack("<ff", uv.vector.x, uv.vector.y))

    for edge in mesh.edges:
        for i in range(2):
            hash.update(edge.vertices[i].to_bytes(4))

    for polygon in mesh.polygons:
        for i in range(3):
            hash.update(polygon.vertices[i].to_bytes(4))
        hash.update(polygon.material_index.to_bytes(4))

    # materials
    for mat_slot in obj.material_slots:
        hash.update(int.to_bytes(mat_slot.slot_index))
        if mat_slot.material and mat_slot.material.node_tree:
            for node in mat_slot.material.node_tree.nodes:
                if node.type == "TEX_IMAGE":
                    image = node.image
                    hash.update(node.image.filepath.encode())

    return hash.hexdigest()


def get_vector_bytes(vec):
    return struct.pack("<fff", vec[0], vec[1], vec[2])
