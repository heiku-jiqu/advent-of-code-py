from unittest import TestCase


def compare_packet(left: list, right: list) -> bool:
    for l, r in zip(left, right):
        match (l, r):
            case (int(l), int(r)):
                r = compare_integers(l, r)
                if r is None:
                    continue
                else:
                    return r
            case (list(l), list(r)):
                print('both lists')
                r = compare_packet(l, r)
                if r is None:
                    continue
                else:
                    return r
            case (list(l), int(r)):
                print('l list, r int')
                return compare_packet(l, [r])
            case (int(l), list(r)):
                print('l int', 'r list')
                return compare_packet([l], r)
            case _:
                print('unmatched')

def compare_integers(l: int, r: int) -> None | bool:
    if l == r:
        return None
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
