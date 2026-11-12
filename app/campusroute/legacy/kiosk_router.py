"""Legacy kiosk router (v0.3, 2023 hackathon prototype).

Inherited from the information-kiosk team. It still powers the offline
"print my route" export on the lobby kiosks, so it ships with the app but is
NOT used by the web API. Do not modify: BACKLOG item CR-9 tracks replacing it
with campusroute.routing.

Run it: python3 -m campusroute.legacy.kiosk_router
"""
import heapq
import itertools
import sys
from collections import deque


class _N:
    __slots__ = ("k", "v", "p", "n")

    def __init__(self, k=None, v=None):
        self.k = k
        self.v = v
        self.p = None
        self.n = None


class LRU:
    def __init__(self, cap):
        if cap < 1:
            raise ValueError("cap")
        self.cap = cap
        self.m = {}
        self.h = _N()
        self.t = _N()
        self.h.n = self.t
        self.t.p = self.h
        self.hit = 0
        self.miss = 0

    def _unlink(self, x):
        x.p.n = x.n
        x.n.p = x.p

    def _front(self, x):
        x.n = self.h.n
        x.p = self.h
        self.h.n.p = x
        self.h.n = x

    def get(self, k, d=None):
        x = self.m.get(k)
        if x is None:
            self.miss += 1
            return d
        self.hit += 1
        self._unlink(x)
        self._front(x)
        return x.v

    def put(self, k, v):
        x = self.m.get(k)
        if x is not None:
            x.v = v
            self._unlink(x)
            self._front(x)
            return None
        out = None
        if len(self.m) >= self.cap:
            z = self.t.p
            self._unlink(z)
            del self.m[z.k]
            out = z.k
        x = _N(k, v)
        self.m[k] = x
        self._front(x)
        return out

    def clear(self):
        self.m.clear()
        self.h.n = self.t
        self.t.p = self.h

    def keys(self):
        r = []
        x = self.h.n
        while x is not self.t:
            r.append(x.k)
            x = x.n
        return r

    def __len__(self):
        return len(self.m)

    def ratio(self):
        t = self.hit + self.miss
        return self.hit / t if t else 0.0


class G:
    def __init__(self, directed=False):
        self.a = {}
        self.y = directed
        self.s = 0

    def add(self, u, v, w=1.0):
        if w < 0:
            raise ValueError("w")
        self.a.setdefault(u, {})
        self.a.setdefault(v, {})
        if v not in self.a[u]:
            self.s += 1
        self.a[u][v] = w
        if not self.y:
            self.a[v][u] = w
        return self

    def remove(self, u, v):
        if u in self.a and v in self.a[u]:
            del self.a[u][v]
            self.s -= 1
            if not self.y and u in self.a[v]:
                del self.a[v][u]
            return True
        return False

    def nbrs(self, u):
        return self.a.get(u, {}).items()

    def nodes(self):
        return list(self.a)

    def deg(self, u):
        return len(self.a.get(u, ()))

    def comps(self):
        g = set()
        r = []
        for b in self.a:
            if b in g:
                continue
            c = []
            q = deque([b])
            g.add(b)
            while q:
                u = q.popleft()
                c.append(u)
                for v, _ in self.nbrs(u):
                    if v not in g:
                        g.add(v)
                        q.append(v)
            r.append(sorted(c, key=str))
        return r


def dijkstra(g, s, goal=None):
    d = {s: 0.0}
    prev = {}
    cnt = itertools.count()
    h = [(0.0, next(cnt), s)]
    done = set()
    while h:
        c, _, u = heapq.heappop(h)
        if u in done:
            continue
        done.add(u)
        if u == goal:
            break
        for v, w in g.nbrs(u):
            nc = c + w
            if nc < d.get(v, float("inf")):
                d[v] = nc
                prev[v] = u
                heapq.heappush(h, (nc, next(cnt), v))
    return d, prev


