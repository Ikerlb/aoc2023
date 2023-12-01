import fileinput

def replace(line):
    snums = {}
    snums["one"] = "1"
    snums["two"] = "2"
    snums["three"] = "3"
    snums["four"] = "4"
    snums["five"] = "5"
    snums["six"] = "6"
    snums["seven"] = "7"
    snums["eight"] = "8"
    snums["nine"] = "9"

    lmn = min(((i, sn) for sn in snums if (i := line.find(sn)) != -1), default = None)
    rmx = max(((i, sn) for sn in snums if (i := line.rfind(sn)) != -1), default = None)

    if lmn is None and rmx is None:
        return line
    elif lmn == rmx:
        i, sn = lmn
        return line[:i] + snums[sn] + line[i + len(sn):]
    else:
        li, lsn = lmn
        ri, rsn = rmx
        left = line[:li] + snums[lsn]
        mid = line[li + len(lsn):ri]
        right = line[ri:] + snums[rsn] + line[ri + len(rsn):]
        return left + mid + right

def calibration(lines):
    for line in lines:
        digits = [int(c) for c in line if c.isdigit()]
        yield digits[0] * 10 + digits[-1]

def part1(lines):
    return sum(calibration(lines))

def part2(lines):
    return sum(calibration(map(replace, lines)))

lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]

# p1
print(part1(lines))

# p2
print(part2(lines))
