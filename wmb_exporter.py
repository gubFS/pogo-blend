import bpy
from .gub_byte_array import GubByteArray
from .wmb_objects.wmb_entity import *
from .wmb_objects.wmb_path import *
from .wmb_objects.wmb_info import WMBInfo

object_list_offset = 0
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

    pogo_objects = [
        PogoSpawn(spawn),
        PogoPathProgress(path_progress),
        PogoStartLine(start_line)
    ]
    for obj in custom_map_collection.objects:
        if obj in [spawn, path_progress, start_line]: continue
        try: obj["pogo_entity"]
        except KeyError:
            continue
        entity = WMBEntity(obj)
        entity.origin *= global_scale
        pogo_objects.append(entity)

    header = get_header()
    objects_header = GubByteArray()
    encoded_objects_array = [WMBInfo().to_bytes()]
    for obj in pogo_objects:
        encoded_objects_array.append(obj.to_bytes())

    # write the objects header which is number of objects and an array of offsets to each object from the start of the list
    objects_header.store_32(len(encoded_objects_array))
    object_header_size = 4 + len(encoded_objects_array) * 4
    objects_offset = len(header) + object_header_size
    encoded_objects = GubByteArray()
    for encoded_object in encoded_objects_array:
        objects_header.store_32(object_header_size + len(encoded_objects))
        encoded_objects.store_buffer(encoded_object)

    header.store_32_at(len(header), object_list_offset)
    header.store_32_at(len(objects_header) + len(encoded_objects), object_list_offset + 4)

    f = open(filepath, "wb")

    f.write(header)
    f.write(objects_header)
    f.write(encoded_objects)

    f.close()

def get_header():
    header = GubByteArray()

    header.store_string("WMB7") # file format version
    # the following are "LIST" objects that include a offset from the start of the file and a length in bytes
    header.store_64(0) # palettes WMB1..6 only
    header.store_64(0) # legacy1 WMB1..6 only
    header.store_64(0) # texturess, not needed?
    header.store_64(0) # legacy2 WMB1..6 only
    header.store_64(0) # pvs BSP only
    header.store_64(0) # bsp_nodes BSP only
    header.store_64(0) # materials, not needed?
    header.store_64(0) # legacy3 WMB1..6 only
    header.store_64(0) # legacy4 WMB1..6 only
    header.store_64(0) # aabb_hulls WMB1...6 only
    header.store_64(0) # bsp_leafs BSP only
    header.store_64(0) # bsp_blocks BSP only
    header.store_64(0) # legacy5 WMB1...6 only
    header.store_64(0) # legacy6 WMB1..6 only
    header.store_64(0) # legacy7 WMB1..6 only

    # object list offset goes here but i will write it later
    global object_list_offset 
    object_list_offset = header.get_position()
    header.store_64(0) # write it for now to keep proper offsets

    header.store_64(0) # lightmaps, not needed?
    header.store_64(0) # blocks, not used in caterpillar
    header.store_64(0) # legacy8 WMB1..6 only
    header.store_64(0) # lightmaps_terrain, not used???

    return header

# def apply_map_scale(custom_map_collection, scale):
#     layer_collection = bpy.context.view_layer.layer_collection.children['CustomMap']
#     bpy.context.view_layer.active_layer_collection = layer_collection
#     bpy.ops.object.add(type='EMPTY')
#     scale_root = bpy.context.object
#
#     objects = custom_map_collection.objects.values()
#     objects.remove(scale_root)
#
#     for obj in objects:
#         obj.parent = scale_root
#     scale_root.scale *= scale
#     bpy.context.evaluated_depsgraph_get().update()
#
#     return (objects, scale_root)
#
# def unapply_map_scale(objects, scale_root):
#     for obj in objects:
#         obj.parent = None
#     bpy.data.objects.remove(scale_root, do_unlink=True)

class ContextError(BaseException):
    pass

# ExportHelper is a helper class, defines filename and invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Operator

class WMBExporter(Operator, ExportHelper):
    bl_idname = "pogo_blend.wmb_export"
    bl_label = "Export Project to WMB (Pogostuck Map)"
    bl_description = "Exports this project to a Pogostuck Custom Map project"

    filename_ext = ".wmb"

    filter_glob: StringProperty(
        default="*.wmb",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    global_scale: FloatProperty(
            name="Scale Multiplier",
            description="Use this to scale on export",
            min=0.0, max=100.0,
            default=100.0,
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
    self.layout.operator(WMBExporter.bl_idname, text="Pogostuck Custom Map")

# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(WMBExporter)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(WMBExporter)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

