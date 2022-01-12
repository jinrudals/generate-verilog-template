from utils.bases.BaseClass import Grouping, MyHasahble

class Assign(MyHasahble):
  def __init__(self, name, expression, source = None):
    self.name = name
    self.expression = expression
    self.source = source

class Assigns(Grouping):
  def add(self, target, expression, source = None):
    self.lsts.add(Assign(target, expression, source))
