import random
import unittest
from sorting import bubble_sort, quick_sort


class SortingTests(unittest.TestCase):
    def test_edge_cases_and_input_unchanged(self):
        cases = [[], [1], [1, 2, 3], [3, 2, 1], [2] * 20,
                 [0, -5, 2, -5, 9], [1.5, -2.3, 0.0], ['я', 'а', 'б', 'а']]
        for sort in (bubble_sort, quick_sort):
            for values in cases:
                with self.subTest(sort=sort.__name__, values=values):
                    original = values.copy()
                    result = sort(values)
                    self.assertEqual(result, sorted(values))
                    self.assertEqual(values, original)
                    self.assertIsNot(result, values)

    def test_generators(self):
        for sort in (bubble_sort, quick_sort):
            self.assertEqual(sort(x for x in (3, 1, 2)), [1, 2, 3])

    def test_random_against_sorted(self):
        rng = random.Random(123)
        for size in range(120):
            values = [rng.randrange(-30, 31) for _ in range(size)]
            for sort in (bubble_sort, quick_sort):
                with self.subTest(sort=sort.__name__, size=size):
                    self.assertEqual(sort(values), sorted(values))

    def test_quick_sort_large_inputs(self):
        for values in (list(range(10000)), list(range(10000, 0, -1)), [7] * 10000):
            self.assertEqual(quick_sort(values), sorted(values))

    def test_bubble_sort_stable(self):
        class Item:
            def __init__(self, key, label):
                self.key, self.label = key, label

            def __lt__(self, other):
                return self.key < other.key

        values = [Item(2, 'a'), Item(1, 'b'), Item(2, 'c'), Item(1, 'd')]
        self.assertEqual([x.label for x in bubble_sort(values)], ['b', 'd', 'a', 'c'])


if __name__ == '__main__':
    unittest.main()
