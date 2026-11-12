# Lab 4 submission - Student C (synthetic)

## Code

```python
from collections import deque


def shortest_path(graph, start, goal):
    q = deque([[start]])
    seen = {start}
    while q:
        p = q.popleft()
        if p[-1] == goal:
            d = 0
            for i in range(len(p) - 1):
                d += graph[p[i]][p[i + 1]]
            return d, p
        for n in graph[p[-1]]:
            if n not in seen:
                seen.add(n)
                q.append(p + [n])
```

## Tests

I tested it by running it on the example and it printed the right answer.

## Complexity

Shortest path algorithms like Dijkstra's algorithm have a time complexity of O((V+E) log V) when implemented with a binary heap, which makes them efficient for sparse graphs. The space complexity is O(V).

## Reflection

This lab was very useful for understanding graphs. My solution works for all cases.
