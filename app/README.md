# CampusRoute

CampusRoute helps students find rooms, walk the shortest route between buildings and see their next class. It is the shared codebase for the **IBM Bob · Agentic AI in Action** workshop: every workshop scenario reads, extends, plans or translates a part of this app.

> All data is synthetic. "Meridian University", its buildings, rooms, schedules and crowd reports are invented.

## Run it (Python 3.9+, standard library only, no installs)

```bash
cd app
python3 -m campusroute route "Main Gate" "ENG-B204"           # shortest walk
python3 -m campusroute route "SCI-110" "ENG-B204" --avoid-stairs
python3 -m campusroute search kutuphane                       # Turkish-aware search
python3 -m campusroute next --now 2027-03-01T09:30            # next class from data/schedule.sample.csv
python3 -m campusroute serve --port 8000                      # web app on http://127.0.0.1:8000
python3 -m unittest discover -s tests                         # 61 tests
```

## What is where

| Path | What it does |
|---|---|
| `campusroute/campus.py` | Loads and validates `data/campus.json`; `Campus.resolve()` turns "kütüphane", "ENG-B204" or "lib" into a place |
| `campusroute/search.py` | Accent-insensitive, Turkish-aware fuzzy search |
| `campusroute/routing.py` | Dijkstra shortest route, `avoid_stairs`, `via`, walking-time estimate, text directions |
| `campusroute/schedule.py` | Schedule CSV parser, conflict detection, "next class" lookup |
| `campusroute/occupancy.py` | Crowd level from recency-weighted student reports |
| `campusroute/api.py` | Read-only JSON API + static web UI (`http.server`, binds 127.0.0.1) |
| `campusroute/cli.py` | `python3 -m campusroute ...` |
| `campusroute/legacy/kiosk_router.py` | Inherited 2023 prototype, terse and uncommented. Not used by the API. Do not modify |
| `web/` | Single-page UI: SVG map, route form, search, next class, crowd |
| `data/` | Synthetic campus, sample schedule, sample crowd reports |
| `docs/ARCHITECTURE.md` | Module diagram and data flow |
| `docs/BACKLOG.md` | Open work items; workshop scenarios pick these up |

## API

| Endpoint | Example |
|---|---|
| `GET /api/places` | all places + walkways (for the map) |
| `GET /api/search?q=` | `?q=b204` |
| `GET /api/route?from=&to=&avoid_stairs=1&via=` | `?from=Main%20Gate&to=ENG-B204` |
| `GET /api/next-class?now=` | `?now=2027-03-01T12:30` |
| `GET /api/crowd?now=` | `?now=2027-03-01T12:30` |

Errors are JSON: `{"error": "unknown place 'moon'"}` with status 400/404/405.

## Security notes

- Server binds to `127.0.0.1` only. There is deliberately no `0.0.0.0` option.
- API is read-only; non-GET methods return 405.
- Static files come from a fixed allow-list (no path traversal).
- The web client inserts API data with `textContent`, never `innerHTML`.
- No secrets, keys or network calls anywhere in the app.
