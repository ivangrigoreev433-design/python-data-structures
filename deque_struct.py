"""Дек на двусвязных узлах: добавление и удаление с двух концов за O(1)."""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class _Node:
    value: Any
    prev: Optional['_Node'] = None
    next: Optional['_Node'] = None


class Deque:
    def __init__(self, values=()):
        self._head = None
        self._tail = None
        self._size = 0
        for value in values:
            self.append(value)

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def append(self, value):
        node = _Node(value, prev=self._tail)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def appendleft(self, value):
        node = _Node(value, next=self._head)
        if self._head is None:
            self._tail = node
        else:
            self._head.prev = node
        self._head = node
        self._size += 1

    def pop(self):
        if self._tail is None:
            raise IndexError("Дек пуст")
        value = self._tail.value
        self._tail = self._tail.prev
        self._size -= 1
        if self._tail is None:
            self._head = None
        else:
            self._tail.next = None
        return value

    def popleft(self):
        if self._head is None:
            raise IndexError("Дек пуст")
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        if self._head is None:
            self._tail = None
        else:
            self._head.prev = None
        return value

    def peekleft(self):
        if self._head is None:
            raise IndexError("Дек пуст")
        return self._head.value

    def peekright(self):
        if self._tail is None:
            raise IndexError("Дек пуст")
        return self._tail.value
