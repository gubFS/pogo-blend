import bpy

def register():
    bpy.utils.register_class(EditMapDescription)
    bpy.utils.register_class(SelectMapImage)
    bpy.utils.register_class(PogoCollectionPanel)

def unregister():
    bpy.utils.unregister_class(EditMapDescription)
    bpy.utils.unregister_class(SelectMapImage)
    bpy.utils.unregister_class(PogoCollectionPanel)

class EditMapDescription(bpy.types.Operator):
    bl_idname = "pogo_blend.edit_map_description"
    bl_label = "Edit Map Description"
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.wm.window_new()
        context.area.ui_type = 'TEXT_EDITOR'
        try: bpy.data.texts["levelDescription.txt"]
        except KeyError:
            bpy.ops.text.new()
            context.space_data.text.name = "levelDescription.txt"
        context.space_data.text = bpy.data.texts["levelDescription.txt"]
        return {'FINISHED'}

class SelectMapImage(bpy.types.Operator):
    bl_idname = "pogo_blend.select_map_image"
    bl_label = "Select Map Image"
    bl_options = {'REGISTER'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(default="*.png;*.jpg;*.jpeg;*.tga;*.svg")

    def execute(self, context):
        context.collection.custom_map.map_image = self.filepath
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PogoCollectionPanel(bpy.types.Panel):
    bl_label = "Pogo Blend"
    bl_idname = "COLLECTION_PT_collection_pogo_blend"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout
        collection = context.collection
        if collection.name != "CustomMap": return
        custom_map = collection.custom_map

        layout.prop(custom_map, "map_name")
        # layout.prop(custom_map, "map_description")
        layout.operator("pogo_blend.edit_map_description")

        row = layout.row()
        row.prop(custom_map, "map_image")
        row.operator("pogo_blend.select_map_image", icon="IMAGE_DATA", text="")

        layout.prop(custom_map, "spawn", placeholder="Empty", icon='EMPTY_DATA')
        layout.prop(custom_map, "path_progress", placeholder="Curve", icon='CURVE_DATA')
        layout.prop(custom_map, "start_line", placeholder='Mesh', icon='MESH_DATA')
