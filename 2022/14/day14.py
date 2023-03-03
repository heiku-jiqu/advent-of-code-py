from dataclasses import dataclass
from unittest import TestCase
from itertools import pairwise, chain
from typing import Self, NamedTuple
from enum import StrEnum, auto


class Coord(NamedTuple):
    x: int
    y: int

    def distance_to(self, other: Self) -> tuple[int,int]:
        return (other.x - self.x, other.y - self.y)
        
class Trace:
    tiles: list[Coord]

    def __init__(self, coord_joints: list[Coord]) -> None:
        self.tiles = list()
        for start, end in pairwise(coord_joints):
            match start.distance_to(end):
                case (int(diff_x), 0):
                    sign = int(diff_x / abs(diff_x))
                    self.tiles.extend(Coord(start.x + i, start.y) for i in range(0, diff_x, sign)) 
                case (0, int(diff_y)):
                    sign = int(diff_y / abs(diff_y))
                    self.tiles.extend(Coord(start.x, start.y + i) for i in range(0, diff_y, sign))
                case _:
                    raise Exception('Unexpected diagonal scan')
        self.tiles.append(coord_joints[-1])
    
class TileType(StrEnum):
    SAND = auto()
    AIR = auto()
    ROCK = auto()

class Grid(dict[Coord, TileType]):
    def __missing__(self, key):
        if key not in self:
            self[key] = TileType.AIR

    def produce_one_sand(self):
        self[Coord(500,0)] = TileType.SAND

# parse rocks path into full coords
# Grid class with accessor of tile?
# Find bounding box of all rocks
# 

# sand_in_bounding_box = True
# while sand_in_bounding_box:
#   produce_one_sand
#   while sand_not_at_rest:
#       try move_sand
#           down or left or right
#       else all_possible_paths_blocked
#           set_sand_at_rest
#   sand_in_bounding_box = grid_check_sand_in_bounding_box
# 
# grid_calculate_number_of_sand_at_rest

if __name__ == "__main__":
    with open('input.txt') as f:
        input = [x.strip() for x in f.readlines()]
    print(input)
    
def parse_string_to_coord_list(s: str) -> list[Coord]:
    list_of_coords_string = s.split(' -> ')
    out = list()
    for coord_str in list_of_coords_string:
        x, y = coord_str.split(',')
        out.append(Coord(int(x),int(y)))
    return out

class TestClasses(TestCase):
    def test_distance_to(self):
        start = Coord(1,2)
        end = Coord(2,4)
        self.assertEqual(
            start.distance_to(end),
            (1,2)
        )

    def test_parse_string_to_coord_list(self):
        input = "498,4 -> 498,6 -> 496,6"
        output = [Coord(498,4), Coord(498,6), Coord(496,6)]
        self.assertEqual(parse_string_to_coord_list(input), output)

    def test_init_trace(self):
        input = [Coord(498,4), Coord(498,6), Coord(496,6)]
        output = [Coord(498,4), Coord(498,5), Coord(498,6), Coord(497,6), Coord(496,6)]
        tile = Trace(input)
        self.assertEqual(
            tile.tiles,
            output
        )
    
    def test_init_grid(self):
        input = [Trace([Coord(498,4), Coord(498,6), Coord(496,6)]),
                 Trace([Coord(503,4), Coord(502,4), Coord(502,9), Coord(494,9)])]
        coords = [trace.tiles for trace in input]
        grid = Grid({coord:TileType.ROCK for coord in chain(*coords)})
        grid.produce_one_sand()
        self.assertEqual(
            grid[Coord(500,0)], TileType.SAND
        )
