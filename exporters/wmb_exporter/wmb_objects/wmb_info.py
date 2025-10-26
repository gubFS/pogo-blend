from ...gub_byte_array import GubByteArray
from enum import Enum

class LMapSize(Enum):
    LMS_256x256 = 0
    LMS_512x512 = 1
    LMS_1024x1024 = 2

class WMBInfo:
    def __init__(self):

        self.type = 5 # 5 is the type id for info
        self.origin = [0, 0, 0]
        self.azimuth = 0.0
        self.elevation = 60.0
        self.flags = 0x37 # should be 0x7F???
        self.version = 7.35 # GS8 is 7.35
        self.gamma = 2
        self.l_map_size = LMapSize.LMS_256x256
        self.dw_sun_color = 0x00939393
        self.dw_ambient_color = 0x00303030
        self.dw_fog_color = [0x00FFFFFF, 0x003063FF, 0x00FF3030, 0] # these are colors, i think?

    def to_bytes(self):
        bytes = GubByteArray()

        bytes.store_32(self.type)
        bytes.store_vec3f(self.origin)
        bytes.store_float(self.azimuth)
        bytes.store_float(self.elevation)
        bytes.store_32(self.flags)
        bytes.store_float(self.version)
        bytes.store_8(self.gamma)
        bytes.store_8(self.l_map_size.value)
        bytes.store_8s(0, 2) # unused
        bytes.store_32(self.dw_sun_color)
        bytes.store_32(self.dw_ambient_color)
        bytes.store_32_buffer(self.dw_fog_color)

        return bytes
