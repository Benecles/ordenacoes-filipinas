#!/usr/bin/env python3
"""A lesson page may only change through the gate (cable management 14/11).

Every passing gate (workshop run.py --step gate) writes tools/lessons/<lesson>.gate.json with the shell sources it
judged and their fingerprint. This check recomputes the fingerprint; a source edited after its PASS fails check_all.
Same hash as run.py's sources_hash: sha256 over (relative path, NUL, bytes, NUL) in the stamp's order, first 16 hex."""
import hashlib, json, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
bad = 0
stamps = sorted((root / 'tools/lessons').glob('*.gate.json'))
import os
gating = set(filter(None, os.environ.get('GATING_LESSON', '').split(',')))  # the gate runs check_all before it can write its stamp: skip those lessons (a comma list when one machine change touches several, 17/11)
for p in stamps:
    s = json.loads(p.read_text())
    if s['lesson'] in gating:
        continue
    h = hashlib.sha256()
    for rel in s['sources']:
        f = root / rel
        h.update(rel.encode() + b'\0' + (f.read_bytes() if f.exists() else b'') + b'\0')
    if h.hexdigest()[:16] != s['hash']:
        bad += 1
        print(f"FAIL {s['lesson']}: sources changed since its gate PASS (round {s['round']}); rerun the gate and commit the new stamp")
print(f"gate stamps: {'FAIL' if bad else 'PASS'} ({len(stamps)} lesson(s), {bad} changed since PASS)")
sys.exit(1 if bad else 0)
