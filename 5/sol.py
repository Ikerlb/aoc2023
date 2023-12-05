import fileinput
from collections import defaultdict

lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]

def parse(txt):
    seeds, rest = txt.split("\n\n", 1)
    smaps = rest.split("\n\n")
    maps = defaultdict(list)
    for smap in smaps:
        lines = smap.splitlines("\n")
        name, _ = lines[0].split(" ") 
        for line in lines[1:]:
            dests, srcs, length = map(int, line.split(" ")) 
            maps[name].append((dests, srcs, length))
    seeds = seeds.split(": ")[1]
    return [int(s) for s in seeds.split(" ")], maps

seeds, mappings = parse("\n".join(lines))

def transform(mapping, num):
    for dests, srcs, lengths in mapping:
        if srcs <= num <= srcs + lengths:
            delta = num - srcs
            return dests + delta
    return num

def transform_range(mapping, start, end):
    for dests, srcs, lengths in mapping:
        if srcs <= start <= end <= srcs + lengths - 1:
            deltas = start - srcs
            deltae = end - srcs
            return [[dests + deltas, dests + deltae]]
        elif srcs <= start <= srcs + lengths - 1:
            rests, reste = srcs + lengths, end
            deltas = start - srcs
            deltae = srcs + lengths - 1 - srcs
            inter = [dests + deltas, dests + deltae]
            return [inter] + transform_range(mapping, rests, reste)
        elif srcs <= end <= srcs + lengths - 1:
            rests, reste = start, srcs - 1
            inter = [dests, dests + end - srcs]
            return [inter] + transform_range(mapping, rests, reste)
    else:
        return [[start, end]]

categories = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location"
]

def part1(mappings, seeds, categories):
    vals = seeds
    for cat in categories:
        vals = [transform(mappings[cat], val) for val in vals]
    return min(vals)

def part2(mappings, seeds, categories):
    intervals = []
    for i in range(0, len(seeds), 2):
        intervals.append((seeds[i], seeds[i] + seeds[i + 1] - 1))
    for cat in categories:
        nintervals = []
        for s, e in intervals:
            nintervals.extend(transform_range(mappings[cat], s, e))
        intervals = nintervals
    return min(inter[0] for inter in intervals)

print(part1(mappings, seeds, categories))
print(part2(mappings, seeds, categories))
