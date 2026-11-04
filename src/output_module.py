"""Вывод результата обработки матрицы."""


def print_result(result):
    print("\nГотовая матрица:")
    for row in result["matrix"]:
        print(" ".join(f"{value:g}" for value in row))

    print(
        f"Минимум: {result['min_value']:g}; "
        f"исходная строка: {result['min_row'] + 1}"
    )
    print(
        f"Максимум: {result['max_value']:g}; "
        f"исходная строка: {result['max_row'] + 1}"
    )

    if result["min_row"] == result["max_row"]:
        print("Экстремумы находятся в одной строке. Матрица не изменилась.")
    else:
        print("Строки с минимумом и максимумом переставлены.")
