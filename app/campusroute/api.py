"""Tiny JSON API + static web UI, standard library only.

Security defaults (this is a workshop app, but habits matter):
- binds to 127.0.0.1 only; there is no option to listen on all interfaces
- read-only GET endpoints; every other method gets 405
- static files come from a fixed allow-list, never from the request path
- responses carry nosniff and a same-origin Content-Security-Policy
"""

from __future__ import annotations

import json
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Callable, Optional
from urllib.parse import parse_qs, urlparse

from . import occupancy, routing, schedule, search
from .campus import Campus, UnknownPlaceError, load_campus

APP_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = APP_DIR / "web"
DATA_DIR = APP_DIR / "data"
STATIC_FILES = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
    "/style.css": ("style.css", "text/css; charset=utf-8"),
}
HOST = "127.0.0.1"


class ApiError(Exception):
    def __init__(self, status: HTTPStatus, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def _flag(value: Optional[str]) -> bool:
    return (value or "").lower() in ("1", "true", "yes", "on")


def _parse_now(value: Optional[str]) -> datetime:
    if not value:
        return datetime.now()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ApiError(HTTPStatus.BAD_REQUEST, "now must be ISO 8601, e.g. 2027-03-01T09:30") from None


class CampusApi:
    """Request-independent logic, easy to unit test without sockets."""

    def __init__(self, campus: Campus, sessions, reports, clock: Callable[[], datetime] = datetime.now):
        self.campus = campus
        self.sessions = sessions
        self.reports = reports
        self.clock = clock

    def places(self, _q):
        return {
            "places": [
                {"id": p.id, "name": p.name, "kind": p.kind, "x": p.x, "y": p.y, "hours": p.hours}
                for p in self.campus.places.values()
            ],
            "edges": [
                {"a": e.a, "b": e.b, "meters": e.meters, "stairs": e.stairs, "covered": e.covered}
                for e in self.campus.edges
            ],
        }

    def search(self, q):
        text = q.get("q", [""])[0]
        if len(text) > 100:
            raise ApiError(HTTPStatus.BAD_REQUEST, "query too long")
        hits = search.search(self.campus, text, limit=8)
        return {"query": text, "results": [h.__dict__ for h in hits]}

    def route(self, q):
        try:
            start = self.campus.resolve(q.get("from", [""])[0])
            goal = self.campus.resolve(q.get("to", [""])[0])
            via = [self.campus.resolve(v).id for v in q.get("via", []) if v]
        except UnknownPlaceError as exc:
            raise ApiError(HTTPStatus.NOT_FOUND, str(exc)) from None
        try:
            r = routing.shortest_route(self.campus, start.id, goal.id,
                                       avoid_stairs=_flag(q.get("avoid_stairs", [""])[0]), via=via)
        except routing.NoRouteError as exc:
            raise ApiError(HTTPStatus.NOT_FOUND, str(exc)) from None
        return r.to_dict(self.campus)

    def next_class(self, q):
        now = _parse_now(q.get("now", [""])[0]) if q.get("now") else self.clock()
        current = schedule.current_session(self.sessions, now)
        upcoming = schedule.next_session(self.sessions, now)
        body = {"now": now.isoformat(timespec="minutes"), "current": None, "next": None}
        if current:
            body["current"] = schedule.format_session(current)
        if upcoming:
            session, when = upcoming
            room = self.campus.rooms.get(session.room)
            body["next"] = {
                "session": schedule.format_session(session),
                "starts": when.isoformat(timespec="minutes"),
                "in_minutes": schedule.minutes_until(now, when),
                "place": room.place if room else None,
            }
        return body

    def crowd(self, q):
        now = _parse_now(q.get("now", [""])[0]) if q.get("now") else self.clock()
        levels = {}
        for place in self.campus.places.values():
            level = occupancy.crowd_level(self.reports, place.id, now)
            if level is not None:
                levels[place.id] = level
        return {"now": now.isoformat(timespec="minutes"), "levels": levels}

    ROUTES = {
        "/api/places": "places",
        "/api/search": "search",
        "/api/route": "route",
        "/api/next-class": "next_class",
        "/api/crowd": "crowd",
    }

    def handle(self, path: str, query: dict):
        name = self.ROUTES.get(path)
        if name is None:
            raise ApiError(HTTPStatus.NOT_FOUND, "no such endpoint")
        return getattr(self, name)(query)


def make_handler(api: CampusApi):
    class Handler(BaseHTTPRequestHandler):
        server_version = "CampusRoute/1.0"

        def _send(self, status, body: bytes, content_type: str):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status, payload):
            self._send(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8")

        def do_GET(self):  # noqa: N802 (http.server naming)
            url = urlparse(self.path)
            if url.path in STATIC_FILES:
                filename, ctype = STATIC_FILES[url.path]
                self._send(HTTPStatus.OK, (WEB_DIR / filename).read_bytes(), ctype)
                return
            try:
                payload = api.handle(url.path, parse_qs(url.query))
            except ApiError as exc:
                self._json(exc.status, {"error": exc.message})
                return
            self._json(HTTPStatus.OK, payload)

        def _not_allowed(self):
            self._json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "read-only API"})

        do_POST = do_PUT = do_DELETE = do_PATCH = _not_allowed

        def log_message(self, fmt, *args):  # keep test output quiet
            if getattr(self.server, "verbose", False):
                super().log_message(fmt, *args)

    return Handler


def build_api(clock: Callable[[], datetime] = datetime.now) -> CampusApi:
    campus = load_campus()
    sessions = schedule.load_schedule(DATA_DIR / "schedule.sample.csv")
    with open(DATA_DIR / "crowd.sample.json", encoding="utf-8") as fh:
        reports = [occupancy.parse_report(r) for r in json.load(fh)["reports"]]
    return CampusApi(campus, sessions, reports, clock)


def make_server(port: int = 8000, api: Optional[CampusApi] = None, verbose: bool = False):
    server = ThreadingHTTPServer((HOST, port), make_handler(api or build_api()))
    server.verbose = verbose
    return server


def serve(port: int = 8000) -> None:
    server = make_server(port, verbose=True)
    print("CampusRoute running at http://%s:%d  (Ctrl+C to stop)" % (HOST, server.server_port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
