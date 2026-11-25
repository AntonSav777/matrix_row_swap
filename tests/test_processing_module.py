import pytest

from src.processing_module import swap_extreme_rows


def test_swaps_rows_with_extremes():
    matrix = [[3.5, 4.0], [-2.5, 1.0], [8.0, 2.0]]
    result = swap_extreme_rows(matrix)

    assert result["matrix"] == [[3.5, 4.0], [8.0, 2.0], [-2.5, 1.0]]
    assert result["min_row"] == 1
    assert result["max_row"] == 2


def test_keeps_rows_when_extremes_are_together():
    matrix = [[-2.5, 8.0], [3.5, 4.0]]
    result = swap_extreme_rows(matrix)

    assert result["matrix"] == [[-2.5, 8.0], [3.5, 4.0]]
    assert result["min_row"] == result["max_row"] == 0


def test_rejects_number_outside_float_range():
    with pytest.raises(ValueError, match="Все числа должны быть конечными"):
        swap_extreme_rows([[10**400]])


@pytest.mark.parametrize("matrix", [None, 5, []], ids=["none", "number", "empty"])
def test_rejects_invalid_matrix_container(matrix):
    with pytest.raises(ValueError, match="Матрица должна быть непустым списком"):
        swap_extreme_rows(matrix)
