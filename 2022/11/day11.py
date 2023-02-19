from dataclasses import dataclass
from typing import Callable, List, Self
from unittest import TestCase


class Monkey:
    def __init__(self) -> None:
        self.items: List[int]
        self.operation: Callable
        self.test: Callable[[], int]

    def parse_items(self, s: str) -> Self:
        split_string = s.replace("Starting items: ", "").split(", ")
        self.items = [int(x) for x in split_string]
        return self

    def parse_operation(self, s: str) -> Self:
        operator, number = s.replace("Operation: new = old ", "").split(" ")
        if number == 'old':
            match operator:
                case '+':
                    self.operation =  lambda x: x + x
                case '*':
                    self.operation = lambda x: x * x
                case _:
                    raise Exception('Unknown Operation')
        else:
            number = int(number)
            match operator:
                case '+':
                    self.operation =  lambda x: x + number
                case '*':
                    self.operation = lambda x: x * number
                case _:
                    raise Exception('Unknown Operation')


def parse_input(input: str) -> List[List[str]]:
    parsed = [chunk.split("\n") for chunk in input.split("\n\n")]
    return [[line.strip() for line in chunk if line.strip() != ""] for chunk in parsed]


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read()
    parsed_input = parse_input(input)
    print(parsed_input)
    print([len(x) for x in parsed_input])


class TestMonkey(TestCase):
    def test_parse_items(self):
        m = Monkey()
        item_string = "Starting items: 72, 64, 51, 57, 93, 97, 68"
        m.parse_items(item_string)
        self.assertEqual(m.items, [72, 64, 51, 57, 93, 97, 68])

    def test_parse_items_mult(self):
        m = Monkey()
        op_string = "Operation: new = old * 19"
        m.parse_operation(op_string)
        self.assertEqual(m.operation(2), 2 * 19)

    def test_parse_items_add(self):
        m = Monkey()
        op_string = "Operation: new = old + 19"
        m.parse_operation(op_string)
        self.assertEqual(m.operation(2), 2 + 19)
        
    def test_parse_items(self):
        m = Monkey()
        op_string = "Operation: new = old * old"
        m.parse_operation(op_string)
        self.assertEqual(m.operation(2), 4)
