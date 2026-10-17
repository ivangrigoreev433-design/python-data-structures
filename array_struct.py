"""Динамический массив с ручным управлением ёмкостью."""
import ctypes


class DynamicArray:
    def __init__(self, values=()):
        self._size = 0
        self._capacity = 1
        self._data = (ctypes.py_object * self._capacity)()
        for value in values:
            self.append(value)

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    def _index(self, index):
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("Индекс вне границ массива")
        return index

    def __getitem__(self, index):
        return self._data[self._index(index)]

    def __setitem__(self, index, value):
        self._data[self._index(index)] = value

    def __iter__(self):
        for index in range(self._size):
            yield self._data[index]

    def _grow(self):
        self._capacity *= 2
        data = (ctypes.py_object * self._capacity)()
        for index in range(self._size):
            data[index] = self._data[index]
        self._data = data

    def append(self, value):
        if self._size == self._capacity:
            self._grow()
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """Вставить перед индексом 0..len; отрицательные индексы запрещены."""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if not 0 <= index <= self._size:
            raise IndexError("Индекс вне границ массива")
        if self._size == self._capacity:
            self._grow()
        for position in range(self._size, index, -1):
            self._data[position] = self._data[position - 1]
        self._data[index] = value
        self._size += 1

    def pop(self, index=-1):
        index = self._index(index)
        value = self._data[index]
        for position in range(index, self._size - 1):
            self._data[position] = self._data[position + 1]
        self._size -= 1
        self._data[self._size] = None
        return value
