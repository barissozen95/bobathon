# CampusRoute architecture

```mermaid
flowchart LR
    subgraph data["data/ (synthetic)"]
        CJ[campus.json]
        SC[schedule.sample.csv]
        CR[crowd.sample.json]
    end
    CJ --> campus["campus.py<br/>load + validate"]
    campus --> search["search.py<br/>normalize + fuzzy"]
    campus --> routing["routing.py<br/>Dijkstra"]
    SC --> schedule["schedule.py<br/>parse + next class"]
    CR --> occupancy["occupancy.py<br/>crowd level"]
    search --> api["api.py<br/>JSON on 127.0.0.1"]
    routing --> api
    schedule --> api
    occupancy --> api
    api --> web["web/<br/>index.html + app.js"]
    routing --> cli["cli.py"]
    search --> cli
    schedule --> cli
    legacy["legacy/kiosk_router.py<br/>(not wired in)"]:::old
    classDef old fill:#eee,stroke:#999,stroke-dasharray: 4 4
```

## Key decisions

1. **Standard library only.** The app must run on any lab machine with Python 3.9+, no `pip install`.
2. **Pure core, thin edges.** `schedule`, `routing`, `occupancy` never read the clock or the network. The API injects `now` (`clock=` parameter), which keeps tests deterministic.
3. **Graph = undirected walkways.** Each edge has `meters`, `stairs`, `covered`. `avoid_stairs` filters edges, it does not add a penalty.
4. **Resolve strictly, suggest fuzzily.** `Campus.resolve()` only accepts exact id/name/alias/room code (after normalization). Fuzzy matches are shown as suggestions, never silently used, so a typo cannot route you to the wrong building.
5. **Walking time** = `ceil(meters / 80)` minutes. It is an estimate.

## Data model

```mermaid
classDiagram
    class Campus { places; rooms; edges; resolve(query); neighbors(id, avoid_stairs) }
    class Place { id; name; kind; x; y; aliases; hours }
    class Edge { a; b; meters; stairs; covered }
    class Room { code; place; floor; label }
    Campus "1" --> "*" Place
    Campus "1" --> "*" Edge
    Campus "1" --> "*" Room
    Room --> Place : located in
```
