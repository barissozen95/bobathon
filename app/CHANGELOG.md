# Changelog

## 1.4.0
- Crowd levels (`/api/crowd`), recency-weighted, half rounds up.
- `avoid_stairs` and `via` on routes.

## 1.3.0
- Turkish-aware search (`ı/İ/I` fold to `i`, accents removed).
- `Campus.resolve()` stops auto-accepting fuzzy matches (a typo once routed a student to the wrong building).

## 1.2.0
- Schedule CSV: comments, blank lines, real line numbers in errors.

## 1.0.0
- First release: campus map, Dijkstra routes, CLI.
