#!/usr/bin/env python3
"""Expand figure parts in a lesson.json before rendering.

usage: python3 -m tools.figkit.parts.expand IN.json OUT.json
       then: python3 tools/lesson_renderer.py --input OUT.json --output PAGE.html --check-classes
"""
from __future__ import annotations

import json
import sys

from . import expand_block


def main(a: list[str]) -> int:
    if len(a) != 2:
        print(__doc__)
        return 2
    data = json.loads(open(a[0], encoding="utf-8").read())
    n = 0
    for i, b in enumerate(data.get("blocks", [])):
        if b.get("type") == "figure" and "part" in b:
            data["blocks"][i] = expand_block(b)
            n += 1
    open(a[1], "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"expanded {n} part(s) -> {a[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
