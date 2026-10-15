"""Bridge web server (stdlib only). Run: python server.py [--port 7070]"""
import json
import os
import random
import string
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from table import Table

STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
FILES = {"/": ("index.html", "text/html; charset=utf-8"),
         "/help.js": ("help.js", "application/javascript; charset=utf-8"),
         "/app.js": ("app.js", "application/javascript; charset=utf-8"),
         "/style.css": ("style.css", "text/css; charset=utf-8")}
TABLES = {}
LOCK = threading.Lock()
MAX_TABLES = 50
IDLE_SECONDS = 6 * 3600


def new_code():
    while True:
        code = "".join(random.choice(string.ascii_uppercase) for _ in range(4))
        if code not in TABLES:
            return code


def cleanup():
    now = time.time()
    for code in [c for c, t in TABLES.items() if now - t.touched > IDLE_SECONDS]:
        del TABLES[code]


def get_table(code):
    t = TABLES.get((code or "").upper())
    if not t:
        raise ValueError("Table not found")
    t.touched = time.time()
    return t


def handle(path, q, body):
    with LOCK:
        cleanup()
        if path == "/api/state":
            t = get_table(q.get("table"))
            return t.view(q.get("token"))
        if path == "/api/create":
            if len(TABLES) >= MAX_TABLES:
                raise ValueError("Too many tables")
            t = Table(new_code())
            TABLES[t.code] = t
            token, seat = t.join(body.get("name"), 2)
            if body.get("solo"):
                t.start(solo=True)
            return dict(table=t.code, token=token, seat=seat)
        t = get_table(body.get("table"))
        token = body.get("token")
        if path == "/api/join":
            tok, seat = t.join(body.get("name"), body.get("seat"))
            return dict(table=t.code, token=tok, seat=seat)
        if path == "/api/start":
            if t.seat_of(token) != t.host:
                raise ValueError("Only the host can start")
            if not t.started:
                t.start()
        elif path == "/api/bid":
            t.bid(token, str(body.get("call")))
        elif path == "/api/play":
            t.play(token, str(body.get("card")))
        elif path == "/api/next":
            t.next_deal(token)
        else:
            raise KeyError(path)
        return t.view(token)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data, ctype="application/json"):
        raw = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _api(self, body):
        u = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(u.query).items()}
        try:
            self._send(200, handle(u.path, q, body))
        except KeyError:
            self._send(404, {"error": "Not found"})
        except ValueError as e:
            self._send(400, {"error": str(e)})

    def do_GET(self):
        path = urlparse(self.path).path
        if path in FILES:
            name, ctype = FILES[path]
            with open(os.path.join(STATIC, name), "rb") as f:
                return self._send(200, f.read(), ctype)
        if path == "/api/state":
            return self._api({})
        self._send(404, {"error": "Not found"})

    def do_POST(self):
        try:
            n = min(int(self.headers.get("Content-Length", 0)), 10000)
            body = json.loads(self.rfile.read(n) or b"{}")
            if not isinstance(body, dict):
                raise ValueError
        except ValueError:
            return self._send(400, {"error": "Bad request"})
        self._api(body)

    def log_message(self, *a):
        pass


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=int(os.environ.get("PORT", 7070)))
    a = p.parse_args()
    print("Bridge server on http://0.0.0.0:%d" % a.port, flush=True)
    ThreadingHTTPServer(("0.0.0.0", a.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
