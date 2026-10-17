"""AVL-дерево множества: уникальные сравнимые ключи, поиск, вставка, удаление."""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class _Node:
    key: Any
    left: Optional['_Node'] = None
    right: Optional['_Node'] = None
    height: int = 1


def _height(node):
    return node.height if node is not None else 0


def _update(node):
    node.height = 1 + max(_height(node.left), _height(node.right))


def _rotate_right(node):
    root = node.left
    node.left = root.right
    root.right = node
    _update(node)
    _update(root)
    return root


def _rotate_left(node):
    root = node.right
    node.right = root.left
    root.left = node
    _update(node)
    _update(root)
    return root


def _balance(node):
    _update(node)
    factor = _height(node.left) - _height(node.right)
    if factor > 1:
        if _height(node.left.left) < _height(node.left.right):
            node.left = _rotate_left(node.left)
        return _rotate_right(node)
    if factor < -1:
        if _height(node.right.right) < _height(node.right.left):
            node.right = _rotate_right(node.right)
        return _rotate_left(node)
    return node


class AVLTree:
    def __init__(self, values=()):
        self._root = None
        self._size = 0
        for value in values:
            self.insert(value)

    def __len__(self):
        return self._size

    def __contains__(self, key):
        node = self._root
        while node is not None:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def __iter__(self):
        def inorder(node):
            if node is not None:
                yield from inorder(node.left)
                yield node.key
                yield from inorder(node.right)
        return inorder(self._root)

    def insert(self, key):
        """Вернуть True при вставке, False для уже существующего ключа."""
        def add(node):
            if node is None:
                return _Node(key), True
            if key == node.key:
                return node, False
            if key < node.key:
                node.left, inserted = add(node.left)
            else:
                node.right, inserted = add(node.right)
            return _balance(node), inserted

        self._root, inserted = add(self._root)
        self._size += int(inserted)
        return inserted

    def remove(self, key):
        """Удалить ключ; если ключа нет, вызвать KeyError."""
        def delete(node, target):
            if node is None:
                raise KeyError(target)
            if target < node.key:
                node.left = delete(node.left, target)
            elif target > node.key:
                node.right = delete(node.right, target)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key = successor.key
                node.right = delete(node.right, successor.key)
            return _balance(node)

        self._root = delete(self._root, key)
        self._size -= 1
