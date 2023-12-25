import fileinput

def parse(pattern):
    p = []
    for row in pattern:
        p.append([int(c == "#") for c in row])
    return p

lines = "".join(line for line in fileinput.input(encoding = "utf-8"))

patterns = [parse(pattern.splitlines()) for pattern in lines.split("\n\n")]

def h_reflect(pattern, r):
    res = 0
    for r1, r2 in zip(reversed(pattern[:r]), pattern[r:]):
        res += diff(r1, r2)
        if res > 1:
            return None
    return res

def col(pattern, c):
    return [row[c] for row in pattern]

def diff(i1, i2):
    return sum(i != j for i, j in zip(i1, i2))

def v_reflect(pattern, c):
    res = 0
    for c1, c2 in zip(reversed(range(c)), range(c, len(pattern[0]))):
        res += diff(col(pattern, c1), col(pattern, c2))
        if res > 1:
            return None
    return res

def find_reflection_line(pattern):
    # vertical
    for c in range(1, len(pattern[0])):
        if v_reflect(pattern, c) == 0:
            return "v", c

    # horizontal
    for r in range(1, len(pattern)):
        if h_reflect(pattern, r) == 0:
            return "h", r

    return None

def smudges(pattern):
    vsmudges, hsmudges = [], []

    # vertical
    for c in range(1, len(pattern[0])):
        if v_reflect(pattern, c) == 1:
            vsmudges.append(c)

    # horizontal
    for r in range(1, len(pattern)):
        if h_reflect(pattern, r) == 1:
            hsmudges.append(r)

    return vsmudges, hsmudges

def format(pattern):
    return "\n".join("".join("#" if c == 1 else "." for c in row) for row in pattern)

def summarize(pattern):
    res = 0
    r = find_reflection_line(pattern)
    orient, n = r
    if orient == "h": 
        res += 100 * n
    else:
        res += n
    return res

def part1(patterns):
    return sum(summarize(pattern) for pattern in patterns)

def part2(patterns):
    res = 0
    for pattern in patterns:
        vsmudges, hsmudges = smudges(pattern)
        assert(len(vsmudges) + len(hsmudges) <= 1)
        if vsmudges:
            res += vsmudges.pop()
        else:
            res += 100 * hsmudges.pop()
    return res

print(part1(patterns))
print(part2(patterns))
