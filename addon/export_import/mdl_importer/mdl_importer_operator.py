import os
import struct
from io import BufferedReader
from pathlib import Path

import bpy
import bpy_extras
from mathutils import Vector

from ... import pogo_blend_utils as pbu

file: BufferedReader


class MDLTri:
    def __init__(
        self, verts: tuple[int, int, int], uvs: tuple[int, int, int], skin_idx: int
    ):
        self.verts = verts[::-1]
        self.uvs = uvs[::-1]
        self.skin_idx = skin_idx


class MDLVert:
    def __init__(
        self, vert: tuple[float, float, float], normal: tuple[float, float, float]
    ):
        self.vert = vert
        self.normal = normal


def import_mdl(context, filepath, scale):
    skins: list[str] = []
    uvs: list[tuple[float, float]] = []
    tris: list[MDLTri] = []
    verts: list[MDLVert] = []

    with open(filepath, "rb") as f:
        global file
        file = f

        # header
        if f.read(4).decode() != "MDL7":
            raise IOError(f"{filepath} is not a MDL7 file")
        skip(4)
        num_bones = read_32()
        skip(4 * 4)
        bone_struct_size = read_16()
        skip(2 * 9)

        skip(num_bones * bone_struct_size)

        # group
        if read_8() != 1:
            raise IOError("Mesh is not triangle based")
        skip(3)  # unused
        skip(4)
        skip(16)  # name
        num_skins = read_32()
        num_uvs_points = read_32()
        num_tris = read_32()
        num_verts = read_32()
        skip(4)

        for i in range(num_skins):
            skip(4)
            filename_length = read_32()
            skip(4)
            skip(16)
            if filename_length != 0:
                filename = read_str()
                skins.append(filename)

        for i in range(num_uvs_points):
            uvs.append((read_float(), read_float()))

        for i in range(num_tris):
            tris.append(
                MDLTri(
                    (read_16(), read_16(), read_16()),
                    (read_16(), read_16(), read_16()),
                    read_32(),
                ),
            )
            skip(10)

        for i in range(num_verts):
            vert = (read_float() * scale, read_float() * scale, read_float() * scale)
            skip(2)
            normal = (read_float(), read_float(), read_float())
            verts.append(MDLVert(vert, normal))

    # file read done
    name = Path(filepath).stem
    mesh = bpy.data.meshes.new(name=name)
    mesh.from_pydata(
        list(vert.vert for vert in verts), [], list(tri.verts for tri in tris)
    )
    obj = bpy.data.objects.new(name=name, object_data=mesh)
    context.collection.objects.link(obj)
    obj.location = context.scene.cursor.location
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj

    if len(uvs) != 0:
        uv_layer = mesh.uv_layers.new(name="layer")
        for i, tri in enumerate(tris):
            mesh.polygons[i].material_index = (
                tri.skin_idx if tri.skin_idx != 0xFFFFFFFF else 0
            )
            for j in range(3):
                vec = Vector(uvs[tri.uvs[j]])
                vec.y = 1 - vec.y
                uv_layer.uv[(i * 3) + j].vector = vec

    for skin in skins:
        if skin == "":
            bpy.ops.object.material_slot_add()
            continue
        imagepath = os.path.join(os.path.dirname(filepath), skin)
        if not os.path.exists(imagepath):
            print(f"Could not find {imagepath}!")
            continue
        mat = bpy.data.materials.new(name=Path(skin).stem)
        mat.use_nodes = True
        image_node = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
        img = bpy.data.images.load(imagepath)
        image_node.image = img
        disp = mat.node_tree.nodes["Principled BSDF"].inputs[0]
        mat.node_tree.links.new(disp, image_node.outputs[0])
        obj.data.materials.append(mat)


def skip(bytes: int) -> None:
    file.seek(bytes, 1)


def read_str() -> str:
    s = ""
    while byte := file.read(1):
        if byte == (0).to_bytes():
            return s
        else:
            s = f"{s}{byte.decode()}"
    return s


def read_float() -> float:
    return struct.unpack("<f", file.read(4))[0]


def read_8() -> int:
    return int.from_bytes(file.read(1), "little")


def read_16() -> int:
    return int.from_bytes(file.read(2), "little")


def read_32() -> int:
    return int.from_bytes(file.read(4), "little")


class MDLImporterOperator(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    bl_idname = "pogo_blend.import_mdl"
    bl_label = "Import mesh from MDL (Gamestudio A8)"
    bl_description = "Imports meshes from MDL files."
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".mdl"

    filter_glob: bpy.props.StringProperty(
        default="*.mdl",
        options={"HIDDEN"},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    global_scale: bpy.props.FloatProperty(
        name="Scale Multiplier",
        description="Use this to scale on export",
        min=0.0,
        max=1000.0,
        default=1 / 50,
    )

    @classmethod
    def poll(cls, context):
        return True
        return pbu.get_preferences().mdl_importer

    def execute(self, context):
        try:
            import_mdl(context, self.filepath, self.global_scale)
        except BaseException as e:
            error_type = {"ERROR"}
            self.report(error_type, str(e))
            raise e  # NOTE: Only for debugging purposes
            return {"CANCELLED"}
        else:
            return {"FINISHED"}


def register():
    bpy.utils.register_class(MDLImporterOperator)


def unregister():
    bpy.utils.unregister_class(MDLImporterOperator)
