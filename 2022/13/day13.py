from unittest import TestCase
from itertools import zip_longest, compress

def compare_packet(left: list, right: list) -> bool:
    # zip_longest pads with None when iterable runs out of items
    for l, r in zip_longest(left, right):
        match (l, r):
            case (int(l), int(r)):
                r = compare_integers(l, r)
                if r is None:
                    continue
                else:
                    return r
            case (list(l), list(r)):
                r = compare_packet(l, r)
                if r is None:
                    continue
                else:
                    return r
            case (list(l), int(r)):
                return compare_packet(l, [r])
            case (int(l), list(r)):
                return compare_packet([l], r)
            case (None, _):
                return True
            case (_, None):
                return False
            case _:
                raise Exception('unmatched pattern!')

def compare_integers(l: int, r: int) -> None | bool:
    if l == r:
        return None
    if l > r:
        return False
    else:
        return True


if __name__ == "__main__":
    with open("input.txt") as f:
        input = f.read()
    packets_list = input.split('\n\n')

    part1_right_order = list()
    for pair in packets_list:
        (packet_left, packet_right) = [x for x in pair.split('\n') if x != '']
        left = eval(packet_left)
        right = eval(packet_right)
        ans = compare_packet(left, right)
        part1_right_order.append(ans)
    
    part1_answer = sum(
        compress(
            map(lambda x: x + 1, list(range(len(part1_right_order)))),
            part1_right_order
    ))

    print(f"Part 1: {part1_answer}")
    



class TestComparisons(TestCase):
    def test_pair1(self):
        left = [1, 1, 3, 1, 1]
        right = [1, 1, 5, 1, 1]
        self.assertTrue(compare_packet(left, right))
    
    def test_pair2(self):
        left = [[1],[2,3,4]] 
        right = [[1],4]
        self.assertTrue(compare_packet(left, right))
    
    def test_pair3(self):
        left = [9]
        right = [[8,7,6]]
        self.assertFalse(compare_packet(left, right))

    def test_pair4(self):
        left = [[4,4],4,4]
        right = [[4,4],4,4,4]
        self.assertTrue(compare_packet(left, right))

    def test_pair5(self):
        left = [7,7,7,7]
        right = [7,7,7] 
        self.assertFalse(compare_packet(left, right))

    def test_pair6(self):
        left = []
        right = [3]
        self.assertTrue(compare_packet(left, right))

    def test_pair7(self):
        left = [[[]]]
        right = [[]]
        self.assertFalse(compare_packet(left, right))

    def test_pair8(self):
        left = [1,[2,[3,[4,[5,6,7]]]],8,9]
        right = [1,[2,[3,[4,[5,6,0]]]],8,9]
        self.assertFalse(compare_packet(left, right))
