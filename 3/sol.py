import fileinput
import re
from itertools import product
from collections import defaultdict

class Node:
    def __init__(self, val, xs, xe, y):
        self.val = val
        self.xs = xs
        self.xe = xe
        self.y = y

    def vicinity(self):
        s = set()
        for x in range(self.xs, self.xe):
            g = product((0, -1, 1), repeat = 2)
            next(g) # burn
            s.update((x + dx, self.y + dy) for dx, dy in g)
        return s - {(x, self.y) for x in range(self.xs, self.xe)}

    # supposing there is only ever one symbol adjacent to a node
    def is_symbol_adjacent(self, grid, symbols):
        for vx, vy in self.vicinity():
            if not 0 <= vy < len(grid):
                continue
            if not 0 <= vx < len(grid[0]):
                continue
            if grid[vy][vx] in symbols:
                return (vy, vx)
        return None

    def __repr__(self):
        return f"v={self.val}, [{self.xs}, {self.xe}] on row {self.y}"

def parse(line, row):
    regex = r'(\d+)'
    res = []
    for i in re.finditer(regex, line):
        scol, ecol = i.span()
        res.append(Node(int(i[0]), scol, ecol, row))
    return res

lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]
grid = [list(line) for line in lines]
nodes = []
for row, line in enumerate(lines):
    nodes.extend(parse(line, row))

def part1(grid, nodes):
    symbols = '+-/&#%$=@*'
    res = 0
    for node in nodes:
        if (adj := node.is_symbol_adjacent(grid, symbols)) is not None:
            res += node.val
    return res

def prod(l):
    res = 1
    for n in l:
        res *= n
    return res

def part2(grid, nodes):
    symbols = '*'
    groups = defaultdict(list)
    for node in nodes:
        if (adj := node.is_symbol_adjacent(grid, symbols)) is not None:
            groups[adj].append(node.val)
    return sum(prod(l) for l in groups.values() if len(l) > 1)

print(part1(grid, nodes))
print(part2(grid, nodes))

