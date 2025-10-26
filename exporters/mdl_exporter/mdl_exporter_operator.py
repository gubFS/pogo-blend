import bpy
from .mdl_exporter import MDLExporter

def export_to_mdl(context, filepath, only_selected, scale):
    objects = context.scene.collection.all_objects
    if only_selected: objects = context.selected_objects

    objs = []
    for obj in objects:
        if obj.type == 'MESH':
            objs.append(obj)

    print(f"Exporting {len(objs)} objects to mdl")
    MDLExporter(filepath, objs, scale).export()

# ExportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper

class MDLExporterOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "pogo_blend.mdl_export"
    bl_label = "Export meshes to MDL (Gamestudio A8)"
    bl_description = "Exports meshes to MDL files. Does not support bones."

    filename_ext = ".mdl"

    filter_glob: bpy.props.StringProperty(
        default="*.mdl",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned to the class instance from the operator settings before calling.
    selected_only: bpy.props.BoolProperty(
        name="Export selected only",
        default=True,
    )

    global_scale: bpy.props.FloatProperty(
            name="Scale Multiplier",
            description="Use this to scale on export",
            min=0.0, max=1000.0,
            default=50.0,
    )

    def execute(self, context):
        try: export_to_mdl(context, self.filepath, self.selected_only, self.global_scale)
        except BaseException as e:
            error_type = {'ERROR'}
            self.report(error_type, str(e))
            raise e
            return {'CANCELLED'}
        else: return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(MDLExporterOperator.bl_idname, text="MDL (.mdl)")

# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(MDLExporterOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(MDLExporterOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

