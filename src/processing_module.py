"""Поиск экстремумов и перестановка строк матрицы."""

import math


def swap_extreme_rows(matrix):
    if not isinstance(matrix, list) or not matrix:
        raise ValueError("Матрица должна быть непустым списком строк.")

    if not isinstance(matrix[0], list) or not matrix[0]:
        raise ValueError("Строки матрицы не должны быть пустыми.")

    width = len(matrix[0])

    for row in matrix:
        if not isinstance(row, list) or len(row) != width:
            raise ValueError("Строки должны иметь одинаковую длину.")

        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError("Матрица должна содержать только числа.")
            try:
                finite = math.isfinite(value)
            except OverflowError:
                finite = False
            if not finite:
                raise ValueError("Все числа должны быть конечными.")

    min_row = max_row = 0
    min_value = max_value = matrix[0][0]

    for i, row in enumerate(matrix):
        for value in row:
            if value < min_value:
                min_value = value
                min_row = i
            if value > max_value:
                max_value = value
                max_row = i

    result = [row[:] for row in matrix]
    result[min_row], result[max_row] = result[max_row], result[min_row]

    return {
        "matrix": result,
        "min_value": min_value,
        "max_value": max_value,
        "min_row": min_row,
        "max_row": max_row,
    }
