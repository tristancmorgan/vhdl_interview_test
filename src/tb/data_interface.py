from metaclasses import MultipleMeta
from cocotb.handle import HierarchyObject, ModifiableObject
from cocotb.triggers import RisingEdge
from bits_math import BitsMath
import logging

log = logging.getLogger("cocotb")

class DataDriver(metaclass=MultipleMeta):
    def __init__(self, clk:ModifiableObject, data:ModifiableObject, name:str="data_driver"):
        self.clk = clk
        self.data = data
        self.name = name

    def __init__(self, dut:HierarchyObject, prefix:str="", name:str="data_driver"):
        self.clk = getattr(dut, f"clk_i")
        self.data = getattr(dut, f"{prefix}data_i")
        self.name = name

    async def drive(self, stim):
        log.debug(f"{self.name}: driving {stim}")
        self.data.value = stim
        await RisingEdge(self.clk)
        self.data.value = BitsMath.random(len(self.data))

class DataMonitor(metaclass=MultipleMeta):
    def __init__(self, clk:ModifiableObject, rst:ModifiableObject, data:ModifiableObject, name:str="data_monitor"):
        self.clk = clk
        self.rst = rst
        self.data = data
        self.name = name    

    def __init__(self, dut:HierarchyObject, prefix:str="", name:str="data_monitor"):
        self.clk = getattr(dut, f"clk_i")
        self.rst = getattr(dut, f"rst_i")
        self.data = getattr(dut, f"{prefix}data_o")
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
