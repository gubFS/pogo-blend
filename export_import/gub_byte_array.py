import struct


class GubByteArray(bytearray):
    def __init__(self):
        self.big_endian = False

    def pack(self, format, *args):
        format = ">" if self.big_endian else "<" + format
        self.extend(struct.pack(format, *args))

    def get_position(self):
        return len(self)

    def store_8(self, value):
        self.pack("B", value)

    def store_8s(self, value, amount):
        for _ in range(amount):
            self.store_8(value)

    def store_16(self, value):
        self.pack("H", value)

    def store_32(self, value):
        self.pack("I", value)

    def store_32_at(self, value, offset):
        format = ">" if self.big_endian else "<" + "I"
        bytes = struct.pack(format, value)
        for i, byte in enumerate(bytes):
            self[offset + i] = byte

    def store_32s(self, value, amount):
        for _ in range(amount):
            self.store_32(value)

    def store_32_buffer(self, buffer):
        for value in buffer:
            self.store_32(value)

    def store_64(self, value):
        self.pack("Q", value)

    def store_float(self, value):
        self.pack("f", value)

    def store_float_buffer(self, floats, amount=-1):
        if amount == -1:
            amount = len(floats)
        for i in range(amount):
            f = 0.0
            if i < len(floats):
                f = floats[i]
            self.store_float(f)

    def store_buffer(self, buffer):
        self.extend(buffer)

    def store_vec3f(self, vec):
        self.pack("3f", vec[0], vec[1], vec[2])

    def store_vec3f_buffer(self, vecs):
        for vec in vecs:
            self.store_vec3f(vec)

    def store_string(self, value, size=-1):
        if size == -1:
            size = len(value)
        format = f"{size}s"
        self.pack(format, value.encode("utf-8"))
