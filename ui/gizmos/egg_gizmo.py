# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import math

import bpy
from mathutils import Matrix

from ... import pogo_blend_preferences as pbu

BOUNDS_STRETCH = 4096

EGG_RESPAWN_MIN_Z = 8710

EGG_PLAYER_RESPAWN_MIN_X = 10780
EGG_PLAYER_RESPAWN_MIN_Z = 7995

EGG_SPAWN_X = 13100
EGG_SPAWN_Z = 10500

EGG_FIREWORKS_MIN_Z = 8890
EGG_FIREWORKS_MAX_Z = 9920
EGG_FIREWORKS_MAX_X = 11770


class PogoLineStripGizmo(bpy.types.Gizmo):
    __slots__ = ("custom_shape", "matrix")

    def draw(self, context):
        self.draw_custom_shape(self.custom_shape, matrix=self.matrix)

    def _get_matrix(self):
        return Matrix.Identity()

    def _get_verts(self):
        return []

    def _get_color(self):
        return (1.0, 1.0, 1.0)

    def setup(self):
        if not hasattr(self, "custom_shape"):
            self.custom_shape = self.new_custom_shape('LINE_STRIP', self._get_verts())
        if not hasattr(self, "matrix"):
            self.matrix = self._get_matrix()
        self.color = self._get_color()


class PogoEggBounds(PogoLineStripGizmo):
    bl_idname = "VIEW3D_GT_pogo_egg_bounds"

    def _get_matrix(self):
        map_scale = pbu.get_preferences().map_scale
        return Matrix.LocRotScale(
            (EGG_PLAYER_RESPAWN_MIN_X / map_scale, 0, EGG_RESPAWN_MIN_Z / map_scale),
            None,
            (BOUNDS_STRETCH for _ in range(3)),
        )

    def _get_verts(self):
        return [(-1, 0, 0), (1, 0, 0)]

    def _get_color(self):
        return (1.0, 0, 0)


class PogoEggPlayerBounds(PogoLineStripGizmo):
    bl_idname = "VIEW3D_GT_pogo_egg_player_bounds"

    def _get_matrix(self):
        map_scale = pbu.get_preferences().map_scale
        return Matrix.LocRotScale(
            (EGG_PLAYER_RESPAWN_MIN_X / map_scale, 0, EGG_PLAYER_RESPAWN_MIN_Z / map_scale),
            None,
            (BOUNDS_STRETCH for _ in range(3)),
        )

    def _get_verts(self):
        return [(0, 0, 1), (0, 0, 0), (1, 0, 0)]

    def _get_color(self):
        return (0, 1.0, 0)


class PogoEggSpawn(PogoLineStripGizmo):
    bl_idname = "VIEW3D_GT_pogo_egg_spawn"

    def _get_matrix(self):
        map_scale = pbu.get_preferences().map_scale
        return Matrix.LocRotScale(
            (EGG_SPAWN_X / map_scale, 0, EGG_SPAWN_Z / map_scale),
            None,
            (0.5 for _ in range(3)),
        )

    def _get_verts(self):
        verts = 4
        return [(math.sin((i / verts) * math.tau), 0, math.cos((i / verts) * math.tau)) for i in range(verts + 1)]

    def _get_color(self):
        return (1.0, 0, 0)


class PogoEggFireworks(PogoLineStripGizmo):
    bl_idname = "VIEW3D_GT_pogo_egg_fireworks"

    def _get_matrix(self):
        map_scale = pbu.get_preferences().map_scale
        delta_z = EGG_FIREWORKS_MAX_Z - EGG_FIREWORKS_MIN_Z
        return Matrix.LocRotScale(
            (EGG_FIREWORKS_MAX_X / map_scale, 0, (EGG_FIREWORKS_MIN_Z + delta_z * 0.5) / map_scale),
            None,
            (BOUNDS_STRETCH, 1, delta_z * 0.5 / map_scale),
        )

    def _get_verts(self):
        return [(-1, 0, 1), (0, 0, 1), (0, 0, -1), (-1, 0, -1)]

    def _get_color(self):
        return (1.0, 1.0, 0)


class PogoEggGroup(bpy.types.GizmoGroup):
    bl_idname = "OBJECT_GGT_pogo_egg_group"
    bl_label = "PogoBlend Egg Gizmo Group"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SCALE'}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and "pogo_entity" in obj and obj.pogo_entity.action_override == "egg_act"

    def setup(self, context):
        for gizmo in [PogoEggBounds, PogoEggPlayerBounds, PogoEggSpawn, PogoEggFireworks]:
            self.gizmos.new(gizmo.bl_idname)


classes = (
    PogoEggBounds,
    PogoEggPlayerBounds,
    PogoEggSpawn,
    PogoEggFireworks,
    PogoEggGroup,
)
