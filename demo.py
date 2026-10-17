"""Запуск: python demo.py."""
from array_struct import DynamicArray
from linked_list import LinkedList
from deque_struct import Deque
from avl_tree import AVLTree
from sorting import bubble_sort, quick_sort


def main():
    array = DynamicArray([3, 1, 2])
    array.append(4)
    print('Массив:', list(array))
    linked = LinkedList([2, 3])
    linked.prepend(1)
    print('Список:', list(linked))
    queue = Deque([2, 3])
    queue.appendleft(1)
    queue.append(4)
    print('Дек:', list(queue), '| снято справа:', queue.pop())
    tree = AVLTree([30, 10, 20, 40, 50])
    tree.remove(30)
    print('AVL-дерево:', list(tree), '| есть 20:', 20 in tree)
    values = [5, -2, 3, 3, 0]
    print('Пузырьковая сортировка:', bubble_sort(values))
    print('Быстрая сортировка:', quick_sort(values))


if __name__ == '__main__':
    main()
