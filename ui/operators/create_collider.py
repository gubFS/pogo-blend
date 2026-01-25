import bpy
from mathutils import Vector

from ... import pogo_blend_utils as pbu


class CreateColliderContext:
    def __enter__(self):
        screen, area = pbu.get_view_3d_context()
        self.temp_override = bpy.context.temp_override(screen=screen, area=area)
        self.temp_override.__enter__()

        context = bpy.context
        scene = context.scene

        self.c_camera = scene.camera
        self.c_resolution = (scene.render.resolution_x, scene.render.resolution_y)
        self.c_cursor = scene.cursor.location.copy()
        self.c_selected_objects = context.selected_objects
        self.c_active_object = context.view_layer.objects.active

        # add camera
        bpy.ops.object.camera_add(
            location=(0, 0, 0),
            rotation=(1.570796, 0, 0),
            scale=(1, 1, 1),
        )
        self.camera = context.object
        self.camera.data.type = 'ORTHO'
        scene.camera = self.camera

        return self

    def create_collider(self, obj, extrude_length=4.0) -> bpy.types.Object:
        context = bpy.context
        scene = context.scene

        # select obj
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj

        # preprocessing
        bpy.ops.object.convert(target='MESH', keep_original=True, merge_customdata=False)
        obj = context.object
        obj_mesh = obj.data
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.001)
        bpy.ops.mesh.dissolve_limited(angle_limit=0.001)
        bpy.ops.object.editmode_toggle()

        # find the real bounding box without rotation
        bottom_left = Vector((0, 0, 0))
        top_right = Vector((0, 0, 0))
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
        x = int(diff.x * 100)
        y = int(diff.z * 100)
        scale = max(diff.x, diff.z) + 1.0
        center = (top_right + bottom_left) * 0.5
        center_world = obj.matrix_world.translation + center
        scene.render.resolution_x = x
        scene.render.resolution_y = y
        self.camera.data.ortho_scale = scale
        self.camera.location = center_world
        self.camera.location.y += diff.y * -0.5 - 1.0

        # create the grease pencil
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        bpy.ops.object.grease_pencil_add(type='LINEART_OBJECT')
        pencil = context.object

        # configure lineart
        lineart = pencil.modifiers["Lineart"]
        lineart.silhouette_filtering = 'INDIVIDUAL'
        lineart.use_crease = False
        lineart.use_intersection = False
        lineart.use_back_face_culling = True
        lineart.use_clip_plane_boundaries = False
        lineart_data = pencil.data
        lineart_material = lineart.target_material

        # move the objects so no other object will occlude the outline
        self.camera.matrix_world.translation.y -= 1000
        obj.matrix_world.translation.y -= 1000

        # convert to mesh and extrude collider
        bpy.ops.object.convert(target='MESH')
        collider_object = context.object
        collider_mesh = collider_object.data

        self.camera.matrix_world.translation.y += 1000
        obj.matrix_world.translation.y += 1000
        collider_object.matrix_world.translation.y += 1000

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='VERT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.resize(value=(1, 0, 1))
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, extrude_length, 0)})
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.dissolve_limited(angle_limit=0.001)

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.view3d.snap_cursor_to_active()
        scene.cursor.location.x = obj.matrix_world.translation.x
        scene.cursor.location.z = obj.matrix_world.translation.z
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')

        collider = self.create_collider_object(obj, collider_mesh)

        # cleanup
        bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.meshes.remove(obj_mesh, do_unlink=True)
        bpy.data.objects.remove(collider_object, do_unlink=True)
        bpy.data.materials.remove(lineart_material, do_unlink=True)
        bpy.data.grease_pencils_v3.remove(lineart_data, do_unlink=True)

        return collider

    def create_collider_object(self, obj, data=None):
        collider = bpy.data.objects.new(f"{obj.name}_col", data)
        if data is not None:
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

    def __exit__(self, exc_type, exc_value, traceback):
        context = bpy.context
        scene = context.scene

        camera_data = self.camera.data
        bpy.data.objects.remove(self.camera, do_unlink=True)
        bpy.data.cameras.remove(camera_data, do_unlink=True)

        scene.camera = self.c_camera
        scene.render.resolution_x = self.c_resolution[0]
        scene.render.resolution_y = self.c_resolution[1]

        scene.cursor.location = self.c_cursor

        bpy.ops.object.select_all(action='DESELECT')
        for obj in self.c_selected_objects:
            obj.select_set(True)
        context.view_layer.objects.active = self.c_active_object

        self.temp_override.__exit__()


class CreatePogoCollider(pbu.AltOperator):
    bl_idname = "pogo_blend.create_collider"
    bl_label = "Create a Pogostuck Collider"
    bl_description = "Creates a collider around the selected objects, based on their sideview"
    bl_options = {'REGISTER', 'UNDO'}

    def poll_obj(self, obj):
        return obj.type == 'MESH'

    def execute(self, context):
        if len(self.objs) == 0:
            self.report({'ERROR'}, "No mesh objects selected")
            return {'CANCELLED'}

        with CreateColliderContext() as ctx:
            for obj in self.objs:
                ctx.create_collider(obj)

        return {'FINISHED'}


classes = (CreatePogoCollider,)
