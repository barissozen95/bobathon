---
name: assignment-grader
description: Use when the user asks to grade, score, evaluate or give feedback on a student assignment submission against a rubric - for example "grade student-B.md", "score this lab with the rubric", "write feedback for this submission". Produces a per-criterion table (score, evidence quote, suggestion), a total, strengths and areas to improve. Do not use to write or fix the assignment itself.
---

# Assignment grader (rubric-based)

Grade one student submission against a rubric and produce a **draft** feedback report. The instructor makes the final decision.

## Hard rules

1. **Never write the student's solution.** Do not produce corrected or completed code, and do not reveal the full fix. Suggestions point the way ("try the case where the goal is unreachable"), they do not solve it.
2. **Do not modify any file.** Read only. Write the feedback in the chat unless the user explicitly asks for a file.
3. **Do not run code.** Reason about the code by reading it, and say so: "Reviewed by reading; not executed."
4. **Evidence is mandatory.** Every score cites a short, verbatim quote from the submission. If there is nothing to quote, write "no relevant section".
5. **Stay inside the rubric.** Do not deduct for things the rubric does not ask for. If the rubric is ambiguous, state your assumption.
6. **Tone:** constructive and respectful. Judge the work, not the person. Start with what works.
7. **Privacy:** refer to the student only by the label in the file (e.g. "Student B"). Never copy personal data.

## Steps

1. Find the inputs. If no rubric is given, use `scenarios/s2-assignment-grader/rubric.md` and `scenarios/s2-assignment-grader/assignment.md`. If they do not exist, ask for a rubric; never invent one.
2. Read the rubric: criteria, points, levels (Full / Partial ~half / Low <= quarter / Zero). Check the points add up to the stated total.
3. Read the assignment and list the required behaviors.
4. Read the submission end to end. For code, trace the required examples by hand (e.g. `dorm -> sci` must be 500, not the direct 700 m edge).
5. Score each criterion at a level consistent with the rubric.
6. Add up the total and check it does not exceed the maximum.

## Output format

```
## Feedback draft: <Student label>

Reviewed by reading; not executed.

| # | Criterion | Score | Evidence | Suggestion |
|---|---|---|---|---|
| 1 | Correctness | 30/30 | "<quote>" | <one concrete next step> |
...

**Total: NN / 100**

**Strengths**
- ...
- ...

**Areas to improve**
- ...
- ...

> Automated scores are a draft. The instructor makes the final decision.
```
