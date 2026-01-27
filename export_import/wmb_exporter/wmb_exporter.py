# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

from ..gub_byte_array import GubByteArray


class WMBExporter:
    def __init__(self, filepath, wmb_objects):
        self.filepath = filepath
        self.wmb_objects = wmb_objects
        self.object_list_offset = 0

    def export(self):
        header = self.get_header_bytes()

        objects_header = GubByteArray()
        encoded_objects_array = [obj.to_bytes() for obj in self.wmb_objects]

        # write the objects header which is number of objects and an array of offsets to each object from the start of the list
        objects_header.store_32(len(encoded_objects_array))
        object_header_size = 4 + len(encoded_objects_array) * 4
        encoded_objects = GubByteArray()
        for encoded_object in encoded_objects_array:
            objects_header.store_32(object_header_size + len(encoded_objects))
            encoded_objects.store_buffer(encoded_object)

        header.store_32_at(len(header), self.object_list_offset)
        header.store_32_at(len(objects_header) + len(encoded_objects), self.object_list_offset + 4)

        with open(self.filepath, "wb") as f:
            f.write(header)
            f.write(objects_header)
            f.write(encoded_objects)

    def get_header_bytes(self):
        header = GubByteArray()

        header.store_string("WMB7")  # file format version
        # the following are "LIST" objects that include a offset from the start of the file and a length in bytes
        header.store_64(0)  # palettes WMB1..6 only
        header.store_64(0)  # legacy1 WMB1..6 only
        header.store_64(0)  # texturess, not needed?
        header.store_64(0)  # legacy2 WMB1..6 only
        header.store_64(0)  # pvs BSP only
        header.store_64(0)  # bsp_nodes BSP only
        header.store_64(0)  # materials, not needed?
        header.store_64(0)  # legacy3 WMB1..6 only
        header.store_64(0)  # legacy4 WMB1..6 only
        header.store_64(0)  # aabb_hulls WMB1...6 only
        header.store_64(0)  # bsp_leafs BSP only
        header.store_64(0)  # bsp_blocks BSP only
        header.store_64(0)  # legacy5 WMB1...6 only
        header.store_64(0)  # legacy6 WMB1..6 only
        header.store_64(0)  # legacy7 WMB1..6 only

        # object list offset goes here but i will write it later
        self.object_list_offset = header.get_position()
        header.store_64(0)  # write it for now to keep proper offsets

        header.store_64(0)  # lightmaps, not needed?
        header.store_64(0)  # blocks, not used in caterpillar
        header.store_64(0)  # legacy8 WMB1..6 only
        header.store_64(0)  # lightmaps_terrain, not used???

        return header
