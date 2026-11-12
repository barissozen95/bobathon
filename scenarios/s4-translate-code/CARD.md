# Scenario 4: Port a real module to another language

> **Track:** Build · **Coding needed:** yes · **Time:** ~10 min core (tight!), +5 bonus
> **Bob features:** Ask mode analysis · Agent mode translation · `@` mentions · approval workflow · running tests · literate coding (`Cmd/Ctrl + I`)
> **App link:** backlog **CR-12**: the mobile client needs `app/campusroute/schedule.py` on-device, *same behavior, same tests*

## Why this matters
"Translate this file" is easy. "Translate it so 20 tests still pass" is engineering. Python and JavaScript disagree on weekdays, integer division, dict ordering and CSV parsing, and every one of those is in this file. Your job is to make Bob prove behavior is preserved.

## You will produce
1. A list of porting traps found by Bob, which you check against the source.
2. `scenarios/s4-translate-code/out/schedule.mjs` (or your language).
3. `scenarios/s4-translate-code/out/schedule.test.mjs`: the 20 Python tests, ported and passing.
4. One small change made with literate coding, reviewed as an inline diff.

## Inputs
- Source: `app/campusroute/schedule.py` (CSV parsing, conflicts, "next class" lookup).
- Tests: `app/tests/test_schedule.py` (20 tests). Run the original with `cd app && python3 -m unittest tests.test_schedule`.

## Before you start
- **Default target: JavaScript (Node 18+)**: `node --version`. Tests use the built-in `node:test`, nothing to install.
- Other targets work. Replace "JavaScript/Node" in the prompts with Java 17 (`javac -version`), Kotlin, Swift, Go or C#. Use only the standard library. No JUnit/Maven/npm downloads.
- **Auto-approve OFF.**

## Core steps (~10 min)

### 1. Ask: find the traps before translating (2 min)
**Ask** mode:

```text
@/app/campusroute/schedule.py I will port this to JavaScript (Node 18, ES modules, no dependencies). List every place where a naive translation would change behavior. Check specifically: weekday numbering, % with negative numbers, // vs Math.floor/trunc, dict insertion order, csv quoting, str.isdigit, datetime arithmetic, sort stability, None. For each: line number, Python behavior, JS pitfall. Max 10 bullets.
```

**Check:** open the file at two of the line numbers Bob gives. Is the code really there? (`datetime.weekday()` is Monday=0. What is JS `getDay()`?)

### 2. Agent: translate (3 min)
Switch to **Agent**:

```text
Port @/app/campusroute/schedule.py to JavaScript as scenarios/s4-translate-code/out/schedule.mjs (ES module, Node 18+, no dependencies). Preserve behavior exactly, including error messages. Handle the traps from your analysis explicitly and mark each with a comment starting "PY:". Do not modify anything under app/.
```

Read the approval card: the only file written should be `out/schedule.mjs`.

### 3. Agent: port the tests, run, fix the CODE (4 min)
```text
Port @/app/tests/test_schedule.py to scenarios/s4-translate-code/out/schedule.test.mjs using node:test and node:assert/strict. Same inputs, same expected values. Every Python test must have a JS counterpart with the same name. Run: node --test scenarios/s4-translate-code/out/
If a test fails, fix schedule.mjs. Never change an expected value to make a test pass.
```

**Check:** if Bob changed a test, compare it side by side with `test_schedule.py`. Changing the *expected value* is the most common way a "successful" port is actually broken.

### 4. Literate coding: a small change (1 min)
Open `out/schedule.mjs`, click inside `parseDay`, press `Cmd + I` (Mac) / `Ctrl + I` (Win/Linux) or click the **magic wand** icon. Type the instruction (it shows in blue):

```text
also accept Turkish day abbreviations Pzt, Sal, Car, Per, Cum, Cmt, Paz
```

Press **Generate** (`Cmd/Ctrl + Enter`). Review the inline diff. Accept with `Cmd/Ctrl + Enter`, reject with `Cmd/Ctrl + Shift + Backspace`. Re-run the tests. **One test should now fail. Which one, and is the test or the change "right"?** (Hint: `test_bad_day` uses `Pzt`.)

> Docs note: one quickstart page lists `Cmd/Ctrl + M` for literate coding; the feature page says `Cmd/Ctrl + I`. Use whatever your UI shows; the magic wand always works.

## Bonus
- **What didn't translate 1:1? (Ask):** `Compare @/app/campusroute/schedule.py and @/scenarios/s4-translate-code/out/schedule.mjs. Which Python idioms had no direct JS equivalent and how were they compensated? 5 bullets.` Compare with the trap table below.
- **Mutation test it:** ask Bob to temporarily replace `(date.getDay() + 6) % 7` with `date.getDay()`, run the tests, report how many fail, then revert. If **zero** tests fail, the test port is too weak.

## Porting traps that really exist in this file
| Where in `schedule.py` | Trap |
|---|---|
| `now.weekday()` | Python Monday=0. JS `Date.getDay()` is **Sunday=0** |
| `_occurrence_after`: `% 7` | Python `%` is never negative. JS `-1 % 7 === -1` |
| `minutes_until`: `int()` and `//` | `int` truncates toward zero, `//` floors; JS needs `Math.trunc` / `Math.floor` |
| `weekly_minutes` → dict | Python dict keeps insertion order. A JS object moves integer-like keys (`"101"`) first. Use `Map` |
| `parse_schedule` → `csv.reader` | JS has no CSV parser; `"CS203, Section 2"` (quoted comma) breaks a naive `split(",")` |
| `parse_time`: `isascii() and isdigit()` | `"²".isdigit()` is True in Python. Translate the *intent* (ASCII digits) |
| `timedelta(days=7)` | Adding `7*24h` in ms is wrong across a DST change; add calendar days |
| `sorted(..., key=tuple)` | Need an explicit comparator; JS sort is stable since ES2019 |
| `datetime(2027, 3, 1)` in tests | JS `new Date(2027, 2, 1)`: **months are 0-based** |
| `room.upper()` | Fine in JS, but Java's `toUpperCase()` depends on locale (Turkish `i` → `İ`). Use `Locale.ROOT` |

## If you get stuck
| Problem | Fix |
|---|---|
| `node: command not found` | Pick another installed language, or do steps 1-2 and review the translation in Ask mode. |
| ESM import errors | Use `.mjs` extensions and `import ... from "./schedule.mjs"` (with extension). |
| Bob adds npm packages / Jest | Reject. `Use node:test only. No installs.` |
| Dates off by one day | Weekday mapping or 0-based months. Ask Bob to print `weekday(new Date(2027, 2, 1))`, which must be 0. |

**Facilitator fallback:** steps 1-2 are the core. The facilitator has a reference JS port (22/22 tests pass, mutation-checked) to copy into `out/` so the participant can still do steps 3-4.

## Your responsibility
A translation is not correct because it compiles. It is correct when the original tests pass, unchanged in meaning. Read every changed expected value. Don't submit a Bob translation as your own coursework.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Your Bob version's UI labels win.
