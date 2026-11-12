# Lab 4 submission - Student B (synthetic)

## Code

```python
import math


def shortest_path(graph, start, goal):
    # dijkstra
    dist = {}
    prev = {}
    for n in graph:
        dist[n] = math.inf
    dist[start] = 0
    unvisited = list(graph.keys())
    while unvisited:
        # find the closest unvisited node
        u = unvisited[0]
        for n in unvisited:
            if dist[n] < dist[u]:
                u = n
        unvisited.remove(u)
        if u == goal:
            break
        for v in graph[u]:
            alt = dist[u] + graph[u][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    path = []
    x = goal
    while x != start:
        path.insert(0, x)
        x = prev[x]
    path.insert(0, start)
    return dist[goal], path
```

## Tests

```python
import unittest
from lab4 import MINI, shortest_path


class T(unittest.TestCase):
    def test1(self):
        self.assertEqual(shortest_path(MINI, "dorm", "engB"), (580, ["dorm", "north", "engA", "engB"]))

    def test2(self):
        self.assertEqual(shortest_path(MINI, "lib", "lib"), (0, ["lib"]))
```

## Complexity

Dijkstra is O(n log n) because it uses a priority queue. Space is O(n).

## Reflection

It works on the example from the handout. I did not have time to test unreachable nodes. I think my code is fine but the variable names could be better.
