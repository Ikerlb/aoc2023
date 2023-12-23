import fileinput
from collections import Counter

lines = [line[:-1] for line in fileinput.input(encoding = "utf-8")]

def parse(line):
    hand, bid = line.split(" ")
    return hand, int(bid)

def value_p1(hand_bid):
    order = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9":  9,
        "8":  8,
        "7":  7,
        "6":  6,
        "5":  5,
        "4":  4,
        "3":  3,
        "2":  2,
    }

    hand_s, bid = hand_bid
    hand = Counter(hand_s)
    hand_ord = tuple(map(lambda x: order[x], hand_s))
    mc = hand.most_common()
    if len(hand) == 1:
        # fiver
        return (6,) + hand_ord
    if len(hand) == 2 and mc[0][1] == 4:
        # poker
        return (5,) + hand_ord
    if len(hand) == 2:
        # full house
        return (4,) + hand_ord
    if len(hand) == 3 and mc[0][1] == 3:
        # triplet
        return (3,) + hand_ord
    if len(hand) == 3:
        # two pairs
        return (2,) + hand_ord
    if len(hand) == 4:
        return (1,) + hand_ord 
    return (0,) + hand_ord

def value_p2(hand_bid):
    order = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "9":  9,
        "8":  8,
        "7":  7,
        "6":  6,
        "5":  5,
        "4":  4,
        "3":  3,
        "2":  2,
        "J":  1,
    }
    
    hand_s, bid = hand_bid
    hand_ord = tuple(map(lambda x: order[x], hand_s))
    jokers = hand_s.count("J")

    if jokers == 5:
        # this is unbeatable
        # i though maybe this
        # was unbeatable
        # turns out nope
        return (6, ) + hand_ord

    hand = Counter(c for c in hand_s if c != "J")
    mc = [[c, f] for c, f in hand.most_common()]
    mc[0][1] += jokers

    if len(mc) == 1:
        # fiver
        return (6,) + hand_ord
    if len(mc) == 2 and mc[0][1] == 4:
        # poker
        return (5,) + hand_ord
    if len(mc) == 2:
        # full house
        return (4,) + hand_ord
    if len(mc) == 3 and mc[0][1] == 3:
        return (3,) + hand_ord
    if len(mc) == 3:
        # two pairs
        return (2,) + hand_ord
    if len(mc) == 4:
        # one pair
        return (1,) + hand_ord 
    # high card
    return (0,) + hand_ord

def part1(hands):
    hands.sort(key = value_p1)
    return sum(i * bid for i, (_, bid) in enumerate(hands, 1))
    
def part2(hands):
    hands.sort(key = value_p2)
    return sum(i * bid for i, (_, bid) in enumerate(hands, 1))


hands = [parse(line) for line in lines]

print(part1(hands[:]))
print(part2(hands[:]))

