# AGENTS.md: IBM Bob · Agentic AI in Action workspace

Context for AI agents (IBM Bob) working in this repository.

## What this is
A workshop workspace for university students. `app/` is **CampusRoute**, a small but real campus-navigation app (Python 3.9+ standard library only). `scenarios/` holds seven independent exercises that read, extend, translate or plan parts of the app.

## Commands
- App tests: `cd app && python3 -m unittest discover -s tests` (63 tests, must stay green)
- Run app: `cd app && python3 -m campusroute serve --port 8000` then open http://127.0.0.1:8000
- CLI: `cd app && python3 -m campusroute route "Main Gate" "ENG-B204"`
- RouteQL acceptance tests: `python3 scenarios/s3-build-a-language/test_routeql.py`
- Schedule port tests (JS): `node --test scenarios/s4-translate-code/out/`

## Rules for agents
- **Never modify** `app/campusroute/legacy/kiosk_router.py`, any `test_*.py` provided with a scenario, or scenario input files (lecture notes, rubric, submissions, CV, brief, team), unless the user explicitly asks.
- Participant output goes in `scenarios/<scenario>/out/` or `scenarios/<scenario>/plans/`.
- Standard library only. No `pip install`, `npm install`, downloads, or network calls from code.
- No `eval`, `exec`, `compile`, `os.system`, `subprocess` in interpreters or app code.
- Servers bind to `127.0.0.1` only.
- All people and data here are synthetic. Do not add real personal data.
- When tests fail, fix the code, not the expected values.
- Students are learning: when asked for hints, give hints, not full solutions.

## Code style
- Python: type hints where helpful, docstrings on public functions, `unittest` tests next to behavior changes.
- Errors: domain exceptions (`UnknownPlaceError`, `NoRouteError`, `ScheduleError`, `CampusDataError`) with human-readable messages.
