# panopt.py

#!/usr/bin/env python3
"""
UROPS PANOPT | Home
- Minimal, standard-library-only web server
- FEED 1: CesiumJS + Google Photorealistic 3D Tiles (Map Tiles API key required)
- Reads GMP_MAP_TILES_API_KEY from .env if present (no external deps)

Run:
  python panopt.py
Then open:
  http://127.0.0.1:8080/
"""

from __future__ import annotations

import json
import os
import time

# for adbs exchange
import math
import urllib.error
import urllib.parse
import urllib.request

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from pages.home import HTML_PAGE

import math
import urllib.error
import urllib.parse
import urllib.request

HOST = "127.0.0.1"
PORT = 8080
ADSBX_API_URL = "https://adsbexchange.com/api/aircraft"

def iso_utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def load_dotenv(path: str = ".env", override: bool = False) -> bool:
    """
    Minimal .env loader (standard library only).
    - Supports KEY=VALUE lines
    - Ignores blank lines and comments (# ...)
    - Strips optional surrounding quotes
    Returns True if file was found and parsed.
    """
    if not os.path.exists(path):
        return False

    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue

            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()

            # Strip inline comments like: KEY=value # comment
            if " #" in v:
                v = v.split(" #", 1)[0].rstrip()

            # Remove surrounding quotes
            if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
                v = v[1:-1]

            if not k:
                continue
            if override or (k not in os.environ):
                os.environ[k] = v

    return True


def adsbx_credentials_present() -> bool:
    return bool(os.environ.get("ADSBX_API_AUTH", "").strip())


def fetch_adsbx_aircraft_near(lat: float, lon: float, dist_nm: int = 100) -> dict:
    api_auth = os.environ.get("ADSBX_API_AUTH", "").strip()
    if not api_auth:
        raise RuntimeError("ADSBexchange credentials are not configured.")

    dist_nm = max(1, min(int(dist_nm), 100))

    url = f"{ADSBX_API_URL}/lat/{lat}/lon/{lon}/dist/{dist_nm}/"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "api-auth": api_auth,
        },
        method="GET",
    )

    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def estimate_radius_nm_from_view(
    center_lat: float,
    center_lon: float,
    lamin: float | None,
    lomin: float | None,
    lamax: float | None,
    lomax: float | None,
) -> int:
    if None in (lamin, lomin, lamax, lomax):
        return 50

    # Conservative estimate from center to far corner, clamped to ADSBx 100 NM cap.
    dlat = max(abs(center_lat - lamin), abs(center_lat - lamax))
    dlon = max(abs(center_lon - lomin), abs(center_lon - lomax))

    lat_nm = dlat * 60.0
    lon_nm = dlon * 60.0 * max(math.cos(math.radians(center_lat)), 0.1)
    radius_nm = math.ceil(math.hypot(lat_nm, lon_nm))

    return max(5, min(radius_nm, 100))


def build_placeholder_feed(n: int) -> dict:
    base_items = [
        f"Item {n}.1 (example)",
        f"Item {n}.2 (example)",
        f"Item {n}.3 (example)",
    ]
    return {
        "feed": n,
        "source": f"placeholder://feed-{n}",
        "updated_utc": iso_utc_now(),
        "description": f"Placeholder feed {n} (server-generated).",
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

    def _html_with_keys(self) -> bytes:
        key = os.environ.get("GMP_MAP_TILES_API_KEY", "").strip()
        if not key:
            key = "REPLACE_ME_SET_ENV_GMP_MAP_TILES_API_KEY"
        return HTML_PAGE.replace("__GMP_MAP_TILES_API_KEY__", key).encode("utf-8")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("/", "/index.html"):
            self._send(200, self._html_with_keys(), "text/html; charset=utf-8")
            return
        
        if path == "/favicon.ico":
            try:
                with open("favicon.ico", "rb") as f:
                    body = f.read()
                self._send(200, body, "image/x-icon")
            except FileNotFoundError:
                self._send(404, b"Not Found", "text/plain; charset=utf-8")
            return

        if path.startswith("/api/feed/"):
            try:
                n_str = path.rsplit("/", 1)[-1]
                n = int(n_str)
                if n < 2 or n > 6:
                    raise ValueError("feed out of range (expected 2..6)")
                payload = build_placeholder_feed(n)
                body = json.dumps(payload, indent=2).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except Exception as e:
                body = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")
            return
        
        
        if path == "/api/adsbx/aircraft":
            try:
                qs = urllib.parse.parse_qs(parsed.query)

                def get_float(name: str) -> float | None:
                    raw = qs.get(name, [None])[0]
                    if raw in (None, ""):
                        return None
                    return float(raw)

                lat = get_float("lat")
                lon = get_float("lon")
                lamin = get_float("lamin")
                lomin = get_float("lomin")
                lamax = get_float("lamax")
                lomax = get_float("lomax")

                if lat is None or lon is None:
                    raise ValueError("lat and lon are required")

                dist_nm = estimate_radius_nm_from_view(lat, lon, lamin, lomin, lamax, lomax)
                payload = fetch_adsbx_aircraft_near(lat=lat, lon=lon, dist_nm=dist_nm)

                body = json.dumps(payload).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except urllib.error.HTTPError as e:
                try:
                    detail = e.read().decode("utf-8", errors="replace")
                except Exception:
                    detail = ""
                body = json.dumps({
                    "ok": False,
                    "error": f"ADSBexchange HTTP {e.code}",
                    "detail": detail,
                }).encode("utf-8")
                self._send(502, body, "application/json; charset=utf-8")
            except Exception as e:
                body = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")
            return

        self._send(404, b"Not Found", "text/plain; charset=utf-8")

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

                resp = {
                    "ok": True,
                    "updated_utc": iso_utc_now(),
                    "received": {"action": action, "payload": payload},
                }
                body = json.dumps(resp, indent=2).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except Exception as e:
                body = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")
            return

        self._send(404, b"Not Found", "text/plain; charset=utf-8")

    def log_message(self, fmt, *args):
        return


def main() -> None:
    # Load dotenv before starting server
    loaded = load_dotenv(".env", override=False)
    load_dotenv(".env.local", override=False)  # optional secondary file
    
    if not adsbx_credentials_present():
            print("NOTE: ADSBexchange credentials are not set. ADSBx overlay will be unavailable.")
    
    key = os.environ.get("GMP_MAP_TILES_API_KEY", "").strip()

    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Serving on http://{HOST}:{PORT}/")
    if not loaded:
        print("NOTE: .env not found in current directory.")
    if not key:
        print("NOTE: GMP_MAP_TILES_API_KEY is not set. FEED 1 will not load tiles.")
    server.serve_forever()


if __name__ == "__main__":
    main()