import bpy

class PogoBlendPrefrences(bpy.types.AddonPreferences):
    bl_idname = __package__

    mdl_importer: bpy.props.BoolProperty(
        default=False,
        name="MDL Importer",
        description="Add mdl impoterter to importers",
    )
    mdl_exporter:bpy.props.BoolProperty(
        default=False,
        name="MDL Exporter",
        description="Add mdl exporter to exporters",
    )

    custom_maps_path: bpy.props.StringProperty(
        default="",
        name="Custom Maps directory",
        description="The path to the directory where custom maps will be put",
    )
    map_scale: bpy.props.FloatProperty(
        default=50.0,
        name="Map Scale",
        description="The default map scale. 50 means the default Cube is roughly half the size of the Pogo Dude"
    )

    show_overrides: bpy.props.BoolProperty(
        default=False,
        name="Enable overrides",
        description="Adds a panel to entities that shows all editiable fields. Not relevant in most normal use cases"
    )

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "mdl_importer")
        layout.prop(self, "mdl_exporter")
        layout.prop(self, "custom_maps_path")
        layout.prop(self, "map_scale")
        layout.prop(self, "show_overrides")

def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences

def register():
    bpy.utils.register_class(PogoBlendPrefrences)

def unregister():
    bpy.utils.unregister_class(PogoBlendPrefrences)
