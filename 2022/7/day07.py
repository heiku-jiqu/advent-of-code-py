from collections import defaultdict


def main():
    with open("input.txt") as f:
        input = f.read()
    input_split = input.split("$ ")
    commands = [[c for c in i.split("\n") if c] for i in input_split]

    filesys = defaultdict(int)
    current_dir = None

    for c in commands:
        if len(c) == 0:
            continue
        if c[0].startswith("cd"):
            if c[0] == "cd ..":
                current_dir = current_dir[: current_dir.rfind("/")]
            elif c[0] == "cd /":
                current_dir = "/"
            else:
                name = c[0][3:]
                current_dir = current_dir + "/" + name
        if c[0].startswith("ls"):
            for item in c[1:]:
                if item.startswith("dir"):
                    pass
                else:
                    size, filename = item.split(" ")
                    size = int(size)
                    update_dir = current_dir
                    for i in range(current_dir.count("/")):
                        filesys[update_dir] += size
                        update_dir = update_dir[: update_dir.rfind("/")]

    part1_dirs_size = [v for k, v in filesys.items() if v <= 100000]
    print(f"Part 1: {sum(part1_dirs_size)}")

    total_disk_space = 70000000
    disk_used = filesys["/"]
    space_needed = 30000000

    eligible_dirs = [
        v
        for k, v in filesys.items()
        if total_disk_space - (disk_used - v) > space_needed
    ]
    print(f"Part 2: {min(eligible_dirs)}")


if __name__ == "__main__":
    main()
