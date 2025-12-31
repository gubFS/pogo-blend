import platform
from pathlib import Path

import bpy


class SelectCustomMapsDir(bpy.types.Operator):
    bl_idname = "pogo_blend.select_custom_maps_dir"
    bl_label = "Select the Custom Maps folder"
    bl_options = {"REGISTER"}

    directory: bpy.props.StringProperty(
        name="Custom Maps folder",
        description="New maps will be created in the selected folder",
        subtype="DIR_PATH",
    )

    # Filters folders
    filter_folder: bpy.props.BoolProperty(default=True, options={"HIDDEN"})

    def execute(self, context):
        get_preferences().custom_maps_path = self.directory
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        # Tells Blender to hang on for the slow user input
        return {"RUNNING_MODAL"}


class PogoBlendPrefrences(bpy.types.AddonPreferences):
    bl_idname = __package__

    mdl_importer: bpy.props.BoolProperty(
        default=False,
        name="MDL Importer",
        description="Add mdl impoterter to importers",
    )
    mdl_exporter: bpy.props.BoolProperty(
        default=False,
        name="MDL Exporter",
        description="Add mdl exporter to exporters",
    )

    custom_maps_path: bpy.props.StringProperty(
        default="",
        name="Custom Maps folder",
        description="The path to the folder where custom maps will be put",
    )
    map_scale: bpy.props.FloatProperty(
        default=50.0,
        name="Map Scale",
        description="The default map scale. 50 means the default Cube is roughly half the size of the Pogo Dude",
    )

    show_overrides: bpy.props.BoolProperty(
        default=False,
        name="Enable overrides",
        description="Adds a panel to entities that shows all editiable fields. Not relevant in most normal use cases",
    )

    build_on_save: bpy.props.BoolProperty(
        default=False,
        name="Build on save",
        description="Builds the Custom Map whenever the Blender file is saved. Reload Blender to apply",
    )

    # show_all_materials: bpy.props.BoolProperty(
    #     default=False,
    #     name="Show all materials",
    #     description="Some irrelevant materials are hidden, choose to show them here",
    # )
    #
    # show_all_actions: bpy.props.BoolProperty(
    #     default=False,
    #     name="Show all actions",
    #     description="Some irrelevant actions are hidden, choose to show them here",
    # )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "mdl_importer")
        layout.prop(self, "mdl_exporter")
        row = layout.row()
        row.prop(self, "custom_maps_path")
        row.operator("pogo_blend.select_custom_maps_dir", text="", icon="FILE_FOLDER")
        layout.prop(self, "map_scale")
        layout.prop(self, "show_overrides")
        layout.prop(self, "build_on_save")
        if bpy.ops.pogo_blend.make_asset_library.poll():
            layout.operator("pogo_blend.make_asset_library")
        # layout.prop(self, "show_all_materials")
        # layout.prop(self, "show_all_actions")


def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences


def register():
    bpy.utils.register_class(SelectCustomMapsDir)
    bpy.utils.register_class(PogoBlendPrefrences)

    cmp = get_preferences().custom_maps_path
    if cmp == None or cmp == "":
        cmp = next(Path("/").rglob("steamapps/common/Pogostuck/CustomMaps"), "")
    get_preferences().custom_maps_path = str(cmp)


def unregister():
    bpy.utils.unregister_class(SelectCustomMapsDir)
    bpy.utils.unregister_class(PogoBlendPrefrences)
