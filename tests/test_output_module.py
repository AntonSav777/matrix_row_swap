from src.output_module import print_result


def test_prints_distinct_decimal_values(capsys):
    result = {
        "matrix": [[1.0000002], [1.0000001]],
        "min_value": 1.0000001,
        "max_value": 1.0000002,
        "min_row": 0,
        "max_row": 1,
    }

    print_result(result)
    lines = capsys.readouterr().out.strip().splitlines()

    assert lines[1:3] == ["1.0000002", "1.0000001"]
    assert "Минимум: 1.0000001; исходная строка: 1" in lines
    assert "Максимум: 1.0000002; исходная строка: 2" in lines
    assert "Строки с минимумом и максимумом переставлены." in lines


def test_prints_message_when_matrix_did_not_change(capsys):
    result = {
        "matrix": [[1.0, 2.0]],
        "min_value": 1.0,
        "max_value": 2.0,
        "min_row": 0,
        "max_row": 0,
    }

    print_result(result)
    output = capsys.readouterr().out

    assert "\n1 2\n" in output
    assert "Матрица не изменилась." in output
