#!/usr/bin/env python3
"""List colored inline SVG text on changed lesson pages and reject structural marks.

Meaning colors may mark a demonstrated result or a procedural limit. They do not
style article numbers, dates, step numbers, or headings. This checker is scoped to
lesson pages changed against the PR base so legacy pages can be corrected as touched.
"""
from __future__ import annotations

from html.parser import HTMLParser
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LESSON_PATH = re.compile(
    r"^courses/[^/]+/(?:aula|unidade|suplemento|revisao)[^/]*\.html$",
    re.IGNORECASE,
)
NEUTRAL_FILLS = {
    "none", "currentcolor", "inherit", "transparent",
    "var(--ink)", "var(--ink-2)", "var(--muted)", "var(--paper)",
    "var(--paper-2)", "var(--grid)", "var(--grid-major)",
}
ARTICLE = re.compile(
    r"\b(?:art(?:igo|igos)?|arts?)\s*\.?\s*\d+[A-Za-zºª]?\b"
    r"|^\s*\d{3,4}\s*[·•]\s*[^\d\s]",
    re.IGNORECASE,
)
DATE = re.compile(
    r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b"
    r"|\b\d{1,2}\s+(?:de\s+)?(?:jan(?:eiro)?|fev(?:ereiro)?|mar(?:ço)?|"
    r"abr(?:il)?|mai(?:o)?|jun(?:ho)?|jul(?:ho)?|ago(?:sto)?|set(?:embro)?|"
    r"out(?:ubro)?|nov(?:embro)?|dez(?:embro)?)\.?\s*(?:de\s+)?\d{4}\b"
    r"|\b(?:jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)\.?/\d{4}\b"
    r"|^\s*(?:19|20)\d{2}\s*$",
    re.IGNORECASE,
)
STEP = re.compile(
    r"\b(?:passo|etapa|posição|step|stage)\s*(?:n[º.]?\s*)?\d+\b"
    r"|\b\d{1,2}[ºª]?\s+(?:passo|etapa)\b",
    re.IGNORECASE,
)
HEADING_CLASS = re.compile(r"(?:^|\s)(?:hdr|head|heading|header|title|kicker)(?:$|\s)", re.I)
STEP_CLASS = re.compile(
    r"(?:^|\s)(?:passo|etapa|step|stage|n|no|num|number)(?:$|\s)", re.I
)


def style_value(style: str, key: str) -> str | None:
    match = re.search(rf"(?:^|;)\s*{re.escape(key)}\s*:\s*([^;]+)", style, re.I)
    return match.group(1).strip() if match else None


def is_colored(fill: str | None) -> bool:
    if not fill:
        return False
    normalized = re.sub(r"\s+", "", fill).lower()
    return normalized not in NEUTRAL_FILLS


