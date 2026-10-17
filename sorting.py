"""Сортировки возвращают новый список и не меняют входные данные."""


def bubble_sort(values):
    result = list(values)
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if result[index + 1] < result[index]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break
    return result


def quick_sort(values):
    """Итеративная быстрая сортировка с трёхчастным разбиением.

    Равные опорному значения отделяются сразу; рекурсии нет, поэтому
    большие входы не упираются в ограничение глубины стека Python.
    """
    result = list(values)
    stack = [(0, len(result) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = result[(low + high) // 2]
        left, current, right = low, low, high
        while current <= right:
            if result[current] < pivot:
                result[left], result[current] = result[current], result[left]
                left += 1
                current += 1
            elif pivot < result[current]:
                result[current], result[right] = result[right], result[current]
                right -= 1
            else:
                current += 1
        # Большую часть кладём первой, чтобы меньшую обработать следующей.
        parts = [(low, left - 1), (right + 1, high)]
        if parts[0][1] - parts[0][0] < parts[1][1] - parts[1][0]:
            parts.reverse()
        stack.extend(part for part in parts if part[0] < part[1])
    return result
