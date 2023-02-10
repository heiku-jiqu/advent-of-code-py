from dataclasses import dataclass
from typing import Tuple
from copy import deepcopy


@dataclass
class Position:
    x: int
    y: int

    def diff(self, other) -> Tuple[int, int]:
        return (self.x - other.x, self.y - other.y)


def move(
    direction: str, length: int, head: Position, tail: Position
) -> Tuple[Position, Position]:
    new_head = head
    new_tail = tail
    for i in range(length):
        new_head, new_tail = move_one_step(direction, new_head, new_tail)
    return (new_head, new_tail)


def move_one_step(
    direction: str, head: Position, tail: Position
) -> Tuple[Position, Position]:
    new_head = head
    new_tail = tail
    if direction == "R":
        new_head.x = head.x + 1
    if direction == "L":
        new_head.x = head.x - 1
    if direction == "U":
        new_head.y = head.y + 1
    if direction == "D":
        new_head.y = head.y - 1

    new_tail = update_tail(new_head, tail)
    return (new_head, new_tail)


def update_tail(new_head: Position, old_tail: Position) -> Position:
    x_diff, y_diff = new_head.diff(old_tail)
    # new head on top of old tail
    if (x_diff, y_diff) == (0, 0):
        return old_tail
    # new head 1 tile L/R/U/D of old tail
    elif (
        (x_diff, y_diff) == (1, 0)
        or (x_diff, y_diff) == (-1, 0)
        or (x_diff, y_diff) == (0, 1)
        or (x_diff, y_diff) == (0, -1)
        or (abs(x_diff), abs(y_diff)) == (1, 1)
    ):
        return old_tail
    # new head 2 tiles L/R/U/D of old tail
    elif (x_diff, y_diff) == (2, 0):
        old_tail.x = old_tail.x + 1
        return old_tail
    elif (x_diff, y_diff) == (-2, 0):
        old_tail.x = old_tail.x - 1
        return old_tail
    elif (x_diff, y_diff) == (0, 2):
        old_tail.y = old_tail.y + 1
        return old_tail
    elif (x_diff, y_diff) == (0, -2):
        old_tail.y = old_tail.y - 1
        return old_tail
    # new head 2 tiles L/R/U/D of old tail and 1 tile L/R/U/D of old tail
    elif x_diff == 2:
        old_tail.x = old_tail.x + 1
        old_tail.y = old_tail.y + y_diff
        return old_tail
    elif x_diff == -2:
        old_tail.x = old_tail.x - 1
        old_tail.y = old_tail.y + y_diff
        return old_tail
    elif y_diff == 2:
        old_tail.y = old_tail.y + 1
        old_tail.x = old_tail.x + x_diff
        return old_tail
    elif y_diff == -2:
        old_tail.y = old_tail.y - 1
        old_tail.x = old_tail.x + x_diff
        return old_tail


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.readlines()

    # head and tail start at same position
    h_pos = Position(0, 0)
    t_pos = Position(0, 0)
    visited = [(h_pos, t_pos)]
    num_moves = 0

    for i, line in enumerate(input):
        direction, length = line.split(" ")
        num_moves = num_moves + int(length)
        # print(f"direction: {direction}, length: {length}")
        for i in range(int(length)):
            h_pos, t_pos = move_one_step(direction, h_pos, t_pos)
            # print(f"{h_pos}, {t_pos}")
            visited.append(deepcopy((h_pos, t_pos)))

    tail_visited = set()
    for v in visited:
        tail_visited.add((v[1].x, v[1].y))
    print(f"Part 1: {len(tail_visited)}")
