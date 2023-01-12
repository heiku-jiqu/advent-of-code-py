with open("input.txt") as f:
    input = [s.strip() for s in f.readlines()]


print(input[: input.index("")])
print("               \n\n")
print(input[input.index("") + 1 :])

