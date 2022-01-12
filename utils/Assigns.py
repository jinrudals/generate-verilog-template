from utils.bases.BaseClass import Grouping, MyHasahble

class Assign(MyHasahble):
  def __init__(self, name, expression, source = None):
    self.name = name
    self.expression = expression
    self.source = source

class Assigns(Grouping):
  def add_raw(self, assign : Assign):
    self.lsts.add(assign)
  def add(self, target, expression, source = None):
    self.add_raw(Assign(target, expression, source))
