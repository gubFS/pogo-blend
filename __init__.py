if "bpy" in locals():
    import importlib
    if "pogo_blend" in locals():
        importlib.reload(pogo_blend)
import bpy
from . import pogo_blend

def register():
    pogo_blend.register()

def unregister():
    pogo_blend.unregister()

