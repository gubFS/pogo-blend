# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import bpy

from .. import pogo_blend_utils as pbu
from ..export_import.mdl_importer.mdl_importer import import_mdl

config = {
    "models": [
        {
            "filename": "anvil.mdl",
            "name": "Anvil",
            "material": "anvil_mat",
            "flags": [
                "flag_unlit",
            ],
            "mark_materials": True,
        },
        {
            "filename": "appA_slime3.mdl",
            "name": "Slime",
            "material": "pinkSap_mat",
            "action": "pinkSap_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
                "flag_transparent",
            ],
            "mark_materials": True,
        },
        {
            "filename": "cloud1.mdl",
            "name": "Cloud1",
            "material": "cloud_mat",
            "flags": [
                "flag_unlit",
            ],
            "reuse_materials": "anvil.mdl",
        },
        {
            "filename": "cloud2.mdl",
            "name": "Cloud2",
            "material": "cloud_mat",
            "flags": [
                "flag_unlit",
            ],
            "reuse_materials": "anvil.mdl",
        },
        {
            "filename": "dode.mdl",
            "name": "Grape",
            "material": "fruit_mat",
            "flags": [
                "flag_unlit",
            ],
            "reuse_materials": "anvil.mdl",
        },
        {
            "filename": "dungeonWheel1.mdl",
            "name": "Wheel",
            "material": "monoWheel_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "m3Thorn1.mdl",
            "name": "Thorns",
            "material": "monoSpikes_mat",
            "action": "monolithThorn_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
            "reuse_materials": "anvil.mdl",
        },
        {
            "filename": "moai.mdl",
            "name": "Moai",
            "action": "moai_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
            "reuse_materials": "anvil.mdl",
        },
        {
            "filename": "modeBlock0.mdl",
            "name": "Mode Block",
            "material": "fruitTex_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "mushroomFly1.mdl",
            "name": "Mushroom1",
            "material": "fruitTexB_mat",
            "action": "mushroom_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
        },
        {
            "filename": "mushroomFly2.mdl",
            "name": "Mushroom2",
            "material": "fruitTexB_mat",
            "action": "mushroom_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
            "reuse_materials": "mushroomFly1.mdl",
        },
        {
            "filename": "mushroomTree2.mdl",
            "name": "Brown Mushroom",
            "material": "fruitBNOSM_mat",
            "action": "mushroom_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
                "flag_5",
            ],
            "reuse_materials": "anvil.mdl",
        },
        {
            "filename": "pencil.mdl",
            "name": "Pencil",
            "material": "pencil_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "startFinishM.mdl",
            "name": "Finish Line",
            "material": "startFinish_mat",
            "flags": [
                "flag_unlit",
                "flag_transparent",
            ],
            "skills": {
                "skill_1": 1.0,
            },
            "action": "skillset_act",
            "ambient": 100.0,
        },
        {
            "filename": "startingCurve.mdl",
            "name": "Start Line",
            "material": "startFinish_mat",
            "flags": [
                "flag_unlit",
                "flag_transparent",
            ],
            "skills": {
                "skill_1": 1.0,
            },
            "action": "skillset_act",
            "ambient": 100.0,
            "reuse_materials": "startFinishM.mdl",
        },
    ],
    "textures": [
        {
            "filename": "Models/colorPalette.tga",
            "name": "Color Palette",
        },
        {
            "filename": "Textures/broBlock.tga",
            "name": "Bro Block",
        },
        {
            "filename": "Textures/metalshutter1.tga",
            "name": "Metal Shutter",
            "include_author": False,
        },
        {
            "filename": "Textures/pixelBricks.tga",
            "name": "Pixel Bricks",
        },
    ],
}


MODEL_CATALOG = "cb8ca03c-b0b7-495a-a4fb-4c29c2d25432"
TEXTURE_CATALOG = "d95305f4-7ef9-4fe3-a98c-073a52a7dfce"


