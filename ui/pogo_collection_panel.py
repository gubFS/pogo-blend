from pathlib import Path

import bpy

from .. import pogo_blend_utils as pbu


class EditMapDescription(bpy.types.Operator):
    bl_idname = "pogo_blend.edit_map_description"
    bl_label = "Edit Map Description"
    bl_description = "Opens the Map Description in a text editor"
    bl_options = {'REGISTER'}

    def execute(self, context):
        pbu.open_temp_text_editor()
        if "levelDescription.txt" not in bpy.data.texts:
            bpy.ops.text.new()
            context.space_data.text.name = "levelDescription.txt"
        context.space_data.text = bpy.data.texts["levelDescription.txt"]
        bpy.ops.text.move(type='FILE_TOP')
        return {'FINISHED'}


class RefreshSplits(bpy.types.Operator):
    bl_idname = "pogo_blend.refresh_splits"
    bl_label = "Refresh Splits"
    bl_description = "Refreshes the splits"
    bl_options = {'REGISTER'}

    def execute(self, context):
        pbu.get_custom_map().update_splits()
        return {'FINISHED'}


class PogoSplitList(bpy.types.UIList):
    bl_idname = "POGO_UL_pogo_blend_split_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.split_region.name, translate=False, icon_value=icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class StaticFilesList(bpy.types.UIList):
    bl_idname = "POGO_UL_pogo_blend_static_files_list"

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.filepath, translate=False, icon_value=icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class PogoCollectionPanel(bpy.types.Panel):
    bl_label = "PogoBlend"
    bl_idname = "COLLECTION_PT_collection_pogo_blend"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout
        collection = context.collection
        if collection.name != "CustomMap":
            return
        custom_map = collection.custom_map

        layout.operator("pogo_blend.build_custom_map", text="Build Custom Map")

        map_information_panel_header, map_information_panel = layout.panel("map_information_panel")
        map_information_panel_header.label(text="Map Information")
        if map_information_panel:
            row = map_information_panel.row()
            row.prop(custom_map, "map_name")
            path = pbu.get_preferences().custom_maps_path
            if path != "" and Path(path).exists():
                map_path = Path(path).joinpath(custom_map.map_name)
                if map_path.exists():
                    path = str(map_path)
                row.operator("wm.path_open", text="", icon='FILE_FOLDER').filepath = path

            map_information_panel.operator("pogo_blend.edit_map_description")

            map_information_panel.template_ID(custom_map, "map_image", text="Map Image", open="image.open")

        required_objects_panel_header, required_objects_panel = layout.panel("required_objects_panel")
        required_objects_panel_header.label(text="Required Objects")
        if required_objects_panel:
            required_objects_panel.prop(custom_map, "spawn", placeholder="Empty", icon="EMPTY_DATA")
            required_objects_panel.prop(custom_map, "path_progress", placeholder="Curve", icon="CURVE_DATA")
            required_objects_panel.prop(custom_map, "start_line", placeholder="Mesh", icon="MESH_DATA")

        splits_panel_header, splits_panel = layout.panel("splits_panel")
        splits_panel_header.label(text="Splits")
        if splits_panel:
            row = splits_panel.row()
            row.template_list(
                "POGO_UL_pogo_blend_split_list",
                "",
                context.collection.custom_map,
                "splits",
                context.collection.custom_map,
                "active_split_idx",
            )

            col = row.column()
            col.operator("pogo_blend.active_split_move", icon="TRIA_UP", text="").direction = 'UP'
            col.operator("pogo_blend.active_split_move", icon="TRIA_DOWN", text="").direction = 'DOWN'
            col.operator("pogo_blend.refresh_splits", icon="FILE_REFRESH", text="")

        mode_panel_header, mode_panel = layout.panel("mode_panel")
        mode_panel_header.label(text="Modes")
        if mode_panel:
            row = mode_panel.row()
            col = row.column()
            col.prop(custom_map, "double_jump")
            col.prop(custom_map, "no_boost")
            col.prop(custom_map, "ice")

            col = row.column()
            col.prop(custom_map, "puzzle")
            col.prop(custom_map, "no_bonk")
            col.prop(custom_map, "mushroom_power")

        static_files_panel_header, static_files_panel = layout.panel("static_files_panel")
        static_files_panel_header.label(text="Static Files")
        if static_files_panel:
            static_files_panel.label(text="Any files added to this list will be copied to the Custom Map folder.")
            row = static_files_panel.row()
            row.template_list(
                "POGO_UL_pogo_blend_static_files_list",
                "",
                context.collection.custom_map,
                "static_files",
                context.collection.custom_map,
                "active_static_file_idx",
            )

            col = row.column(align=True)
            col.operator("pogo_blend.static_file_add", icon='ADD', text="")
            col.operator("pogo_blend.static_file_remove", icon='REMOVE', text="")


classes = (
    EditMapDescription,
    RefreshSplits,
    PogoSplitList,
    StaticFilesList,
    PogoCollectionPanel,
)
