import fileinput
import re

def parse(line):
    _, rest = line.split(": ")
    winning, have = rest.split(" | ")
    winning = {int(w) for w in re.findall(r'(\d+)', winning)}
    have = {int(h) for h in re.findall(r'(\d+)', have)}
    return winning, have

def part1(games):
    res = 0
    for winning, have in games:
        inter = have & winning
        if inter:
            i = len(inter) - 1
            res += 1 << i
    return res

def part2(games):
    res = 0
    copies = [1 for _ in range(len(games))]
    for i, (winning, have) in enumerate(games):
        inter = have & winning
        for j in range(1, len(inter) + 1):
            copies[i + j] += copies[i]
    return sum(copies)

games = [parse(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

print(part1(games))
print(part2(games))
