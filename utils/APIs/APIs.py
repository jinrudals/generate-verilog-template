import re, os
from utils.Verilog import Verilog
from utils.Wires import Wire
def toJinja(each):
  return "{{ " + each + " }}"
'''
Write a Verilog module to target directory
'''
def write(target, verilogModule: Verilog):
  with open(os.path.join(target, verilogModule.filename), "w") as f:
    f.write(verilogModule.toModule())

'''
Find jinja variables from string
'''
def find_jinja_template(strings):
  data = []
  p = re.compile(".*\{\{\s+([a-z|A-Z|0-9|_]*)\s+\}\}.*")
  for each in strings.split("\n"):
    k = p.match(each)
    if k != None:
      data.append(k.group(1))
  return data

'''
Add ports defined in socto module
'''
def toPort(module, instanceName, function = None):
  if function == None:
    def f(x):
      return (x.name, True)
    function = f
  if isinstance(instanceName, Verilog):
    instanceName = instanceName.key
  instance = module.instances[instanceName]
  for each in [each for each in instance["raw"].ports.get()]:
    (portName, result) = function(each)
    if result:
      module.ports.add(name=portName, direction=each.direction, bit=each.bit, target=None, source=instance["raw"])
  # wires = [each for each in module.wires.get() if each.source == instance["raw"]]
  # for each in wires:
  #   name = each.name.replace(f"Wire_{instanceName}_","")
  #   if function(name)[1]:
  #     module.wires.remove(each)

'''
'''
def to_the_pad(module, instance, jinja):
  pors_name_list = [each.name for each in module.ports.get()]
  wires = [each for each in module.wires.get() if each.source == module.instances[instance]["raw"] and "PAD_" + each.name.replace(f"Wire_{instance}_","") in pors_name_list]
  data = {}
  for each in wires:
    x = Wire(bit = each.bit, name = each.name, source = each.source)
    module.wires.remove(x)
    data[each.name] = toJinja("PAD_" + each.name.replace(f"Wire_{instance}_",""))
  for each in jinja:
    if each not in data.keys():
      data[each] = toJinja(each)

  return data
def connect_instance_with_port(module, instance, instance_jinja):
  pors_name_list = [each.name for each in module.ports.get()]
  wires = [each for each in module.wires.get() if each.source == module.instances[instance]["raw"] and each.name.replace(f"Wire_{instance}_","") in pors_name_list]
  data = {}
  # for each in instance_jinja:0
  #   if each not in [each.name for each in module.wires.get()]:
  #     data[each] =
  for each in wires:
    x = Wire(bit = each.bit, name = each.name, source = each.source)
    module.wires.remove(x)
    data[each.name] = toJinja(each.name.replace(f"Wire_{instance}_",""))
  # print(instance)
  for each in instance_jinja:
    if each not in data.keys():
      data[each] = toJinja(each)
  return data

def finalize(module, instance, jinja):
  data = {}
  if len(jinja) == 0:
    return data
  max_length = max([len(each) for each in jinja])
  for each in jinja:
    data[each] = "  " + each.ljust(max_length) + "  "
  return data

def by_port(module, instance, jinja):
  module.wires = type(module.wires)()
  data = {each : toJinja(each.replace("Wire_","")) for each in jinja}
  return data

def name_match(module, instance, jinja):
  data = {}
  # print(module.wires.get())
  design_ports = [each for each in module.instances["designTop"]["raw"].ports.get() if each.direction != "inout"]
  pad_wires = [each for each in module.wires.get() if each.source != None and each.source == Verilog("","", "padTop")]
  for each in design_ports:
    x = each.name + f"_pin_{each.direction}"
    y  = [each for each in jinja if x in each]
    if len(y) == 0:
      continue
    key = y[0]
    removing_wire = [each for each in pad_wires if each.name in key][0]
    module.wires.remove(removing_wire)
    data[key] = toJinja("Wire_designTop_" + each.name)
  for each in jinja:
    if each not in data.keys():
      data[each] = toJinja(each)#"{{ " + each + " }}"
  return data
  # designTop_wires = [(f"{each.prefix}{each.name}".strip(), each.direction.strip(), each.name.strip()) for each in  module.instances["designTop"]["raw"].ports.get()]
  # data = {}
  # socTop_wires = module.wires.get()
  # pad_wires = [each for each in list(socTop_wires) if each.prefix == "padTop_"]
  # for (wire, direction, name) in designTop_wires:
  #   if direction == "inout":
  #     continue

  #   x = name + f"_pin_{direction.strip()}"
  #   y = [each for each in jinja if x in each]
  #   if len(y) == 0:
  #     continue
  #   z = y[0]
  #   removingWire = [each for each in pad_wires if each.name.strip() in z][0]
  #   module.wires.remove(removingWire)
  #   data[z] = wire
  # for each in jinja:
  #   if each not in data.keys():
  #     data[each] = "{{ " + each + " }}"
  # return data
