# Take-home challenge: "Open now?" (CampusRoute backlog CR-11)

> Synthetic interview task for the fictional **Synthetic Labs** "Junior Backend Developer, CampusRoute team" role.
> Time box: 25 minutes in a real interview. In the workshop: use Bob for **hints, not answers**.

Every place in `app/data/campus.json` has an `hours` string, for example:

```
Mon-Fri 08:00-24:00; Sat 10:00-18:00; Sun 12:00-20:00
```

Implement `is_open(hours, now)` in `opening_hours.py` so the web app can show an "Open now" badge.

## Rules

1. `hours` is a list of segments separated by `;`. A segment is `<days> <HH:MM>-<HH:MM>` or `<days> closed`.
2. `<days>` is a single day (`Mon`) or a forward range (`Mon-Fri`, `Sat-Sun`). Day names are the 3-letter English names, case-insensitive. A backwards range such as `Sat-Mon` is invalid.
3. Start is **inclusive**, end is **exclusive**: `08:00-17:00` is open at 08:00, closed at 17:00.
4. `24:00` is allowed as an **end** time and means midnight at the end of that day.
5. If the end is earlier than the start, the interval **crosses midnight**: `Fri 20:00-02:00` is open from Friday 20:00 to Saturday 02:00.
6. Several segments may mention the same day; their hours add up. `closed` removes any hours given **earlier** for those days.
7. Days that are never mentioned are closed.
8. Extra spaces are fine. Anything else that does not follow the rules raises `ValueError` (unknown day, invalid time like `25:00`, start equal to end, empty `hours`).

## Run the tests

```bash
cd scenarios/s7-career-and-interview/challenge
python3 -m unittest test_opening_hours -v
```

At the start all 14 tests fail with `NotImplementedError`. The challenge is done when they all pass **and you can explain your solution without Bob**.
