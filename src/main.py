"""Управляющий модуль: локальная обработка или REST API."""

import argparse
import sys

from input_module import read_matrix
from processing_module import swap_extreme_rows
from output_module import print_result
from api_client import swap_rows_remote


def main(argv=()):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--remote",
        action="store_true",
        help="Обрабатывать матрицу через REST API",
    )
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000",
        help="Адрес REST API",
    )
    args = parser.parse_args(argv)

    try:
        matrix = read_matrix()

        if args.remote:
            result = swap_rows_remote(matrix, args.url)
        else:
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
    raise SystemExit(main(sys.argv[1:]))
