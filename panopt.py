#!/usr/bin/env python3
"""
UROPS PANOPT | Home
- Minimal, standard-library-only web server
- Placeholder API-feed endpoints (FEED 2..6) you can replace later
- Frontend polls feeds periodically and renders them into bordered panels

Run:
  python panopt.py
Then open:
  http://127.0.0.1:8080/
"""

from __future__ import annotations

### for web processing and serving HTML ###
import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

### for the main page w/ streams ###
from pages.home import HTML_PAGE

### (PORT) AND (HOSTNAME) ###
HOST = "127.0.0.1"
PORT = 8080

### returns time now ###
def iso_utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


### minimal POST handler ###
def do_POST(self):
    parsed = urlparse(self.path)
    path = parsed.path

    if path == "/api/action":
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            data = json.loads(raw.decode("utf-8") or "{}")

            action = data.get("action")
            payload = data.get("payload")

            # TODO: route actions here
            body = json.dumps({
                "ok": True,
                "received": {"action": action, "payload": payload},
            }, indent=2).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
        except Exception as e:
            body = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
            self._send(400, body, "application/json; charset=utf-8")
        return

    self._send(404, b"Not Found", "text/plain; charset=utf-8")


### builds a placeholder feeed window ###
def build_placeholder_feed(n: int) -> dict:
    # Replace this function with real API calls + categorization.
    # Keep the output shape stable so the frontend doesn't need rewriting.
    base_items = [
        f"Item {n}.1 (example)",
        f"Item {n}.2 (example)",
        f"Item {n}.3 (example)",
    ]
    return {
        "feed": n,
        "source": f"placeholder://feed-{n}",
        "updated_utc": iso_utc_now(),
        "categories": {
            "alerts": [base_items[0]],
            "events": [base_items[1]],
            "misc": [base_items[2]],
        },
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._send(200, HTML_PAGE.encode("utf-8"), "text/html; charset=utf-8")
            return

        if path.startswith("/api/feed/"):
            try:
                n_str = path.rsplit("/", 1)[-1]
                n = int(n_str)
                if n < 2 or n > 6:
                    raise ValueError("feed out of range")
                payload = build_placeholder_feed(n)
                body = json.dumps(payload, indent=2).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except Exception as e:
                body = json.dumps({"error": str(e)}).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")
            return

        self._send(404, b"Not Found", "text/plain; charset=utf-8")

    def log_message(self, fmt, *args):
        # quieter logs; comment out to restore default logging
        return


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serving on http://{HOST}:{PORT}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
