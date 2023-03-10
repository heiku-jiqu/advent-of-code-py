filepath = "input.txt"
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()


def split_list(l: list[str], s: str) -> list:
    output = []
    sublist = []
    for item in l:
        if item == s:
            output.append(sublist)
            sublist = []
        else:
            sublist.append(item)
    return output


grouped_list = split_list([line.rstrip() for line in lines], "")
grouped_int_list = [[int(x) for x in l] for l in grouped_list]
sum_list = [sum(l) for l in grouped_int_list]
output_part1 = max(sum_list)
output_part2 = sum(sorted(sum_list)[-3:])

print(f"Part 1: {output_part1}")
print(f"Part 2: {output_part2}")