def build_path(prev, s, t):
    if s == t:
        return [s]
    if t not in prev:
        return None
    r = [t]
    while r[-1] != s:
        r.append(prev[r[-1]])
    r.reverse()
    return r


def astar(g, s, t, h):
    cnt = itertools.count()
    f = [(h(s, t), next(cnt), 0.0, s)]
    prev = {}
    best = {s: 0.0}
    closed = set()
    while f:
        _, _, c, u = heapq.heappop(f)
        if u == t:
            return c, build_path(prev, s, t)
        if u in closed:
            continue
        closed.add(u)
        for v, w in g.nbrs(u):
            nc = c + w
            if nc < best.get(v, float("inf")):
                best[v] = nc
                prev[v] = u
                heapq.heappush(f, (nc + h(v, t), next(cnt), nc, v))
    return float("inf"), None


class Router:
    def __init__(self, g, cap=8):
        self.g = g
        self.c = LRU(cap)
        self.ver = 0

    def _key(self, s, t):
        return (self.ver, s, t)

    def shortest(self, s, t):
        if s not in self.g.a or t not in self.g.a:
            return float("inf"), None
        k = self._key(s, t)
        z = self.c.get(k)
        if z is not None:
            return z
        d, prev = dijkstra(self.g, s, t)
        if t not in d:
            z = (float("inf"), None)
        else:
            z = (d[t], build_path(prev, s, t))
        self.c.put(k, z)
        return z

    def update(self, u, v, w=None):
        if w is None:
            self.g.remove(u, v)
        else:
            self.g.add(u, v, w)
        self.ver += 1
        self.c.clear()

    def batch(self, pairs):
        return [self.shortest(s, t) for s, t in pairs]

    def center(self):
        best = None
        for u in self.g.nodes():
            d, _ = dijkstra(self.g, u)
            if len(d) != len(self.g.a):
                continue
            e = max(d.values())
            if best is None or e < best[0] or (e == best[0] and str(u) < str(best[1])):
                best = (e, u)
        return best


def grid_graph(lines):
    g = G()
    cells = {}
    for i, s in enumerate(lines):
        for j, c in enumerate(s):
            if c == "#":
                continue
            cells[(i, j)] = c
    for (i, j), c in cells.items():
        for di, dj in ((1, 0), (0, 1)):
            q = (i + di, j + dj)
            if q in cells:
                m = 1.0
                if cells[q] == "~":
                    m = 3.0
                g.add((i, j), q, m)
    st = end = None
    for k, c in cells.items():
        if c == "S":
            st = k
        elif c == "E":
            end = k
    return g, st, end


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def draw(lines, path):
    on = set(path or ())
    out = []
    for i, s in enumerate(lines):
        row = []
        for j, c in enumerate(s):
            if (i, j) in on and c not in "SE":
                row.append("*")
            else:
                row.append(c)
        out.append("".join(row))
    return "\n".join(out)


def sample_city():
    g = G()
    E = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("D", "F", 6),
        ("E", "F", 3), ("G", "H", 1),
    ]
    for u, v, w in E:
        g.add(u, v, w)
    return g


def run():
    g = sample_city()
    r = Router(g, cap=3)
    for s, t in [("A", "F"), ("A", "E"), ("A", "F"), ("B", "F"), ("A", "G")]:
        c, y = r.shortest(s, t)
        print(s, t, c, y)
    print("cache", r.c.keys(), round(r.c.ratio(), 2))
    r.update("C", "D", 1)
    print("after", r.shortest("A", "F"))
    print("comps", g.comps())
    print("center", Router(sample_city()).center())

    grid = [
        "S..#....",
        ".#.#.##.",
        ".#...#..",
        ".####.~.",
        "......~E",
    ]
    gg, b, e = grid_graph(grid)
    c1, p1 = astar(gg, b, e, manhattan)
    d, prev = dijkstra(gg, b, e)
    print("grid", c1, d[e], len(p1))
    print(draw(grid, p1))


if __name__ == "__main__":
    sys.exit(run())
