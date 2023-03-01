from dataclasses import dataclass
from unittest import TestCase


@dataclass
class Coord:
    x: int
    y: int

class Trace:
    tiles: list[Coord]

    def __init__(self, coord_joints: list[Coord]) -> None:
        tiles = list()
        for start, end in pairwise(coord_joints):
            match start.distance_to(end):
                case (int(diff_x), 0):
                    tiles.expand([Coord(start.x + i,start.y) for i in range(diff_x)])
                case _:
                    print('unmatched')

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
    
class TestClasses(TestCase):
    def ParseStringToCoordList(self):
        input = "498,4 -> 498,6 -> 496,6"
        output = [Coord(498,4), Coord(498,6), Coord(496,6)]
        self.assertEqual(parse_string_to_coord_list(input), output)
    def TestInitTrace(self):
        input = [Coord(498,4), Coord(498,6), Coord(496,6)]
        output = [Coord(498,4), Coord(498,5), Coord(498,6), Coord(497,6), Coord(496,6)]
        tile = Trace(input)
        self.assertEqual(
            tile.tiles,
            output
        )
