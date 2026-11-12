# Project brief: CampusRoute v2.0 "Accessible campus" sprint (synthetic)

## Context

CampusRoute (see `app/README.md`) is used by students to find rooms and walk to class. The CS302 Software Engineering course has adopted it as a group project: a team of four ships **v2.0** in four weeks. Work items come from `app/docs/BACKLOG.md`.

## Goal

A student with a wheelchair, a broken leg or a heavy bag can plan a step-free route, see whether a building is open, and use the app in Turkish.

## Must ship (in priority order)

1. **CR-11 "Open now?" badge.** Parse the `hours` strings, add `open_now` to the API, show a badge in the web UI.
2. **CR-13 Step-free routing v2.** Add elevators and ramps to the campus data; routes with "avoid stairs" may use them.
3. **CR-19 Turkish UI.** All visible text in the web UI available in Turkish and English.

## Nice to have (only if the must-haves are done)

- CR-15 Dark theme.
- CR-16 Campus events calendar.

## Out of scope (do not plan these)

- **CR-14 crowd report submission.** The API stays read-only this semester; it needs a security review first.
- Native mobile apps.
- Any paid service, external map API or real user data.

## Definition of done

- All existing tests still pass (`python3 -m unittest discover -s tests` in `app/`), plus new tests for every new behavior.
- A usability test with at least 5 (synthetic) student personas, including two with mobility needs.
- One-page user guide, in English and Turkish.
- A 5-minute live demo.

## Calendar

- **Start:** Monday 1 March 2027
- **Weeks:** W1 1-5 Mar · W2 8-12 Mar · W3 15-19 Mar · W4 22-26 Mar
- **Demo and hand-in:** Friday 26 March 2027, 14:00. Nothing new is merged after Thursday 25 March 18:00.
