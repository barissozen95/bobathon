# CS201 Lab 4: Shortest paths on the CampusRoute mini graph

**Course:** CS201 Data Structures (Meridian University) · **Weight:** 5% · **Format:** one Markdown file with code + report

## Task

Implement:

```python
def shortest_path(graph, start, goal):
    """graph: dict of dicts, graph[u][v] = walking distance in meters (> 0), undirected.
    Returns (distance, path) where path is a list of nodes from start to goal."""
```

Required behavior:

1. Returns the path with the **smallest total distance** (weights matter, not the number of hops).
2. `start == goal` returns `(0, [start])`.
3. If `goal` is unreachable, return `(math.inf, [])`. Do not crash.
4. If `start` or `goal` is not in the graph, raise `ValueError`.
5. You may assume all weights are positive. State this assumption in your report.

Use this graph for your examples (a simplified piece of the CampusRoute map):

```python
MINI = {
    "dorm": {"lib": 190, "north": 230, "sci": 700},
    "lib":  {"dorm": 190, "north": 160, "quad": 150},
    "north": {"dorm": 230, "lib": 160, "engA": 200},
    "quad": {"lib": 150, "engA": 230, "sci": 160},
    "engA": {"north": 200, "quad": 230, "engB": 150},
    "engB": {"engA": 150},
    "sci":  {"quad": 160, "dorm": 700},
    "pool": {},
}
# expected: shortest_path(MINI, "dorm", "engB") == (580, ["dorm", "north", "engA", "engB"])
# expected: shortest_path(MINI, "dorm", "sci")  == (500, ["dorm", "lib", "quad", "sci"])   # NOT the direct 700 m path
```

## Deliverables (in one Markdown file)

1. **Code**: your `shortest_path` function.
2. **Tests**: at least 4 `unittest` tests, including the edge cases above.
3. **Complexity**: time and space complexity, with a one-paragraph justification.
4. **Reflection**: 3-5 sentences: what was hard, what you would improve.
