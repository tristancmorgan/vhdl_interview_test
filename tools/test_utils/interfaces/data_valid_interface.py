from tools.test_utils.metaclasses import MultipleMeta
from cocotb.handle import HierarchyObject, ModifiableObject
from cocotb.triggers import RisingEdge
from tools.test_utils.bits_math import BitsMath
import logging

log = logging.getLogger("cocotb")

class DataValidDriver(metaclass=MultipleMeta):
    def __init__(self, clk:ModifiableObject, data:ModifiableObject, valid: ModifiableObject, name:str="data_valid_driver"):
        self.clk = clk
        self.data = data
        self.valid = valid
        self.name = name

    def __init__(self, dut:HierarchyObject, prefix:str="", name:str="data_valid_driver"):
        self.clk = getattr(dut, f"clk_i")
        self.data = getattr(dut, f"{prefix}data_i")
        self.valid = getattr(dut, f"{prefix}valid_i")
        self.name = name

    def clear(self):
        self.data.value = BitsMath.random(len(self.data))
        self.valid.value = 0

    async def drive(self, stim):
        log.debug(f"{self.name}: driving {stim}")
        self.data.value = stim
        self.valid.value = 1
        await RisingEdge(self.clk)
        self.clear()

class DataValidMonitor(metaclass=MultipleMeta):
    def __init__(self, clk:ModifiableObject, rst:ModifiableObject, data:ModifiableObject, valid: ModifiableObject, name:str="data_valid_monitor"):
        self.clk = clk
        self.rst = rst
        self.data = data
        self.valid = valid
        self.name = name    

    def __init__(self, dut:HierarchyObject, prefix:str="", name:str="data_valid_monitor"):
        self.clk = getattr(dut, f"clk_i")
        self.rst = getattr(dut, f"rst_i")
        self.data = getattr(dut, f"{prefix}data_o")
        self.valid = getattr(dut, f"{prefix}valid_o")
        self.name = name

    async def recv(self):
        log.debug(f"{self.name}: starting recv")
        while True:
            await RisingEdge(self.clk)
            if not self.rst.value:
                log.debug(f"{self.name}: received {self.data.value} with type {type(self.data.value)}")
                yield self.data.value

    async def monitor(self, expect_queue):
        log.debug(f"{self.name}: starting monitor")
        async for actual in self.recv():
            expect_queue.check(actual)
