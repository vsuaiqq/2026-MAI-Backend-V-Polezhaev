from __future__ import annotations

import json
import random
import string
import time
from typing import Iterable


ALLOWED_SPECIAL = "#[]().,!@&^%*"


def _generate_password() -> str:
    length = random.randint(8, 16)

    required = [
        random.choice(string.digits),
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(ALLOWED_SPECIAL),
    ]

    pool = string.ascii_letters + string.digits + ALLOWED_SPECIAL
    remaining = [random.choice(pool) for _ in range(length - len(required))]

    chars = required + remaining
    random.shuffle(chars)
    return "".join(chars)


def app(environ: dict, start_response) -> Iterable[bytes]:
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET").upper()

    if method != "GET":
        start_response("405 Method Not Allowed", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Method Not Allowed"]

    if path.rstrip("/") not in ("", "/", "/password"):
        start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
        return [b"Not Found"]

    password = _generate_password()
    payload = {"password": password, "len": len(password)}
    body = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")

    time.sleep(0.05)

    start_response(
        "200 OK",
        [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Cache-Control", "no-store"),
        ],
    )
    return [body]
