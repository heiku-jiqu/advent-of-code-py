from re import findall
from dataclasses import dataclass

with open("input.txt") as f:
    input = [s.rstrip("\n") for s in f.readlines()]

input_start_stacks = input[: input.index("") - 1]
input_move_list = input[input.index("") + 1 :]


def parse_input_stacks(input: list[str]) -> list[list[str]]:
    output = []
    for i, loc in enumerate(range(1, 35, 4)):
        temp = [s[loc] for s in input_start_stacks]
        temp.reverse()
        output.append([crate for crate in temp if crate != " "])
    return output


@dataclass
class Move:
    from_stack: int
    to_stack: int
    num_move: int


def parse_moves(input: list[str]) -> list:
    output = []
    for s in input:
        i_list = findall(r"\d+", s)
        i_list = [int(i) for i in i_list]
        output.append(
            Move(num_move=i_list[0], from_stack=i_list[1], to_stack=i_list[2])
        )
    return output


def do_move(stacks, move: Move):
    stacks[move.to_stack - 1].append(stacks[move.from_stack - 1].pop())
    if move.num_move == 1:
        return None
    else:
        new_move = move
        new_move.num_move = new_move.num_move - 1
        do_move(stacks, new_move)


start_stacks = parse_input_stacks(input_start_stacks)
parsed_moves = parse_moves(input_move_list)
for move in parsed_moves:
    do_move(start_stacks, move)
part1_answer = "".join([s[-1] for s in start_stacks])
print(f"Part 1: {part1_answer}")
