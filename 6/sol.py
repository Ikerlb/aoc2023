import fileinput

lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]

def parse(lines):
    _, time = lines[0].split(":")
    _, distance = lines[1].split(":")

    time = [int(t) for t in time.split()]
    distance = [int(d) for d in distance.split()]

    return time, distance

def num_ways(time, record):
    res = sum(1 for i in range(time+1) if (d := i * (time - i)) > record)
    return res

def part1(time, distance):
    res = 1
    for t, d in zip(time, distance):
        res *= num_ways(t, d)
    return res

def part2(time, distance):
    time = int("".join(map(str, time)))
    distance = int("".join(map(str, distance)))
    return num_ways(time, distance)

time, distance = parse(lines)

print(part1(time, distance))
print(part2(time, distance))
