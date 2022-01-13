import copy
class MyHasahble(object):
  def _in_init(self):
    return [each for each in dir(self) if not hasattr(type(self), each)]

  def __repr__(self):
    members = self._in_init()
    member = ", ".join([f"{member} : {str(getattr(self, member))}" for member in members])
    name    = type(self).__name__
    return f"{name}({member})"
  def __eq__(self, other):
    members = self._in_init()
    return len([False for each in self._in_init() if getattr(self, each) == getattr(other, each)]) != 0
  def __hash__(self):
    return hash(self.__repr__())
  def copy(self, key, value):
    members = self._in_init()
    if key not in members:
      return self
    else:
      x = copy.deepcopy(self)
      setattr(x, key, value)
      return x

class Grouping:
  def __init__(self):
    self.lsts = set()
  def get(self):
    return self.lsts

  @staticmethod
  def bit_to_string(length):
    if type(length) == str:
      return length
    if length == 1:
      return ""
    else:
      return f"[{length - 1}:0]"

  def _in_init_function_of_member(self):
    lsts = self.get()
    if len(lsts) == 0:
      return []
    first = list(lsts)[0]
    return [each for each in dir(first) if not hasattr(type(first), each)]

  def remove(self, member):
    self.lsts.remove(member)

  def align(self):
    members = self._in_init_function_of_member()
    data = dict()
    for member in members:
      k = [getattr(each, member.strip()) for each in list(self.get()) if isinstance(getattr(each, member), str)]
      if len(k) != 0:
        data[member] = max([len(each) for each in k])
    for member in data.keys():
      for each in self.get():
        if member == "bit":
          original = getattr(each, member)
          if len(original.strip()) == 0:
            setattr(each, "aligned_" + member, original.ljust(data[member]))
          else:
            aligned = original[1:].rjust(data[member] - 1)
            setattr(each, "aligned_" + member, f"[{aligned}")
        elif member == "name" and type(self).__name__ == "Wires":
          setattr(each, "aligned_" + member, f"{getattr(each, member)}".ljust(data[member]))
          maximum = data["rhs"]
          if maximum != 0:
            rhs = getattr(each, "rhs")
            name = getattr(each, "aligned_name")
            newLength = len(" = ") + maximum
            if rhs != "":
              name = name + f" = {rhs}"
            setattr(each, "aligned_" + "name", name.ljust(data["name"] + newLength))
            # print(maximum)
            # if getattr(each, "rhs") == 0:

          # if "rhs" in data.keys():
          #   rhs = getattr(each, "rhs")
        else:
          setattr(each, "aligned_" + member, f"{getattr(each, member)}".ljust(data[member]))
    return self
  def sort(self, key="name"):
    lsts = list(self.lsts)
    lsts.sort(key=lambda x : getattr(x, key))
    self.lsts = lsts
    return self
