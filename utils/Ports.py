from utils.bases.BaseClass import Grouping, MyHasahble

'''
Port of Module
- direction / bit / name is required
- target information  : when for being instantiated
- source information  : how this port is generated
'''

class Port(MyHasahble):
  def __init__(self, name, direction, bit, target = None, source = None):
    self.name = name
    self.direction = direction
    self.bit = bit
    self.target = target
    self.source = source
  # def copy(self, key, value):

  #   return Port()
class Ports(Grouping):
  def add_raw(self, port : Port):
    self.lsts.add(port)
  def add(self, name : str, direction : str, bit : int, target = None, source = None) -> None:
    self.add_raw(Port(name=name, direction=direction, bit=self.bit_to_string(bit), target=target, source=source))