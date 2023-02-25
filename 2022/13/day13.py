from unittest import TestCase


def compare_packet(left: list[int], right: list[int]) -> bool:
    for l, r in zip(left, right):
        match (l, r):
            case (int(l), int(r)):
                if l == r:
                    continue
                else:
                    return compare_integers(l, r)
            case (list(l), list(r)):
                print('both lists')
            case (list(l), int(r)):
                print('l list, r int')
            case (int(l), list(r)):
                print('l int', 'r list')
            case _:
                print('unmatched')

def compare_integers(l: int, r: int) -> bool:
    if l > r:
        return False
    else:
        return True


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.readlines()
    print(input)


class TestComparisons(TestCase):
    def test_all_integers(self):
        left = [1, 1, 3, 1, 1]
        right = [1, 1, 5, 1, 1]
        self.assertTrue(compare_packet(left, right))
    
    def test_all_lists(self):
        left = [[1],[2,3,4]] 
        right = [[1],4]
        self.assertTrue(compare_packet(left, right))
