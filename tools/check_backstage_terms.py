#!/usr/bin/env python3
"""Reject Processo thread-figure labels that expose internal exam/pipeline metadata."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "courses" / "processo-civil-i"
THREAD = re.compile(
    r"<!--\s*(processo-thread-[^:]+):start\s*-->(.*?)<!--\s*\1:end\s*-->",
    re.IGNORECASE | re.DOTALL,
)
BACKSTAGE = {
    "exam bank/version": re.compile(
        r"\bP1\s+2018/2\b"
        r"|\bvers(?:ão|ões)\s+identificada(?:s)?\s+por\s+ato\b"
        r"|\bV1\s+e\s+V2\s+são\s+variantes\s+do\s+exame\b"
        r"|\bdatas\s+de\s+serviço\s+permanecem\s+vinculadas\s+à\s+versão\s+que\s+as\s+registra\b"
        r"|\bP[12]\s*[·•]\s*V\d+\s*[·•]\s*Q\d+\b",
        re.IGNORECASE,
    ),
    "pipeline layer": re.compile(r"\bCAMADA\s+ANALÍTICA\b", re.IGNORECASE),
    "internal registry number": re.compile(r"\bREGISTRO\s*[·•]\s*\d+\b", re.IGNORECASE),
    "course position number": re.compile(r"\bPOSIÇÃO\s+\d+\b", re.IGNORECASE),
}


def main() -> int:
    failures = 0
    for page in sorted(COURSE.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for match in THREAD.finditer(text):
            thread_id, block = match.groups()
            for label, pattern in BACKSTAGE.items():
                for hit in pattern.finditer(block):
                    line = text.count("\n", 0, match.start()) + 1
                    print(f"FAIL {page.relative_to(ROOT)}:{line} [{thread_id}] {label}: {hit.group(0)}")
                    failures += 1
    if failures:
        print(f"backstage-terms: FAIL ({failures} label(s) across thread figures)")
        return 1
    print("backstage-terms: PASS (all Processo thread figures are clear)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
