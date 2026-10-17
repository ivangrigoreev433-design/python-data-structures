"""Односвязный список с указателями на начало и конец."""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class _Node:
    value: Any
    next: Optional['_Node'] = None


class LinkedList:
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

    def __contains__(self, value):
        return any(item == value for item in self)

    def append(self, value):
        node = _Node(value)
        if self._tail is None:
            self._head = node
        else:
            self._tail.next = node
        self._tail = node
        self._size += 1

    def prepend(self, value):
        self._head = _Node(value, self._head)
        if self._tail is None:
            self._tail = self._head
        self._size += 1

    def pop_front(self):
        if self._head is None:
            raise IndexError("Список пуст")
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        if self._head is None:
            self._tail = None
        return value

    def remove(self, value):
        """Удалить первое совпадение; при отсутствии вызвать ValueError."""
        previous = None
        current = self._head
        while current is not None:
            if current.value == value:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next
                if current is self._tail:
                    self._tail = previous
                self._size -= 1
                return
            previous, current = current, current.next
        raise ValueError("Значение не найдено")
