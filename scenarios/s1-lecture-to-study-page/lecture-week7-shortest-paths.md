# CS201 Data Structures - Week 7 - Shortest Paths
(my notes from the lecture, typed up quickly, sorry for the mess)

prof started with: "how does CampusRoute know the fastest way from the dorm to ENG-B?" -> that's a shortest path problem on a graph

## graphs recap
- graph G = (V, E). V = vertices (nodes), E = edges
- campus: buildings + path junctions = vertices, walkways = edges
- weighted graph: every edge has a weight w(u,v). for us weight = meters
- undirected (you can walk both ways). one-way streets would be directed
- adjacency list = dict of dicts: graph["lib"]["quad"] = 150. memory O(V+E)
- adjacency matrix = V x V table, O(V^2) memory, good only for dense graphs
- campus graph is SPARSE (each building connects to ~3 others) so use adjacency list

## BFS (breadth first search)
- explores level by level using a QUEUE (FIFO)
- gives shortest path in number of EDGES (hops)
- correct for shortest path ONLY if all weights are equal
- O(V + E)
- example he drew: dorm -> lib -> quad -> sci is 3 hops but maybe not fewest meters!!

## Dijkstra's algorithm (1956, published 1959)
- shortest paths from ONE source to all vertices, weighted graph
- idea: "greedy" - always settle the closest not-yet-settled vertex
- uses a PRIORITY QUEUE (min-heap), in python: heapq
- steps:
  1. dist[source] = 0, every other dist = infinity
  2. push (0, source) into heap
  3. pop smallest (d, u). if u already settled -> skip (lazy deletion!)
  4. settle u. for each neighbor v: if d + w(u,v) < dist[v] -> update dist[v], prev[v] = u, push (dist[v], v)
  5. repeat until heap empty (or until goal is settled if you only need one target - early exit)
- rebuild path by following prev[] backwards from goal, then reverse
- complexity with binary heap: O((V + E) log V)
- with plain array instead of heap: O(V^2) - actually fine for small dense graphs
- IMPORTANT: Dijkstra works with negative edge weights as long as there is no negative cycle   <- prof said this is a common exam question
- tie-breaking: python heapq compares tuples, if two distances equal it compares the NEXT element -> can crash if nodes aren't comparable. fix: push (dist, counter, node) with itertools.count()

## A* (A-star)
- Dijkstra + a heuristic h(v) = estimated remaining distance to goal
- priority = g(v) + h(v) where g = distance so far
- h must be ADMISSIBLE (never overestimates) -> then A* still finds the optimal path
- on a campus map: straight-line (euclidean) distance between building coordinates is admissible because you can't walk shorter than a straight line
- on a grid with only up/down/left/right moves: manhattan distance |dx| + |dy|
- if h = 0 everywhere, A* = Dijkstra
- usually explores far fewer nodes than Dijkstra when the heuristic is good

## Bellman-Ford (only mentioned, not on the midterm)
- handles negative weights, detects negative cycles
- O(V * E), slower
- relax all edges V-1 times

## comparison table (he put this on the board)
| algorithm | weights | data structure | time |
| BFS | unweighted / equal | queue | O(V+E) |
| Dijkstra | non-negative | min-heap | O((V+E) log V) |
| A* | non-negative + heuristic | min-heap | depends on h, worst case like Dijkstra |
| Bellman-Ford | can be negative | none (loops) | O(VE) |

## real world stuff (CampusRoute)
- "avoid stairs" option = just remove stair edges from the graph and run Dijkstra again. not a new algorithm!
- "via the cafe" = two runs: start->cafe, cafe->goal, glue paths together
- caching: if many students ask the same route, cache (start, goal) -> result. BUT invalidate cache when the map changes (e.g. walkway closed for construction)
- walking time = meters / speed. they use 80 m/min. ceil it so you're not late

## things to review before the midterm
- run Dijkstra BY HAND on the small graph from slide 14 (A-F, answer A->F = 13)
- why does BFS fail on weighted graphs? give a counter example
- what makes a heuristic admissible
- complexity of each, and WHY (heap operations are log V)

homework: Lab 4, implement shortest_path for the mini campus graph (see Lab 4 handout). due next friday
