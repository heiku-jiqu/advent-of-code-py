from unittest import TestCase
from enum import StrEnum, auto
from typing import Tuple, List
from dataclasses import dataclass
import re


@dataclass
class Sensor:
    x: int
    y: int


@dataclass
class Beacon:
    x: int
    y: int


class TileType(StrEnum):
    Sensor = auto()
    Beacon = auto()
    NonBeacon = auto()
    Undiscovered = auto()


def parse_input_line(s: str) -> Tuple[Sensor, Beacon]:
    x_list = [int(x) for x in re.findall(r"x=(-?\d+)", s)]
    y_list = [int(x) for x in re.findall(r"y=(-?\d+)", s)]
    return (Sensor(x_list[0], y_list[0]), Beacon(x_list[1], y_list[1]))


def manhat_distance(a, b) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def find_non_beacon_in_row(pairs: List[Tuple[Sensor, Beacon]], row: int) -> int:
    row_tiles = dict()
    row_tiles.update({(s.x, s.y): TileType.Sensor for s, _ in pairs})
    row_tiles.update({(b.x, b.y): TileType.Sensor for _, b in pairs})
    for s, b in pairs:
        s_b_manhat_dist = manhat_distance(s, b)
        s_row_dist = abs(s.y - row)
        residual_dist = s_b_manhat_dist - s_row_dist
        if residual_dist >= 0:
            for i in range(-(residual_dist), residual_dist + 1):
                if row_tiles.get((s.x + i, row), None) not in [
                    TileType.Beacon,
                    TileType.Sensor,
                ]:
                    row_tiles.update({(s.x + i, row): TileType.NonBeacon})

    non_beacons = sorted(
        [k for k, v in row_tiles.items() if v == TileType.NonBeacon], key=lambda x: x[0]
    )
    return len(non_beacons)


if __name__ == "__main__":
    with open("input.txt") as f:
        input = [x.strip() for x in f.readlines()]

    parsed_input = [parse_input_line(l) for l in input]
    part1_answer = find_non_beacon_in_row(parsed_input, 2000000)
    print(f"Part 1: {part1_answer}")


class TestParseInput(TestCase):
    def test_parse_input_line(self):
        input = (
            "Sensor at x=3482210, y=422224: closest beacon is at x=2273934, y=-202439"
        )
        output = (Sensor(3482210, 422224), Beacon(2273934, -202439))
        self.assertEqual(parse_input_line(input), output)

    def test_manhat_distance(self):
        self.assertEqual(manhat_distance(Sensor(2, 18), Beacon(-2, 15)), 4 + 3)


class TestExample(TestCase):
    def test_parse_example_input(self):
        with open("example_input.txt") as f:
            input = [x.strip() for x in f.readlines()]
        parsed_input = [parse_input_line(l) for l in input]
        answer = find_non_beacon_in_row(parsed_input, 10)
        self.assertEqual(answer, 26)

