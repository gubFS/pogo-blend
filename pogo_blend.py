from . import pogo_blend_preferences

from .pogo_classes import pogo_classes

from .UI import ui

from .exporters.mdl_exporter import mdl_exporter_operator
from .exporters.wmb_exporter import wmb_exporter_operator

def register():
    pogo_blend_preferences.register()

    pogo_classes.register()

    ui.register()

    mdl_exporter_operator.register()
    wmb_exporter_operator.register()

def unregister():
    pogo_blend_preferences.unregister()

    pogo_classes.unregister()

    ui.unregister()

    mdl_exporter_operator.unregister()
    wmb_exporter_operator.unregister()
