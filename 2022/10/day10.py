import unittest
from dataclasses import dataclass
from typing import List


def parse_input(input: List[str]) -> List[int]:
    # stores the register value at START of the cycle
    cycle_states = [1]

    for i, line in enumerate(input):
        if line.startswith("noop"):
            # print(line)
            cycle_states.append(cycle_states[-1])
        elif line.startswith("addx"):
            command, val = line.split(" ")
            cycle_states.append(cycle_states[-1])
            cycle_states.append(cycle_states[-1] + int(val))
    return cycle_states


def get_special_registers(registers: List[int]) -> List[int]:
    special_registers = list(range(20, 221, 40))
    return [registers[i] for i in special_registers]


def sum_special_registers(registers: List[int]) -> int:
    special_registers = list(range(20, 221, 40))
    return sum([registers[i - 1] * i for i in special_registers])


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.readlines()
        input = [line.strip() for line in input]

    registers = parse_input(input)
    part1_answer = sum_special_registers(registers)
    print(f"Part 1: {part1_answer}")


class TestFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_noop(self):
        self.noop_input = ["noop"]
        self.assertEqual(
            parse_input(self.noop_input),
            [1, 1],
            "expect second cycle register is same as first cycle",
        )

    def test_parse_addx(self):
        self.addx_input = ["addx 2"]
        self.assertEqual(
            parse_input(self.addx_input),
            [1, 1, 3],
            "start of 3rd cycle (end of 2nd cycle) register added 2",
        )

    def test_sum_special_registers(self):
        registers = list(range(1, 221))
        self.assertEqual(
            sum_special_registers(registers),
            sum([x ** 2 for x in [20, 60, 100, 140, 180, 220]]),
        )

    def test_example_input(self):
        with open("example_input.txt") as f:
            input = f.readlines()
        input = [line.strip() for line in input]
        registers = parse_input(input)
        answer = sum_special_registers(registers)
        print(registers)
        print(get_special_registers(registers))
        self.assertEqual(13140, answer)

