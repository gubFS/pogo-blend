import bpy

def register():
    bpy.utils.register_class(PogoSplit)
    bpy.utils.register_class(PogoCustomMap)
    bpy.utils.register_class(ActiveSplitMove)
    bpy.types.Collection.custom_map = bpy.props.PointerProperty(type=PogoCustomMap)

def unregister():
    bpy.utils.unregister_class(PogoSplit)
    bpy.utils.unregister_class(PogoCustomMap)
    bpy.utils.unregister_class(ActiveSplitMove)
    del bpy.types.Collection.custom_map

class PogoSplit(bpy.types.PropertyGroup):
    split_reigon: bpy.props.PointerProperty(type=bpy.types.Object)

class ActiveSplitMove(bpy.types.Operator):
    bl_idname="pogo_blend.active_split_move"
    bl_label="Move active split"

    direction: bpy.props.StringProperty()

    def execute(self, context):
        custom_map_collection = bpy.data.collections["CustomMap"]
        custom_map = custom_map_collection.custom_map
        current_idx = custom_map.active_split_idx

        new_idx = current_idx
        if self.direction == 'DOWN':
            new_idx = min(current_idx + 1, len(custom_map.splits) - 1)
        elif self.direction == 'UP':
            new_idx = max(current_idx - 1, 0)
        custom_map.splits.move(current_idx, new_idx)
        custom_map.active_split_idx = new_idx

        return {'FINISHED'}

class PogoCustomMap(bpy.types.PropertyGroup):
    map_name: bpy.props.StringProperty(name="Map Name")
    map_image: bpy.props.StringProperty(name="Map Image")

    splits: bpy.props.CollectionProperty(type=PogoSplit, name="Splits")
    active_split_idx: bpy.props.IntProperty()

    spawn: bpy.props.PointerProperty(type=bpy.types.Object, name="Spawn", poll=lambda prop, obj: obj.type == 'EMPTY')
    def path_poll(prop, obj):
            try: obj["pogo_path"]
            except KeyError: return False
            return True
    path_progress: bpy.props.PointerProperty(type=bpy.types.Object, name="Progress Path", poll=path_poll)
    start_line: bpy.props.PointerProperty(type=bpy.types.Object, name="Start Line", poll=lambda prop, obj: obj.type == 'MESH')

    double_jump: bpy.props.BoolProperty(name="Double Jump")
    puzzle: bpy.props.BoolProperty(name="Puzzle")
    no_boost: bpy.props.BoolProperty(name="No boost")
    no_bonk: bpy.props.BoolProperty(name="No bonk")
    mushroom_power: bpy.props.BoolProperty(name="Mushroom power", description="Enables mushrooms to have a bounce power", default=True)
    ice: bpy.props.BoolProperty(name="Ice")


