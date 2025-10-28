import bpy
from . import pogo_entity
from . import pogo_path
from . import pogo_reigon
from . import pogo_custom_map

def register():
    pogo_entity.register()
    pogo_path.register()
    pogo_reigon.register()
    pogo_custom_map.register()

def unregister():
    pogo_entity.unregister()
    pogo_path.unregister()
    pogo_reigon.unregister()
    pogo_custom_map.unregister()
