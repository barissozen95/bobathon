# RouteQL v1: language specification

RouteQL is a tiny scripting language for CampusRoute kiosks (backlog item **CR-18**). A kiosk operator writes a `.rql` file; the interpreter prints routes and search results using the real CampusRoute engine in `app/campusroute`.

## Example

```
# Getting to my first lecture
let home = "North Dormitory"
route home to "ENG-B204"
find "cafe"
```

## Lexical rules

| Token | Rule |
|---|---|
| Comment | `#` to end of line, ignored. A `#` inside a string is part of the string |
| String | `"` ... `"` on one line. No escape sequences. An unclosed string is a syntax error |
| Identifier | `[A-Za-z_][A-Za-z0-9_]*`, case-sensitive |
| Keywords | `let route to via avoid stairs find print` (lowercase only; cannot be used as variable names) |
| Symbols | `=` and `,` |
| Whitespace | spaces and tabs separate tokens. **One statement per line.** Blank lines are allowed |

## Grammar (EBNF)

```
program   = { line } ;
line      = [ statement ] [ comment ] NEWLINE ;
statement = let | route | find | print ;
let       = "let" IDENT "=" STRING ;
route     = "route" place "to" place [ "via" place { "," place } ] [ "avoid" "stairs" ] ;
find      = "find" STRING ;
print     = "print" ( STRING | IDENT ) ;
place     = STRING | IDENT ;
```

## Semantics

1. **Parse first, then run.** The whole file is parsed before anything executes. A syntax error anywhere means *no output at all*, only the error.
2. `let x = "..."` stores the string. Re-assigning a variable is allowed.
3. A `place` is resolved with `Campus.resolve()` from `app/campusroute/campus.py` (place id, name, alias or room code; case- and accent-insensitive). Fuzzy matches are **not** accepted.
4. `route A to B [via C, D] [avoid stairs]` calls `routing.shortest_route()` and prints:
   ```
   <start name> -> <goal name>: <meters> m, <minutes> min
     <name> > <name> > ... > <name>
   ```
   If the route uses stairs, append ` (stairs)` to the first line.
5. `find "text"` calls `search.search(campus, text, limit=3)` and prints `find "text":` followed by one line per hit, `  - <label>`, or `  (no matches)`.
6. `print` writes the string, or the value of the variable, on its own line.
7. Runtime errors stop the program. Output already printed stays.

## Errors

Every error is printed to **standard error** as one line and the interpreter exits with status **1**:

```
Error on line <N>: <message>
```

| Situation | Message (must contain) |
|---|---|
| Unclosed string | `unterminated string` |
| Unexpected token / missing keyword | `syntax error` |
| Variable used before `let` | `undefined variable '<name>'` |
| Place cannot be resolved | the `UnknownPlaceError` message, e.g. `unknown place 'libary' (did you mean: Central Library?)` |
| No path | the `NoRouteError` message |

Line numbers are 1-based and count every physical line, including comments and blank lines.

## Command line

```
python3 scenarios/s3-build-a-language/out/routeql.py <file.rql>
```

Exit status: 0 on success, 1 on any RouteQL error, 2 for usage errors (missing file argument, file not found).

## Hard constraints

- Python 3.9+, standard library only, plus `import campusroute` from `app/` (add it to `sys.path` relative to the script's own location).
- **No `eval`, `exec`, `compile`, `os.system`, `subprocess`.** RouteQL text is data, never Python code.
- No network access, no file writes. The interpreter only reads the `.rql` file it was given.
- Do not add language features that are not in this spec.
