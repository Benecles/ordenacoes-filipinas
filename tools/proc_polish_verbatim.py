#!/usr/bin/env python3
"""Block changes to Processo exam text by matching rendered items to the exam bank."""

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path


BLOCKS = {"article", "aside", "blockquote", "div", "li", "ol", "p", "section", "ul"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def exact_text(value):
    # Ignore only HTML line wrapping and spacing; preserve words, case, and punctuation.
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


class Node:
    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []

    def has_class(self, name):
        return name in self.attrs.get("class", "").split()

    def all(self, predicate):
        out = []
        for child in self.children:
            if isinstance(child, Node):
                if predicate(child):
                    out.append(child)
                out.extend(child.all(predicate))
        return out

    def text(self):
        parts = []
        for child in self.children:
            if isinstance(child, Node):
                if child.tag in BLOCKS:
                    parts.append(" ")
                parts.append(child.text())
                if child.tag in BLOCKS:
                    parts.append(" ")
            else:
                parts.append(child)
        return exact_text("".join(parts))


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        if tag == "br":
            self.stack[-1].children.append(" ")
            return
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def read_tree(path):
    tree = Tree()
    tree.feed(path.read_text(encoding="utf-8"))
    return tree.root


def all_appearances(bank):
    by_id = {}
    records = []
    for question in bank.get("questions", []):
        appearances = question.get("appearances", [])
        if appearances:
            by_id[question.get("id", "")] = exact_text(appearances[0].get("verbatim_text", ""))
        for appearance in appearances:
            records.append({
                "year": str(appearance.get("year", "")),
                "number": str(appearance.get("question_number", "")),
                "source": exact_text(appearance.get("verbatim_text", "")),
            })
    return by_id, records


def candidates(records, year=None, number=None):
    return [r for r in records if (year is None or r["year"] == str(year)) and
            (number is None or r["number"] == str(number))]


def parse_label(label):
    year = re.search(r"(?:19|20)\d{2}", label)
    number = re.search(r"quest[ãa]o\s*(\d+)|\bq\s*(\d+)\b", label, re.I)
    if not year or not number:
        return None, None
    return year.group(0), next(x for x in number.groups() if x)


def question_id_number(value):
    match = re.search(r"-q(\d+)(?:\([^)]*\))?$", value or "", re.I)
    return match.group(1) if match else None


def options_after_stem(source, stem):
    at = source.find(stem)
    if at < 0:
        return {}
    tail = source[at + len(stem):]
    matches = list(re.finditer(r"(?:^|\s)([a-e])[.)]\s*", tail))
    out = {}
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(tail)
        out[match.group(1).lower()] = exact_text(tail[start:end]).strip(" ;")
    return {k: v for k, v in out.items() if v}


def exact_source_stem(stem, source):
    at = source.find(stem)
    if at < 0:
        return False
    end = at + len(stem)
    following = source[end:end + 1]
    # A stem cannot stop just before punctuation that belongs to the source.
    return not following or following.isspace()


def exact_source_case(case_text, source):
    start = 0
    while case_text:
        at = source.find(case_text, start)
        if at < 0:
            return False
        end = at + len(case_text)
        before = source[at - 1:at]
        after = source[end:end + 1]
        if (not before or before.isspace()) and (not after or after.isspace()):
            return True
        start = at + 1
    return False


def button_label(button, index):
    raw = button.attrs.get("data-opt", "")
    if raw.isdigit():
        return chr(ord("a") + int(raw))
    if raw.lower() in "abcde":
        return raw.lower()
    return chr(ord("a") + index)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("site")
    parser.add_argument("--bank", required=True)
    parser.add_argument("--only", nargs="*", help="limit checks to these Processo HTML filenames")
    args = parser.parse_args()
    bank = json.loads(Path(args.bank).read_text(encoding="utf-8"))
    by_id, records = all_appearances(bank)
    course = Path(args.site) / "courses" / "processo-civil-i"
    errors = 0
    stems = 0
    options = 0
    cases = 0
    authored_cards = 0

    pages = sorted(course.glob("*.html"))
    if args.only:
        wanted = set(args.only)
        pages = [page for page in pages if page.name in wanted]
        missing = wanted - {page.name for page in pages}
        if missing:
            print(f"FAIL missing requested page(s): {', '.join(sorted(missing))}")
            errors += len(missing)
    for page in pages:
        tree = read_tree(page)

        # The review page uses one canonical bank record per exam question.
        for section in tree.all(lambda n: n.has_class("bank-question")):
            prompt = next(iter(section.all(lambda n: n.has_class("pergunta"))), None)
            if not prompt:
                print(f"FAIL {page.name}: {section.attrs.get('id', 'bank-question')} has no .pergunta")
                errors += 1
                continue
            item_id = section.attrs.get("id", "")
            current = prompt.text()
            stems += 1
            options += len(re.findall(r"(?:^|\s)[a-e][.)]\s", current))
            if item_id not in by_id or current != by_id.get(item_id):
                print(f"FAIL {page.name} #{item_id}: exam text differs from verbatim_text")
                errors += 1

        # Explicit exam blocks are checked as complete question-and-option text.
        for exam in tree.all(lambda n: n.tag == "div" and n.has_class("exam")):
            paragraphs = exam.all(lambda n: n.tag == "p")
            li_count = len(exam.all(lambda n: n.tag == "li"))
            if not paragraphs:
                print(f"FAIL {page.name}: div.exam has no stem paragraph")
                errors += 1
                continue
            current_stem = re.sub(r"^\s*\d+\.\s*", "", paragraphs[0].text())
            number_match = re.match(r"\s*(\d+)\.\s*", paragraphs[0].text())
            number = number_match.group(1) if number_match else None
            current_options = [node.text() for node in exam.all(lambda n: n.tag == "li")]
            matched = []
            for record in candidates(records, None, number):
                if not exact_source_stem(current_stem, record["source"]):
                    continue
                expected = options_after_stem(record["source"], current_stem)
                if len(expected) != len(current_options):
                    continue
                if all(expected.get(chr(ord("a") + i)) == value for i, value in enumerate(current_options)):
                    matched.append(record)
            stems += 1
            options += li_count
            if not matched:
                print(f"FAIL {page.name}: div.exam text differs from the bank")
                errors += 1

        # Exam-sourced bet cards are identified by their year and question label.
        for bet in tree.all(lambda n: n.has_class("bet")):
            label = next(iter(bet.all(lambda n: n.has_class("bet-k"))), None)
            if not label:
                continue
            year, number = parse_label(label.text())
            if not year or not number:
                continue
            source_records = candidates(records, year, number)
            if not source_records:
                print(f"FAIL {page.name}: no bank item for exam {year}, question {number}")
                errors += 1
                continue
            qnode = next(iter(bet.all(lambda n: n.has_class("bet-q"))), None)
            if not qnode:
                continue
            qsource = next(iter(qnode.all(lambda n: n.has_class("bet-q-source"))), None)
            # Cards without a source marker are authored practice prompts, not exam quotations.
            if not qsource:
                authored_cards += 1
                continue
            stem = qsource.text()
            matched = [r for r in source_records if exact_source_stem(stem, r["source"])]
            # A source marker can also wrap an authored prompt; only exact bank text is exam text.
            if not matched:
                authored_cards += 1
                continue
            stems += 1
            if qnode.text() != stem:
                print(f"FAIL {page.name}: exam .bet-q differs from exam {year}, question {number}")
                errors += 1

            opt_box = next(iter(bet.all(lambda n: n.has_class("bet-opts"))), None)
            buttons = opt_box.all(lambda n: n.tag == "button") if opt_box else []
            option_matches = []
            has_expected_options = any(options_after_stem(r["source"], stem) for r in matched)
            actual_options = []
            for i, btn in enumerate(buttons):
                label = button_label(btn, i)
                value = re.sub(rf"^{label}[.)]\s*", "", btn.text())
                actual_options.append((label, value))
            if has_expected_options:
                options += len(actual_options)
            for record in matched:
                expected = options_after_stem(record["source"], stem)
                if not expected:
                    continue
                if len(actual_options) == len(expected) and all(expected.get(k) == value for k, value in actual_options):
                    option_matches.append(True)
            if has_expected_options and not option_matches:
                print(f"FAIL {page.name}: exam .bet-opts differ from exam {year}, question {number}")
                errors += 1

            case = next(iter(bet.all(lambda n: n.has_class("bet-case"))), None)
            case_label = next(iter(case.all(lambda n: n.has_class("bet-case-label"))), None) if case else None
            case_text = next(iter(case.all(lambda n: n.has_class("bet-case-text"))), None) if case else None
            if case and case_label and case_text and re.search(r"(?:prova|avalia[çc][ãa]o)", case_label.text(), re.I):
                cases += 1
                if not any(exact_source_case(case_text.text(), r["source"]) for r in matched):
                    print(f"FAIL {page.name}: exam .bet-case differs from exam {year}, question {number}")
                    errors += 1

    checked = stems + options + cases
    print(f"{checked} exam items checked (stems {stems}, options {options}, cases {cases}); {errors} mismatch(es); {authored_cards} authored cards excluded")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
