from unittest.mock import patch

from src.input_module import read_matrix


def test_reads_decimal_values():
    with patch("builtins.input", side_effect=["1", "2", "1.5 -2.5"]):
        matrix = read_matrix()

    assert matrix == [[1.5, -2.5]]


def test_retries_row_with_wrong_length(capsys):
    with patch("builtins.input", side_effect=["1", "2", "5", "5 6"]):
        matrix = read_matrix()

    assert matrix == [[5.0, 6.0]]
    assert "Нужно ввести ровно 2 чисел." in capsys.readouterr().out


def test_retries_row_with_nonfinite_value(capsys):
    with patch("builtins.input", side_effect=["1", "2", "inf 4", "3 4"]):
        matrix = read_matrix()

    assert matrix == [[3.0, 4.0]]
    assert "Все числа должны быть конечными." in capsys.readouterr().out
