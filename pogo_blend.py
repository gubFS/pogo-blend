import bpy

from .pogo_classes import pogo_classes
from . import pogo_object_panel
from . import pogo_collection_panel
from .exporters.mdl_exporter import mdl_exporter_operator
from .exporters.wmb_exporter import wmb_exporter_operator

def register():
    pogo_classes.register()
    pogo_object_panel.register()
    pogo_collection_panel.register()
    mdl_exporter_operator.register()
    wmb_exporter_operator.register()

def unregister():
    pogo_classes.unregister()
    pogo_object_panel.unregister()
    pogo_collection_panel.unregister()
    mdl_exporter_operator.unregister()
    wmb_exporter_operator.unregister()
