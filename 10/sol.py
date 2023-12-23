import fileinput
from itertools import chain, product
from collections import defaultdict, deque

grid = [list(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

accesible = {
    (1,0): {"|", "J", "L"},
    (0, 1): {"-", "J", "7"},
    (-1, 0): {"|", "F", "7"},
    (0,-1): {"-", "L", "F"}
}

# down  (1,  0)
# right (0,  1)
# up    (-1, 0)
# left  (0, -1)
directions = {
    'L': [(-1, 0), (0, 1)],
    '-': [(0, -1), (0, 1)],
    '7': [(0, -1), (1, 0)],
    '|': [(-1, 0), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    'F': [(0, 1), (1, 0)]
}

def opposite(tup):
    r, c = tup
    return -r, -c

pipes = set(chain(*accesible.values()))

def dfs(grid, groups, pipes, accesible, directions, r, c, group):
    s = [(r, c)]
    groups[r][c] = group
    res = 0
    while s:
        r, c = s.pop()
        res += 1
        for dr, dc in directions[grid[r][c]]:
            nr, nc = r + dr, c + dc
            if not in_bounds(grid, nr, nc):
                continue
            if groups[nr][nc] not in pipes:
                continue
            if groups[nr][nc] not in accesible[dr, dc]:
                continue
            s.append((nr, nc))
            groups[nr][nc] = group
    return res

def format(grid, path, other):
    d = {
        "|": "┃",
        "-": "━",
        "F": "┏",
        "J": "┛",
        "L": "┗",
        "7": "┓",
        "S": "S"
    }
    res = []
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[r])):
            if grid[r][c] in d and (r, c) in path:
                row.append(d[grid[r][c]])
            elif (r, c) in other:
                row.append("X")
            else:
                row.append(grid[r][c])
        res.append("".join(row))
    return "\n".join(res)

def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def find_s_shape(grid, groups, sr, sc, directions, accesible):
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    for d1, d2 in product(dirs, repeat = 2):
        dr1, dc1 = d1
        dr2, dc2 = d2
        if dr1 == dr2 and dc1 == dc2:
            continue
        r1, c1 = sr + dr1, sc + dc1
        r2, c2 = sr + dr2, sc + dc2
        if not in_bounds(groups, r1, c1):
            continue
        if not in_bounds(groups, r2, c2):
            continue
        if grid[r1][c1] not in directions:
            continue
        if grid[r2][c2] not in directions:
            continue
        dirs1 = [groups[r1+dr][c1+dc] for dr, dc in directions[grid[r1][c1]]]
        dirs2 = [groups[r2+dr][c2+dc] for dr, dc in directions[grid[r2][c2]]]
        
        if "S" not in dirs1 or "S" not in dirs2:
            continue
        if groups[r1][c1] == groups[r2][c2]: 
            od1 = opposite(d1)
            od2 = opposite(d2)
            return (accesible[od1] & accesible[od2]).pop()

def furthest_distance(grid, directions, r, c):
    q = deque([(r, c)])
    visited = {(r, c)}
    res = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in directions[grid[r][c]]:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    q.append((nr, nc))
        res += 1
    return res - 1

def path(grid, directions, sr, sc):
    s = [(sr, sc)]
    seen = {(sr, sc)}
    path = []
    while s:
        r, c = s.pop()
        path.append((r, c))
        for dr, dc in directions[grid[r][c]]:
            nr, nc = r + dr, c + dc
            if (nr, nc) not in seen:
                seen.add((nr, nc))
                s.append((nr, nc))
    return path

def complete_pipe_loop(grid, accesible, directions):
    n, m = len(grid), len(grid[0])
    groups = [row[:] for row in grid]
    i = 0
    for r, c in product(range(n), range(m)):
        if groups[r][c] in pipes:
            dfs(grid, groups, pipes, accesible, directions, r, c, i)
            i += 1
        elif groups[r][c] == "S":
            sr, sc = r, c
    s = find_s_shape(grid, groups, sr, sc, directions, accesible)
    grid[sr][sc] = s
    return grid, sr, sc

def part1(grid, directions, sr, sc):
    return furthest_distance(grid, directions, sr, sc)

def ccw(r, c):
    return -c, r

def cw(r, c):
    return c, -r

# well this obviously overflowed stack
#def floodfill(grid, r, c, visited):
#    if not in_bounds(grid, r, c):
#        return 0
#    if (r, c) in visited:
#        return 0
#    res = 1
#    visited.add((r, c))
#    for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
#        res += floodfill(grid, r + dr, c + dc, visited)
#    return res

def floodfill(grid, r, c, visited):
    s = [(r, c)]
    visited.add((r, c))
    res = 0
    while s:
        r, c = s.pop()
        res += 1
        for dr, dc in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in visited:
                continue
            if not in_bounds(grid, nr, nc):
                continue
            s.append((nr, nc))
            visited.add((nr, nc))
    return res

def solve(grid, path, f):
    visited = set(path)
    res = 0
    counted = set()
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        dr, dc = f(r2 - r1, c2 - c1)
        for nr, nc in [(r1+dr, c1+dc), (r2+dr, c2+dc)]:
            if in_bounds(grid, nr, nc) and (nr, nc) not in visited:
                res += floodfill(grid, nr, nc, visited)
                #print(f"res is {res}")
                #print(format(grid, set(path), visited), end = "\n\n")
    return res

def part2(grid, path):
    return [solve(grid, path, ccw), solve(grid, path, cw)]

grid, sr, sc = complete_pipe_loop(grid, accesible, directions)

print(part1(grid, directions, sr, sc))

# i think answer can be both!
# but looking at the input
# the minimum should be the winner
path = path(grid, directions, sr, sc)
print(part2(grid, path))