class SVGTextParser(HTMLParser):
    """Collect each colored text run, respecting inherited SVG fill and tspans."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.svg_ids: list[str] = []
        self.stack: list[dict[str, str | None]] = []
        self.foreign_depth = 0
        self.text: dict | None = None
        self.items: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key.lower(): (value or "") for key, value in attrs_list}
        if tag == "svg":
            self.svg_ids.append(attrs.get("id", ""))
        parent_fill = self.stack[-1]["fill"] if self.stack else None
        own_fill = attrs.get("fill") or style_value(attrs.get("style", ""), "fill")
        fill = own_fill or parent_fill
        inherited_classes = self.stack[-1]["classes"] if self.stack else ""
        classes = " ".join(part for part in (inherited_classes, attrs.get("class", "")) if part)
        self.stack.append({"tag": tag, "fill": fill, "classes": classes})
        if tag == "foreignobject":
            self.foreign_depth += 1
        if tag == "text" and self.svg_ids and not self.foreign_depth:
            self.text = {
                "svg": self.svg_ids[-1],
                "line": self.getpos()[0],
                "attrs": attrs,
                "classes": classes,
                "full": [],
                "runs": [],
            }

    def handle_data(self, data: str) -> None:
        if not self.text or self.foreign_depth or not data:
            return
        self.text["full"].append(data)
        fill = self.stack[-1]["fill"] if self.stack else None
        runs = self.text["runs"]
        if runs and runs[-1]["fill"] == fill:
            runs[-1]["parts"].append(data)
        else:
            runs.append({"fill": fill, "parts": [data]})

    def handle_endtag(self, tag: str) -> None:
        if tag == "text" and self.text:
            full_text = " ".join("".join(self.text["full"]).split())
            for run in self.text["runs"]:
                fill = run["fill"]
                text = " ".join("".join(run["parts"]).split())
                if not text or not is_colored(fill):
                    continue
                attrs = self.text["attrs"]
                self.items.append({
                    "svg": self.text["svg"],
                    "line": self.text["line"],
                    "text": text,
                    "full_text": full_text,
                    "fill": fill,
                    "classes": self.text["classes"],
                    "id": attrs.get("id", ""),
                    "role": attrs.get("data-color-role", "").strip().lower(),
                })
            self.text = None
        if tag == "foreignobject" and self.foreign_depth:
            self.foreign_depth -= 1
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break
        if tag == "svg" and self.svg_ids:
            self.svg_ids.pop()


def categories(item: dict[str, object]) -> list[str]:
    text = str(item["text"])
    full_text = str(item["full_text"])
    classes = str(item["classes"])
    ident = str(item["id"])
    found: list[str] = []
    if ARTICLE.search(text) or ARTICLE.search(full_text) or re.fullmatch(r"\d{3}", text):
        found.append("article number")
    if DATE.search(text) or DATE.search(full_text):
        found.append("date")
    if STEP.search(text) or STEP.search(full_text) or (
        re.fullmatch(r"\d{1,2}[ºª]?", text)
        and STEP_CLASS.search(classes + " " + ident)
    ):
        found.append("step number")
    letters = "".join(char for char in text if char.isalpha())
    full_letters = "".join(char for char in full_text if char.isalpha())
    if HEADING_CLASS.search(classes) or HEADING_CLASS.search(ident) or (
        letters and letters == letters.upper()
    ) or (full_letters and full_letters == full_letters.upper()):
        found.append("heading")
    return found


def parse_colored_text(markup: str) -> list[dict[str, object]]:
    parser = SVGTextParser()
    parser.feed(markup)
    parser.close()
    return parser.items


def self_check() -> bool:
    examples = [
        ("Art. 354", "article number"),
        ("15/01/2016", "date"),
        ("nov/2012", "date"),
        ("2016", "date"),
        ("Etapa 3", "step number"),
        ("354 · COM MÉRITO", "heading"),
    ]
    for text, expected in examples:
        markup = f'<svg id="probe"><text style="fill:var(--dif)">{text}</text></svg>'
        items = parse_colored_text(markup)
        if not items or expected not in categories(items[0]):
            print(f"FAIL colored-svg-text self-check: did not recognize {expected}: {text}")
            return False
    return True


def changed_lessons(base: str) -> list[Path] | None:
    try:
        tracked = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        working = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        print(f"FAIL colored-svg-text: cannot compare against base {base!r}: {error}")
        return None
    changed = set(tracked.stdout.splitlines()) | set(working.stdout.splitlines()) | set(untracked.stdout.splitlines())
    paths = []
    for name in sorted(changed):
        if LESSON_PATH.fullmatch(name):
            path = ROOT / name
            if path.is_file():
                paths.append(path)
    return paths


def main() -> int:
    if not self_check():
        return 1
    base = (
        os.environ.get("COURSE_FLOOR_BASE")
        or os.environ.get("PROC_FLOOR_BASE")
        or "origin/codex/processo-r3"
    )
    pages = changed_lessons(base)
    if pages is None:
        return 1
    if not pages:
        print("colored-svg-text: PASS (no changed lesson pages)")
        return 0

    failures = 0
    for page in pages:
        relpath = page.relative_to(ROOT).as_posix()
        parser = SVGTextParser()
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
        colored = parser.items
        print(f"colored SVG text · {relpath}: {len(colored)} item(s)")
        for item in colored:
            print(
                f"  L{item['line']} svg#{item['svg']} fill={item['fill']!r} "
                f"<text> {item['text']!r}"
            )
            role = str(item["role"])
            print(f"  semantic role={role or '(missing)'}")
            hits = categories(item)
            reasons = []
            if role not in {"limit", "decided"}:
                reasons.append("missing or invalid semantic color role")
            if any(hit != "heading" for hit in hits):
                reasons.extend(hit for hit in hits if hit != "heading")
            if reasons:
                print(f"FAIL {relpath}: {', '.join(reasons)} in colored SVG text: {item['text']!r}")
                failures += 1
    if failures:
        print(f"colored-svg-text: FAIL ({failures} prohibited colored text item(s))")
        return 1
    print(f"colored-svg-text: PASS ({len(pages)} changed lesson page(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
