from . import add_pogo_reigon
from . import add_pogo_menu

from . import pogo_object_panel
from . import pogo_collection_panel

def register():
    add_pogo_reigon.register()
    add_pogo_menu.register()

    pogo_object_panel.register()
    pogo_collection_panel.register()

def unregister():
    add_pogo_reigon.unregister()
    add_pogo_menu.unregister()

    pogo_object_panel.unregister()
    pogo_collection_panel.unregister()
