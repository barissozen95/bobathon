"""Command line interface: python3 -m campusroute <command> ..."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from . import __version__, routing, schedule, search
from .campus import CampusDataError, UnknownPlaceError, load_campus


def _cmd_search(args) -> int:
    campus = load_campus(args.campus)
    hits = search.search(campus, args.query, limit=args.limit)
    if not hits:
        print("No matches for '%s'." % args.query)
        return 1
    for hit in hits:
        print("%3d  %-5s  %s" % (hit.score, hit.kind, hit.label))
    return 0


def _cmd_route(args) -> int:
    campus = load_campus(args.campus)
    start, goal = campus.resolve(args.start), campus.resolve(args.goal)
    via = [campus.resolve(v).id for v in args.via]
    route = routing.shortest_route(campus, start.id, goal.id, avoid_stairs=args.avoid_stairs, via=via)
    print("%s -> %s: %d m, about %d min%s" % (
        start.name, goal.name, route.meters, route.minutes,
        "" if not route.has_stairs else " (includes stairs)"))
    for n, line in enumerate(routing.describe(route, campus), start=1):
        print("  %d. %s" % (n, line))
    return 0


def _cmd_next(args) -> int:
    sessions = schedule.load_schedule(args.schedule)
    now = datetime.fromisoformat(args.now) if args.now else datetime.now()
    for a, b in schedule.find_conflicts(sessions):
        print("warning: %s overlaps %s" % (schedule.format_session(a), schedule.format_session(b)))
    current = schedule.current_session(sessions, now)
    if current:
        print("Now:  %s" % schedule.format_session(current))
    upcoming = schedule.next_session(sessions, now)
    if upcoming is None:
        print("Schedule is empty.")
        return 1
    session, when = upcoming
    print("Next: %s (in %d min)" % (schedule.format_session(session), schedule.minutes_until(now, when)))
    return 0


def _cmd_serve(args) -> int:
    from .api import serve
    serve(args.port)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="campusroute", description="Campus navigation for students.")
    p.add_argument("--version", action="version", version="campusroute " + __version__)
    p.add_argument("--campus", help="path to a campus JSON file (default: data/campus.json)")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("search", help="find a building or room")
    s.add_argument("query")
    s.add_argument("--limit", type=int, default=5)
    s.set_defaults(func=_cmd_search)

    r = sub.add_parser("route", help="shortest walking route")
    r.add_argument("start")
    r.add_argument("goal")
    r.add_argument("--via", action="append", default=[], help="pass through this place (repeatable)")
    r.add_argument("--avoid-stairs", action="store_true")
    r.set_defaults(func=_cmd_route)

    n = sub.add_parser("next", help="next class from a schedule CSV")
    n.add_argument("--schedule", default="data/schedule.sample.csv")
    n.add_argument("--now", help="ISO time, e.g. 2027-03-01T09:30 (default: real clock)")
    n.set_defaults(func=_cmd_next)

    v = sub.add_parser("serve", help="run the web app on http://127.0.0.1:PORT")
    v.add_argument("--port", type=int, default=8000)
    v.set_defaults(func=_cmd_serve)
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (UnknownPlaceError, routing.NoRouteError, schedule.ScheduleError, CampusDataError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print("error: file not found: %s" % exc.filename, file=sys.stderr)
        return 2
