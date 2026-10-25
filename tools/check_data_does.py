#!/usr/bin/env python3
"""Require reader-action labels on every Processo lesson figure."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

COURSE = Path(__file__).resolve().parents[1] / "courses" / "processo-civil-i"
BANNED = {"ilustra", "mostra", "resume", "apresenta"}
FAIL_REASONS = {"restates the text", "record card", "words in a shape", "ornament"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
INFINITIVE = re.compile(r"^[a-zà-ÿ]+(?:-(?:se|me|te))?$", re.I)


class Figures(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.items = []

    def handle_starttag(self, tag, attrs):
        attr_pairs = [(key.lower(), value or "") for key, value in attrs]
        values = dict(attr_pairs)
        in_figure = "figure" in self.stack
        in_form = "form" in self.stack
        if tag == "figure":
            self.items.append((tag, values.get("id", ""), attr_pairs))
        elif tag == "form" and not in_figure:
            self.items.append((tag, values.get("id", ""), attr_pairs))
        elif tag == "svg" and not in_figure and not in_form:
            classes = set(values.get("class", "").split())
            if "figkit" in classes or "data-family" in values:
                self.items.append((tag, values.get("id", values.get("class", "svg")), attr_pairs))
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                del self.stack[i:]
                break


def valid(value):
    fields = [field.strip() for field in value.split(" · ")]
    if len(value.split()) > 25:
        return False, "over 25 words"
    if not fields or fields[0].lower() in BANNED:
        return False, "banned or missing verb"
    if fields[0].lower() == "falha":
        if len(fields) == 2 and fields[1] in FAIL_REASONS:
            return True, ""
        return False, "invalid falha reason"
    if len(fields) != 3 or not all(fields):
        return False, "expected verb · object · question"
    verb = fields[0].lower()
    if not INFINITIVE.fullmatch(verb) or not verb.endswith(("ar", "er", "ir")):
        return False, "verb must be infinitive"
    if not fields[2].endswith("?"):
        return False, "question must end in ?"
    return True, ""


def main():
    failures = []
    pages = sorted(COURSE.glob("aula-*.html"))
    page_count = 0
    figure_count = 0
    for page in pages:
        parser = Figures()
        parser.feed(page.read_text(encoding="utf-8"))
        if not parser.items:
            continue
        page_count += 1
        figure_count += len(parser.items)
        for tag, ident, attrs in parser.items:
            labels = [value for key, value in attrs if key == "data-does"]
            label = f"{page.name} <{tag}>#{ident or '(no id)'}"
            if len(labels) != 1:
                failures.append(f"{label}: expected one data-does attribute, found {len(labels)}")
                continue
            ok, reason = valid(labels[0])
            if not ok:
                failures.append(f"{label}: {reason}: {labels[0]}")
    if failures:
        print("data-does: FAIL")
        print("\n".join(f"  {failure}" for failure in failures))
        return 1
    print(f"data-does: PASS ({figure_count} labelled figures across {page_count} Processo lessons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
