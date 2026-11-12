# Lab 4 submission - Student A (synthetic)

## Code

```python
import heapq
import itertools
import math


def shortest_path(graph, start, goal):
    """Dijkstra's algorithm on a dict-of-dicts graph with positive weights.

    Returns (distance, path). Unreachable goal -> (math.inf, []).
    Raises ValueError if start or goal is not a node of the graph.
    """
    if start not in graph or goal not in graph:
        raise ValueError("unknown node: %r" % (start if start not in graph else goal))
    dist = {start: 0}
    prev = {}
    counter = itertools.count()          # tie-breaker so nodes are never compared
    heap = [(0, next(counter), start)]
    settled = set()
    while heap:
        d, _, node = heapq.heappop(heap)
        if node in settled:
            continue                     # stale heap entry (lazy deletion)
        settled.add(node)
        if node == goal:
            break
        for neighbor, weight in graph[node].items():
            candidate = d + weight
            if candidate < dist.get(neighbor, math.inf):
                dist[neighbor] = candidate
                prev[neighbor] = node
                heapq.heappush(heap, (candidate, next(counter), neighbor))
    if goal not in settled:
        return math.inf, []
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return dist[goal], path
```

## Tests

```python
import math
import unittest

from lab4 import MINI, shortest_path


class ShortestPathTest(unittest.TestCase):
    def test_example_route(self):
        self.assertEqual(shortest_path(MINI, "dorm", "engB"), (580, ["dorm", "north", "engA", "engB"]))

    def test_weights_beat_hop_count(self):
        # the direct dorm-sci edge is 1 hop but 700 m
        self.assertEqual(shortest_path(MINI, "dorm", "sci"), (500, ["dorm", "lib", "quad", "sci"]))

    def test_same_node(self):
        self.assertEqual(shortest_path(MINI, "lib", "lib"), (0, ["lib"]))

    def test_unreachable(self):
        self.assertEqual(shortest_path(MINI, "dorm", "pool"), (math.inf, []))

    def test_unknown_node(self):
        with self.assertRaises(ValueError):
            shortest_path(MINI, "dorm", "mars")

    def test_symmetric_distance(self):
        self.assertEqual(shortest_path(MINI, "sci", "engB")[0], shortest_path(MINI, "engB", "sci")[0])
```

## Complexity

With a binary heap, every edge can push at most one entry, so the heap holds O(E) entries and each push/pop costs O(log E) = O(log V) (because E <= V^2). Total time is **O((V + E) log V)**. Space is **O(V + E)**: `dist`, `prev` and `settled` are O(V), the heap is O(E) because of lazy deletion. The early exit at the goal does not change the worst case.

## Reflection

The hardest part was the tie-breaker: my first version pushed `(d, node)` and it worked only because the node names are strings. I added `itertools.count()` after reading why heapq compares the second element. I assumed all weights are positive, as the handout allows; with negative weights Dijkstra can settle a node too early, so Bellman-Ford would be needed. Next time I would also return the list of steps with distances, like the CampusRoute directions.
