import fileinput
import re

def parse_workflow(line):
    regex = r'([a-zA-Z]+)\{(.+)\}'
    label, rules = next(re.finditer(regex, line)).groups()
    return label, rules.split(",")

def parse_ratings(line):
    pass    

lines = "".join(line for line in fileinput.input(encoding = "utf-8"))
wfs, rts = lines.split("\n\n")

wfs = [parse_workflow(line) for line in wfs.splitlines()]
rts = [parse_ratings(line) for line in rts.splitlines()]

