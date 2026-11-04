"""Управляющий модуль программы."""

from input_module import read_matrix
from processing_module import swap_extreme_rows
from output_module import print_result


def main():
    try:
        matrix = read_matrix()
        result = swap_extreme_rows(matrix)
        print_result(result)
        return 0
    except ValueError as error:
        print(f"Ошибка обработки: {error}")
        return 1
    except (EOFError, KeyboardInterrupt):
        print("\nВвод прерван.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
