"""Проверка управляющего модуля с заглушкой обработки."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import main


class TopDownIntegrationTest(unittest.TestCase):
    def test_controller_with_processing_stub(self):
        matrix = [[1.0, 9.0], [-3.0, 4.0]]
        stub_result = {
            "matrix": [[-3.0, 4.0], [1.0, 9.0]],
            "min_value": -3.0,
            "max_value": 9.0,
            "min_row": 1,
            "max_row": 0,
        }

        with patch("builtins.input", side_effect=[
            "2", "2", "1 9", "-3 4"
        ]), patch(
            "main.swap_extreme_rows", return_value=stub_result
        ) as processing_stub, patch(
            "builtins.print"
        ) as output:
            exit_code = main.main()

        self.assertEqual(exit_code, 0)
        processing_stub.assert_called_once_with(matrix)
        output.assert_any_call("-3 4")
        output.assert_any_call("1 9")


if __name__ == "__main__":
    unittest.main(verbosity=2)
