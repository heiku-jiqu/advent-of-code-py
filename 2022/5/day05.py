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


start_stacks = parse_input_stacks(input_start_stacks)
print(start_stacks)
