#!/usr/bin/env bash
# IBM Bob · Agentic AI in Action: 30-second machine check.
# Read-only: no network, no installs, writes nothing outside Python's own caches.
# Usage: bash setup-check.sh   (run from the bobathon/ folder)

cd "$(dirname "$0")" || exit 2
GREEN=$'\033[32m'; YELLOW=$'\033[33m'; RED=$'\033[31m'; OFF=$'\033[0m'
red=0; yellow=0
ok()   { printf "  ${GREEN}OK${OFF}    %s\n" "$1"; }
warn() { printf "  ${YELLOW}WARN${OFF}  %s\n" "$1"; yellow=$((yellow+1)); }
fail() { printf "  ${RED}FAIL${OFF}  %s\n" "$1"; red=$((red+1)); }

echo "Bobathon setup check"
echo

# 1. Workspace layout
if [ -f app/campusroute/__init__.py ] && [ -d scenarios ] && [ -f AGENTS.md ]; then
  ok "workspace folder looks right ($(pwd))"
else
  fail "run this from the bobathon/ folder (app/ and scenarios/ not found)"
fi
case "$(pwd)" in *" "*) warn "your path contains spaces; some tools dislike that";; esac

# 2. Python 3.9+
PY=""
for c in python3 python py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then PY="$c"; break; fi
done
if [ -n "$PY" ]; then
  ok "Python $("$PY" -c 'import platform; print(platform.python_version())') ($PY)"
else
  fail "Python 3.9+ not found: needed for scenarios 3, 4 (original tests), 5, 7B and the app"
fi

# 3. App test suite
if [ -n "$PY" ]; then
  if out=$(cd app && "$PY" -m unittest discover -s tests 2>&1); then
    ok "CampusRoute tests: $(printf '%s\n' "$out" | grep -E '^Ran ' )"
  else
    fail "CampusRoute tests failed. Re-extract the package. Last lines:"
    printf '%s\n' "$out" | tail -5 | sed 's/^/        /'
  fi
  if (cd app && "$PY" -m campusroute route "Main Gate" "ENG-B204" >/dev/null 2>&1); then
    ok "CLI works (python3 -m campusroute route ...)"
  else
    fail "CLI did not run"
  fi
fi

# 4. Optional: Node for Scenario 4
if command -v node >/dev/null 2>&1; then
  major=$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null)
  if [ "${major:-0}" -ge 18 ]; then ok "Node $(node --version) (Scenario 4 default target)"
  else warn "Node $(node --version) is older than 18: Scenario 4 should target another language"; fi
else
  warn "Node.js not found: Scenario 4 can target Java/Swift/Go/... instead"
fi

# 5. Optional: Java for Scenario 4 alternative
if javac -version >/dev/null 2>&1; then ok "JDK: $(javac -version 2>&1)"; fi

# 6. Port for the web app
if [ -n "$PY" ]; then
  if "$PY" - <<'PYEOF' 2>/dev/null
import socket, sys
s = socket.socket()
try:
    s.bind(("127.0.0.1", 8000))
except OSError:
    sys.exit(1)
finally:
    s.close()
PYEOF
  then ok "port 8000 free on 127.0.0.1"
  else warn "port 8000 busy: use 'python3 -m campusroute serve --port 8010'"; fi
fi

# 7. Bob config shipped
[ -f .bob/skills/assignment-grader/SKILL.md ] && [ -f .bob/custom_modes.yaml ] \
  && ok "Bob skill + custom mode present (.bob/)" \
  || warn ".bob/ config missing: Scenario 2 fast path unavailable"

echo
if [ $red -gt 0 ]; then echo "${RED}Not ready${OFF}: $red problem(s). Show this to the facilitator."; exit 1
elif [ $yellow -gt 0 ]; then echo "${YELLOW}Ready with warnings${OFF}: read the WARN lines."; exit 0
else echo "${GREEN}Ready.${OFF} Open this folder in Bob and start with GUIDE.md."; exit 0; fi
