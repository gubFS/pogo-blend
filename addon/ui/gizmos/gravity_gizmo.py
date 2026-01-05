import math

import bpy
from mathutils import Matrix, Vector

custom_shape_verts = (
    (-0.3, 0, 2),
    (0.3, 0, 2),
    (0, 0, 20),
    (-0.3, 0, 2),
    (0.3, 0, 2),
    (0, 0, 0),
)


class PogoGravityArrow(bpy.types.Gizmo):
    bl_idname = "VIEW3D_GT_pogo_gravity_arrow"
    __slots__ = ("custom_shape",)

    def _update_offset_matrix(self):
        obj = bpy.context.object
        power = obj.pogo_reigon.gravity_power / 999
        power = 1 - ((1 - power) ** 3)
        self.matrix_offset = Matrix.Rotation(math.radians(obj.pogo_reigon.gravity_angle) + 3.14, 4, "Y") @ Matrix.Scale(power * 0.4, 4, Vector((0, 0, 1)))

    def draw(self, context):
        self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape)

    def draw_select(self, context, select_id):
        self._update_offset_matrix()
        self.draw_custom_shape(self.custom_shape, select_id=select_id)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = self.new_custom_shape('TRIS', custom_shape_verts)


class GravityReigonGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_pogo_gravity_group"
    bl_label = "PogoBlend Gravity Arrow"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and "pogo_reigon" in obj and obj.pogo_reigon.reigon_type == "gravityReg_"

    def setup(self, context):
        gz = self.gizmos.new(PogoGravityArrow.bl_idname)

        gz.color = 1.0, 0.3, 1.0
        gz.alpha = 0.2
        gz.color_highlight = gz.color
        gz.alpha_highlight = gz.alpha

        self.gz = gz

    def refresh(self, context):
        obj = context.object
        self.gz.matrix_basis = obj.matrix_world.normalized()


def register():
    bpy.utils.register_class(PogoGravityArrow)
    bpy.utils.register_class(GravityReigonGroup)


def unregister():
    bpy.utils.unregister_class(PogoGravityArrow)
    bpy.utils.unregister_class(GravityReigonGroup)
