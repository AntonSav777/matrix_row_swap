"""Вывод результата обработки матрицы."""


def format_number(value):
    text = str(value)
    if text.endswith(".0"):
        return text[:-2]
    return text


def print_result(result):
    print("\nГотовая матрица:")
    for row in result["matrix"]:
        print(" ".join(format_number(value) for value in row))

    min_value = format_number(result["min_value"])
    max_value = format_number(result["max_value"])

    print(f"Минимум: {min_value}; исходная строка: {result['min_row'] + 1}")
    print(f"Максимум: {max_value}; исходная строка: {result['max_row'] + 1}")

    if result["min_row"] == result["max_row"]:
        print("Экстремумы находятся в одной строке. Матрица не изменилась.")
    else:
        print("Строки с минимумом и максимумом переставлены.")
