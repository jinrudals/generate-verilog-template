from utils.Verilog import Verilog
import utils.APIs.APIs as api
import argparse, os

calculator = Verilog("calculator", "calculator.v")
adder = Verilog("adder", "adder")
subtractor  = Verilog("subtractor", "subtractor")

adder.ports.add("a", direction="input", bit=7)
adder.ports.add("b", direction="input", bit=7)
adder.ports.add("sum", direction="output", bit=8)
adder.assigns.add("sum", "a + b")

subtractor.ports.add("a", direction="input", bit=7)
subtractor.ports.add("b", direction="input", bit=7)
subtractor.ports.add("result", direction="output", bit=8)
subtractor.assigns.add("result", "a - b")

calculator.add_instance(adder)
calculator.add_instance(subtractor)
api.toPort(calculator,adder, lambda x : (x.name, x.name != "sum"))
calculator.ports.add(name="control", bit=1, direction="input")
calculator.ports.add(name="output", bit=8, direction="output")


calculator.update_instance("adder", api.connect_instance_with_port, api.finalize)
calculator.update_instance("subtractor", api.connect_instance_with_port, api.finalize)

calculator.assigns.add("output", f"control ? Wire_adder_sum : Wire_subtractor_result")
line = calculator.toModule()
print(line)