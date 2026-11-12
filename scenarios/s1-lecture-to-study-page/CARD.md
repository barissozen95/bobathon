# Scenario 1: Turn a messy lecture into a study page

> **Track:** Learning · **Coding needed:** none · **Time:** ~10 min core, +5 bonus
> **Bob features:** Ask mode · `@` file and URL mentions · Mermaid rendered in chat · Ask → Agent switch · file creation with approval
> **App link:** these are the CS201 lecture notes on the algorithm inside `app/campusroute/routing.py`

## Why this matters
Everyone has messy notes the night before a midterm. You will turn them into a concept map and a one-page HTML study sheet. You'll also catch the **factual error hidden in the notes**: Bob is a study partner, not an oracle.

## You will produce
1. A concept summary (in chat).
2. A Mermaid concept map rendered in chat.
3. `scenarios/s1-lecture-to-study-page/out/study-page.html`, which opens in a browser and shows the map.
4. The name of the wrong claim in the notes, and the correction.

## Inputs
- `lecture-week7-shortest-paths.md`: typed-up lecture notes on BFS, Dijkstra, A* and Bellman-Ford, with a CampusRoute angle.

## Core steps (~10 min)

### 1. Ask: extract the concepts (2 min)
Select **Ask** in the mode selector (Ask never changes files) and paste:

```text
@/scenarios/s1-lecture-to-study-page/lecture-week7-shortest-paths.md
Summarize this lecture for a midterm. List the 4 algorithms, what each one needs (weights, data structure), its time complexity, and how they relate to each other. Max 15 bullets.
```

**Check:** Does Bob's complexity for Dijkstra match the notes (`O((V + E) log V)`)?

### 2. Ask: find the error (2 min)
```text
One statement in these notes is factually wrong and would cost points on an exam. Which one is it, why is it wrong, and what is the correct statement? Quote the exact line.
```

**Check:** Look up the line yourself. Do you agree? (The answer is in the facilitator key, but decide first.)

### 3. Ask: concept map in chat (2 min)
```text
Draw a Mermaid flowchart concept map of this lecture: algorithms as nodes, edges labelled with relationships like "generalizes", "needs", "fails when". Put labels with parentheses in double quotes. Give it as a mermaid code block so it renders here.
```

### 4. Agent: build the study page (3 min)
Switch the mode selector to **Agent** and paste:

```text
Create scenarios/s1-lecture-to-study-page/out/study-page.html from @/scenarios/s1-lecture-to-study-page/lecture-week7-shortest-paths.md:
- sections: key ideas, comparison table, the concept map from our chat, "common exam traps" (include the corrected error), 5 self-test questions with answers hidden in <details>
- load Mermaid pinned over HTTPS: https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js and call mermaid.initialize({ startOnLoad: true })
- a single self-contained file, clean readable CSS, no other external resources
- fix the wrong claim; do not copy it
Do not modify the lecture notes file.
```

An **approval card** appears before Bob writes the file. Read it: is the path `out/study-page.html`? Then approve.

### 5. Open it (1 min)
Open `out/study-page.html` in your browser. The map should render; the corrected Dijkstra statement should be in "common exam traps".

## Bonus
- **Add a web source (Ask):**
  ```text
  @/scenarios/s1-lecture-to-study-page/lecture-week7-shortest-paths.md @https://en.wikipedia.org/wiki/A*_search_algorithm
  Using both, explain in 5 bullets why a straight-line distance heuristic is admissible on the CampusRoute map but a "number of buildings left" heuristic might not be.
  ```
- **Connect to the real code (Ask):**
  ```text
  @/app/campusroute/routing.py Which lines of this file implement steps 1-5 of Dijkstra in the lecture notes? Does it use lazy deletion and a tie-breaker counter?
  ```
  **Check:** open `routing.py` and confirm the line numbers.

## If you get stuck
| Problem | Fix |
|---|---|
| Mermaid shows an error | `The Mermaid has a syntax error. Rewrite it as a simple flowchart TD, wrap every label in double quotes, no special characters in node ids.` |
| Agent did not create the file | Check the mode selector says **Agent**. Ask is read-only by design. |
| HTML map is blank | The Mermaid script loads from the internet. Check your connection and that the `<script>` tag uses the exact pinned URL. |
| Bob "found" a different error | Ask: `Quote the line and give a counter-example graph that proves it wrong.` If it can't, it's probably not the error. |

**Facilitator fallback:** if time runs out, steps 1-3 are the core. A hand-written reference page is in the facilitator pack.

## Your responsibility
Bob can be fluent and wrong. Verify every complexity claim and the "error" against the notes and the code. These are synthetic notes; your own course notes may contain things you shouldn't upload. Check your course's AI policy.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Your Bob version's UI labels win.
