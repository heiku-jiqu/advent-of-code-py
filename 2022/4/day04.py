from typing import Self


class Section:
    def __init__(self, s: str):
        nums = [int(x) for x in s.split("-")]
        (self.start, self.end) = nums

    def __repr__(self):
        return f"({self.start}, {self.end})"

    def contains(self, other: Self) -> bool:
        if self.start <= other.start and self.end >= other.end:
            return True
        else:
            return False


with open("input.txt") as f:
    input = [line.strip().split(",") for line in f.readlines()]

sections = [(Section(x), Section(y)) for (x, y) in input]
contains = [s for s in sections if s[0].contains(s[1]) or s[1].contains(s[0])]

print(f"Part 1: {len(contains)}")
