# SPDX-FileCopyrightText: 2026 gubFS
# SPDX-License-Identifier: GPL-3.0-or-later

from ...gub_byte_array import GubByteArray


class WMBPath:
    def __init__(self, obj, global_scale: float = 50.0):
        self.type = 6  # 6 is the ID for path types
        self.name = obj.name

        location = obj.matrix_world.translation
        scale = obj.matrix_world.to_scale().to_3d()
        path_points = obj.data.splines[0].points

        self.points = {}
        for i, point in enumerate(path_points):
            hash = self._hash_point(point)
            point = point.co.to_3d()
            point.rotate(obj.matrix_world.to_euler())
            point = point * scale + location
            point *= global_scale
            if hash not in self.points:
                self.points[hash] = (len(self.points), point, [])
                if i == 0:
                    continue
                prev_hash = self._hash_point(path_points[i - 1])
                self.points[prev_hash][2].append(self.points[hash][0])
        self.points = sorted(self.points.values(), key=lambda p: p[0])

    def _hash_point(self, point):
        return point.co.copy().freeze()

    def to_bytes(self) -> GubByteArray:
        bytes = GubByteArray()

        bytes.store_32(self.type)
        bytes.store_string(self.name, 20)
        bytes.store_float(len(self.points))  # number of points, as a float for who knows why
        bytes.store_32s(0, 3)  # unused

        # number of edges, which is 3 + no_of_edges * 5, for some reason
        bytes.store_32(3 + (len(self.points) - 1) * 5)
        bytes.store_vec3f_buffer([point for _, point, _ in self.points])

        # store skills (6 of em) per point? paths have no skills, what?
        bytes.store_32s(0, len(self.points) * 6)

        # store which two points make an edge. also as a float btw
        for idx, point, edges in self.points:
            for edge in edges:
                bytes.store_float(idx + 1)  # +1 cuz 1-indexed
                bytes.store_float(edge + 1)

                # store the length of the edge
                distance = (self.points[edge][1] - point).length
                bytes.store_float(distance)

                bytes.store_float(0)  # beizer
                bytes.store_float(0)  # weight
                bytes.store_float(0)  # skill

        return bytes


class PogoPathProgress(WMBPath):
    def __init__(self, obj):
        super().__init__(obj)
        self.name = "path_progress"
