import os 

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.types import LogicArray, Logic
from cocotb.runner import get_runner

import pytest

from tools.test_utils.bits_math import BitsMath
from tools.test_utils.expect_queue import ExpectQueue
from tools.test_utils.interfaces.data_interface import DataDriver, DataMonitor

import random
import logging

log = logging.getLogger("cocotb")

async def reset(dut):
    dut.rst_i.value = 1
    await RisingEdge(dut.clk_i)
    dut.rst_i.value = 0

@cocotb.test()
async def pipe(dut):
    clock = Clock(dut.clk_i, 10, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    monitor = DataMonitor(dut)
    driver = DataDriver(dut)

    for _ in range(20):
        if random.choice([True, False]):
            log.debug(f"testing with reset")
            expect_queue = ExpectQueue()
            await reset(dut)

            # Fill the expect queue with the reset values
            for _ in range(dut.PIPE_DEPTH.value):
                expect_queue.expect(BitsMath.clear(dut.DATA_WIDTH.value))

            monitor_coro = cocotb.start_soon(monitor.monitor(expect_queue))

            for i in range(200):
                stim = BitsMath.random(dut.DATA_WIDTH.value)
                expect_queue.expect(stim)
                await driver.drive(stim)

            await RisingEdge(dut.clk_i)
        else:
            log.debug(f"testing without reset")
            expect_queue = ExpectQueue()

            async def do_drive():
                for i in range(200):
                    stim = BitsMath.random(dut.DATA_WIDTH.value)
                    expect_queue.expect(stim)
                    await driver.drive(stim)
            
            drive_coro = cocotb.start_soon(do_drive())

            # Wait for the pipe to be full of known values before we start checking the output
            for _ in range(dut.PIPE_DEPTH.value):
                await RisingEdge(dut.clk_i)

            monitor_coro = cocotb.start_soon(monitor.monitor(expect_queue))

            await drive_coro

        # Wait for the contents of the pipe to be flushed
        for _ in range(dut.PIPE_DEPTH.value):
            await RisingEdge(dut.clk_i)

        monitor_coro.kill()
        expect_queue.teardown()

@pytest.mark.parametrize(
    "parameters", [
        {"DATA_WIDTH": "1", "PIPE_DEPTH": "5"},
        {"DATA_WIDTH": "32", "PIPE_DEPTH": "0"},
        {"DATA_WIDTH": "32", "PIPE_DEPTH": "1"},
        {"DATA_WIDTH": "32", "PIPE_DEPTH": "2"},
        {"DATA_WIDTH": "32", "PIPE_DEPTH": "9"},
    ]
)
def test_pipe(parameters):
    proj_path = os.path.dirname(os.path.dirname(__file__))

    sources = [os.path.abspath(os.path.join(proj_path, "hdl", "pipe.vhd"))]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=sources,
        build_args=["--std=08"],
        hdl_toplevel="pipe",
        always=True,
    )

    runner.test(
        hdl_toplevel="pipe",
        test_module="src.tb.test_pipe",
        test_args=["--std=08"],
        plusargs=[f"-g{k}={v}" for k, v in parameters.items()]
    )

