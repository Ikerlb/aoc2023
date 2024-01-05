import fileinput
from collections import defaultdict

grid = [list(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

# (0, 1) -> (-1,0)
# (-1,0) -> (0,-1)
# (0,-1) -> (1, 0)
# (1, 0) -> (0, 1)
def ccw(dr, dc):
    return -dc, dr

# (0, 1) -> (1, 0)
# (1, 0) -> (0,-1)
# (0,-1) -> (-1,0)
# (-1,0) -> (0, 1)
def cw(dr, dc):
    return dc, -dr


# for /
# (0,-1)</ -> v ccw
# (0, 1)>/ -> ^ ccw
# (-1,0)^/ -> > cw
# (1, 0)v/ -> < cw

# for \
# (0,-1)<\ -> ^ cw
# (0, 1)>\ -> v cw
# (-1,0)^\ -> < cww
# (1, 0)v\ -> > cww

def move(dr, dc, char):
    match (dr, dc, char):
        case (_, _, "."):
            return [(dr, dc)]
        case (0, _, "/"):
            return [ccw(dr, dc)]
        case (_, 0, "/"):
            return [cw(dr, dc)]
        case (0, _, "\\"):
            return [cw(dr, dc)]
        case (_, 0, "\\"):
            return [ccw(dr, dc)]
        case (0, 1, "-") | (0, -1, "-"):
            return [(dr, dc)]
        case (0, 1, "|") | (0, -1, "|"):
            return [(1, 0), (-1, 0)]
        case (1, 0, "|") | (-1, 0, "|"):
            return [(dr, dc)]
        case (1, 0, "-") | (-1, 0, "-"):
            return [(0, 1), (0, -1)]
        case default:
            print("que pedo que pedo que pedo", dr, dc, char)

def fmt_dir(dr, dc):
    match (dr, dc):
        case (0, 1):
            return ">"
        case (0, -1):
            return "<"
        case (1, 0):
            return "v"
        case (-1, 0):
            return "^"


def format(grid, d):
    res = []
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[r])):
            if (r, c) in d and len(d[(r, c)]) == 1:
                row.append(fmt_dir(*d[(r, c)][0]))
            elif (r, c) in d:
                row.append(str(len(d[(r, c)])))
            else:
                row.append(".")
        res.append("".join(row))
    return "\n".join(res)

def beams(grid, r, c, dr, dc):
    s = [(r, c, dr, dc)]
    d = defaultdict(list)
    d[(r, c)].append((dr, dc))
    while s:
        r, c, dr, dc = s.pop()
        for ndr, ndc in  move(dr, dc, grid[r][c]):
            if not 0 <= (nr := r + ndr) < len(grid):
                continue
            if not 0 <= (nc := c + ndc) < len(grid[0]):
                continue
            if (nr, nc) in d and (ndr, ndc) in d[(nr, nc)]:
                continue
            s.append((nr, nc, ndr, ndc))
            d[(nr, nc)].append((ndr, ndc))
    return d

def energy(grid, r, c, dr, dc):
    bs = beams(grid, r, c, dr, dc)
    return len(bs)

def part1(grid):
    return energy(grid, 0, 0, 0, 1)

def part2(grid):
    s = []

    n, m = len(grid), len(grid[0])

    # from left to right
    s.extend((r, 0, 0, 1) for r in range(n))

    # from right to left
    s.extend((r, m - 1, 0, -1) for r in range(n))

    # from top to bottom
    s.extend((0, c, 1, 0) for c in range(m))

    # from bottom to top
    s.extend((n - 1, c, -1, 0) for c in range(m))

    return max(energy(grid, *tup) for tup in s)

print(part1(grid))
print(part2(grid))
