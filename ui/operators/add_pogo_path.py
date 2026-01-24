import bpy


class AddPogoPath(bpy.types.Operator):
    bl_idname = "pogo_blend.add_pogo_path"
    bl_label = "Add Pogo Path"
    bl_description = "Adds a Pogo Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.curve.primitive_nurbs_path_add(enter_editmode=True)
        obj = context.object
        path = obj.data

        obj.name = "PogoPath"
        spline = path.splines[0]
        spline.type = 'POLY'
        bpy.ops.curve.select_all(action='SELECT')
        spline.points[0].select = False
        spline.points[-1].select = False
        bpy.ops.curve.delete(type='VERT')
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.rotation_euler[0] = 1.570796
        obj.pogo_path

        return {'FINISHED'}


classes = (AddPogoPath,)