def make_asset_library(context, filepath: str):
    custom_maps_path = pbu.get_preferences().custom_maps_path
    if custom_maps_path == "":
        return
    base_map = Path(custom_maps_path).joinpath("BaseMap")
    if base_map is None or base_map == "":
        return

    assets = []
    materials = {}
    for mdl in config["models"]:
        path = Path(base_map).joinpath("Models", mdl["filename"])
        import_mdl(context, path, 1 / 50)
        obj = context.object
        obj.pogo_entity
        obj.pogo_entity.filename_override = mdl["filename"]
        if "name" in mdl:
            obj.name = mdl["name"]
        if "material" in mdl:
            try:
                obj.pogo_entity.material = mdl["material"]
            except TypeError:
                obj.pogo_entity.material_override = mdl["material"]
        if "action" in mdl:
            try:
                obj.pogo_entity.action1 = mdl["action"]
            except TypeError:
                obj.pogo_entity.action_override = mdl["action"]
        if "flags" in mdl:
            for flag in mdl["flags"]:
                obj.pogo_entity[flag] = True
        if "skills" in mdl:
            for skill, value in mdl["skills"].items():
                obj.pogo_entity[skill] = value
        if "ambient" in mdl:
            obj.pogo_entity.ambient = mdl["ambient"]

        assets.append((mdl, obj, MODEL_CATALOG))

        if "mark_materials" in mdl and mdl["mark_materials"]:
            for mat in obj.material_slots:
                mat = mat.material
                match mat.name:
                    case "gradientTest":
                        mat.name = "Gradient"
                    case "slimeBubbles":
                        mat.name = "Slime Bubbles"
                assets.append((mdl, mat, TEXTURE_CATALOG))

        if "reuse_materials" not in mdl or mdl["reuse_materials"] == "":
            materials[mdl["filename"]] = [material_slot.material for material_slot in obj.material_slots]
        else:
            reused_materials = materials.get(mdl["reuse_materials"], [])
            for i, material_slot in enumerate(obj.material_slots):
                if i >= len(reused_materials):
                    break
                material_slot.material = reused_materials[i]
    bpy.ops.outliner.orphans_purge()  # get rid of the images generated on reused materials

    for texture in config["textures"]:
        texture_path = Path(base_map).joinpath(texture["filename"])
        mat = bpy.data.materials.new(name=texture_path.stem)
        mat.use_nodes = True
        image_node = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
        img = bpy.data.images.load(str(texture_path))
        image_node.image = img
        disp = mat.node_tree.nodes["Principled BSDF"].inputs[0]
        mat.node_tree.links.new(disp, image_node.outputs[0])
        if "name" in texture:
            mat.name = texture["name"]
        assets.append((texture, mat, TEXTURE_CATALOG))

    for conf, asset, catalog in assets:
        asset.asset_mark()
        asset.asset_generate_preview()
        ad = asset.asset_data
        if "include_author" not in conf or conf["include_author"]:
            ad.author = "Superku"
            ad.copyright = "Superku"
        ad.description = ""
        ad.license = "Only to be used for the purposes of making Pogostuck Custom Maps"
        ad.catalog_id = catalog

    view_3d_area = next((area for area in bpy.context.screen.areas if area.type == 'VIEW_3D'), None)
    if view_3d_area is not None:
        view_3d_area.ui_type = 'ASSETS'
    bpy.app.timers.register(lambda: set_library(view_3d_area))  # the area params takes a frame to initialize so wait for that
    bpy.app.timers.register(lambda: go_back(filepath))


def set_library(area):
    area.spaces.active.params.asset_library_reference = 'LOCAL'


def go_back(filepath: str):
    bpy.context.window.cursor_set('WAIT')
    if bpy.app.is_job_running('RENDER_PREVIEW'):
        return 0.1
    asset_libary_dir = Path(__file__).parent
    pogostuck = Path(asset_libary_dir).joinpath("pogostuck.blend")
    bpy.ops.wm.save_mainfile(filepath=str(pogostuck))
    bpy.context.window.cursor_set('DEFAULT')
    if filepath != "":
        bpy.ops.wm.open_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.read_homefile()


class MakeAssetLibraryOperator(bpy.types.Operator):
    bl_idname = "pogo_blend.make_asset_library"
    bl_label = "Make asset library"
    bl_description = "Make asset library"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context) -> bool:
        asset_libary_dir = Path(__file__).parent
        pogostuck = Path(asset_libary_dir).joinpath("pogostuck.blend")
        if pogostuck.exists():
            return False

        custom_map_dir = Path(pbu.get_preferences().custom_maps_path)
        if not custom_map_dir.exists():
            return False
        basemap = Path(custom_map_dir).joinpath("BaseMap")
        if not basemap.exists():
            return False

        return True

    def execute(self, context):
        if bpy.data.is_dirty:
            if not bpy.data.is_saved:
                self.report({'ERROR_INVALID_CONTEXT'}, "Save your current Blender file first, or create an empty one with no changes")
                return {'CANCELLED'}
            bpy.ops.wm.save_mainfile()
        filepath = bpy.data.filepath
        bpy.ops.wm.read_homefile(app_template="", use_empty=True)
        bpy.app.timers.register(lambda: make_asset_library(context, filepath), first_interval=0.01)
        return {"FINISHED"}


classes = (MakeAssetLibraryOperator,)
