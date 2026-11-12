<img src="assets/bob.png" alt="Bob, a smiling robot in a blue hard hat" width="110" align="right">

# IBM Bob · Agentic AI in Action · Your Agentic Friend

A hands-on workshop where university students use **IBM Bob** as an *agent*, not an autocomplete: it plans, acts with your approval, and is checked by tests. Everything happens on one realistic codebase, **CampusRoute**, a campus navigation app.

**Live site → [barissozen95.github.io/bobathon](https://barissozen95.github.io/bobathon/)**

**Start here → [the guide page with all scenarios](https://barissozen95.github.io/bobathon/)** (step by step). After you download the repo you can also open `index.html` offline. Prefer plain Markdown? Read [GUIDE.md](GUIDE.md).

## Get the repo

```bash
git clone https://github.com/barissozen95/bobathon.git bobathon
cd bobathon
bash setup-check.sh
```

No Git? [Download the ZIP](https://github.com/barissozen95/bobathon/archive/refs/heads/main.zip), unpack it and rename the folder to `bobathon`.

Then in Bob choose **File → Open Folder…** and open the `bobathon` folder itself. Every `@/...` path in the guide starts from that folder.

## What's inside

```
bobathon/                 ← open THIS folder as your Bob workspace
├── assets/               Bob mascot images used by the guide page
├── index.html            guide page: setup + 7 scenarios (start here)
├── GUIDE.md              the same guide as detailed English text
├── AGENTS.md             project context Bob reads
├── setup-check.sh        30-second machine check
├── app/                  CampusRoute: Python app, web UI, 63 tests
├── scenarios/            7 scenario cards + inputs (menu: scenarios/README.md)
└── .bob/                 skill + custom mode used in Scenario 2
```

## Scenarios

Pick two. Each one stands alone and its core steps take about 10 minutes.

| # | Scenario | Coding? |
|---|---|---|
| [1](scenarios/s1-lecture-to-study-page/CARD.md) | Turn a messy lecture into a study page | No |
| [2](scenarios/s2-assignment-grader/CARD.md) | Teach Bob to grade: skill + read-only mode | Read Python |
| [3](scenarios/s3-build-a-language/CARD.md) | Build a programming language: RouteQL | Yes |
| [4](scenarios/s4-translate-code/CARD.md) | Port a real module to another language | Yes |
| [5](scenarios/s5-understand-legacy-code/CARD.md) | Understand legacy code you didn't write | Read Python |
| [6](scenarios/s6-project-plan/CARD.md) | Plan a 4-week team sprint, then change it | No |
| [7](scenarios/s7-career-and-interview/CARD.md) | CV review or an interview take-home | Path B only |

Everything in the repo, including the guide page, the scenario cards and the prompts you paste into Bob, is in English.

## Working as a team

1. One teammate **forks** this repo on GitHub and adds the others under **Settings → Collaborators**.
2. Everyone clones the fork: `git clone https://github.com/<user>/<fork>.git bobathon`
3. Everyone works on their own branch and pushes their output:

   ```bash
   git switch -c s3-ayse
   git add scenarios
   git commit -m "S3: RouteQL interpreter"
   git push -u origin s3-ayse
   ```

4. Open a pull request in your fork and review each other's work.

Outputs go in `scenarios/<scenario>/out/` and `scenarios/<scenario>/plans/`. Do not change the input files (lecture notes, rubric, submissions, CV, brief, tests); if you change one by mistake, restore it with `git checkout -- <file>`.

## Quick check

```bash
bash setup-check.sh
cd app && python3 -m campusroute serve     # http://127.0.0.1:8000
```

## Rules

- Keep auto-approve off and read every approval card: the agent writes files and runs commands on your laptop.
- No API keys, passwords or real personal data in prompts or files.
- Submitting Bob's work as your own coursework is cheating; follow your course's AI policy.

All people, places and data are synthetic.

---

*This README was made by **IBM Bob**.*
