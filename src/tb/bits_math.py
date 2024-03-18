import random
from cocotb.binary import BinaryValue

class BitsMath:
    @classmethod
    def random(cls, len):
        return BinaryValue("".join([random.choice(["0", "1"]) for _ in range(len)]))

    @classmethod
    def unknown(cls, len):
        return BinaryValue("".join(["X" for _ in range(len)]))

    @classmethod
    def clear(cls, len):
        return BinaryValue("".join(["0" for _ in range(len)]))

