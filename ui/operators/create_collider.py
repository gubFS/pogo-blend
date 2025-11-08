import bpy
from mathutils import Vector


def create_collider(obj) -> bpy.types.Object:
    context = bpy.context
    scene = context.scene

    # note context for cleanup
    c_camera = scene.camera
    c_resolution = (scene.render.resolution_x, scene.render.resolution_y)
    c_collection = context.collection

    # select obj
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj

    # add camera
    bpy.ops.object.camera_add(
        location=obj.location, rotation=(1.570796, 0, 0), scale=(1, 1, 1)
    )
    camera = context.object
    camera.data.type = "ORTHO"
    scene.camera = camera
    # find the real bounding box without rotation
    bottom_left = Vector(obj.bound_box[0])
    top_right = Vector(obj.bound_box[0])
    for vec in obj.bound_box:
        vec = Vector(vec)
        vec.rotate(obj.matrix_world.to_euler())
        vec *= obj.matrix_world.to_scale()
        bottom_left.x = min(bottom_left.x, vec.x)
        bottom_left.y = min(bottom_left.y, vec.y)
        bottom_left.z = min(bottom_left.z, vec.z)
        top_right.x = max(top_right.x, vec.x)
        top_right.y = max(top_right.y, vec.y)
        top_right.z = max(top_right.z, vec.z)
    diff = top_right - bottom_left
    x = int(diff[0] * 100)
    y = int(diff[2] * 100)
    scale = max(diff[0], diff[2]) + 1.0
    scene.render.resolution_x = x
    scene.render.resolution_y = y
    camera.data.ortho_scale = scale
    camera.location[1] += bottom_left[1] - 1.0

    # create the grease pencil
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    context.view_layer.objects.active = obj
    bpy.ops.object.grease_pencil_add(type="LINEART_OBJECT")
    pencil = context.object

    # configure lineart
    lineart = pencil.modifiers["Lineart"]
    lineart.silhouette_filtering = "INDIVIDUAL"
    lineart.use_crease = False
    lineart.use_intersection = False

    # convert to mesh and extrude collider
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.transform.resize(value=(1, 0, 1))
    bpy.ops.mesh.edge_face_add()
    bpy.ops.mesh.delete(type="ONLY_FACE")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 2, 0)})
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.normals_make_consistent()
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
    collider = context.object
    collider.location[1] = 0
    collider.name = f"{obj.name}_col"
    collider.data.name = f"{obj.name}_col"
    collider.users_collection[0].objects.unlink(collider)
    obj.users_collection[0].objects.link(collider)

    # cleanup
    camera_data = camera.data
    bpy.data.objects.remove(camera)
    bpy.data.cameras.remove(camera_data)

    scene.camera = c_camera
    scene.render.resolution_x = c_resolution[0]
    scene.render.resolution_y = c_resolution[1]

    return collider


class CreatePogoCollider(bpy.types.Operator):
    bl_idname = "pogo_blend.create_collider"
    bl_label = "Create a Pogostuck Collider"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = context.selected_objects
        if not objs:
            self.report({"ERROR"}, "No objects selected")
            return {"CANCELLED"}
        for obj in objs:
            create_collider(obj)
        return {"FINISHED"}


def register():
    bpy.utils.register_class(CreatePogoCollider)


def unregister():
    bpy.utils.unregister_class(CreatePogoCollider)
