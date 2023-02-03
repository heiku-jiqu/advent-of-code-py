from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class File:
    name: str
    size: int


class Directory:
    def __init__(self, name=None, parent_dir=None):
        self.name = name
        self.parent_dir = parent_dir
        self.child_dirs = list()
        self.files = list()
        self.size = 0

    def add_child_dir(self, child_dir: Directory):
        self.child_dirs.append(child_dir)

    def add_file(self, f: File):
        self.files.append(f)

    def get_filesize(self):
        return sum(s.size for s in self.files)

    def get_dirsize(self, fs):
        if len(self.child_dirs) == 0:
            return self.get_filesize()
        else:
            return self.get_filesize + sum(
                fs[child].get_dirsize(fs) for child in self.child_dirs
            )


def main():
    with open("input.txt") as f:
        input = f.read()
    input_split = input.split("$ ")
    commands = [[c for c in i.split("\n") if c] for i in input_split]
    print(commands)

    def dict_factory():
        return Directory()

    filesys = defaultdict(dict_factory)
    current_dir = None
    for c in commands:
        print(c)
        if len(c) == 0:
            continue
        if c[0].startswith("cd"):
            if c[0] == "cd ..":
                current_dir = filesys[current_dir.parent_dir]
                # print(current_dir.name)
            if c[0] == "cd /":
                current_dir = filesys["/"]
                current_dir.name = "/"
                # print(current_dir.name)
            else:
                name = c[0][3:]
                current_dir = filesys[name]
                current_dir.name = name
                # print(current_dir.name)
        if c[0].startswith("ls"):
            for item in c[1:]:
                if item.startswith("dir"):
                    current_dir.add_child_dir(item[4:])
                    # print(item[4:])
                else:
                    size, filename = item.split(" ")
                    size = int(size)
                    current_dir.add_file(File(name=filename, size=size))
                    # print(f"size: {size}, filename: {filename}")
    # dir = Directory("/")
    # dir.files = [File("abc", 100), File("def", 202)]
    # print(dir.get_filesize())
    part1_dirs = [k for k, v in filesys.items() if v.get_dirsize(filesys) <= 100000]
    print(part1_dirs)


if __name__ == "__main__":
    main()
