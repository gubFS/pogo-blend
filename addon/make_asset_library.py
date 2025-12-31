from pathlib import Path

import bpy

from . import pogo_blend_utils as pbu
from .export_import.mdl_importer.mdl_importer_operator import import_mdl

config = {
    "models": [
        {
            "filename": "anvil.mdl",
            "material": "anvil_mat",
            "flags": [
                "flag_unlit",
            ],
            "mark_materials": True,
        },
        {
            "filename": "appA_slime3.mdl",
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
            "material": "cloud_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "cloud2.mdl",
            "material": "cloud_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "dode.mdl",
            "material": "fruit_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "dungeonWheel1.mdl",
            "material": "monoWheel_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "m3Thorn1.mdl",
            "material": "monoSpikes_mat",
            "action": "monolithThorn_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
        },
        {
            "filename": "moai.mdl",
            "action": "moai_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
        },
        {
            "filename": "modeBlock0.mdl",
            "material": "fruitTex_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "mushroomFly1.mdl",
            "material": "fruitTexB_mat",
            "action": "mushroom_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
        },
        {
            "filename": "mushroomFly2.mdl",
            "material": "fruitTexB_mat",
            "action": "mushroom_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
        },
        {
            "filename": "mushroomTree2.mdl",
            "material": "fruitBNOSM_mat",
            "action": "mushroom_act",
            "flags": [
                "flag_unlit",
                "flag_polygon",
            ],
        },
        {
            "filename": "pencil.mdl",
            "material": "pencil_mat",
            "flags": [
                "flag_unlit",
            ],
        },
        {
            "filename": "startFinishM.mdl",
            "material": "startFinish_mat",
            "flags": [
                "flag_unlit",
                "flag_transparent",
            ],
            "ambient": 100.0,
        },
        {
            "filename": "startingCurve.mdl",
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
    ],
    "textures": [
        "Models/colorPalette.tga",
        "Textures/broBlock.tga",
        "Textures/metalshutter1.tga",
        "Textures/pixelBricks.tga",
    ],
}


MODEL_CATALOG = "cb8ca03c-b0b7-495a-a4fb-4c29c2d25432"
TEXTURE_CATALOG = "d95305f4-7ef9-4fe3-a98c-073a52a7dfce"


def make_asset_library(context, filepath: str):
    custom_maps_path = pbu.get_preferences().custom_maps_path
    if custom_maps_path == "":
        return
    base_map = Path(custom_maps_path).joinpath("BaseMap")
    if base_map == None or base_map == "":
        return

    assets = []
    for mdl in config["models"]:
        path = Path(base_map).joinpath("Models", mdl["filename"])
        import_mdl(context, path, 1/50)
        obj = context.object
        obj.pogo_entity
        obj.pogo_entity.filename_override = mdl["filename"]
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

        assets.append((obj, MODEL_CATALOG))

        if "mark_materials" in mdl and mdl["mark_materials"]:
            for mat in obj.material_slots:
                assets.append((mat.material, TEXTURE_CATALOG))

    for texture in config["textures"]:
        texture_path = Path(base_map).joinpath(texture)
        mat = bpy.data.materials.new(name=texture_path.stem)
        mat.use_nodes = True
        image_node = mat.node_tree.nodes.new(type="ShaderNodeTexImage")
        img = bpy.data.images.load(str(texture_path))
        image_node.image = img
        disp = mat.node_tree.nodes["Principled BSDF"].inputs[0]
        mat.node_tree.links.new(disp, image_node.outputs[0])
        assets.append((mat, TEXTURE_CATALOG))

    for asset, catalog in assets:
        asset.asset_mark()
        asset.asset_generate_preview()
        ad = asset.asset_data
        ad.author = "Henrik Felix Pohl"
        ad.copyright = "Henrik Felix Pohl"
        ad.description = "Only to be used for the purposes of making Pogostuck Custom Maps"
        ad.license = "Only to be used for the purposes of making Pogostuck Custom Maps"
        ad.catalog_id = catalog

        bpy.app.timers.register(lambda: go_back(filepath))


def go_back(filepath: str):
    if bpy.app.is_job_running('RENDER_PREVIEW'):
        return 0.1
    asset_libary_dir = Path(__file__).parent.joinpath("pogo_blend_asset_library")
    pogostuck = Path(asset_libary_dir).joinpath("pogostuck.blend")
    bpy.ops.wm.save_mainfile(filepath=str(pogostuck))
    if filepath != "":
        bpy.ops.wm.open_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.read_homefile()


class MakeAssetLibraryOperator(bpy.types.Operator):
    bl_idname = "pogo_blend.make_asset_library"
    bl_label = "Make asset library"
    bl_description = "Make asset library"
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context) -> bool:
        asset_libary_dir = Path(__file__).parent.joinpath("pogo_blend_asset_library")
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
            bpy.ops.wm.save_mainfile()
        filepath = bpy.data.filepath
        bpy.ops.wm.read_homefile(app_template="", use_empty=True)
        bpy.app.timers.register(lambda: make_asset_library(context, filepath), first_interval=0.01)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MakeAssetLibraryOperator)


def unregister():
    bpy.utils.unregister_class(MakeAssetLibraryOperator)
