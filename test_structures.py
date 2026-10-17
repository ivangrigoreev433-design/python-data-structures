"""Проверки интерфейсов, граничных случаев и структурных инвариантов."""
import random
import unittest
from collections import deque

from array_struct import DynamicArray
from linked_list import LinkedList
from deque_struct import Deque
from avl_tree import AVLTree


class DynamicArrayTests(unittest.TestCase):
    def test_growth_and_indexing(self):
        array = DynamicArray(range(100))
        self.assertEqual(list(array), list(range(100)))
        self.assertGreaterEqual(array.capacity, len(array))
        self.assertEqual(array[-1], 99)
        array[-1] = 500
        self.assertEqual(array[99], 500)

    def test_insert_and_pop(self):
        array = DynamicArray([2])
        array.insert(0, 1)
        array.insert(2, 4)
        array.insert(2, 3)
        self.assertEqual(list(array), [1, 2, 3, 4])
        self.assertEqual(array.pop(1), 2)
        self.assertEqual(array.pop(), 4)
        self.assertEqual(list(array), [1, 3])

    def test_invalid_indices(self):
        array = DynamicArray()
        with self.assertRaises(IndexError):
            array.pop()
        array.append(None)
        self.assertIsNone(array[0])
        for index in (-2, 1):
            with self.subTest(index=index), self.assertRaises(IndexError):
                _ = array[index]
            with self.subTest(index=index), self.assertRaises(IndexError):
                array[index] = 0
        for index in (-1, 2):
            with self.assertRaises(IndexError):
                array.insert(index, 0)
        with self.assertRaises(TypeError):
            _ = array['0']
        with self.assertRaises(TypeError):
            array.insert(0.5, 1)

    def test_random_operations_against_list(self):
        rng = random.Random(42)
        array, reference = DynamicArray(), []
        for _ in range(1000):
            action = rng.choice(['append', 'insert', 'pop', 'set'])
            value = rng.randrange(-100, 100)
            if action == 'append':
                array.append(value)
                reference.append(value)
            elif action == 'insert':
                index = rng.randrange(len(reference) + 1)
                array.insert(index, value)
                reference.insert(index, value)
            elif reference:
                index = rng.randrange(-len(reference), len(reference))
                if action == 'pop':
                    self.assertEqual(array.pop(index), reference.pop(index))
                else:
                    array[index] = reference[index] = value
            self.assertEqual(list(array), reference)
            self.assertEqual(len(array), len(reference))


class LinkedListTests(unittest.TestCase):
    def test_operations_and_duplicates(self):
        linked = LinkedList([2, 3, 2])
        linked.prepend(1)
        linked.append(4)
        linked.remove(2)
        self.assertEqual(list(linked), [1, 3, 2, 4])
        self.assertIn(2, linked)
        self.assertNotIn(99, linked)
        self.assertEqual(linked.pop_front(), 1)
        linked.remove(4)
        linked.append(5)
        self.assertEqual(list(linked), [3, 2, 5])
        self.assertEqual(len(linked), 3)

    def test_empty_and_singleton(self):
        linked = LinkedList()
        with self.assertRaises(IndexError):
            linked.pop_front()
        with self.assertRaises(ValueError):
            linked.remove(1)
        linked.prepend(None)
        linked.remove(None)
        self.assertEqual(len(linked), 0)
        linked.append(3)
        self.assertEqual(linked.pop_front(), 3)
        linked.append(4)
        self.assertEqual(list(linked), [4])
        with self.assertRaises(ValueError):
            linked.remove(7)
        self.assertEqual(list(linked), [4])

    def test_random_operations_against_list(self):
        rng = random.Random(23)
        linked, reference = LinkedList(), []
        for _ in range(700):
            action = rng.randrange(4)
            value = rng.randrange(20)
            if action == 0:
                linked.append(value)
                reference.append(value)
            elif action == 1:
                linked.prepend(value)
                reference.insert(0, value)
            elif action == 2 and reference:
                self.assertEqual(linked.pop_front(), reference.pop(0))
            elif value in reference:
                linked.remove(value)
                reference.remove(value)
            else:
                with self.assertRaises(ValueError):
                    linked.remove(value)
            self.assertEqual(list(linked), reference)
            self.assertEqual(len(linked), len(reference))
            if reference:
                self.assertEqual(linked._tail.value, reference[-1])
                self.assertIsNone(linked._tail.next)
            else:
                self.assertIsNone(linked._head)
                self.assertIsNone(linked._tail)


