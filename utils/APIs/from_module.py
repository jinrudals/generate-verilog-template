import re
import argparse
import json

from utils.Verilog import Verilog

def parsing():
  parser = argparse.ArgumentParser("Parsing Arguments")
  parser.add_argument("--module", help="Module path", required=True)

  parser.add_argument("--output", "-o", help="Output file path", default="ouput.json")
  parser.add_argument("--print", "-p", help="Print Enable", action="store_true")
  parser.add_argument("--enable-output", "-e", help="Enable writing output file", action="store_true", dest="enable_flag")
  return parser

def get_matching_line_number(content, search_pattern, start_from=0):
  p = re.compile(search_pattern)
  for (line, each) in enumerate(content[start_from:]):
    if p.match(each):
      return line + start_from
  return None

def calculate(temp):
  bit_matcher = re.compile("\[\s*([0-9]+):\s*([0-9]+)\]")
  x = bit_matcher.match(temp)
  answer = int(x.group(1)) - int(x.group(2)) + 1
  return answer

def get_matching_temp(data, flag):
  mydata = []
  p = re.compile("\s*,?\s*(input|output|inout)\s*(\[\s*[0-9]+:\s*[0-9]+\])?\s*([a-z|A-Z|_|0-9]*)\s*,?\s*")

  for each in data:
    x = p.match(each)
    if x == None:
      continue
    bitwidth    = 1 if x.group(2) == None else calculate(x.group(2))
    direction   = x.group(1)
    name        = x.group(3)
    temp = {"NAME" : name, "DIRECTION": direction, "BIT" : bitwidth}
    if flag:
      print(temp)
    mydata.append(temp)
  return mydata

def get_required_lines_only(lines):
  start_index = get_matching_line_number(lines, "\s*module [A-Z|a-z|0-9|_]*\s*\(")
  end_index   = get_matching_line_number(lines, '\s*\);', start_index)
  return lines[start_index:end_index]

def get_module_name(line):
  p = re.compile("\s*module\s*([A-Z|a-z|0-9|_]*)\s*\(.*")
  return p.match(line).group(1)

def main(args):
  print_flag = False if "print" not in args.keys() else args["print"]
  data = dict()
  with open (args["module"]) as f:
    lines = f.readlines()
  lines    = get_required_lines_only(lines)
  data["module"] = get_module_name(lines[0])
  data["ports"] = get_matching_temp(lines[1:], print_flag)

  if "enable_flag" in args.keys() and args["enable_flag"]:
    destination = "test.json" if "output" not in args.keys() else args["output"]
    with open(destination, "w") as f:
      json.dump(data, f, indent=4)
  return data
def asVerilog(args):
  data = main(args)
  output = Verilog(data["module"], args["module"])
  for each in data["ports"]:
    output.ports.add(name=each["NAME"], direction=each["DIRECTION"], bit=each["BIT"])
  return output
if __name__ == "__main__":
  args = parsing().parse_args()
  main(vars(args))