"""REST API для перестановки строк матрицы."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from processing_module import swap_extreme_rows

MAX_BODY_SIZE = 1_000_000


class MatrixHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(
            payload, ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {"status": "ok"})
        else:
            self.send_json(404, {"error": "Маршрут не найден."})

    def do_POST(self):
        if self.path != "/api/swap-rows":
            self.send_json(404, {"error": "Маршрут не найден."})
            return

        content_type = self.headers.get(
            "Content-Type", ""
        ).split(";")[0].strip().lower()

        if content_type != "application/json":
            self.send_json(415, {"error": "Требуется application/json."})
            return

        if self.headers.get("Transfer-Encoding"):
            self.send_json(400, {"error": "Требуется Content-Length."})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Неверный Content-Length."})
            return

        if length <= 0:
            self.send_json(400, {"error": "Тело запроса пустое."})
            return

        if length > MAX_BODY_SIZE:
            self.send_json(413, {"error": "Запрос слишком большой."})
            return

        self.connection.settimeout(5)

        try:
            body = self.rfile.read(length)
        except (TimeoutError, OSError):
            self.send_json(408, {"error": "Время чтения запроса истекло."})
            return

        if len(body) != length:
            self.send_json(400, {"error": "Тело запроса передано не полностью."})
            return

        try:
            payload = json.loads(body.decode("utf-8"))
        except (ValueError, RecursionError):
            self.send_json(400, {"error": "Некорректный JSON или UTF-8."})
            return

        if not isinstance(payload, dict) or "matrix" not in payload:
            self.send_json(400, {"error": "Требуется объект с полем matrix."})
            return

        try:
            result = swap_extreme_rows(payload["matrix"])
        except ValueError as error:
            self.send_json(422, {"error": str(error)})
            return

        self.send_json(200, result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    with ThreadingHTTPServer(
        ("127.0.0.1", args.port), MatrixHandler
    ) as server:
        print(
            f"REST API: http://127.0.0.1:{server.server_port}",
            flush=True,
        )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен.")


if __name__ == "__main__":
    main()
