#!/bin/sh
# Cheap site-wide checks. Run from anywhere; exits non-zero on any FAIL.
# 1. Fronts are reproducible: regenerating from tools/fronts/data must not change committed courses/*/index.html.
# 2. check_front: macro order, dead/missing lesson links, bibliografia.
# 3. anatomy_check: loose prose, late panels, uncropped kit squares (FLIGHT-LOG F-014..F-016).
cd "$(dirname "$0")/.." || exit 2
slugs=$(python3 - <<'PY'
import json
from pathlib import Path

# `data/` also holds non-course datasets (for example professors.json).
# Only course-front records have the course object schema.
for path in sorted(Path("tools/fronts/data").glob("*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "course" in data:
        print(path.stem)
PY
)
python3 tools/fronts/front.py $slugs >/dev/null && python3 -c "import sys; sys.path.insert(0, 'tools'); import assetver; assetver.run()" >/dev/null || exit 1
fail=0
for s in $slugs; do
  if ! git diff --quiet -- "courses/$s/index.html"; then
    echo "FAIL $s: regenerated front differs from committed (data out of sync with live; see git diff)"; fail=1
  fi
done
python3 tools/fronts/check_front.py $slugs | grep -v '^WARN' || fail=1
python3 tools/fronts/check_register_data.py $slugs | grep FAIL && fail=1
python3 tools/anatomy_check.py | tail -1 | grep -q PASS || { python3 tools/anatomy_check.py | grep -v "^anatomy"; echo "FAIL anatomy (tools/anatomy_check.py)"; fail=1; }
COURSE_FLOOR_BASE=${COURSE_FLOOR_BASE:-origin/codex/processo-r3} python3 tools/check_course_floors.py processo-civil-i || fail=1
python3 tools/proc_polish_verbatim.py . --bank tools/exam-bank/processo-verbatim-reference.json || fail=1
COURSE_FLOOR_BASE=${COURSE_FLOOR_BASE:-${PROC_FLOOR_BASE:-origin/codex/processo-r3}} python3 tools/check_colored_svg_text.py || fail=1
python3 tools/check_backstage_terms.py || fail=1
python3 tools/check_data_does.py || fail=1
python3 tools/svg_breakout_check.py | grep -v PASS || true
python3 tools/svg_breakout_check.py >/dev/null || fail=1
# every shared script parses (backstage-egg.js shipped a bare comment on 15/10 and the home egg died silently)
for f in assets/*.js backstage/*.js; do node --check "$f" 2>/dev/null || { echo "FAIL syntax $f (node --check)"; fail=1; }; done
[ $fail = 0 ] && echo "check_all: PASS" || echo "check_all: FAIL"
exit $fail
