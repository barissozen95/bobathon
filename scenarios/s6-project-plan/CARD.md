# Scenario 6: Plan a 4-week team sprint, then change it

> **Track:** Projects & career · **Coding needed:** none · **Time:** ~10 min core, +5 bonus
> **Bob features:** Plan mode (writes Markdown, no code, no commands) · `@` mentions of several files · Mermaid timeline/gantt in chat · plan saved to a file · Ask mode for risk review
> **App link:** the real backlog `app/docs/BACKLOG.md` (CR-11, CR-13, CR-19 …)

## Why this matters
Group projects fail on planning, not on code. You'll have Bob turn a brief, a backlog and a team sheet into phases, an owner-per-task table and a timeline. Then you'll **check the arithmetic** and **break the plan on purpose** with a change request. The skill being trained is *not trusting a confident table*.

## You will produce
1. Phases and a task table (task, backlog ID, owner, hours, week).
2. A per-person, per-week hours check that never exceeds capacity.
3. A Mermaid timeline (gantt or fallback).
4. A re-plan after a change request.
5. `scenarios/s6-project-plan/plans/sprint-plan.md`.

## Inputs
- `brief.md`: v2.0 "Accessible campus" sprint: must-ship CR-11, CR-13, CR-19; nice-to-have CR-15, CR-16; **CR-14 out of scope**; demo **Fri 26 Mar 2027, 14:00**; code freeze Thu 25 Mar 18:00.
- `team.md`: 4 synthetic people, hours per week. **The weekly 1-hour meeting is included** in those hours, so real task capacity is 142 h, not 158 h. Ada has exams in W2.
- `app/docs/BACKLOG.md`: item descriptions.

Bring a calculator, or use the Python REPL.

## Core steps (~10 min)

### 1. Plan mode: phases and tasks (3 min)
Select **Plan** mode:

```text
@/scenarios/s6-project-plan/brief.md @/scenarios/s6-project-plan/team.md @/app/docs/BACKLOG.md
Plan this 4-week sprint. Do not write code.
1. Phases per week (W1-W4) with a one-line goal each.
2. A task table: task | backlog ID | owner | hours | week. Match tasks to strengths; give Elif small coding tasks; schedule around Ada's W2 exams.
3. A capacity table: person x week, planned hours vs available hours. Remember the 1-hour weekly meeting is already inside the available hours.
Only plan the must-ship items first; add nice-to-haves only if capacity remains. Do not plan out-of-scope items.
```

### 2. Audit the numbers (2 min)
For **two people**, add up their task hours per week yourself. Then check:
- Did Bob subtract the meeting hour (Ada W2 = 5 h of tasks, not 6)?
- Is anything planned after the **Thursday 18:00 code freeze**?
- Did CR-14 sneak in?
- Does every PR have a reviewer who isn't the author?

If something's off:
```text
Ada's W2 tasks add up to X h but she has 5 h after the meeting. Fix the capacity table and move work so nobody exceeds capacity. Show only the changed rows.
```

### 3. Timeline in chat (2 min)
```text
Draw a Mermaid gantt chart of this plan: dateFormat YYYY-MM-DD, starting 2027-03-01, one section per backlog item, a milestone for the demo on 2027-03-26.
```
If it doesn't render, see "If you get stuck".

### 4. Change request: break the plan (2 min)
```text
Change: Mert is sick for all of W3 and can only do 4 hours that week. Re-plan W3 and W4. Keep the must-ship items and the demo date. Say explicitly what you dropped or moved and why. Show only what changed and the new capacity table.
```

**Check:** did Bob drop a *nice-to-have* (e.g. dark theme) rather than a must-ship? Did the numbers stay under capacity?

### 5. Save it (1 min)
```text
Save the final plan (phases, task table, capacity table, gantt code block, change log) to scenarios/s6-project-plan/plans/sprint-plan.md.
```

## Bonus
- **Risk review (Ask):** `@/scenarios/s6-project-plan/plans/sprint-plan.md As a skeptical TA, list the 5 biggest risks in this plan, each with an early warning sign and a mitigation. Consider: the team has never worked together, Elif is the only one who has run a usability test, and CR-13 changes campus data that the tests depend on.`
- **Make it concrete:** `For task CR-11, write the first three GitHub-style issues (title, acceptance criteria, owner, estimate) based on @/scenarios/s7-career-and-interview/challenge/README.md.`

## If you get stuck
| Problem | Fix |
|---|---|
| Gantt doesn't render | `Use a Mermaid flowchart LR with one node per week instead.` Or: `Give the timeline as a Markdown table: week x person.` |
| Plan file not saved | Plan mode can write Markdown. If it refuses, ask it again with the exact path, or switch to Agent just to save it. |
| Bob asks many clarifying questions | Answer by clicking an option; that's normal in Plan mode. |
| Numbers keep being wrong | Ask Bob to show its sums per person per week as a calculation, then check one line yourself. |

**Facilitator fallback:** steps 1, 2 and 4 are the core. A hand-checked reference plan (all sums verified) is in the facilitator pack.

## Your responsibility
The plan is yours, not Bob's. Check every total. Use only synthetic names here; don't paste classmates' real availability or personal data.

> Prompts follow the Bob docs but have not yet been run in a live Bob session. Mermaid `gantt` is not mentioned in the Bob docs: rehearse it.
