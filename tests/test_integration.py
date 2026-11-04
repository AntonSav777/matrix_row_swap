"""Интеграционные проверки с настоящим модулем обработки."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main
from processing_module import swap_extreme_rows


class IntegrationTest(unittest.TestCase):
    def run_program(self, answers):
        with patch("builtins.input", side_effect=answers), patch(
            "builtins.print"
        ) as output:
            code = main.main()
        return code, output

    def test_real_modules(self):
        code, output = self.run_program([
            "3", "4",
            "1 2 3 4",
            "-5 6 7 8",
            "9 10 11 12",
        ])
        self.assertEqual(code, 0)
        rows = [
            call.args[0] for call in output.call_args_list
            if call.args
        ]
        self.assertEqual(rows[1:4], [
            "1 2 3 4",
            "9 10 11 12",
            "-5 6 7 8",
        ])

    def test_invalid_input_then_correction(self):
        code, output = self.run_program([
            "0", "abc", "2",
            "-1", "2",
            "a b", "1", "nan 2", "1 9",
            "-3 4",
        ])
        self.assertEqual(code, 0)
        output.assert_any_call("-3 4")
        output.assert_any_call("1 9")

    def test_single_element(self):
        result = swap_extreme_rows([[7.0]])
        self.assertEqual(result["matrix"], [[7.0]])
        self.assertEqual(result["min_row"], 0)
        self.assertEqual(result["max_row"], 0)

    def test_extremes_in_same_row(self):
        result = swap_extreme_rows([[-5, 9], [2, 3]])
        self.assertEqual(result["matrix"], [[-5, 9], [2, 3]])

    def test_first_occurrence_and_original_unchanged(self):
        matrix = [[9, 2], [-5, 9], [-5, 3]]
        result = swap_extreme_rows(matrix)
        self.assertEqual(result["min_row"], 1)
        self.assertEqual(result["max_row"], 0)
        self.assertEqual(result["matrix"], [
            [-5, 9], [9, 2], [-5, 3]
        ])
        self.assertEqual(matrix, [[9, 2], [-5, 9], [-5, 3]])

    def test_invalid_matrix(self):
        for matrix in (
            [], [[]], [[1], [2, 3]],
            [["text"]], [[True]], [[float("inf")]],
        ):
            with self.subTest(matrix=matrix):
                with self.assertRaises(ValueError):
                    swap_extreme_rows(matrix)

    def test_interrupted_input(self):
        with patch("builtins.input", side_effect=EOFError), patch(
            "builtins.print"
        ):
            self.assertEqual(main.main(), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
