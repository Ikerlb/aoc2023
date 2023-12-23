import fileinput
from functools import lru_cache
from itertools import chain

def parse(line):
    arr, cont = line.split(" ")
    return list(arr), [int(n) for n in cont.split(",")]


def count_ways(s, conts):
    @lru_cache(None)
    def ways(i, j, c, prv):

        if i >= len(s) and j == len(conts):
            return int(c == 0)
        if i >= len(s):
            return 0

        if c == 0 and prv == "#" and s[i] == "#":
            return 0
        if c == 0 and prv == "#" and s[i] == "?":
            return ways(i + 1, j, 0, ".")
        if s[i] == "?" and j == len(conts):
            return ways(i + 1, j, 0, ".")

        if s[i] == "#" and j == len(conts):
            return 0
        if s[i] == "#" and c + 1 < conts[j]:
            return ways(i + 1, j, c + 1, "#")
        if s[i] == "#" and c + 1 == conts[j]:
            return ways(i + 1, j + 1, 0, "#")

        if s[i] == "." and c == 0:
            return ways(i + 1, j, 0, ".")
        if s[i] == "." and c > 0:
            return 0

        if s[i] != "?":
            return 0

        if c + 1 < conts[j]:
            res = ways(i + 1, j, c + 1, "#")
        else:
            res = ways(i + 1, j + 1, 0, "#")

        if c == 0:
            res += ways(i + 1, j, 0, ".")

        return res
    return ways(0, 0, 0, None)

def unfold(s, c):
    ns = "?".join("".join(s) for _ in range(5))
    nc = c * 5
    return ns, nc

springs = [parse(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

def part1(springs):
    return sum(count_ways(*s) for s in springs)

def part2(springs):
    nsprings = [unfold(*s) for s in springs]
    return sum(count_ways(*s) for s in nsprings)

print(part1(springs))
print(part2(springs))

