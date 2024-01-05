import fileinput
from itertools import repeat

grid = [list(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

def split_by(l, elem):
    indices = [-1]
    indices.extend(i for i in range(len(l)) if l[i] == elem)
    indices.append(len(l))

    res = []
    for i, j in zip(indices, indices[1:]):
        res.append(l[i + 1:j])
    return res

def support(grid):
    res = 0
    for i, row in enumerate(grid):
        c = row.count('O')
        res += (len(grid) - i) * c
    return res

# mutates grid
def _rotate(grid, level):
    s, e = level, len(grid) - 1 - level

    for i in range(e - s):
        aux = grid[s][s+i]    
        grid[s][s+i] = grid[s+i][e]
        grid[s+i][e] = grid[e][e-i]
        grid[e][e-i] = grid[e-i][s]
        grid[e-i][s] = aux

# mutates grid
def rotate(grid):
    for l in range(len(grid) // 2):
        _rotate(grid, l)    
    return grid

def format(grid):
    return "\n".join("".join(row) for row in grid)

def intersperse(l, delimiter):
    res = l[0][:]
    for x in l[1:]:
        res.append(delimiter)
        res.extend(x)
    return res

# just tilt to the left
# worry about rotations
# elsewhere
def _tilt(grid):
    res = []
    for row in grid:
        nrow = []
        for chunk in split_by(row, "#"):
            c = chunk.count("O")
            n = len(chunk)
            nrow.append(list(repeat("O", c)) + list(repeat(".", n - c)))
        res.append(intersperse(nrow, "#"))
    return res

# 0 goes <
# 1 goes ^
# 2 goes >
# 3 goes v
# mutates grid
def tilt(grid, direction):
    grid = [row[:] for row in grid]
    for _ in range(direction):
        rotate(grid)
    grid = _tilt(grid)
    for _ in range((4 - direction) % 4):
        rotate(grid)
    return grid

def cycle(grid):
    grid = tilt(grid, 1)
    grid = tilt(grid, 0)
    grid = tilt(grid, 3)
    return tilt(grid, 2)

def part1(grid):
    return support(tilt(grid, 1))

def cycle_length(grid):
    i = 0
    s = {format(grid):i}
    while True:
        grid = cycle(grid)
        fmt = format(grid)
        if fmt in s:
            return s[fmt], i + 1
        i += 1
        s[fmt] = i

def part2(grid):
    i, j = cycle_length(grid)
    for _ in range(i):
        grid = cycle(grid)
    for _ in range((1000000000 - i) % (j - i)):
        grid = cycle(grid)
    return support(grid)

print(part1(grid))
print(part2(grid))
