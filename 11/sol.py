import fileinput
from itertools import product, combinations
from math import inf

universe = [list(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

def solve(universe, expansion):
    n, m = len(universe), len(universe[0])

    rows = [0] * n
    cols = [0] * m
    galaxies = []

    for r, c in product(range(n), range(m)):
        if universe[r][c] == "#":
            rows[r] += 1
            cols[c] += 1
            galaxies.append((r, c))

    res = 0
    for g1, g2 in combinations(galaxies, 2):
        r1, c1 = g1
        r2, c2 = g2
        mnr, mxr = sorted([r1, r2])
        mnc, mxc = sorted([c1, c2])
        total = mxr - mnr + mxc - mnc
        total += sum(expansion for i in range(mnr, mxr) if rows[i] == 0)
        total += sum(expansion for i in range(mnc, mxc) if cols[i] == 0)
        res += total
    return res


def part1(universe):
    return solve(universe, 1)

def part2(universe):
    return solve(universe, 999999)

print(part1(universe))
print(part2(universe))
