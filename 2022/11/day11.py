from dataclasses import dataclass
from typing import Callable, List, Self, Dict
from unittest import TestCase
from math import floor


class Monkey:
    def __init__(self) -> None:
        self.items: List[int]
        self.operation: Callable
        self.test: Callable[[int], int]
        self.num_inspect: int = 0
        self.divisor: int
        self.items_modulo: List[List[int]] = list()

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
        return self
    
    def parse_test(self, test_str: str, true_str: str, false_str: str) -> Self:
        divisor = int(test_str.split(' ')[-1])
        self.divisor = divisor
        true_monkey = int(true_str.split(' ')[-1])
        false_monkey = int(false_str.split(' ')[-1])
        self.test = lambda worry: true_monkey if worry % divisor == 0 else false_monkey
        return self

def parse_input(input: str) -> List[List[str]]:
    parsed = [chunk.split("\n") for chunk in input.split("\n\n")]
    return [[line.strip() for line in chunk if line.strip() != ""] for chunk in parsed]

def get_monkeys(parsed: List[List[str]]) -> Dict[int, Monkey]:
    output = dict()
    for config_list in parsed:
        iter_config = iter(config_list)
        monkey_num = int(next(iter_config).split(" ")[-1].replace(":", ""))
        output[monkey_num] = (Monkey()
            .parse_items(next(iter_config))
            .parse_operation(next(iter_config))
            .parse_test(
                next(iter_config),
                next(iter_config),
                next(iter_config)
            )
        )
    return output


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read()
    parsed_input = parse_input(input)

    # Part 1
    monkeys = get_monkeys(parsed_input)
    for _ in range(1):
        for mk in monkeys.values():
            num_items = len(mk.items)
            for i in range(num_items):
                mk.num_inspect += 1
                item = floor(mk.operation(mk.items.pop(0)) / 3)
                target_mk_num = mk.test(item)
                monkeys[target_mk_num].items.append(item)
    part1_num_inspects = sorted([x.num_inspect for x in monkeys.values()])
    part1_answer = part1_num_inspects[-1] * part1_num_inspects[-2]
    print(f"Part 1: {part1_answer}")

    # Part 2
    monkeys = get_monkeys(parsed_input)
    divisors = [x.divisor for x in monkeys.values()]
    for mk in monkeys.values():
        for item in mk.items:
            mk.items_modulo.append([item for d in divisors])
    for _ in range(10000):
        for mk in monkeys.values():
            num_items = len(mk.items_modulo)
            for i in range(num_items):
                mk.num_inspect += 1
                item_modulo = [floor(mk.operation(x) % d) for x, d in zip(mk.items_modulo.pop(0), divisors)]
                selected_item_modulo = divisors.index(mk.divisor)
                target_mk_num = mk.test(item_modulo[selected_item_modulo])
                monkeys[target_mk_num].items_modulo.append(item_modulo)
    part2_num_inspects = sorted([x.num_inspect for x in monkeys.values()])
    part2_answer = part2_num_inspects[-1] * part2_num_inspects[-2]
    print(f"Part 2: {part2_answer}")

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
        
    def test_parse_items_old(self):
        m = Monkey()
        op_string = "Operation: new = old * old"
        m.parse_operation(op_string)
        self.assertEqual(m.operation(2), 4)

    def test_parse_test(self):
        m = Monkey()
        test_str = "Test: divisible by 17"
        true_str = "    If true: throw to monkey 0"
        false_str = "    If false: throw to monkey 1"
        m.parse_test(test_str, true_str, false_str)
        # 17 divisible, so throw to monkey 0
        self.assertEqual(m.test(17), 0)
        # 18 not divisible, so throw to monkey 1
        self.assertEqual(m.test(18), 1)