import fileinput

class Node:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"[{self.label} {self.focal_length}]"

    def remove(self):
        nxt, prv = self.next, self.prev
        prv.next = nxt
        nxt.prev = prv
        self.next = self.prev = None

class LinkedList:
    def __init__(self):
        self.head = Node("__head__", None)  # Dummy head
        self.tail = Node("__tail__", None)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def append(self, new_node):
        last_node = self.tail.prev

        last_node.next = new_node
        new_node.prev = last_node
        new_node.next = self.tail
        self.tail.prev = new_node

    def prepend(self, new_node):
        first_node = self.head.next

        first_node.prev = new_node
        new_node.next = first_node
        new_node.prev = self.head
        self.head.next = new_node

    def __repr__(self):
        return sep.join(map(str, self))

    def __iter__(self):
        current = self.head.next
        while current.next:
            yield current
            current = current.next

    def reverse_display(self, sep = "<->"):
        current = self.tail.prev
        res = []
        while current.prev:
            res.append(str(current))
            current = current.prev
        return sep.join(res)

class Box:
    def __init__(self, i):
        self.i = i
        self.list = LinkedList()
        self.d = {}

    def remove(self, label):
        if label in self.d:
            node = self.d[label]
            node.remove()
            del self.d[label]

    def put(self, label, focal_length):
        if label in self.d:
            node = self.d[label]
            node.focal_length = focal_length
        else:
            node = Node(label, focal_length)
            self.d[label] = node
            self.list.append(node)

    def __bool__(self):
        return bool(self.d)

    def __iter__(self):
        yield from self.list

    def __repr__(self):
        return f"Box {self.i}: {self.list}"

def _hash(s):
    res = 0
    for c in s:
        res += ord(c)
        res *= 17
        res = res % 256
    return res

sequence = "".join(line[:-1] for line in fileinput.input(encoding = "utf-8")).split(",")

# mutates boxes!
def hashmap(boxes, s):
    if "=" in s:
        label, fl = s.split("=")
        box = _hash(label)
        boxes[box].put(label, int(fl))
    else:
        label = s.replace("-", "")
        box = _hash(label)
        boxes[box].remove(label)

def format(boxes):
    res = []
    for box in boxes:
        if not box.d:
            continue
        res.append(f"{box}")
    return "\n".join(res)

def part1(sequence):
    return sum(_hash(s) for s in sequence)

def part2(sequence):
    boxes = [Box(i) for i in range(256)]
    for s in sequence:
        hashmap(boxes, s)
    res = 0
    for i, box in enumerate(boxes, 1):
        br = sum(i * node.focal_length for i, node in enumerate(box, 1))
        res += br * i
    return res
        

print(part1(sequence))
print(part2(sequence))
