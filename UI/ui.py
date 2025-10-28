from . import add_pogo_reigon
from . import add_pogo_menu

def register():
    add_pogo_reigon.register()
    add_pogo_menu.register()

def unregister():
    add_pogo_reigon.unregister()
    add_pogo_menu.unregister()
