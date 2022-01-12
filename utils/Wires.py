from typing import Optional
from utils.bases.BaseClass import Grouping, MyHasahble
'''
Wire of a verilog
- name / bit information
- rhs information
- source information
'''

class Wire(MyHasahble):
  def __init__(self, name, bit, rhs = "", source = None):
    self.name       = name
    self.bit        = bit
    self.rhs        = rhs
    self.source     = source

class Wires(Grouping):
  def add_raw(self, wire : Wire):
    self.lsts.add(wire)
  def add(self, name, bit,rhs = "", source = None):
    self.add_raw(Wire(name, self.bit_to_string(bit), rhs, source))