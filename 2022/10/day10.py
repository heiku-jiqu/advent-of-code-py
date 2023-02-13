import unittest


def addition(x: int, y: int) -> int:
    return x + y

class TestFunctions(unittest.TestCase):
    def test_positive_nums(self):
        self.assertEqual(addition(1, 2), 3)

    def test_negative_nums(self):
        self.assertEqual(addition(1, -2), -1)


if __name__ == "__main__":
    print("hello executable")

