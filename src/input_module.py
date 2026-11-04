"""Ввод и проверка вещественной матрицы."""

import math


def read_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Введите целое положительное число.")


def read_matrix():
    n = read_positive_int("Введите количество строк: ")
    m = read_positive_int("Введите количество столбцов: ")
    matrix = []

    for i in range(n):
        while True:
            try:
                row = list(map(float, input(
                    f"Введите строку {i + 1} ({m} чисел): "
                ).split()))

                if len(row) != m:
                    raise ValueError(f"Нужно ввести ровно {m} чисел.")

                if not all(math.isfinite(value) for value in row):
                    raise ValueError("Все числа должны быть конечными.")

                matrix.append(row)
                break
            except ValueError as error:
                print(f"Ошибка ввода: {error}")

    return matrix
