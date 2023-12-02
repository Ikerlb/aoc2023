import fileinput
from collections import Counter

def parse_set(s):
    cubes = Counter()
    for sc in s.split(", "):
        sn, color = sc.split(" ")
        cubes[color] = int(sn)
    return cubes

def parse(line):
    game, rest = line.split(": ")
    sets = [parse_set(s) for s in rest.split("; ")]
    gid = int(game.split(" ")[1])
    return gid, sets

def part1(games, limits):
    res = 0
    for gid, gconfig in games:
        if all(s[c] <= limits[c] for s in gconfig for c in s):
            res += gid
    return res

def prod(l):
    res = 1
    for n in l:
        res *= n
    return res

def part2(games):
    res = 0
    for gid, gconfig in games:
        mxs = Counter()
        for s in gconfig:
            for c, num in s.items():
                mxs[c] = max(mxs[c], num)
        res += prod(mxs.values())
    return res


lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]
games = [parse(line) for line in lines]

print(part1(games, {"red": 12, "green": 13, "blue": 14}))
print(part2(games))
