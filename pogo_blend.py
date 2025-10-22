if "bpy" in locals():
    import importlib
    if "wmb_classes" in locals():
        importlib.reload(wmb_classes)
    if "pogo_object_panel" in locals():
        importlib.reload(pogo_object_panel)
import bpy
from . import wmb_classes
from . import pogo_object_panel

def register():
    wmb_classes.register()
    pogo_object_panel.register()

def unregister():
    wmb_classes.unregister()
    pogo_object_panel.unregister()
