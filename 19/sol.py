import fileinput
import re
from collections import defaultdict
from math import inf

def parse_workflow(line):
    regex = r'([a-zA-Z]+)\{(.+)\}'
    label, rules = next(re.finditer(regex, line)).groups()
    return label, rules.split(",")

def parse_ratings(line):
    line = line.replace(',', ',"')
    line = line.replace('{', '{"')
    line = line.replace('}', '}')
    line = line.replace("=", '":')
    return eval(line)

def _eval(wfs, wf, context):
    if wf == "A":
        return True
    if wf == "R":
        return False
    for rule in wfs[wf]:
        if ":" not in rule:
            return _eval(wfs, rule, context)
        cond, nxt = rule.split(":")
        cond_res = eval(cond, None, context)
        if cond_res and nxt in "AR":
            return nxt == "A"
        elif cond_res:
            return _eval(wfs, nxt, context)

def count_paths(path):
    lim = 4000
    mns = {"x": 1, "m": 1, "a": 1, "s": 1}
    mxs = {"x": lim, "m": lim, "a": lim, "s": lim}
    for p in path:
        if "<=" in p:
            l, r = p.split("<=")
            mxs[l] = min(mxs[l], int(r))
        elif ">=" in p:
            l, r = p.split(">=")
            mns[l] = max(mns[l], int(r))
        elif "<" in p:
            l, r = p.split("<")
            mxs[l] = min(mxs[l], int(r) - 1)
        elif ">" in p:
            l, r = p.split(">")
            mns[l] = max(mns[l], int(r) + 1)
    res = 1
    for k in mns:
        mn, mx = mns[k], mxs[k]
        res *= (mx - mn + 1)
    return res

def dfs(wfs, wf, path):
    if wf == "A":
        return count_paths(path)
    if wf == "R":
        return 0
    res = unwind = 0
    for rule in wfs[wf]:
        if ":" not in rule:
            res += dfs(wfs, rule, path)
            continue
        cond, nxt = rule.split(":")
        if ">" in cond:
            path.append(cond)
            res += dfs(wfs, nxt, path)
            path.pop()
            unwind += 1
            path.append(cond.replace(">", "<="))
        else:
            path.append(cond)
            res += dfs(wfs, nxt, path)
            path.pop()
            unwind += 1
            path.append(cond.replace("<", ">="))
    for _ in range(unwind):
        path.pop()
    return res

def part1(wfs, rts):
    res = 0
    for rt in rts:
        if _eval(wfs, "in", rt):
            res += rt["x"] + rt["m"] + rt["a"] + rt["s"]
    return res

def part2(wfs):
    return dfs(wfs, "in", [])

lines = "".join(line for line in fileinput.input(encoding = "utf-8"))
wfs, rts = lines.split("\n\n")

wfs = dict(parse_workflow(line) for line in wfs.splitlines())
rts = [parse_ratings(line) for line in rts.splitlines()]

print(part1(wfs, rts))
print(part2(wfs))
