from unittest.mock import patch

import main


def test_main_reports_processing_error(capsys):
    with patch("main.read_matrix", return_value=[[1]]), patch(
        "main.swap_extreme_rows", side_effect=ValueError("Некорректная матрица")
    ):
        code = main.main()

    assert code == 1
    assert "Ошибка обработки: Некорректная матрица" in capsys.readouterr().out


def test_main_passes_matrix_and_url_to_client():
    matrix = [[1], [2]]
    url = "http://127.0.0.1:8001"
    result = {"matrix": [[2], [1]]}

    with patch("main.read_matrix", return_value=matrix), patch(
        "main.swap_rows_remote", return_value=result
    ) as client, patch("main.print_result") as output:
        code = main.main(["--remote", "--url", url])

    assert code == 0
    client.assert_called_once_with(matrix, url)
    output.assert_called_once_with(result)
