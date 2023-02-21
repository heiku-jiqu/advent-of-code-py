from string import ascii_lowercase
from dataclasses import dataclass, field
from unittest import TestCase
from math import inf

@dataclass
class Node:
    position: tuple[int, int]
    letter: str
    height: int = field(init = False)
    neighbour_pos: dict[str, tuple[int, int]] = field(init = False)
    neighbour_height: dict[str, int] = field(init = False)
    distance: int = field(init = False)
    elevation_dict: dict[str, int] = field(init=False)

    def __post_init__(self):
        self.set_height()
        self.set_neighbour_pos()
        self.set_neighbour_height()
        self.elevation_dict = {letter: i for i, letter in enumerate(ascii_lowercase)}
        self.distance = inf

    def set_height(self):
        match self.letter:
            case 'S':
                self.height = 0
                self.distance = 0
            case 'E':
                self.height = len(elevation_dict) - 1
            case _ if self.letter in elevation_dict:
                self.height = elevation_dict[self.letter]
            case _:
                raise Exception("Unknown letter")

    def set_neighbour_pos(self):
        x, y = self.position
        self.neighbour_pos = {
            'r':(x + 1, y), 'l':(x - 1, y), 'u':(x, y + 1), 'd':(x, y - 1)
        }

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    print(input)

    elevation_dict = {letter: i for i, letter in enumerate(ascii_lowercase)}

class TestNode(TestCase):
    def setUp(self) -> None:
        self.start_node = Node((0,0), 'S')
        self.end_node = Node((0,0), 'E')
        self.a_node = Node((0,0), 'a')

    def test_init(self):
        self.assertEqual(self.start_node.height, 0)
        self.assertEqual(self.end_node.height, 25)
        self.assertEqual(self.a_node.height, 0)
        self.assertEqual(self.a_node.neighbour_pos['l'], (-1, 0) )
        self.assertEqual(self.a_node.neighbour_pos['r'], (1, 0) )
        self.assertEqual(self.a_node.neighbour_pos['u'], (0, 1) )
        self.assertEqual(self.a_node.neighbour_pos['d'], (0, -1) )