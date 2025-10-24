import bpy

from . import pogo_classes
from . import pogo_object_panel
from . import pogo_collection_panel

def register():
    pogo_classes.register()
    pogo_object_panel.register()
    pogo_collection_panel.register()

def unregister():
    pogo_classes.unregister()
    pogo_object_panel.unregister()
    pogo_collection_panel.unregister()
