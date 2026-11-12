# Scenario 3: Build a programming language from scratch (RouteQL)

> **Track:** Build · **Coding needed:** yes (Python) · **Time:** ~10 min core (tight!), +10 bonus
> **Bob features:** Plan mode → plan review → **new task** in Agent mode · approval workflow · running commands · `@` mentions
> **App link:** backlog **CR-18**. RouteQL scripts drive the real `campusroute` engine

## Why this matters
Kiosk operators want to script routes: `route "Main Gate" to "ENG-B204" avoid stairs`. You'll have Bob **plan** a lexer, parser and interpreter, *you* approve the plan, then Bob implements it against a real API and a real test suite. This is the core agentic loop: plan, review, act, verify.

## You will produce
1. An approved plan in `scenarios/s3-build-a-language/plans/`.
2. `scenarios/s3-build-a-language/out/routeql.py`, a working interpreter.
3. A green run of the provided acceptance tests (`test_routeql.py`, 16 tests).

## Inputs
- `routeql-spec.md`: the full language (grammar, output format, error format, hard constraints).
- `examples/01-basics.rql` … `04-syntax-error.rql`.
- `test_routeql.py`: black-box acceptance tests. **Do not let Bob edit them.**
- The engine: `app/campusroute/campus.py` (`resolve`), `routing.py` (`shortest_route`), `search.py` (`search`).

## Before you start
- `python3 --version` shows 3.9 or newer.
- **Auto-approve is OFF** (Permissions menu in the chat). Reviewing approval cards is part of this scenario.

## Security rules (also in the prompts)
The interpreter must **not** use `eval`, `exec`, `compile`, `os.system` or `subprocess`. Otherwise a `.rql` file could run arbitrary code on your machine. One test literally feeds it `__import__("os")`.

## Core steps (~10 min)

### 1. Plan mode: get a plan (3 min)
Select **Plan** mode and paste:

```text
Plan a RouteQL interpreter per @/scenarios/s3-build-a-language/routeql-spec.md. Do not write code yet.
Write the plan to scenarios/s3-build-a-language/plans/routeql-plan.md (one file). Cover: lexer (token kinds), parser (one statement per line, recursive descent from the EBNF), AST classes, interpreter, how it imports campusroute from app/ (sys.path relative to the script), error handling with "Error on line N: ..." on stderr and exit codes 0/1/2, and verification with @/scenarios/s3-build-a-language/test_routeql.py.
Constraints: Python 3.9 standard library only; no eval/exec/compile/os.system/subprocess; output file scenarios/s3-build-a-language/out/routeql.py; no features beyond the spec.
```

If Bob asks clarifying questions, pick an option.

### 2. Review the plan like a tech lead (2 min)
Open the plan. Check three things:
- **Scope:** anything that isn't in the spec (loops? functions?) → ask to remove it.
- **"Parse first, then run":** does the plan guarantee that a syntax error on line 2 prints *nothing* for line 1? (Spec rule 1, test `test_04`.)
- **Vague words:** "handle errors appropriately" → ask for the exact message format.

Ask **one** change, e.g.:
```text
Add to the plan: the whole file is parsed before anything runs, so a syntax error produces no stdout at all. Update the plan file.
```

> **Short on time? Stop here.** Producing and critiquing a plan *is* the core learning outcome.

### 3. New task, Agent mode: implement (3 min)
Click **+** (New task) to start a fresh conversation (this keeps the planning chat out of the context), select **Agent**, paste:

```text
Implement @/scenarios/s3-build-a-language/plans/routeql-plan.md. Write scenarios/s3-build-a-language/out/routeql.py. Spec: @/scenarios/s3-build-a-language/routeql-spec.md. Use campusroute.campus.load_campus, Campus.resolve, routing.shortest_route and search.search from app/. No eval/exec/compile/os.system/subprocess. Do not modify test_routeql.py or anything under app/.
```

### 4. Make one deliberate approval decision (with step 3)
For every approval card, read **what file** is written or **what command** runs. If you see `eval`, `exec`, `pip install`, or an edit to `test_routeql.py` or `app/`, **reject** and tell Bob why. Use **Approve** (once) rather than "approve for task" for the first file write.

### 5. Verify (2 min)
```text
Run: python3 scenarios/s3-build-a-language/test_routeql.py
If tests fail, fix routeql.py, never the tests. Show the final result.
```
Then try it yourself in the terminal:
```bash
python3 scenarios/s3-build-a-language/out/routeql.py scenarios/s3-build-a-language/examples/02-accessibility.rql
```
`avoid stairs` should turn the 270 m stair shortcut into a 540 m step-free route.

## Bonus
- **Extend the language:** `Add a "time A to B" statement that prints only the walking minutes. First update routeql-spec.md (grammar + semantics), then routeql.py, then add a test to test_routeql.py. Show me the diff of the spec before you change code.` (Here you *do* allow test edits. Notice the order: spec, code, test.)
- **Learn it (Ask):** `@/scenarios/s3-build-a-language/out/routeql.py For the line: route lab to "ENG-B204" avoid stairs, show the token list, the AST object and which campusroute functions get called, in order.`

## If you get stuck
| Problem | Fix |
|---|---|
| Plan adds loops/functions | `Reduce the plan to exactly what the spec defines.` |
| No plan file | In Agent mode: `Save the plan to scenarios/s3-build-a-language/plans/routeql-plan.md`. |
| `ModuleNotFoundError: campusroute` | `Add the workspace's app/ folder to sys.path using Path(__file__).resolve().parents[3] / "app" (out/ -> s3 -> scenarios -> workspace).` |
| `test_04` fails (output before syntax error) | `Parse the whole file before executing any statement.` |
| Bob edits the tests | Reject. `The tests are the spec. Change routeql.py only.` |
| Too many approval cards | Normal. You can pre-allow **read** and **edit** for this task in Permissions. Never leave **execute** on auto. |

**Facilitator fallback:** steps 1-2 are the core. The facilitator has a tested reference interpreter (passes 16/16). Copy it to `out/` only *after* the participant has reviewed a plan, to continue with step 5 and the bonus.

## Your responsibility
Read code before you run it, especially anything that executes input. "Looks like it works" is not done: done is the acceptance tests passing, and you able to explain the parser. If this resembles a compilers assignment, using Bob to write it for you breaks academic integrity.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Your Bob version's UI labels win.
