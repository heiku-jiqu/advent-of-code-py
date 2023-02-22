from string import ascii_lowercase
from dataclasses import dataclass, field
from unittest import TestCase
from math import inf
from operator import attrgetter

@dataclass
class Node:
    position: tuple[int, int]
    letter: str
    height: int = field(init = False)
    neighbour_pos: dict[str, tuple[int, int]] = field(init = False)
    #neighbour_height: dict[str, int] = field(init = False)
    distance: int = field(init = False)
    elevation_dict: dict[str, int] = field(init=False, repr=False)

    def __post_init__(self):
        self.elevation_dict = {letter: i for i, letter in enumerate(ascii_lowercase)}
        self.set_height()
        self.set_neighbour_pos()
        
        self.distance = 999999

    def set_height(self):
        match self.letter:
            case 'S':
                self.height = 0
                self.distance = 0
            case 'E':
                self.height = len(self.elevation_dict) - 1
            case _ if self.letter in self.elevation_dict:
                self.height = self.elevation_dict[self.letter]
            case _:
                raise Exception("Unknown letter")

    def set_neighbour_pos(self):
        x, y = self.position
        self.neighbour_pos = {
            'r':(x + 1, y), 'l':(x - 1, y), 'u':(x, y + 1), 'd':(x, y - 1)
        }

def find_shortest_path(queue: dict[tuple, Node], start_pos: tuple, forward: bool = True) -> dict[tuple, tuple]:
    previous_node = dict()
    queue[start_pos].distance = 0

    while len(queue) > 0:
        min_dist_node_key = min(queue, key=lambda x: queue.get(x).distance)
        min_dist_node = queue.pop(min_dist_node_key )

        for key in min_dist_node.neighbour_pos.values():
            if key in queue:
                neighbor = queue[key]
                if forward:
                    constraint = neighbor.height <= min_dist_node.height + 1
                else:
                    constraint = neighbor.height + 1 >= min_dist_node.height 
                if constraint:
                    current_distance = min_dist_node.distance + 1
                    if current_distance < neighbor.distance:
                        neighbor.distance = current_distance
                        previous_node[key] = min_dist_node_key
    return previous_node

def calculate_length(path_nodes: dict[tuple, tuple], end_pos: tuple) -> int:
    trace_node = path_nodes[end_pos]
    length_of_path = 0
    while True:
        length_of_path += 1 
        try:
            trace_node = path_nodes[trace_node]
        except KeyError:
            break
    return length_of_path

if __name__ == "__main__":
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    queue = dict()
    start_pos: tuple
    end_pos: tuple
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char == 'S':
                start_pos = (row, col)
            if char == 'E':
                end_pos = (row, col)
            queue[(row, col)] = Node((row, col), char)

    part1_ans = calculate_length(find_shortest_path(queue, start_pos), end_pos)
    print(f"Part 1: {part1_ans}")

    # Part 2
    E_square_pos = end_pos
    a_square_pos_list = list()
    for row, line in enumerate(input):
        for col, char in enumerate(line):
            if char in ['S', 'a']:
                a_square_pos_list.append((row, col))
            queue[(row, col)] = Node((row, col), char)

    part2_paths = find_shortest_path(queue, E_square_pos, forward=False)
    part2_ans = inf
    
    for a_square in a_square_pos_list:
        try:
            length = calculate_length(part2_paths, a_square)
            # print(length, a_square)
            part2_ans = min(part2_ans, length)
        except:
            continue

    print(f"Part 2: {part2_ans}") 
    




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