class DequeTests(unittest.TestCase):
    def test_both_ends(self):
        queue = Deque([2, 3])
        queue.appendleft(1)
        queue.append(4)
        self.assertEqual(queue.peekleft(), 1)
        self.assertEqual(queue.peekright(), 4)
        self.assertEqual(queue.popleft(), 1)
        self.assertEqual(queue.pop(), 4)
        self.assertEqual(list(queue), [2, 3])
        self.assertEqual(len(queue), 2)

    def test_empty_and_reuse(self):
        queue = Deque()
        for method in (queue.pop, queue.popleft, queue.peekleft, queue.peekright):
            with self.assertRaises(IndexError):
                method()
        for add in (queue.append, queue.appendleft):
            for remove in (queue.pop, queue.popleft):
                add(None)
                self.assertIsNone(remove())
                self.assertEqual(len(queue), 0)
                self.assertIsNone(queue._head)
                self.assertIsNone(queue._tail)

    def test_random_operations_against_deque(self):
        rng = random.Random(31)
        queue, reference = Deque(), deque()
        for _ in range(1000):
            action = rng.choice(['append', 'appendleft', 'pop', 'popleft'])
            if action.startswith('append'):
                value = rng.randrange(100)
                getattr(queue, action)(value)
                getattr(reference, action)(value)
            elif reference:
                self.assertEqual(getattr(queue, action)(), getattr(reference, action)())
            self.assertEqual(list(queue), list(reference))
            self.assertEqual(len(queue), len(reference))
            previous, node = None, queue._head
            while node is not None:
                self.assertIs(node.prev, previous)
                previous, node = node, node.next
            self.assertIs(previous, queue._tail)


class AVLTreeTests(unittest.TestCase):
    def assert_valid(self, tree, expected):
        def check(node, lower=None, upper=None):
            if node is None:
                return 0
            if lower is not None:
                self.assertGreater(node.key, lower)
            if upper is not None:
                self.assertLess(node.key, upper)
            left = check(node.left, lower, node.key)
            right = check(node.right, node.key, upper)
            self.assertLessEqual(abs(left - right), 1)
            self.assertEqual(node.height, 1 + max(left, right))
            return node.height
        check(tree._root)
        self.assertEqual(list(tree), sorted(expected))
        self.assertEqual(len(tree), len(expected))

    def test_all_four_insert_rotations(self):
        for values in ([3, 2, 1], [1, 2, 3], [3, 1, 2], [1, 3, 2]):
            with self.subTest(values=values):
                tree = AVLTree(values)
                self.assertEqual(tree._root.key, 2)
                self.assert_valid(tree, set(values))

    def test_duplicates_search_and_missing(self):
        tree = AVLTree([2, 1, 3, 2])
        self.assertFalse(tree.insert(2))
        self.assertTrue(tree.insert(4))
        self.assertIn(4, tree)
        self.assertNotIn(9, tree)
        with self.assertRaises(KeyError):
            tree.remove(9)
        self.assert_valid(tree, {1, 2, 3, 4})

    def test_delete_leaf_one_child_two_children_and_root(self):
        for values, deleted in (([2, 1, 3], 1), ([2, 1], 2),
                                ([4, 2, 6, 5, 7], 4), ([1], 1)):
            with self.subTest(values=values, deleted=deleted):
                tree = AVLTree(values)
                tree.remove(deleted)
                self.assert_valid(tree, set(values) - {deleted})

    def test_empty_and_reuse(self):
        tree = AVLTree()
        self.assert_valid(tree, set())
        self.assertNotIn(1, tree)
        with self.assertRaises(KeyError):
            tree.remove(1)
        tree.insert(1)
        tree.remove(1)
        tree.insert(2)
        self.assert_valid(tree, {2})

    def test_sorted_insertions_and_full_deletion(self):
        tree, expected = AVLTree(), set()
        for value in range(200):
            tree.insert(value)
            expected.add(value)
            self.assert_valid(tree, expected)
        for value in range(200):
            tree.remove(value)
            expected.remove(value)
            self.assert_valid(tree, expected)

    def test_random_operations_against_set(self):
        rng = random.Random(91)
        tree, expected = AVLTree(), set()
        for _ in range(1200):
            value = rng.randrange(-100, 100)
            if rng.randrange(2):
                self.assertEqual(tree.insert(value), value not in expected)
                expected.add(value)
            elif value in expected:
                tree.remove(value)
                expected.remove(value)
            else:
                with self.assertRaises(KeyError):
                    tree.remove(value)
            self.assertEqual(value in tree, value in expected)
            self.assert_valid(tree, expected)


if __name__ == '__main__':
    unittest.main()
