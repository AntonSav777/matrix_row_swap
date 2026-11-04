"""Интеграционные тесты REST API через настоящий HTTP."""

import json
import socket
import sys
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from api_server import MatrixHandler
from api_client import swap_rows_remote
import main


class ApiIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), MatrixHandler
        )
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True
        )
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, path, data=None, content_type="application/json"):
        headers = {"Content-Type": content_type}
        request = Request(
            self.url + path, data=data, headers=headers
        )
        try:
            response = urlopen(request, timeout=5)
        except HTTPError as error:
            response = error
        with response:
            return (
                response.code,
                json.loads(response.read().decode("utf-8")),
            )

    def test_health(self):
        status, body = self.request("/health")
        self.assertEqual(status, 200)
        self.assertEqual(body, {"status": "ok"})

    def test_successful_swap(self):
        result = swap_rows_remote(
            [[1, 2], [-5, 6], [9, 12]], self.url
        )
        self.assertEqual(result["matrix"], [
            [1, 2], [9, 12], [-5, 6]
        ])
        self.assertEqual(result["min_row"], 1)
        self.assertEqual(result["max_row"], 2)
        self.assertEqual(result["min_value"], -5)
        self.assertEqual(result["max_value"], 12)

    def test_invalid_json(self):
        status, body = self.request("/api/swap-rows", b"{broken")
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_missing_matrix(self):
        status, body = self.request("/api/swap-rows", b"{}")
        self.assertEqual(status, 400)
        self.assertIn("error", body)

    def test_invalid_matrix(self):
        for matrix in ([], [[1], [2, 3]], [["text"]], [[True]]):
            with self.subTest(matrix=matrix):
                data = json.dumps({"matrix": matrix}).encode("utf-8")
                status, body = self.request("/api/swap-rows", data)
                self.assertEqual(status, 422)
                self.assertIn("error", body)

    def test_wrong_content_type(self):
        status, _ = self.request(
            "/api/swap-rows", b'{"matrix":[[1]]}', "text/plain"
        )
        self.assertEqual(status, 415)

    def test_unknown_route(self):
        status, _ = self.request("/unknown")
        self.assertEqual(status, 404)

    def test_client_reports_server_error(self):
        with self.assertRaisesRegex(ValueError, "HTTP 422"):
            swap_rows_remote([], self.url)

    def test_unavailable_server(self):
        with socket.socket() as reserved:
            reserved.bind(("127.0.0.1", 0))
            url = f"http://127.0.0.1:{reserved.getsockname()[1]}"
            with self.assertRaisesRegex(ValueError, "Сервер недоступен"):
                swap_rows_remote([[1]], url)

    def test_complete_remote_program(self):
        from unittest.mock import patch

        with patch("builtins.input", side_effect=[
            "2", "2", "1 9", "-3 4"
        ]), patch("builtins.print") as output:
            code = main.main(["--remote", "--url", self.url])

        self.assertEqual(code, 0)
        output.assert_any_call("-3 4")
        output.assert_any_call("1 9")


if __name__ == "__main__":
    unittest.main(verbosity=2)
