import fileinput
import re
from collections import deque

DIRS = {
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0)
}

def parse_hex(hx):
    n, d = int(hx[:-1], 16), int(hx[-1])
    res = *list(DIRS.values())[d], n
    return res

def parse(line):
    regex = r'([RDUL]) (\d+) \(#([a-z0-9]+)\)'
    d, n, hx = next(re.finditer(regex, line)).groups()
    dr, dc = DIRS[d]
    return dr, dc, int(n), hx

def move(r, c, dr, dc):
    dr = dr * steps
    dc = dc * steps
    return r + dr, c + dc

def full_border(plan):
    r = c = 0
    for dr, dc, n, _ in plan:
        for _ in range(n):
            nr, nc = r + dr, c + dc
            yield r, c
            r, c = nr, nc

def walk_p1(plan):
    r = c = 0
    yield r, c
    for dr, dc, n, _ in plan:
        r, c = r + dr * n, c + dc * n
        yield r, c

def walk_p2(plan):
    r = c = 0
    yield r, c
    for _, _, _, hx in plan:
        dr, dc, n = parse_hex(hx)
        r, c = r + dr * n, c + dc * n
        yield r, c


def polygon(plan):
    gen = walk(plan)
    pr, pc, pdr, pdc = next(gen)
    points = [(pr, pc, pdr, pdc)]
    for r, c, dr, dc in gen:
        if (dr, dc) != (pdr, pdc):
            points.append((r, c, dr, dc))
        pr, pc, pdr, pdc = r, c, dr, dc
    return points
    
def det(p, q):
    r1, c1 = p
    r2, c2 = q
    return r2 * c1 - r1 * c2

def signed_area(polygon):
    res = det(polygon[0], polygon[-1])
    for p, q in zip(polygon, polygon[1:]):
        res += det(p, q)
    return res / 2

def diff(p, q):
    r1, c1 = p
    r2, c2 = q
    return abs(r2 - r1) + abs(c2 - c1)

def perimeter(polygon):
    res = diff(polygon[-1], polygon[0])
    for p, q in zip(polygon, polygon[1:]):
        res += diff(p, q)
    return res

def minmax(l):
    mn = mx = next(l)
    for e in l:
        mn = min(mn, e)
        mx = max(mx, e)
    return mn, mx

def bounding_box(border):
    rmn, rmx = minmax(r for r, _  in border)
    cmn, cmx = minmax(c for _, c  in border)
    return rmn, rmx, cmn, cmx

def format(border):
    rmn, rmx, cmn, cmx = bounding_box(border)
    res = []
    for r in range(rmn, rmx + 1):
        row = []
        for c in range(cmn, cmx + 1):
            if (r, c) in border: 
                row.append("#")
            else:
                row.append(".")
        res.append("".join(row))
    return "\n".join(res)

def floodfill(visited, r, c):
    s = [(r, c)]
    while s: 
        r, c = s.pop()
        for dr, dc in DIRS.values():
            nr, nc = r + dr, c + dc
            if (nr, nc) in visited:
                continue
            visited.add((nr, nc))
            s.append((nr, nc))

def ccw(dr, dc):
    return -dc, dr

def cw(dr, dc):
    return dc, -dr

def part1(plan):
    poly = list(walk_p1(plan))
    p = perimeter(poly)
    a = abs(signed_area(poly))
    return int(p // 2 + a) + 1

def part2(plan):
    poly = list(walk_p2(plan))
    p = perimeter(poly)
    a = abs(signed_area(poly))
    return int(p // 2 + a) + 1

plan = [parse(line) for line in fileinput.input(encoding = "utf-8")]

print(part1(plan))
print(part2(plan))
