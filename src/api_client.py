"""Передача матрицы серверу через HTTP и JSON."""

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def swap_rows_remote(matrix, base_url="http://127.0.0.1:8000"):
    try:
        body = json.dumps(
            {"matrix": matrix}, allow_nan=False
        ).encode("utf-8")
    except (ValueError, TypeError, OverflowError) as error:
        raise ValueError("Матрицу нельзя преобразовать в JSON.") from error

    request = Request(
        base_url.rstrip("/") + "/api/swap-rows",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        try:
            details = json.loads(error.read().decode("utf-8"))
            message = details.get("error", "Ошибка обработки запроса.")
        except (ValueError, AttributeError):
            message = "Некорректный ответ сервера."
        raise ValueError(f"HTTP {error.code}: {message}") from error
    except (URLError, TimeoutError, OSError) as error:
        raise ValueError(
            "Сервер недоступен. Проверьте адрес и запуск api_server.py."
        ) from error
    except ValueError as error:
        raise ValueError("Сервер вернул некорректный JSON.") from error

    required = {"matrix", "min_value", "max_value", "min_row", "max_row"}
    if not isinstance(result, dict) or not required.issubset(result):
        raise ValueError("В ответе сервера отсутствуют поля результата.")

    return result
