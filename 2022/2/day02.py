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


class RoundResult(Enum):
    WIN = 6
    DRAW = 3
    LOSE = 0


class RoundSymbols(Enum):
    X = RoundResult.LOSE
    Y = RoundResult.DRAW
    Z = RoundResult.WIN


def score_round(round: Tuple[OpponentSymbols, PlayerSymbols]) -> int:
    if round[1].value == round[0].value:
        result = RoundResult.DRAW
    elif round[1].value == HandShape.Rock:
        if round[0].value == HandShape.Scissors:
            result = RoundResult.WIN
        else:
            result = RoundResult.LOSE
    elif round[1].value == HandShape.Paper:
        if round[0].value == HandShape.Rock:
            result = RoundResult.WIN
        else:
            result = RoundResult.LOSE
    elif round[1].value == HandShape.Scissors:
        if round[0].value == HandShape.Paper:
            result = RoundResult.WIN
        else:
            result = RoundResult.LOSE
    return result.value + round[1].value.value


def score_round_part2(round: Tuple[OpponentSymbols, RoundSymbols]) -> int:
    match round[1].value:
        case RoundResult.DRAW:
            player_shape = round[0].value
        case RoundResult.WIN:
            if round[0].value == HandShape.Rock:
                player_shape = HandShape.Paper
            if round[0].value == HandShape.Paper:
                player_shape = HandShape.Scissors
            if round[0].value == HandShape.Scissors:
                player_shape = HandShape.Rock
        case RoundResult.LOSE:
            if round[0].value == HandShape.Rock:
                player_shape = HandShape.Scissors
            if round[0].value == HandShape.Paper:
                player_shape = HandShape.Rock
            if round[0].value == HandShape.Scissors:
                player_shape = HandShape.Paper

    return round[1].value.value + player_shape.value


with open("input.txt") as f:
    lines = f.read()

rounds = [x for x in lines.split("\n") if x != ""]
rounds_list = [tuple(r.split(" ")) for r in rounds]
rounds_symbols = [(OpponentSymbols[x[0]], PlayerSymbols[x[1]]) for x in rounds_list]

answer_part1 = sum([score_round(x) for x in rounds_symbols])

rounds_symbols_part2 = [(OpponentSymbols[x[0]], RoundSymbols[x[1]]) for x in rounds_list]

answer_part2 = sum([score_round_part2(x) for x in rounds_symbols_part2])

print(f"Part 1: {answer_part1}")
print(f"Part 2: {answer_part2}")
