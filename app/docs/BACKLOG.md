# CampusRoute backlog

Synthetic product backlog. Workshop scenarios reference these items.

| ID | Title | Type | Size | Notes |
|---|---|---|---|---|
| CR-9 | Retire `legacy/kiosk_router.py` | tech debt | M | Kiosk export still calls it. Needs someone to *understand* it first (Scenario 5) |
| CR-11 | "Open now?" badge from `hours` strings | feature | S | Format: `Mon-Fri 08:00-22:00; Sat 10:00-18:00`. Interview take-home uses this (Scenario 7) |
| CR-12 | Mobile client: port `schedule.py` | feature | L | Team wants the schedule logic on-device, same behavior, same tests (Scenario 4) |
| CR-13 | Step-free routing v2: elevators and ramps | feature | M | Today `avoid_stairs` only removes stair edges |
| CR-14 | Crowd report submission (POST) | feature | M | Needs rate limiting and abuse protection before it can exist; API is read-only today |
| CR-15 | Dark theme | UI | S | |
| CR-16 | Campus events calendar | feature | M | |
| CR-17 | Indoor routing across floors | feature | L | Rooms have `floor`; routing ignores it |
| CR-18 | RouteQL: scriptable route queries for kiosks | feature | M | Small language spec in Scenario 3 |
| CR-19 | Turkish UI (i18n) | UI | S | Search already folds Turkish letters |
| CR-20 | Lab assignment: students implement `shortest_path` | teaching | S | Course CS201 uses a simplified graph (Scenario 2) |

## Known issues

- `schedule.parse_time("24:00")` is rejected, but `campus.json` hours use `24:00` to mean midnight. CR-11 must handle that.
- Walking time ignores stairs and slopes.
