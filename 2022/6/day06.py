with open("input.txt") as f:
    s = f.read()


def find_marker_position(text: str, num_unique: int = 4):
    for i, c in enumerate(text):
        if len(set(text[i : i + num_unique])) == num_unique:
            return i + num_unique
    return None


print(f"Part 1: {find_marker_position(s)}")
print(f"Part 2: {find_marker_position(s, 14)}")
