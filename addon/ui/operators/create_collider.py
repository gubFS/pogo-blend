import copy

import bpy
from mathutils import Vector


def create_collider(obj, extrude_length=4.0) -> bpy.types.Object:
    area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
    with bpy.context.temp_override(area=area):
        context = bpy.context
        scene = context.scene

        # note context for cleanup
        c_camera = scene.camera
        c_resolution = (scene.render.resolution_x, scene.render.resolution_y)
        c_cursor = scene.cursor.location.copy()

        # select obj
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        context.view_layer.objects.active = obj

        # add camera
        bpy.ops.object.camera_add(
            location=obj.matrix_world.translation,
            rotation=(1.570796, 0, 0),
            scale=(1, 1, 1),
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
        lineart_data = pencil.data
        lineart_material = lineart.target_material

        # convert to mesh and extrude collider
        bpy.ops.object.convert(target="MESH")
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.transform.resize(value=(1, 0, 1))
        bpy.ops.mesh.edge_face_add()
        bpy.ops.mesh.delete(type="ONLY_FACE")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.extrude_region_move(
            TRANSFORM_OT_translate={"value": (0, extrude_length, 0)}
        )
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.normals_make_consistent()

        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
        bpy.ops.view3d.snap_cursor_to_active()
        scene.cursor.location.x = obj.matrix_world.translation.x
        scene.cursor.location.z = obj.matrix_world.translation.z
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR", center="BOUNDS")

        collider_object = context.object
        collider_mesh = collider_object.data
        collider = create_collider_object(obj, collider_mesh)
        bpy.data.objects.remove(collider_object, do_unlink=True)

        # cleanup
        camera_data = camera.data
        bpy.data.materials.remove(lineart_material, do_unlink=True)
        bpy.data.grease_pencils_v3.remove(lineart_data, do_unlink=True)
        bpy.data.objects.remove(camera, do_unlink=True)
        bpy.data.cameras.remove(camera_data, do_unlink=True)

        scene.camera = c_camera
        scene.render.resolution_x = c_resolution[0]
        scene.render.resolution_y = c_resolution[1]

        scene.cursor.location = c_cursor

        return collider


def create_collider_object(obj, data=None):
    collider = bpy.data.objects.new(f"{obj.name}_col", data)
    if data != None:
        collider.data.name = collider.name

    collider.matrix_world.translation = obj.matrix_world.translation
    collider.matrix_world.translation[1] = 0

    obj.users_collection[0].objects.link(collider)

    collider.pogo_entity
    if "pogo_entity" in obj:
        collider.pogo_entity.copy_from(obj.pogo_entity)
    collider.pogo_entity.flag_passable = False
    collider.pogo_entity.flag_invisible = True
    collider.pogo_entity.flag_unlit = True
    collider.pogo_entity.flag_polygon = True
    collider.pogo_entity.flag_auto_collision = False
    collider.pogo_entity.ambient = 0.0
    collider.pogo_entity.albedo = 50.0
    collider.pogo_entity.material = "ndef"

    return collider


class CreatePogoCollider(bpy.types.Operator):
    bl_idname = "pogo_blend.create_collider"
    bl_label = "Create a Pogostuck Collider"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = filter(lambda obj: obj.type == "MESH", context.selected_objects)
        objs = list(objs)
        if not objs:
            self.report({"ERROR"}, "No mesh objects selected")
            return {"CANCELLED"}
        for obj in objs:
            create_collider(obj)
        return {"FINISHED"}


def menu_func(self, context):
    self.layout.operator(CreatePogoCollider.bl_idname, text="Create a Pogostuck Collider")


def register():
    bpy.utils.register_class(CreatePogoCollider)
    bpy.types.TOPBAR_MT_file_export.append(menu_func)


def unregister():
    bpy.utils.unregister_class(CreatePogoCollider)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func)
