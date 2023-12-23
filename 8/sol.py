import fileinput
from collections import defaultdict
from itertools import cycle
import re

def parse(lines):
    instructions = lines[0]
    regex = r'(.+) = \((.+), (.+)\)'
    g = defaultdict(dict)
    for line in lines[2:]:
        node, l, r = re.findall(regex, line).pop()
        g[node]["L"] = l
        g[node]["R"] = r
    return instructions, g 

lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]
instrs, graph = parse(lines)

def part1(instrs, graph):
    node = "AAA"
    i = 0
    for instr in cycle(instrs):
        if node == "ZZZ":
            break
        node = graph[node][instr]
        i += 1
    return i

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

def lcm(*l):
    if len(l) == 1:
        return l[0]
    res = (l[0] * l[1]) // gcd(l[0], l[1])
    for i in range(2, len(l)):
        res = (res * l[i]) // gcd(res, l[i])
    return res

# after further inspection
# each node only touches a
# single ending node
def find_cycle(graph, node, instrs):
    i = 0
    seen = {}
    for i, instr in enumerate(cycle(instrs)):
        mod = i % len(instrs)
        if (mod, node) in seen:
            return i - seen[(mod, node)]
        seen[(mod, node)] = i
        node = graph[node][instr]
        i += 1

def part2(instrs, graph):
    nodes = [k for k in graph if k[-1] == "A"]
    return lcm(*(find_cycle(graph, node, instrs) for node in nodes))

print(part1(instrs, graph))
print(part2(instrs, graph))
