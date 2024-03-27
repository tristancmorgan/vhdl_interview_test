import os 

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.types import LogicArray, Logic
from cocotb.runner import get_runner

import pytest

from tools.test_utils.bits_math import BitsMath
from tools.test_utils.expect_queue import ExpectQueue
from tools.test_utils.interfaces.data_valid_interface import DataValidDriver, DataValidMonitor

import random
import logging

log = logging.getLogger("cocotb")

async def reset(dut):
    dut.rst_i.value = 1
    await RisingEdge(dut.clk_i)
    dut.rst_i.value = 0

@cocotb.test()
async def reg_stage(dut):
    clock = Clock(dut.clk_i, 10, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    monitor = DataValidMonitor(dut)
    driver = DataValidDriver(dut)

    for _ in range(20):
        driver.clear()
        for _ in range(20): await RisingEdge(dut.clk_i) # Wait for the DUT to reach a nice steady state before starting our monitor

        expect_queue = ExpectQueue()
        monitor_coroutine = cocotb.start_soon(monitor.monitor(expect_queue))

        for _ in range(200):
            stim = BitsMath.random(dut.DATA_WIDTH.value)
            expect_queue.expect(stim)
            await driver.drive(stim)

        for _ in range(20): await RisingEdge(dut.clk_i) # Wait for all events to come out of the DUT

        monitor_coroutine.kill()
        expect_queue.teardown()

@pytest.mark.parametrize(
    "parameters", [
        {"DATA_WIDTH": "1"},
        {"DATA_WIDTH": "32"}
    ]
)
def test_reg_stage(parameters):
    proj_path = os.path.dirname(os.path.dirname(__file__))

    sources = [os.path.abspath(os.path.join(proj_path, "hdl", "reg_stage.vhd"))]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=sources,
        build_args=["--std=08"],
        hdl_toplevel="reg_stage",
        always=True,
    )

    runner.test(
        hdl_toplevel="reg_stage",
        test_module="examples.tb.test_reg_stage",
        test_args=["--std=08"],
        plusargs=[f"-g{k}={v}" for k, v in parameters.items()]
    )

