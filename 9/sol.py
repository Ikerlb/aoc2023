import fileinput
from collections import deque

def parse(line):
    return [int(i) for i in line.split(" ")]

histories = [parse(line[:-1]) for line in fileinput.input(encoding = "utf-8")]

def deltas(history):
    prev = history
    yield prev
    while any(p != 0 for p in prev):
        n = len(prev)
        history = [prev[i + 1] - prev[i] for i in range(n - 1)]
        yield history
        prev = history

def extrapolate_right(history):
    s = list(deltas(history))
    while len(s) > 1:
        last = s.pop()
        s[-1].append(s[-1][-1] + last[-1])
    return s.pop()[-1]

def extrapolate_left(history):
    s = [deque(ss) for ss in deltas(history)]
    while len(s) > 1:
        last = s.pop()
        s[-1].appendleft(s[-1][0] - last[0])
    return s.pop()[0]

def part1(histories):
    return sum(extrapolate_right(history) for history in histories)

def part2(histories):
    return sum(extrapolate_left(history) for history in histories)

print(part1(histories))
print(part2(histories))
