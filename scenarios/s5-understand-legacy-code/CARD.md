# Scenario 5: Understand legacy code you didn't write

> **Track:** Learning · **Coding needed:** read Python · **Time:** ~10 min core, +5 bonus
> **Bob features:** Ask mode (read-only) · `@` file and **line-range** mentions (`@/file:10-20`) · code actions (**Explain with Bob**, **Improve with Bob**) · `Cmd/Ctrl + L` add selection to chat · Mermaid in chat
> **App link:** backlog **CR-9**: `app/campusroute/legacy/kiosk_router.py` must be understood before it can be retired

## Why this matters
On day one of an internship, nobody explains the code to you. This 339-line file has one-letter names and no comments, and the kiosks still depend on it. Use Bob to **speed up your own understanding**, then prove it by writing your own explanation and having Bob grade *you*.

## You will produce
1. A 5-part map of the file with line ranges (in chat, verified by you).
2. An explanation of the cache logic in `Router.shortest`.
3. A Mermaid call-flow diagram starting at `run()`.
4. **Your own 3-sentence "here's how I understand it" note, corrected by Bob.**

## Inputs
`app/campusroute/legacy/kiosk_router.py`. **Do not modify it.** Run it first:

```bash
cd app && python3 -m campusroute.legacy.kiosk_router
```

The first line should be `A F 13.0 ['A', 'C', 'B', 'D', 'E', 'F']`; it ends with an ASCII map.

## Core steps (~10 min)

### 1. Purpose and parts (2 min)
**Ask** mode:

```text
@/app/campusroute/legacy/kiosk_router.py What is this file for? Summarize its main classes and functions in 5 bullets, one sentence each, with the line range of each.
```

**Check:** open two of the ranges. Are they really those classes/functions?

### 2. Zoom in with a line range (2 min)
```text
@/app/campusroute/legacy/kiosk_router.py:49-75 What do get and put do? Why combine a dict with a doubly linked list? What is evicted when the cache is full?
```

### 3. Code action on a method (2 min)
1. Open the file and select `Router.shortest` (**lines 219-232**).
2. Right-click → **Bob** → **Explain with Bob** (or the lightbulb icon).
3. Then select the same lines, press `Cmd + L` / `Ctrl + L` to add them to the chat, and ask:
   ```text
   Is an unreachable result (inf, None) cached too? What happens if s is not in the graph at all?
   ```

**Check:** read lines 220-221 and 226-231 yourself. Two different paths, two different caching behaviors.

### 4. Call-flow diagram (1.5 min)
```text
@/app/campusroute/legacy/kiosk_router.py Draw a Mermaid flowchart of the call flow starting at run(). Only show which functions and methods call which. Wrap labels containing parentheses in double quotes.
```

**Check:** pick two arrows and find the call in the file (e.g. `Router.shortest → dijkstra` is on line 226).

### 5. Learning step: test *your* understanding (2.5 min)
> Write first, **then** ask Bob. If you read Bob's answer first, you've tested nothing.

a) Without looking at Bob's answers, write **3 sentences** in your own words: what the file solves, when the cache is used, what happens after `update()`.

b) Paste in **Ask** mode:

```text
@/app/campusroute/legacy/kiosk_router.py Below is how I understand this file. Only point out what is wrong or missing, with line numbers. Do not re-explain the whole file and do not write code.
1. ...
2. ...
3. ...
```

c) Verify each correction **in the file**, then rewrite your note.

## Bonus
- **Improve with Bob + "why?"**: select `G.comps` (lines 134-151) → **Improve with Bob**. Before accepting anything, ask: `Does this change behavior? How can we be sure? What would a test for it look like?` Then **reject** the change: this file must stay as it is.
- **Map it to the new code (Ask):** `Compare @/app/campusroute/legacy/kiosk_router.py with @/app/campusroute/routing.py. What does the legacy router do that the new one does not (caching, A*, grid maps)? What would we lose if we deleted it today? This is for backlog CR-9.`

## Verify-Bob drill (answers are in the file, look first)
- `grid_graph` (257-279): a `~` cell costs 3.0, but **which end of the edge** decides the cost? Is moving *out of* a `~` cell to the right as expensive as moving *into* it?
- Does `LRU.clear()` (77-80) reset the `hit`/`miss` counters?
- Why does `dijkstra` push `next(cnt)` into the heap (line 172)?
- `run()` returns nothing, so what exit code does `sys.exit(run())` produce (line 339)?
- Why does `center` print `None` for the sample city? (Hint: `comps`.)

## If you get stuck
| Problem | Fix |
|---|---|
| Line-range mention ignored | Path must start with `/`, format `:start-end`, no spaces. Or select and `Cmd/Ctrl + L`. |
| No Bob in right-click menu | Select code first. Try the lightbulb or the Command Palette (`Cmd/Ctrl + Shift + P`, type "Bob"). |
| Mermaid error | `Rewrite as flowchart TD, every label in double quotes.` or `Don't render, output only the Mermaid code block.` |
| Bob gives wrong line numbers | Expected sometimes. That's why you check. `That range is wrong, re-read the file and correct it.` |
| Bob wants to edit the file | You're not in Ask mode. Reject the approval card. |

**Facilitator fallback:** steps 1 and 5 are the core. Never show the answer key or the sample student note before the participant writes their own.

## Your responsibility
Ask mode cannot change files, so exploring is safe. Code actions like **Improve** propose edits: read and reject them here. Bob's explanation is a hypothesis until you've checked it against the code.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Your Bob version's UI labels win.
