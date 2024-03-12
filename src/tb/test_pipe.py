import os 

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.types import LogicArray
from cocotb.runner import get_runner

import collections

class ExpectQueue:
    def __init__(self, name="expect_queue"):
        self.queue = collections.deque()
        self.name = name

    def expect(self, expectation):
        print(f"{self.name}: Expecting {expectation}")
        self.queue.append(expectation)

    def check(self, actual):
        print(f"{self.name}: Checking {actual}")
        assert len(self.queue) > 0, f"{self.name}: Unexpected actual: {actual}"
        expected = self.queue.popleft()
        assert expected == actual, f"{self.name}: Mismatch [E, R]: [{expected},{actual}]"

    def teardown(self):
        assert len(self.queue) == 0, f"{self.name}: {len(self.queue)} expectations remaining after test"


@cocotb.test()
async def pipe(dut):
    clock = Clock(dut.clk_i, 10, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk_i)

    expect_queue = ExpectQueue()

    async def drive():
        dut.data_i.value = 1
        expect_queue.expect(1)

        await RisingEdge(dut.clk_i)

    async def monitor():
        await RisingEdge(dut.clk_i)
        expect_queue.check(dut.data_o.value)

    driver_coro = cocotb.start_soon(drive())
    monitor_coro = cocotb.start_soon(monitor())

    await cocotb.triggers.Combine(cocotb.triggers.Join(driver_coro), cocotb.triggers.Join(monitor_coro))

    expect_queue.teardown()
    





def test_pipe():
    proj_path = os.path.dirname(os.path.dirname(__file__))

    sources = [os.path.abspath(os.path.join(proj_path, "hdl", "pipe.vhd"))]
    print(sources)

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=sources,
        build_args=["--std=08"],
        hdl_toplevel="pipe",
        always=True,
    )

    runner.test(
        hdl_toplevel="pipe",
        test_module="test_pipe",
        test_args=["--std=08"],
        plusargs=["-gPIPE_DEPTH=0", "-gDATA_WIDTH=1"]
    )