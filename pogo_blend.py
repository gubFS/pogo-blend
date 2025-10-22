if "bpy" in locals():
    import importlib
    if "wmb_classes" in locals():
        importlib.reload(wmb_classes)
    if "pogostuck_panel" in locals():
        importlib.reload(pogostuck_panel)
import bpy
from . import wmb_classes
from .wmb_classes import WMBEntity
from . import pogostuck_panel
from .pogostuck_panel import PogostuckPanel

def register():
    bpy.utils.register_class(WMBEntity)
    bpy.types.Object.wmb_entity = bpy.props.PointerProperty(type=WMBEntity)
    bpy.utils.register_class(PogostuckPanel)

def unregister():
    bpy.utils.unregister_class(PogostuckPanel)
    del bpy.types.Object.wmb_entity
    bpy.utils.unregister_class(WMBEntity)
