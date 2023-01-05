from enum import Enum
from typing import Tuple


class HandShape(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3


class OpponentSymbols(Enum):
    A = HandShape.Rock
    B = HandShape.Paper
    C = HandShape.Scissors


class PlayerSymbols(Enum):
    X = HandShape.Rock
    Y = HandShape.Paper
    Z = HandShape.Scissors


def score_round(round: Tuple[OpponentSymbols, PlayerSymbols]):
    if round[1].value == round[0].value:
        result = 3
    elif round[1].value == HandShape.Rock:
        if round[0].value == HandShape.Scissors:
            result = 6
        else:
            result = 0
    elif round[1].value == HandShape.Paper:
        if round[0].value == HandShape.Rock:
            result = 6
        else:
            result = 0
    elif round[1].value == HandShape.Scissors:
        if round[0].value == HandShape.Paper:
            result = 6
        else:
            result = 0
    return result + round[1].value.value


with open("input.txt") as f:
    lines = f.read()

rounds = [x for x in lines.split("\n") if x != ""]
rounds_list = [tuple(r.split(" ")) for r in rounds]
rounds_symbols = [(OpponentSymbols[x[0]], PlayerSymbols[x[1]]) for x in rounds_list]

answer = sum([score_round(x) for x in rounds_symbols])

print(f"Part 1: {answer}")
