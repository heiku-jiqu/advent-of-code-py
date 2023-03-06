from unittest import TestCase
from enum import StrEnum, auto
from typing import Tuple
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


if __name__ == "__main__":
    with open("input.txt") as f:
        input = [x.strip() for x in f.readlines()]
    print(input)
    print(input[0].split("="))

    # in this particular row
    # for each sensor:
    # s_b_manhat_dist =manhat_distance(sensor, beacon) 
    # s_row_dist = distance(sensor.x - row)
    # residual_dist = s_b_manhat_dist - s_row_dist
    # if residual_dist >= 0: 
    #     set NonBeacon for all tiles in (row, s.y +- residual_dist)


class TestParseInput(TestCase):
    def test_parse_input_line(self):
        input = (
            "Sensor at x=3482210, y=422224: closest beacon is at x=2273934, y=-202439"
        )
        output = (Sensor(3482210, 422224), Beacon(2273934, -202439))
        self.assertEqual(parse_input_line(input), output)

    def test_manhat_distance(self):
        self.assertEqual(manhat_distance(Sensor(2, 18), Beacon(-2, 15)), 4 + 3)
