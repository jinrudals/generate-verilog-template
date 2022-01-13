from utils.Ports import Ports
from utils.Wires import Wires
from utils.Assigns import Assigns

import jinja2, os, re

def remove_empty_line(data):
  string = data["content"]
  data["content"] = "\n".join([each for each in string.split("\n") if each.strip() != ""])
  return data

__base      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__resources = os.path.join(__base, os.path.join("resources", "jinja"))
with open(os.path.join(__resources, "module.template")) as f:
  moduleTemplate = jinja2.Template("".join(f.readlines()))
with open(os.path.join(__resources, "instance.template")) as f:
  instaneTemplate = jinja2.Template("".join(f.readlines()))

def find_jinja_template(strings):
  data = []
  p = re.compile(".*\{\{\s+([a-z|A-Z|0-9|_]*)\s+\}\}.*")
  for each in strings.split("\n"):
    k = p.match(each)
    if k != None:
      data.append(k.group(1))
  return data

class Verilog:
  def __repr__(self):
    return f"Verilog (modulename = {self.modulename})"
  def __eq__(self, other):
    return type(other) == Verilog and self.key == other.key
  def __init__(self, modulename, filename = None, key = None):
    self.modulename = modulename
    filename = modulename if filename == None else  filename
    self.filename   = filename if filename.endswith(".v") or filename.endswith(".sv") else filename + ".v"
    self.key        = modulename if key == None else key
    self.instances  = dict()
    self.ports      = Ports()
    self.wires      = Wires()
    self.assigns    = Assigns()

  def add_instance(self, instance, verilog = None):
    if verilog == None:
      verilog = instance
      instance = verilog.key
      # self.addInstance(instance=instance.key, verilog=instance)
    self.instances[instance] = {"raw" : verilog, "content" : verilog.toInstance(instance, self)}
  def update_instance(self, instance, *f):
    if isinstance(instance, Verilog):
      instance = instance.key
    for each in f:
      raw = self.instances[instance]["raw"]
      content = self.instances[instance]["content"]
      jinja_input = find_jinja_template(content)
      results = each(self, instance, jinja_input)
      self.instances[instance]["content"] = jinja2.Template(content).render(**results)
      if "old" not in self.instances[instance].keys():
        self.instances[instance]["old"] = []
      self.instances[instance]["old"].append(content)

  def toModule(self):
    includes = set([each["raw"].filename for each in self.instances.values()])
    return moduleTemplate.render(module=self.modulename, includes=includes, instances=[remove_empty_line(each) for each in  self.instances.values()], ports=self.ports.align().sort().get(), wires=self.wires.align().sort().get(), assigns=self.assigns.align().sort().get())
  def toInstance(self, instanceName, parentModule = None):
    if parentModule != None:
      for each in self.ports.get():
        parentModule.wires.add(name=f"Wire_{instanceName}_{each.name}", bit=each.bit, source=self)
    return instaneTemplate.render(module=self.modulename, instance=instanceName, ports=self.ports.align().sort().get())
