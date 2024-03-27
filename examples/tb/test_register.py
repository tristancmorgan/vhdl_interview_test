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
async def pipe(dut):
    clock = Clock(dut.clk_i, 10, units="us")
    cocotb.start_soon(clock.start(start_high=False))

    monitor = DataValidMonitor(dut)
    driver = DataValidDriver(dut)

    for _ in range(20):
        
        expect_queue.teardown()

@pytest.mark.parametrize(
    "parameters", [
        {"DATA_WIDTH": "1"},
        {"DATA_WIDTH": "32"}
    ]
)
def test_register(parameters):
    proj_path = os.path.dirname(os.path.dirname(__file__))

    sources = [os.path.abspath(os.path.join(proj_path, "hdl", "register.vhd"))]

    runner = get_runner("ghdl")
    runner.build(
        vhdl_sources=sources,
        build_args=["--std=08"],
        hdl_toplevel="register",
        always=True,
    )

    runner.test(
        hdl_toplevel="pipe",
        test_module="src.tb.test_register",
        test_args=["--std=08"],
        plusargs=[f"-g{k}={v}" for k, v in parameters.items()]
    )

