from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


BOOKING_PAGE = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Booking QA Demo</title></head>
<body>
  <main>
    <h1>Create booking</h1>
    <form id="booking-form">
      <label>Name <input id="name" name="name" required></label>
      <label>Nights <input id="nights" name="nights" type="number" min="1" max="28" required></label>
      <button type="submit">Create booking</button>
    </form>
    <p id="status" role="status" aria-live="polite"></p>
  </main>
  <script>
    document.querySelector('#booking-form').addEventListener('submit', async (event) => {
      event.preventDefault();
      const status = document.querySelector('#status');
      const payload = {
        name: document.querySelector('#name').value,
        nights: Number(document.querySelector('#nights').value)
      };
      const response = await fetch('/api/bookings', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const body = await response.json();
      status.textContent = response.ok
        ? `Booking ${body.id} created for ${body.name}` : body.error;
    });
  </script>
</body>
</html>"""


class BookingHandler(BaseHTTPRequestHandler):
    server_version = "BookingQADemo/1.0"

    def log_message(self, _format: str, *_args: Any) -> None:
        return

    def _json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(HTTPStatus.OK, {"status": "ok"})
        elif self.path == "/api/bookings/1":
            self._json(HTTPStatus.OK, {"id": 1, "name": "Demo Guest", "nights": 2, "status": "confirmed"})
        elif self.path == "/booking.html":
            body = BOOKING_PAGE.encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/api/bookings":
            self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        if self.headers.get_content_type() != "application/json":
            self._json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "JSON required"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
            return
        name, nights = payload.get("name"), payload.get("nights")
        if not isinstance(name, str) or not name.strip():
            self._json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "name is required"})
            return
        if not isinstance(nights, int) or isinstance(nights, bool) or not 1 <= nights <= 28:
            self._json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": "nights must be 1..28"})
            return
        self._json(HTTPStatus.CREATED, {"id": 101, "name": name.strip(), "nights": nights, "status": "confirmed"})


def make_server(host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), BookingHandler)
