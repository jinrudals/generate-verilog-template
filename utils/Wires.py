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
  def add(self, name, bit,rhs = "", source = None):
    self.lsts.add(Wire(name, self.bit_to_string(bit), rhs, source))
