from dataclasses import dataclass
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

@dataclass
class RoundPart1:
    opponent: OpponentSymbols
    player: PlayerSymbols

@dataclass
class RoundPart2:
    opponent: OpponentSymbols
    result: RoundSymbols

def score_round(round: RoundPart1) -> int:
    if round.player.value == round.opponent.value:
        result = RoundResult.DRAW
    elif round.player.value == HandShape.Rock:
        if round.opponent.value == HandShape.Scissors:
            result = RoundResult.WIN
        else:
            result = RoundResult.LOSE
    elif round.player.value == HandShape.Paper:
        if round.opponent.value == HandShape.Rock:
            result = RoundResult.WIN
        else:
            result = RoundResult.LOSE
    elif round.player.value == HandShape.Scissors:
        if round.opponent.value == HandShape.Paper:
            result = RoundResult.WIN
        else:
            result = RoundResult.LOSE
    return result.value + round.player.value.value


def score_round_part2(round: RoundPart2) -> int:
    match round.result.value:
        case RoundResult.DRAW:
            player_shape = round.opponent.value
        case RoundResult.WIN:
            if round.opponent.value == HandShape.Rock:
                player_shape = HandShape.Paper
            if round.opponent.value == HandShape.Paper:
                player_shape = HandShape.Scissors
            if round.opponent.value == HandShape.Scissors:
                player_shape = HandShape.Rock
        case RoundResult.LOSE:
            if round.opponent.value == HandShape.Rock:
                player_shape = HandShape.Scissors
            if round.opponent.value == HandShape.Paper:
                player_shape = HandShape.Rock
            if round.opponent.value == HandShape.Scissors:
                player_shape = HandShape.Paper

    return round.result.value.value + player_shape.value


with open("input.txt") as f:
    lines = f.read()

rounds = [x for x in lines.split("\n") if x != ""]
rounds_list = [tuple(r.split(" ")) for r in rounds]

rounds_symbols_part1 = [RoundPart1(OpponentSymbols[x[0]], PlayerSymbols[x[1]]) for x in rounds_list]
answer_part1 = sum([score_round(x) for x in rounds_symbols_part1])
print(f"Part 1: {answer_part1}")

rounds_symbols_part2 = [RoundPart2(OpponentSymbols[x[0]], RoundSymbols[x[1]]) for x in rounds_list]
answer_part2 = sum([score_round_part2(x) for x in rounds_symbols_part2])
print(f"Part 2: {answer_part2}")
