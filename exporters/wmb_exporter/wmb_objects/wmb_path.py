from ...gub_byte_array import GubByteArray
import mathutils

class WMBPath:
    def __init__(self, obj):
        self.type = 6 # 6 is the ID for path types
        self.name = obj.name

        location = obj.matrix_world.translation
        scale = obj.matrix_world.to_scale().to_3d()
        self.points = []
        for point in obj.data.splines[0].points:
            point = point.co.to_3d() * scale + location
            self.points.append(point)

    def to_bytes(self):
        bytes = GubByteArray()

        bytes.store_32(self.type)
        bytes.store_string(self.name, 20)
        bytes.store_float(len(self.points)) # number of points, as a float for who knows why
        bytes.store_32s(0, 3) # unused

        # number of edges, which is 3 + no_of_edges * 5, for some reason
        bytes.store_32(3 + (len(self.points) - 1) * 5)
        bytes.store_vec3f_buffer(self.points)

        # store skills (6 of em) per point? paths have no skills, what?
        bytes.store_32s(0, len(self.points) * 6)

        # store which two points make an edge. For now its just the two next to eachother in the array, also as a float btw
        for i in range(len(self.points) - 1):
            bytes.store_float(i + 1) # +1 cuz 1-indexed
            bytes.store_float(i + 2)

            # store the length of the edge
            distance = (self.points[i+1] - self.points[i]).length
            bytes.store_float(distance)

            bytes.store_float(0) # beizer
            bytes.store_float(0) # weight
            bytes.store_float(0) # skill

        return bytes

class PogoPathProgress(WMBPath):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = "path_progress"
