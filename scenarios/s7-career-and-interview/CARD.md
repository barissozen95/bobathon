# Scenario 7: CV review and a real interview take-home

> **Track:** Projects & career · **Coding needed:** CV path none, interview path Python · **Time:** ~10 min for **one** path
> **Bob features:** `@` mention of a **.docx** (read via Bob's Office reader) · Ask mode analysis · Agent mode writes a *new* file · approval workflow · running tests · (bonus) writing a custom mode
> **App link:** the job is on the CampusRoute team; the take-home is backlog **CR-11** "Open now?"

## Why this matters
Recruiters read your CV for 30 seconds; interviewers ask you to *explain* your take-home. Bob can sharpen both, or quietly make them dishonest. You'll catch Bob if it **adds experience you don't have**, and you'll use Bob for **hints, not answers**.

## Pick ONE path (both don't fit in 10 minutes)
| Path | Steps | For |
|---|---|---|
| **A. CV** | 1-3 | Everyone, no coding |
| **B. Interview** | 4-6 | Python required for step 6 |

## Inputs
- `cv.docx` (and `cv.md`, same content): **Deniz Aydin, entirely synthetic**. Deliberately weak in realistic ways.
- `job-posting.md`: *Junior Backend Developer (Python), CampusRoute team* at the fictional Synthetic Labs.
- `challenge/`: `README.md` (rules), `opening_hours.py` (empty `is_open`), `test_opening_hours.py` (14 tests, all failing at the start).

## Personal data rules
This CV is synthetic. **If you use your own CV, first delete phone, home address, date of birth, ID numbers and photo.** Notice that the synthetic CV *includes* some of these. Did Bob tell you to remove them?

---

## Path A: CV

### 1. Ask: gap analysis (3 min)
**Ask** mode:

```text
@/scenarios/s7-career-and-interview/cv.docx @/scenarios/s7-career-and-interview/job-posting.md
Act as a recruiter for this posting. 1) For each "Must have", is there evidence in the CV? Quote it or say "no evidence". 2) The 5 weakest lines in the CV and why. 3) Anything that should not be on a CV at all. Do not rewrite the CV yet.
```

**Check:** the posting requires automated tests. Is there *any* evidence of testing in the CV? Did Bob notice that the skills list claims Kubernetes and TensorFlow with no project behind them?

### 2. Agent: improved CV in a **new** file, with no invented facts (4 min)
Switch to **Agent**:

```text
Write an improved version of @/scenarios/s7-career-and-interview/cv.md to scenarios/s7-career-and-interview/out/cv-improved.md. Rules:
- Do NOT add any experience, skill, number or achievement that is not in the original. Where a metric would help, insert a placeholder like [ADD: how many bugs fixed?] for me to fill in honestly.
- Rewrite bullets as action + what + result. Cut the generic summary to 2 lines aimed at this posting.
- Remove personal data a CV should not contain. Trim the skills list to what the CV supports.
- Do not modify cv.docx or cv.md.
At the end list every change in a table: original | new | reason.
```

Approve only the write to `out/cv-improved.md`.

### 3. Fabrication audit (3 min)
Compare the two files line by line. For **every** claim in `cv-improved.md`, can you point to the original line? Then ask:

```text
@/scenarios/s7-career-and-interview/cv.md @/scenarios/s7-career-and-interview/out/cv-improved.md
List every statement in the improved CV that is not directly supported by the original. Be strict: rewordings that make a claim stronger count.
```

"Wrote some Python scripts" → "Automated deployment pipelines" is fabrication, even if it sounds good.

---

## Path B: Interview

### 4. Ask: case-study questions (2 min)
```text
@/scenarios/s7-career-and-interview/job-posting.md @/app/README.md
You are interviewing me for this role. Give me 3 short case-study questions about the CampusRoute codebase (e.g. "a student says the route through the library is wrong, how do you debug it?"). Ask them one at a time and wait for my answer before giving feedback.
```

Answer at least one in your own words. Ask for feedback against the "Must have" list.

### 5. Take-home: read before you code (1 min)
Read `challenge/README.md`. Run the tests and see them fail:

```bash
cd scenarios/s7-career-and-interview/challenge && python3 -m unittest test_opening_hours -v
```

### 6. Solve it with Bob as a coach, not a ghostwriter (rest of the time)
Write the code **yourself** in `challenge/opening_hours.py`. When stuck, **Ask** mode:

```text
@/scenarios/s7-career-and-interview/challenge/README.md @/scenarios/s7-career-and-interview/challenge/opening_hours.py
I'm stuck on <your problem, e.g. the overnight interval "Fri 20:00-02:00">. Give me a hint in at most 3 sentences. Do not write code for me.
```

Then let **Agent** only run the tests:

```text
Run: cd scenarios/s7-career-and-interview/challenge && python3 -m unittest test_opening_hours -v
Do not modify any file. Tell me which tests fail and what concept each one is about (not how to fix it).
```

When all 14 pass: explain your solution aloud in 60 seconds. That's the real interview.

---

## Bonus
- **A read-only Career Coach mode (Agent mode writes it):**
  ```text
  Add a custom mode to .bob/custom_modes.yaml, keeping the existing mode. slug: career-coach, name: Career Coach, groups: read only. roleDefinition: a strict but kind career coach for students who never invents experience and never writes code solutions. customInstructions: always ask for evidence; flag personal data; give hints, not answers.
  ```
  Open a new chat in **Career Coach** and repeat step 1. Is the feedback stricter?
- **Wire it into the app:** after the challenge passes, ask Bob in Ask mode how you'd add `open_now` to `/api/places` in `app/campusroute/api.py` with a test, without writing it.

## If you get stuck
| Problem | Fix |
|---|---|
| Bob can't read `cv.docx` | Use `@/scenarios/s7-career-and-interview/cv.md`, same content. |
| Bob invented experience | `Remove every claim not in the original and replace it with an [ADD: ...] placeholder.` |
| Bob writes the solution anyway | Don't paste it. `Hints only, max 3 sentences, no code.` Use Ask mode; it can't write files. |
| `ModuleNotFoundError: opening_hours` | Run the tests from inside `challenge/`. |

**Facilitator fallback:** for Path A, steps 1-2 are the core; for Path B, steps 4-5. The facilitator pack has a CV review key, interview answer notes and a tested reference solution (14/14). **Never show the solution before the attempt.**

## Your responsibility
Everything on your CV must be true and defensible in an interview. A take-home solved by an AI that you can't explain is worse than an honest partial solution. Follow each company's rules on AI use in hiring.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Bob's ability to *write* .docx is not documented; that's why output is Markdown.
