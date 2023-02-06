from dataclasses import dataclass, field


@dataclass
class Grid:
    """Class for keeping track of grid of trees"""

    grid: list[list[int]]
    row_len: int = field(init=False)
    col_len: int = field(init=False)
    visibility: list[list[bool]] = field(init=False)

    def __post_init__(self):
        self.row_len = len(self.grid[0])
        self.col_len = len(self.grid)
        self.visible_left = [self.visible_row(i) for i in range(self.row_len)]
        self.visible_right = [
            self.visible_row(i, view_from="right") for i in range(self.row_len)
        ]
        self.visible_top = [self.visible_col(j) for j in range(self.col_len)]
        self.visible_bottom = [
            self.visible_col(j, view_from="bottom") for j in range(self.col_len)
        ]
        self.visibility = list()
        for i in range(self.row_len):
            self.visibility.append([])
            for j in range(self.col_len):
                self.visibility[i].append(
                    self.visible_left[i][j]
                    or self.visible_right[i][j]
                    or self.visible_top[j][i]
                    or self.visible_bottom[j][i]
                )

    @classmethod
    def from_str_array(cls, input: list[str]):
        """
        Parse an array of string into Grid instance.
        
        >>> Grid.from_str_array(['123', '456'])

        """
        return cls(grid=[[int(c) for c in line] for line in input])

    def visible_row(self, row=0, view_from="left"):
        row = self.grid[row]
        visibility = []
        max_so_far = -1

        if view_from == "left":
            iterable = row
        elif view_from == "right":
            iterable = reversed(row)

        for tree in iterable:
            if tree > max_so_far:
                visibility.append(True)
                max_so_far = tree
            else:
                visibility.append(False)

        return visibility if view_from == "left" else [t for t in reversed(visibility)]

    def visible_col(self, col=0, view_from="top"):
        visibility = []
        max_so_far = -1

        if view_from == "top":
            iterable = range(self.col_len)
        elif view_from == "bottom":
            iterable = reversed(range(self.col_len))

        for i in iterable:
            tree = self.grid[i][col]
            if tree > max_so_far:
                visibility.append(True)
                max_so_far = tree
            else:
                visibility.append(False)

        return visibility if view_from == "top" else [t for t in reversed(visibility)]


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.readlines()
        input = [line.rstrip() for line in input]

    g = Grid.from_str_array(input)
    part1_ans = sum([sum(row) for row in g.visibility])
    print(f"Part 1: {part1_ans}")
