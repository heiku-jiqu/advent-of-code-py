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

    def get_priority(self) -> int:
        for (i, char) in enumerate(ascii_letters):
            if char in self.find_common_item():
                return i + 1


with open("input.txt") as f:
    lines = f.readlines()

answer_part1 = sum([Rucksack(line.rstrip()).get_priority() for line in lines])

print(f"Part 1: {answer_part1}")
