# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy


class PogoPath(bpy.types.PropertyGroup):
    name_override: bpy.props.StringProperty(default="")


classes = (PogoPath,)


def register():
    bpy.types.Object.pogo_path = bpy.props.PointerProperty(type=PogoPath)


def unregister():
    del bpy.types.Object.pogo_path
