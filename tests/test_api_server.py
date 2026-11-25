from io import BytesIO
from unittest.mock import Mock

import pytest

from api_server import MatrixHandler


@pytest.mark.parametrize("path, status, key", [
    ("/health", 200, "status"),
    ("/unknown", 404, "error"),
])
def test_server_get_route(path, status, key):
    handler = Mock()
    handler.path = path

    MatrixHandler.do_GET(handler)

    code, body = handler.send_json.call_args.args
    assert code == status
    assert key in body


def test_server_returns_swapped_matrix():
    handler = Mock()
    handler.path = "/api/swap-rows"
    body = b'{"matrix": [[1], [2]]}'
    handler.headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
    }
    handler.rfile = BytesIO(body)

    MatrixHandler.do_POST(handler)

    code, result = handler.send_json.call_args.args
    assert code == 200
    assert result["matrix"] == [[2], [1]]
