import fileinput
from math import inf
from heapq import heappush, heappop

#def format(grid, sep = ","):
#    return "\n".join(sep.join(map(str, row)) for row in grid)

def format(grid, path = {}, sep = ","):
    res = []
    for r in range(len(grid)):
        row = []
        for c in range(len(grid[0])):
            if (r, c) in path:
                row.append("#")
            else:
                #row.append(str(grid[r][c]))
                row.append(".")
        res.append(sep.join(row))
    return "\n".join(res)

def neighbors(grid, r, c):
    for dr, dc in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if not 0 <= nr < len(grid):
            continue
        if not 0 <= nc < len(grid[0]):
            continue
        yield nr, nc, dr, dc

def opposite(dr, dc):
    return -dr, -dc

def minimum_heat_loss_p1(grid, sr, sc, tr, tc):
    
    h = [(0, sr, sc, 0, 0, 0)]
    seen = {h[0][1:]}

    while h:
        w, r, c, pdr, pdc, cn = heappop(h)
        if (r, c) == (tr, tc):
            return w
        for nr, nc, dr, dc in neighbors(grid, r, c):
            nn = cn + 1 if (pdr,pdc) == (dr,dc) else 1
            if dr == -pdr and dc == -pdc:
                continue
            if nn > 3:
                continue
            if (nr, nc, dr, dc, nn) in seen:
                continue

            # can use the same object if it is too slow
            seen.add((nr, nc, dr, dc, nn))
            heappush(h, (w + grid[nr][nc], nr, nc, dr, dc, nn))

def create_path(grid, seen, end):
    s = [end]
    while s and s[0]:
        k = s.pop()
        yield k[0], k[1]
        s.append(seen[k])

def minimum_heat_loss_p2(grid, sr, sc, tr, tc):
    
    h = [(0, sr, sc, 0, 0, inf)]
    seen = {h[0][1:]: None}

    while h:
        w, r, c, pdr, pdc, cn = heappop(h)
        if (r, c) == (tr, tc) and cn >= 4:
            return w
        for nr, nc, dr, dc in neighbors(grid, r, c):
            nn = cn + 1 if (pdr,pdc) == (dr,dc) else 1
            if dr == -pdr and dc == -pdc:
                continue
            if (cn < 4 and nn == 1) or nn > 10:
                continue
            if (nr, nc, dr, dc, nn) in seen:
                continue

            # can use the same object if it is too slow
            #seen.add((nr, nc, dr, dc, nn))
            seen[(nr, nc, dr, dc, nn)] = (r, c, pdr, pdc, cn)
            heappush(h, (w + grid[nr][nc], nr, nc, dr, dc, nn))
    

def part1(grid):
    n, m = len(grid), len(grid[0])
    return minimum_heat_loss_p1(grid, 0, 0, n - 1, m - 1)

def part2(grid):
    n, m = len(grid), len(grid[0])
    #seen, end = minimum_heat_loss_p2(grid, 0, 0, n - 1, m - 1)
    #path = set(create_path(grid, seen, end))
    #print(format(grid, path = path, sep = ""))
    return minimum_heat_loss_p2(grid, 0, 0, n - 1, m - 1)

lines = fileinput.input(encoding = "utf-8")
grid = [[int(c) for c in line[:-1]] for line in lines]

print(part1(grid))
print(part2(grid))
