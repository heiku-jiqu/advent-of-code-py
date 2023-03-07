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


@dataclass
class Coord:
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

    non_beacons = [k for k, v in row_tiles.items() if v == TileType.NonBeacon]
    # sorted(
    # non_beacons, key=lambda x: x[0]
    # )
    return len(non_beacons)


def construct_perimeter(center: Tuple[int, int], radius: int) -> List[Tuple[int, int]]:
    """
    Returns list coordinates of perimeter around center with manhattan distance `radius`
    """
    out = []
    radius = abs(radius)
    for i in range(radius):
        out.append((-radius + i, i))
        out.append((i, radius - i))
        out.append((radius - i, -i))
        out.append((-i, -radius + i))
    return [(x + center[0], y + center[1]) for (x, y) in out]


def coord_in_sensor_range(
    pairs: List[Tuple[Sensor, Beacon]], coord: Tuple[int, int]
) -> bool:
    for s, b in pairs:
        if manhat_distance(s, b) >= manhat_distance(s, coord):
            return True
        else:
            continue
    return False


def find_distress_beacon(
    pairs: List[Tuple[Sensor, Beacon]], coord_limit: int = 4000000
) -> Tuple[int, int] | None:
    # Find list of search space tiles:
    # since there is only one single possible position,
    # just need to search the perimeter 1unit outside of all Sensor's range
    search_space: List[Tuple[int, int]] = []
    for s, b in pairs:
        s_b_manhat_dist = manhat_distance(s, b)
        perimeter = construct_perimeter((s.x, s.y), s_b_manhat_dist + 1)
        search_space.extend(perimeter)

    for coord in search_space:
        if (
            coord[0] > coord_limit
            or coord[1] > coord_limit
            or coord[0] < 0
            or coord[1] < 0
        ):
            continue
        elif coord_in_sensor_range(pairs, Coord(*coord)):
            continue
        else:
            return coord


if __name__ == "__main__":
    with open("input.txt") as f:
        input = [x.strip() for x in f.readlines()]

    parsed_input = [parse_input_line(l) for l in input]
    part1_answer = find_non_beacon_in_row(parsed_input, 2000000)
    print(f"Part 1: {part1_answer}")

    distress_beacon = find_distress_beacon(parsed_input)
    tuning_frequency = distress_beacon[0] * 4000000 + distress_beacon[1]
    print(f"Part 2: {tuning_frequency}")


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
        distress_beacon = find_distress_beacon(parsed_input, 20)
        self.assertEqual(distress_beacon, (14, 11))
        tuning_frequency = distress_beacon[0] * 4000000 + distress_beacon[1]
        self.assertEqual(tuning_frequency, 56000011)


class TestRadius(TestCase):
    def test_construct_perimeter(self):
        self.assertEqual(
            set(construct_perimeter((0, 0), 2)),
            set([(-2, 0), (-1, 1), (0, 2), (1, 1), (2, 0), (1, -1), (0, -2), (-1, -1)]),
        )

    def test_construct_perimeter_non_origin(self):
        self.assertEqual(
            set(construct_perimeter((1, 1), 1)), set([(0, 1), (1, 2), (2, 1), (1, 0)])
        )
