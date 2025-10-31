import bpy
from ...pogo_blend_preferences import get_preferences
from .wmb_exporter import WMBExporter
from ..mdl_exporter.mdl_exporter import MDLExporter
from .wmb_objects.wmb_entity import *
from .wmb_objects.wmb_path import *
from .wmb_objects.wmb_info import WMBInfo
from .wmb_objects.wmb_reigon import WMBReigon
from ..gub_byte_array import GubByteArray
from PIL import Image
import os


from string import ascii_lowercase
change_chars = "0123456789" + ascii_lowercase
used_names = set()
def get_unique_name(suggestion, required_suffix, max_length):
    suggestion = suggestion.lower().replace(" ", "_")
    base_suggestion = suggestion
    suggestion = suggestion[:min(len(suggestion), max(0,max_length - len(required_suffix)))]
    name = suggestion + required_suffix
    if len(name) > max_length: return None

    change_array = [0]
    while name in used_names:
        if len(change_array) + len(required_suffix) > max_length: return None
        change = ""
        for change_idx in change_array:
            change += change_chars[change_idx]
        suggestion = base_suggestion[:min(len(base_suggestion), max_length - len(required_suffix) - len(change))] + change
        name = suggestion + required_suffix
        for i in range(len(change_array)):
            change_array[i] += 1
            if change_array[i] >= len(change_chars):
                change_array[i] = 0
                if i >= len(change_array) - 1:
                    change_array.append(0)
                    break
            else:
                break
    used_names.add(name)
    return name

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
    used_names.clear()

    undo_map_scale_args = apply_map_scale(custom_map_collection, global_scale)
    try:
        wmb_objects = [
            WMBInfo(),
            PogoSpawn(spawn),
            PogoPathProgress(path_progress),
            PogoStartLine(start_line)
        ]
        meshes = {}
        textures = {}
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
            filename = get_unique_name(obj.name, ".mdl", 33)
            if filename == None:
                print("WARNING: could not find a unique filename")
                continue
            entity.filename = filename
            mdlpath = os.path.join(dirpath, filename)
            if os.path.exists(mdlpath): print(f"WARNING: Overwriting '{mdlpath}'")
            mdl_exporter = MDLExporter(mdlpath, [obj], global_scale)
            for texture, slot_idx in mdl_exporter.skins.copy().items():
                if texture == "": continue
                new_texture = None
                if texture in textures:
                    new_texture = textures[texture]
                else:
                    new_texture = get_unique_name(os.path.splitext(os.path.basename(texture))[0], ".tga", 255)
                if new_texture == None:
                    print("WARNING: could not find a unique filename")
                    continue
                mdl_exporter.skins.pop(texture)
                mdl_exporter.skins[new_texture] = slot_idx
                textures[texture] = new_texture
            mdl_exporter.export()
        export_splits(dirpath, custom_map, splits_to_add)
        WMBExporter(filepath, wmb_objects).export()

        export_map_description(dirpath)
        export_map_image(dirpath, custom_map)
        for texture, new_texture in textures.items():
            export_texture(dirpath, new_texture, texture)
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

def export_map_description(dirpath):
    text = ""
    try: text = bpy.data.texts["levelDescription.txt"].as_string()
    except BaseException: pass
    filepath = os.path.join(dirpath, "levelDescription.txt")
    with open(filepath, 'wb') as f:
        f.write(0xFF.to_bytes()) # utf-16-le header aka 'BOM'
        f.write(0xFE.to_bytes())
        f.write(text.encode('utf-16-le'))

def export_map_image(dirpath, custom_map):
    img = Image.open(custom_map.map_image)
    img.save(os.path.join(dirpath, "workshopPreview.png"), format="PNG")

def export_texture(dirpath, image_name, image_path):
    img = Image.open(image_path)
    img.save(os.path.join(dirpath, image_name), format="TGA")

def apply_map_scale(custom_map_collection, scale):
    scale_root = bpy.data.objects.new(name="ScaleRoot", object_data=None)
    scale_root.location = (0,0,0)
    custom_map_collection.objects.link(scale_root)

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
import time

class WMBExporterOperatorFile(bpy.types.Operator, ExportHelper):
    bl_idname = "pogo_blend.wmb_export_file"
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
    )

    def execute(self, context):
        return bpy.ops.pogo_blend.wmb_export(filepath = self.filepath, global_scale = self.global_scale)

    def invoke(self, context, event):
        self.global_scale=get_preferences().map_scale
        return ExportHelper.invoke(self, context, event)

class WMBExporterOperator(bpy.types.Operator):
    bl_idname = "pogo_blend.wmb_export"
    bl_label = "Export Project to WMB (Pogostuck Map)"
    bl_description = "Exports this project to a Pogostuck Custom Map project"

    filepath: bpy.props.StringProperty(name="File path")

    global_scale: bpy.props.FloatProperty(
            name="Scale Multiplier",
            description="Use this to scale on export",
            min=0.0, max=1000.0,
    )

    def execute(self, context):
        start_time = time.time()
        try: export_to_wmb(context, self.filepath, self.global_scale)
        except BaseException as e:
            error_type = {'ERROR'}
            if type(e) is ContextError: error_type = {'ERROR_INVALID_CONTEXT'}
            self.report(error_type, str(e))
            raise e
            return {'CANCELLED'}
        else:
            self.report({'INFO'}, f"Custom Map built in {math.floor((time.time() - start_time) * 1000)}ms")
            return {'FINISHED'}

    def invoke(self, context, event):
        self.global_scale=get_preferences().map_scale
        return self.execute(context)

# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(WMBExporterOperatorFile.bl_idname, text="Pogostuck Custom Map")

# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(WMBExporterOperator)
    bpy.utils.register_class(WMBExporterOperatorFile)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(WMBExporterOperator)
    bpy.utils.unregister_class(WMBExporterOperatorFile)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

