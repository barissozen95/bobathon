# CS201 Lab 4 rubric (100 points)

Levels for every criterion: **Full** (all points) · **Partial** (about half) · **Low** (a quarter or less) · **Zero** (missing).

| # | Criterion | Points | Full credit means |
|---|---|---|---|
| 1 | Correctness | 30 | Finds the minimum-distance path on weighted graphs, e.g. `dorm -> engB = 580` via `north`. Uses weights, not hop count |
| 2 | Edge cases | 15 | `start == goal`, unreachable goal returns `(math.inf, [])`, unknown node raises `ValueError` |
| 3 | Tests | 20 | At least 4 meaningful `unittest` tests that cover the normal case and the edge cases, with correct expected values |
| 4 | Complexity analysis | 15 | Correct time and space complexity for the implementation *as written*, with justification |
| 5 | Code quality | 10 | Readable names, no dead code, docstring, sensible structure |
| 6 | Reflection | 10 | Honest, specific reflection; states the positive-weight assumption |

## Feedback format

For each criterion: **score**, **evidence** (a short quote from the submission), **suggestion** (one concrete next step, not a solution).
Then: total, two strengths, two areas to improve.

> Automated scores are a draft. The instructor makes the final decision.
