#!/usr/bin/env python3
"""Reject Processo figure labels that expose backstage terms or describe by colour."""
from pathlib import Path
from html.parser import HTMLParser
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
    "pipeline position arrow": re.compile(r"\bPOSIÇÃO\s+\d+\s*→", re.IGNORECASE),
    "PDF source locator": re.compile(r"\bPDF\s+p\.", re.IGNORECASE),
    "exam-bank answer label": re.compile(r"\bresposta\s+verificada\b", re.IGNORECASE),
}
VISIBLE_PIPELINE = {
    "pipeline layer": BACKSTAGE["pipeline layer"],
    "pipeline position arrow": BACKSTAGE["pipeline position arrow"],
    "PDF source locator": BACKSTAGE["PDF source locator"],
}
FIGCAPTION = re.compile(r"<figcaption\b[^>]*>(.*?)</figcaption\s*>", re.IGNORECASE | re.DOTALL)
COLOR_WORD = re.compile(
    r"\b(?:azul(?:is)?|laranj[ao]s?|vermelh[oa]s?|verd[es]|amarel[oa]s?|rox[oa]s?|"
    r"ros[oa]s?|pret[oa]s?|branc[oa]s?|cinz[ae]s?|marr[oô]m|violet[ao]s?|lil[aá]s)\b",
    re.IGNORECASE,
)


class VisibleTextParser(HTMLParser):
    """Collect rendered text and accessible labels, ignoring hidden source attributes."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, bool, bool]] = []
        self.hidden_depth = 0
        self.skip_depth = 0
        self.parts: list[tuple[str, int]] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {k.lower(): (v or "") for k, v in attrs_list}
        hidden = "hidden" in attrs or attrs.get("aria-hidden", "").lower() == "true"
        skipped = tag.lower() in {"script", "style", "noscript"}
        if hidden:
            self.hidden_depth += 1
        if skipped:
            self.skip_depth += 1
        if self.hidden_depth == 0 and self.skip_depth == 0 and attrs.get("aria-label"):
            self.parts.append((attrs["aria-label"], self.getpos()[0]))
        if tag.lower() not in self.VOID:
            self.stack.append((tag.lower(), hidden, skipped))

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, hidden, skipped = self.stack[i]
                del self.stack[i:]
                if hidden:
                    self.hidden_depth = max(0, self.hidden_depth - 1)
                if skipped:
                    self.skip_depth = max(0, self.skip_depth - 1)
                break

    def handle_data(self, data: str) -> None:
        if data.strip() and not self.hidden_depth and not self.skip_depth:
            self.parts.append((data, self.getpos()[0]))


def visible_parts(markup: str) -> list[tuple[str, int]]:
    parser = VisibleTextParser()
    parser.feed(markup)
    parser.close()
    return parser.parts


def main() -> int:
    failures = 0
    for page in sorted(COURSE.glob("*.html")):
        text = page.read_text(encoding="utf-8")
        for caption in FIGCAPTION.finditer(text):
            visible = re.sub(r"<[^>]+>", " ", caption.group(1))
            visible = re.sub(r"&(?:nbsp|amp|lt|gt|quot|#\d+|#x[0-9a-f]+);", " ", visible, flags=re.IGNORECASE)
            for hit in COLOR_WORD.finditer(visible):
                line = text.count("\n", 0, caption.start()) + 1
                print(f"FAIL {page.relative_to(ROOT)}:{line} [figcaption] colour word: {hit.group(0)}")
                failures += 1
        for match in THREAD.finditer(text):
            thread_id, block = match.groups()
            for visible, _ in visible_parts(block):
                for label, pattern in BACKSTAGE.items():
                    for hit in pattern.finditer(visible):
                        line = text.count("\n", 0, match.start()) + 1
                        print(f"FAIL {page.relative_to(ROOT)}:{line} [{thread_id}] {label}: {hit.group(0)}")
                        failures += 1
        for visible, line in visible_parts(text):
            patterns = dict(VISIBLE_PIPELINE)
            if page.name == "aula-03.html":
                patterns["exam-bank answer label"] = BACKSTAGE["exam-bank answer label"]
            for label, pattern in patterns.items():
                for hit in pattern.finditer(visible):
                    print(f"FAIL {page.relative_to(ROOT)}:{line} [visible text] {label}: {hit.group(0)}")
                    failures += 1
    if failures:
        print(f"backstage-terms: FAIL ({failures} label(s) in captions or thread figures)")
        return 1
    print("backstage-terms: PASS (all Processo captions and thread figures are clear)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
