from string import ascii_letters


class Rucksack:
    def __init__(self, s: str):
        self.string = s
        self.compartment1 = self.string[: int(len(self.string) / 2)]
        self.compartment2 = self.string[int(len(self.string) / 2) :]

    def __len__(self) -> int:
        return len(self.string)

    def find_common_item(self) -> set:
        return set(self.compartment1).intersection(self.compartment2)

    def find_group_badge(self, y, z) -> set:
        return set(self.string).intersection(y.string).intersection(z.string)


def get_priority(item) -> int:
    for (i, char) in enumerate(ascii_letters):
        if char in item:
            return i + 1


with open("input.txt") as f:
    lines = f.readlines()

answer_part1 = sum(
    [get_priority(Rucksack(line.rstrip()).find_common_item()) for line in lines]
)

print(f"Part 1: {answer_part1}")

rucksacks = [Rucksack(line.rstrip()) for line in lines]
answer_part2 = sum(
    [
        get_priority(x.find_group_badge(y, z))
        for (x, y, z) in zip(rucksacks[::3], rucksacks[1::3], rucksacks[2::3])
    ]
)

print(f"Part 2: {answer_part2}")
