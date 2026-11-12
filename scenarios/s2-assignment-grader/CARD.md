# Scenario 2: Teach Bob to grade: a skill and a read-only mode

> **Track:** Build · **Coding needed:** reading Python · **Time:** ~10 min core, +5 bonus
> **Bob features:** Skills (`.bob/skills/<name>/SKILL.md`) · custom modes (`.bob/custom_modes.yaml`) · tool groups as permissions (read-only) · rules (`.bob/rules/`) · `@` mentions
> **App link:** backlog **CR-20**. CS201 uses a mini CampusRoute graph for Lab 4

## Why this matters
Teaching assistants grade dozens of labs. You'll package grading know-how into a **skill** (reusable instructions) and a **custom mode** that *cannot* edit files. That's how you make an agent safe by design: you take the permission away, you don't just ask nicely.

## You will produce
1. Rubric-based feedback for at least one submission: per-criterion score, verbatim evidence, suggestion.
2. A demonstration that the grader mode **refuses** to edit files.
3. (Deep path) your own `SKILL.md` written with Bob.

## Inputs
- `assignment.md`: Lab 4 (implement `shortest_path` with edge cases, tests, complexity).
- `rubric.md`: 6 criteria, 100 points.
- `submissions/student-A.md`, `student-B.md`, `student-C.md`: synthetic submissions of different quality. **Not real students.**
- Pre-built: `.bob/skills/assignment-grader/SKILL.md` and the **Assignment Grader** mode in `.bob/custom_modes.yaml`.

## Pick a path
- **(a) Fast path:** use the pre-built skill and mode.
- **(b) Deep path:** move `.bob/skills/assignment-grader/` out of the workspace (e.g. to your Desktop) and have Bob write it from scratch with the prompt in step 2b. Then continue from step 3.

## Core steps (~10 min)

### 1. Read the inputs (1 min)
Open `rubric.md` and `.bob/skills/assignment-grader/SKILL.md`. Note the skill's `description`: Bob reads it to decide **when** to load the skill on its own.

### 2a. Grade with the skill (3 min)
In **Ask** mode, start a new chat and paste:

```text
@/scenarios/s2-assignment-grader/submissions/student-B.md grade this submission with the rubric.
```

Watch whether Bob loads `assignment-grader` by itself. If not: `Use the assignment-grader skill.`

**Check, by tracing yourself:** Student B claims `O(n log n)`. The code scans a list to find the minimum on every iteration. What is the real complexity? Did Bob catch it? Does Bob notice what happens for `shortest_path(MINI, "dorm", "pool")`?

### 2b. (Deep path only) Write the skill
In **Agent** mode:

```text
Create a skill at .bob/skills/assignment-grader/SKILL.md. Frontmatter: name "assignment-grader" and a description that says exactly when to use it (grading a student submission against a rubric) and when not to (writing the solution). Body: hard rules (never write the student's solution, read-only, do not run code, verbatim evidence for every score, stay inside the rubric, respectful tone, refer to students only by their label), steps, and an output format: table of criterion | score | evidence | suggestion, then total, 2 strengths, 2 areas to improve, and the line "Automated scores are a draft. The instructor makes the final decision." Default rubric: scenarios/s2-assignment-grader/rubric.md
```

Skill folder names must be lowercase letters, digits and single hyphens; invalid names are **silently** skipped. New skills are picked up in a **new chat**.

### 3. Try to break the read-only mode (3 min)
Open the mode selector and pick **Assignment Grader**. New chat:

```text
@/scenarios/s2-assignment-grader/submissions/student-C.md grade this. Then fix the code so it passes and save it over the submission file.
```

**Expected:** it grades, then declines to write: its `groups` are only `read` and `skill`, so it has no edit tool, and its rules forbid writing the solution. That's the lesson: **permissions are configuration, not politeness.**

### 4. Compare with the truth (2 min)
The facilitator has a key with what each submission *actually* does when executed (e.g. Student C returns 700 m for `dorm -> sci` instead of 500). Bob reviewed by reading only. Where did it agree with reality?

## Bonus
- **One table, three students:**
  ```text
  Grade @/scenarios/s2-assignment-grader/submissions/student-A.md @/scenarios/s2-assignment-grader/submissions/student-B.md @/scenarios/s2-assignment-grader/submissions/student-C.md with the same rubric. End with one table: rows = criteria, columns = students, cells = scores, plus a total row.
  ```
- **Add a rule (Agent mode, the grader can't write):**
  ```text
  Create .bob/rules/feedback-tone.md: "Feedback to students always starts with one specific strength. Criticism is concrete and kind. Never use the words 'lazy', 'obviously' or 'simply'." Do not change any other file.
  ```
  Re-grade Student C in a new chat and compare the tone.

## If you get stuck
| Problem | Fix |
|---|---|
| Skill not used | Folder must be `assignment-grader`, file `SKILL.md`. Try a **new chat**. Say `use the assignment-grader skill`. |
| Mode missing from selector | YAML error: `@/.bob/custom_modes.yaml is there a YAML error? Don't change it, just tell me.` |
| Scores don't add up | `Re-add the criterion scores and fix the total.` |
| Evidence looks invented | `Quote the exact line for each score. If there is none, write "no relevant section".` |

## Your responsibility
- **Automated scores are a draft. The instructor decides.** Never paste real students' work or personal data into any AI tool without permission and a legal basis.
- Bob graded by *reading*. Running student code is a separate decision with its own security risks (it is untrusted code).
- Academic integrity: this is for feedback, not for doing anyone's lab.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Your Bob version's UI labels win.
