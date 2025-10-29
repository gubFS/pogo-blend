import bpy
from .wmb_exporter import WMBExporter
from ..mdl_exporter.mdl_exporter import MDLExporter
from .wmb_objects.wmb_entity import *
from .wmb_objects.wmb_path import *
from .wmb_objects.wmb_info import WMBInfo
from .wmb_objects.wmb_reigon import WMBReigon
from ..gub_byte_array import GubByteArray
import os

def export_to_wmb(context, filepath, global_scale):
    custom_map_collection = None
    for collection in context.scene.collection.children:
        if collection.name == "CustomMap":
            custom_map_collection = collection
            break
    if custom_map_collection == None:
        raise ContextError("No Custom Map found, please name a collection 'CustomMap'")

    custom_map = custom_map_collection.custom_map
    if custom_map.spawn == None: raise ContextError("You MUST choose a spawn on the 'CustomMap' collection")
    spawn = custom_map.spawn
    if custom_map.path_progress == None: raise ContextError("You MUST choose a progrees path on the 'CustomMap' collection")
    path_progress = custom_map.path_progress
    if custom_map.start_line == None: raise ContextError("You MUST choose a starting line on the 'CustomMap' collection")
    start_line = custom_map.start_line

    dirpath = os.path.dirname(filepath)

    undo_map_scale_args = apply_map_scale(custom_map_collection, global_scale)
    try:
        wmb_objects = [
            WMBInfo(),
            PogoSpawn(spawn),
            PogoPathProgress(path_progress),
            PogoStartLine(start_line)
        ]
        meshes = {}
        paths = [path_progress]
        paths_to_add = []
        splits_to_add = {}
        for obj in custom_map_collection.objects:
            if obj in [spawn, path_progress, start_line]: continue
            match obj.type:
                case 'MESH':
                    try: obj["pogo_entity"]
                    except KeyError: continue
                    entity = WMBEntity(obj)
                    mesh = obj.to_mesh()
                    if obj.pogo_entity.filename_override == "":
                        if mesh not in meshes: meshes[mesh] = (entity, obj)
                    if obj.pogo_entity.path != None:
                        paths_to_add.append((entity, obj.pogo_entity.path))
                    wmb_objects.append(entity)
                case 'EMPTY':
                    try: obj["pogo_reigon"]
                    except KeyError: continue
                    if obj.pogo_reigon.reigon_type == 'ndef': continue
                    reigon = WMBReigon(obj)
                    if obj.pogo_reigon.reigon_type == 'CP_': splits_to_add[obj] = reigon
                    wmb_objects.append(reigon)
                case 'CURVE':
                    try: obj["pogo_path"]
                    except KeyError: continue
                    paths.append(obj)
                    wmb_objects.append(WMBPath(obj))

        for entity, path in paths_to_add:
            try: entity.path = paths.index(path) + 1
            except ValueError: pass

        for entity, obj in meshes.values():
            mdlpath = os.path.join(dirpath, entity.filename)
            if os.path.exists(mdlpath): print(f"WARNING: Overwriting '{mdlpath}'")
            MDLExporter(mdlpath, [obj], global_scale).export()
        export_splits(dirpath, custom_map, splits_to_add)
        WMBExporter(filepath, wmb_objects).export()

    finally:
        unapply_map_scale(*undo_map_scale_args)

def export_splits(dirpath, custom_map, splits):
    filepath = os.path.join(dirpath, "splitSetup.txt")
    bytes = GubByteArray()
    for i, split in enumerate(custom_map.splits.values()):
        split = split.split_reigon
        splits[split].name += str(i)
        bytes.store_string(f"{split.name}\n")
    with open(filepath, 'wb') as f:
        f.write(bytes)

def apply_map_scale(custom_map_collection, scale):
    layer_collection = bpy.context.view_layer.layer_collection.children['CustomMap']
    bpy.context.view_layer.active_layer_collection = layer_collection
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.add(type='EMPTY')
    scale_root = bpy.context.object

    objects = custom_map_collection.objects.values()
    objects.remove(scale_root)

    for obj in objects:
        obj.parent = scale_root
    scale_root.scale *= scale
    bpy.context.evaluated_depsgraph_get().update()

    return (objects, scale_root)

def unapply_map_scale(objects, scale_root):
    for obj in objects:
        obj.parent = None
    bpy.data.objects.remove(scale_root, do_unlink=True)

class ContextError(BaseException): pass

# ExportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper

class WMBExporterOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "pogo_blend.wmb_export"
    bl_label = "Export Project to WMB (Pogostuck Map)"
    bl_description = "Exports this project to a Pogostuck Custom Map project"

    filename_ext = ".wmb"

    filter_glob: bpy.props.StringProperty(
        default="*.wmb",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    global_scale: bpy.props.FloatProperty(
            name="Scale Multiplier",
            description="Use this to scale on export",
            min=0.0, max=1000.0,
            default=50.0,
    )

    # List of operator properties, the attributes will be assigned to the class instance from the operator settings before calling.
    # use_setting: BoolProperty(
    #     name="Example Boolean",
    #     description="Example Tooltip",
    #     default=True,
    # )
    #
    # type: EnumProperty(
    #     name="Example Enum",
    #     description="Choose between two items",
    #     items=(
    #         ('OPT_A', "First Option", "Description one"),
    #         ('OPT_B', "Second Option", "Description two"),
    #     ),
    #     default='OPT_A',
    # )

    def execute(self, context):
        try: export_to_wmb(context, self.filepath, self.global_scale)
        except BaseException as e:
            error_type = {'ERROR'}
            if type(e) is ContextError: error_type = {'ERROR_INVALID_CONTEXT'}
            self.report(error_type, str(e))
            raise e
            return {'CANCELLED'}
        else: return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(WMBExporterOperator.bl_idname, text="Pogostuck Custom Map")

# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(WMBExporterOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(WMBExporterOperator)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

