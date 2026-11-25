import json
from unittest.mock import patch

import pytest

from api_client import swap_rows_remote


def test_client_sends_matrix_as_json():
    matrix = [[1], [2]]
    expected = {
        "matrix": [[2], [1]],
        "min_value": 1,
        "max_value": 2,
        "min_row": 0,
        "max_row": 1,
    }

    with patch("api_client.urlopen") as open_url:
        response = open_url.return_value.__enter__.return_value
        response.read.return_value = json.dumps(expected).encode("utf-8")
        result = swap_rows_remote(matrix, "http://127.0.0.1:8001/")

    request = open_url.call_args.args[0]
    assert request.full_url == "http://127.0.0.1:8001/api/swap-rows"
    assert request.get_method() == "POST"
    assert json.loads(request.data) == {"matrix": matrix}
    assert result == expected


def test_client_rejects_nonfinite_values():
    with patch("api_client.urlopen") as open_url:
        with pytest.raises(ValueError, match="нельзя преобразовать в JSON"):
            swap_rows_remote([[float("inf")]])

    open_url.assert_not_called()


def test_client_rejects_response_without_result_fields():
    with patch("api_client.urlopen") as open_url:
        response = open_url.return_value.__enter__.return_value
        response.read.return_value = b'{"matrix": [[1]]}'
        with pytest.raises(ValueError, match="отсутствуют поля результата"):
            swap_rows_remote([[1]])
