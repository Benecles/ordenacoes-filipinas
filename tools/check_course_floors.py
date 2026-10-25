#!/usr/bin/env python3
"""Blocking floors for one course: python3 tools/check_course_floors.py COURSE [--base REF].
Prose floors compare visible body prose only, excluding hero/header/nav/register metadata."""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE = None
LESSONS = None
NEGATED = re.compile(r"\bnão\s+(?:se\s+)?(?:prova|provam|transforma|transformam|equivale|equivalem|basta|bastam|garante|garantem|substitui|substituem|encerra|encerram|resolve|resolvem|apaga|apagam|elimina|eliminam|esgota|esgotam|autoriza|autorizam|dispensa|dispensam|decide|decidem|significa|significam|cria|criam|converte|convertem|torna|tornam)\b", re.I)
GAP_TALK = re.compile(r"(?i)\b(?:(?:o|do|no|esse|este)\s+(?:excerto|registro)\b|não\s+(?:informa|declara|nomeia|indica|identifica|aponta|registra|menciona|especifica)\b|não\s+(?:cabe|se\s+deve)\s+(?:acrescentar|supor|inventar|presumir)|sem\s+(?:esse|este)\s+dado\b|(?:o\s+texto|a\s+fonte|o\s+caso)\s+não\s+(?:diz|informa|traz)\b)")
BACKSTAGE = re.compile(
    r"\b(?:(?:os|nos|dos|pelos|segundo os?) slides?|materia(?:l|is) da disciplina|"
    r"nest[ae] leitura|dest[ae] leitura|prática autoral|relatad[oa]s? por|"
    r"localizador(?:es)?|fontes e (?:limites|localizadores)|C\d{1,2}\b|blueprint|cerca desta|"
    r"compêndio|compendio|arquivo-fonte|arquivo fonte|\d+-statute\.txt|"
    r"PDF\s+p(?:á?g(?:ina)?)?\.?\s*\d+|p(?:á?g(?:ina)?)?\.?\s*\d+\s+do PDF)\b", re.I)
TAG_SOUP = re.compile(r"<[a-z]+<")
IMAGE = re.compile(r"\.(?:png|jpe?g)$", re.I)
def figure_family_ids():
    """Read family IDs from the checked-in catalog generated from Dictionary.md."""
    catalog = ROOT / "backstage" / "dictionary.html"
    try:
        source = catalog.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"cannot read dictionary family catalog {catalog}: {exc}") from exc
    section = re.search(r"<section\b[^>]*>\s*<h2>\s*Figures\s*</h2>(.*?)</section>", source, re.I | re.S)
    if not section:
        raise RuntimeError(f"dictionary family catalog has no Figures section: {catalog}")
    families = set(re.findall(r"<li\b[^>]*\bid=[\"'](figure\.[^\"']+)[\"']", section.group(1), re.I))
    if not families:
        raise RuntimeError(f"dictionary family catalog has no figure IDs: {catalog}")
    return families
PROC42_LEDGER = ROOT / "tools" / "processo-4.2-complete.json"
PROC42_REQUIRED = {
    *(f"aula-{n:02d}.html" for n in range(1, 19)),
    "aula-06-citacao.html", "aula-08-revelia.html",
    "aula-10-estabilizacao.html", "aula-11-merito.html",
}


class BodyText(HTMLParser):
    EXCLUDED_TAGS = {"head", "script", "style", "svg", "nav", "header"}
    EXCLUDED_CLASSES = {"hero", "deck", "hero-rule", "titleblock", "label", "register", "registro", "metadata", "meta", "site-header"}
    def __init__(self):
        super().__init__(convert_charrefs=True); self.skip = 0; self.stack = []; self.parts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs); classes = set((attrs.get("class") or "").split())
        excluded = tag in self.EXCLUDED_TAGS or bool(classes & self.EXCLUDED_CLASSES) or (tag == "div" and "hidden" in attrs)
        self.stack.append((tag, excluded))
        if excluded: self.skip += 1
        if not self.skip and tag in {"p", "li", "h1", "h2", "h3", "h4", "td", "th", "br", "div"}: self.parts.append(" ")
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, excluded = self.stack.pop(i)
                if excluded: self.skip -= 1
                break
        if not self.skip and tag in {"p", "li", "h1", "h2", "h3", "h4", "td", "th", "div"}: self.parts.append(" ")
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def visible_text(source):
    parser = BodyText()
    parser.feed(source if isinstance(source, str) else source.read_text(encoding="utf-8", errors="replace"))
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()


class Lesson42Parser(HTMLParser):
    """Read the structural promises in a lesson opening and its staged figures."""
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.bet_count = 0
        self.bet_questions = []
        self.bet_options = 0
        self.hero_families = []
        self.staged_figures_outside = 0
        self.panels_outside = 0
        self.timelines_outside = 0
        self.blocks = []

    def active(self, key):
        return next((entry.get(key) for entry in reversed(self.stack) if entry.get(key)), None)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = set((attrs.get("class") or "").split())
        if "bet" in classes:
            self.bet_count += 1
        if "button" == tag and "data-opt" in attrs and self.active("bet"):
            self.bet_options += 1
        bet_question = [] if "bet-q" in classes else None
        if bet_question is not None:
            self.bet_questions.append(bet_question)

        if tag == "header" and "hero" in classes:
            hero = True
        else:
            hero = False
        if tag == "svg" and (attrs.get("data-family") or "figkit" in classes) and self.active("hero"):   # INSTRUMENT-2: an approved family, not the kit
            self.hero_families.append(attrs.get("data-family", ""))
        if tag == "svg" and attrs.get("data-family") == "figure.timeline" and not self.active("scrolly"):
            self.timelines_outside += 1

        if tag == "figure" and attrs.get("data-staged") == "true" and not self.active("scrolly"):
            self.staged_figures_outside += 1
        if tag == "svg" and "panel" in classes:
            block = self.active("scrolly")
            if block:
                block["panels"].append((attrs.get("id", ""), "on" in classes,
                                         attrs.get("data-family", ""), "figkit" in classes))
            else:
                self.panels_outside += 1
        if "step" in classes:
            block = self.active("scrolly")
            if block:
                block["steps"].append(attrs.get("data-panel", ""))

        scrolly = None
        if "scrolly" in classes:
            scrolly = {"panels": [], "steps": []}
            self.blocks.append(scrolly)
        if tag not in self.VOID:
            self.stack.append({"tag": tag, "classes": classes, "hero": hero,
                               "bet": "bet" in classes, "scrolly": scrolly,
                               "bet_question": bet_question})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                self.stack.pop(i)
                break

    def handle_data(self, data):
        for entry in self.stack:
            if entry.get("bet_question") is not None:
                entry["bet_question"].append(data)


def check_42_page(path):
    """Enforce the CEO's 4.2 opening, family, and staged-panel contract."""
    label = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    source = path.read_text(encoding="utf-8", errors="replace")
    parser = Lesson42Parser()
    parser.feed(source)
    parser.close()
    failed = False
    try:
        figure_families = figure_family_ids()
    except RuntimeError as exc:
        print(f"FAIL 4.2 family catalog {label}: {exc}")
        return True

    bet_match = re.search(r"<[^>]+class=[\"'][^\"']*\bbet\b[^\"']*[\"']", source, re.I)
    first_chapter = re.search(r"<section\b[^>]*class=[\"'][^\"']*\bchapter\b", source, re.I)
    if parser.bet_count < 1 or not parser.bet_questions or not "?" in "".join(parser.bet_questions[0]):
        print(f"FAIL 4.2 bet {label}: opening question is missing or is not a question")
        failed = True
    elif not parser.bet_options or not bet_match or (first_chapter and bet_match.start() > first_chapter.start()):
        print(f"FAIL 4.2 bet {label}: opening question needs answer options before the first section")
        failed = True

    if not any(family in figure_families for family in parser.hero_families):
        print(f"FAIL 4.2 hero {label}: .hero needs an SVG tagged with an approved figure family")
        failed = True
    elif any(family not in figure_families for family in parser.hero_families):
        print(f"FAIL 4.2 hero {label}: .hero contains an unapproved or untagged figkit family")
        failed = True

    if parser.staged_figures_outside:
        print(f"FAIL 4.2 scrolly {label}: {parser.staged_figures_outside} staged figure(s) sit outside .scrolly")
        failed = True
    if parser.panels_outside:
        print(f"FAIL 4.2 scrolly {label}: {parser.panels_outside} panel SVG(s) sit outside .scrolly")
        failed = True
    if parser.timelines_outside:
        print(f"FAIL 4.2 scrolly {label}: {parser.timelines_outside} timeline figure(s) need staged panels")
        failed = True
    for index, block in enumerate(parser.blocks, 1):
        ids = [ident for ident, _, _, _ in block["panels"]]
        references = block["steps"]
        if len(ids) < 2 or len(references) < 2:
            print(f"FAIL 4.2 scrolly {label} block {index}: a staged figure needs at least two panels and steps")
            failed = True
            continue
        if any(not ident for ident in ids) or len(ids) != len(set(ids)):
            print(f"FAIL 4.2 scrolly {label} block {index}: panel ids must be present and unique")
            failed = True
        if sum(1 for _, on, _, _ in block["panels"] if on) != 1:
            print(f"FAIL 4.2 scrolly {label} block {index}: exactly one panel must be visible initially")
            failed = True
        if any(family not in figure_families or not figkit for _, _, family, figkit in block["panels"]):
            print(f"FAIL 4.2 scrolly {label} block {index}: each panel needs figkit and an approved family tag")
            failed = True
        if len(references) != len(ids) or set(references) != set(ids):
            print(f"FAIL 4.2 scrolly {label} block {index}: every stage must name one distinct panel")
            failed = True
    if not failed:
        print(f"PASS 4.2 lesson structure {label}")
    return failed


def check_42(selected, require_all=False, explicit=False):
    if COURSE != "processo-civil-i":
        return False
    try:
        ledger = json.loads(PROC42_LEDGER.read_text(encoding="utf-8"))
        complete = ledger["complete_pages"]
        if not isinstance(complete, list) or any(not isinstance(name, str) for name in complete):
            raise ValueError("complete_pages must be a list of page filenames")
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"FAIL 4.2 completion ledger {PROC42_LEDGER}: {exc}")
        return True
    failed = False
    if len(complete) != len(set(complete)):
        print("FAIL 4.2 completion ledger: duplicate page entries")
        failed = True
    unknown = sorted(set(complete) - PROC42_REQUIRED)
    if unknown:
        print("FAIL 4.2 completion ledger: unknown Processo page(s): " + ", ".join(unknown))
        failed = True
    if require_all:
        missing = sorted(PROC42_REQUIRED - set(complete))
        if missing:
            print(f"FAIL 4.2 completion ledger: {len(missing)} of 22 required pages are not declared: " + ", ".join(missing))
            failed = True
    # An explicit --pages invocation exercises the checker against a chosen
    # known-bad page; normal runs check only pages declared complete in the ledger.
    page_names = [p.name for p in selected] if explicit else complete
    if not explicit:
        print(f"4.2 completion ledger: {len(complete)}/22 page(s) declared")
    for name in page_names:
        if name not in PROC42_REQUIRED:
            continue
        page = LESSONS / name
        if not page.is_file():
            print(f"FAIL 4.2 completion ledger: declared page is missing: {page}")
            failed = True
            continue
        failed = check_42_page(page) or failed
    return failed


def all_pages():
    return sorted(p for p in LESSONS.glob("*.html") if p.name.startswith(("aula-", "unidade-", "revisao-")))


def check_content(selected):
    failed = False
    for p in selected:
        label = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
        s = visible_text(p)
        findings = list(NEGATED.finditer(s))
        words = len(re.findall(r"\b\w+\b", s, re.UNICODE))
        rate = len(findings) * 1000 / max(words, 1)
        # The negated-inference floor applies to lessons only, not the review.
        if p.name.startswith("aula-") and rate > 0.5:
            print(f"FAIL negated-inference {label}: {len(findings)} / {words} words ({rate:.3f}/1000; limit 0.5)")
            failed = True
        gap_findings = list(GAP_TALK.finditer(s))
        gap_rate = len(gap_findings) * 1000 / max(words, 1)
        if p.name.startswith("aula-") and gap_rate > 0.5:
            print(f"FAIL gap-talk {label}: {len(gap_findings)} / {words} words ({gap_rate:.3f}/1000; limit 0.5)")
            failed = True
        backstage = list(BACKSTAGE.finditer(s))
        if backstage:
            print(f"FAIL backstage {label}: {len(backstage)} match(es): " + ", ".join(repr(m.group()) for m in backstage[:4]))
            failed = True
        soup = list(TAG_SOUP.finditer(p.read_text(encoding="utf-8", errors="replace")))
        if soup:
            print(f"FAIL tag-soup {label}: {len(soup)} match(es)")
            failed = True
        raw = p.read_text(encoding="utf-8", errors="replace")
    # Tag soup is cheap and has no known legal-content false positives, so scan the full tree.
    for p in all_pages():
        soup = list(TAG_SOUP.finditer(p.read_text(encoding="utf-8", errors="replace")))
        if soup:
            label = str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)
            print(f"FAIL tag-soup {label}: {len(soup)} match(es)")
            failed = True
    if not selected:
        print(f"PASS changed-page content floors: no changed {COURSE} lesson/review body prose")
    return failed


def check_images(base, head=None):
    if not base:
        print("FAIL image-floor: supply a base commit (PROC_FLOOR_BASE or --base)")
        return True
    diff = [base, head] if head else [f"{base}...HEAD"]
    result = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", *diff], cwd=ROOT, text=True, capture_output=True)
    if result.returncode:
        print(f"FAIL image-floor: cannot diff against {base}: {result.stderr.strip()}")
        return True
    bad = [line for line in result.stdout.splitlines() if IMAGE.search(line) and "/assets/" not in f"/{line.lstrip('/')}" and not line.startswith("assets/")]
    if bad:
        print(f"FAIL image-floor: {len(bad)} PNG/JPG added outside assets/: " + ", ".join(bad[:6]))
        return True
    print("PASS image-floor: no PNG/JPG additions outside assets/")
    return False


def outputs_are_idempotent(first, second):
    """True only when two generator runs leave the same output bytes."""
    return first == second


def check_s7():
    builder = ROOT / "tools/exam-bank/build_s7.py"
    # Build with a tiny, generated fixture so CI does not need the private workshop inputs.
    try:
        with tempfile.TemporaryDirectory(prefix="proc-s7-") as tmp:
            tmp = Path(tmp)
            site = tmp / "site"
            (site / "courses/processo-civil-i").mkdir(parents=True)
            for name in ("revisao-p1.html", "cartoes.html"):
                src = LESSONS / name
                if src.exists():
                    (site / "courses/processo-civil-i" / name).write_bytes(src.read_bytes())
            bank = {"questions": []}
            lesson_ids = ["aula-01.html", "aula-02.html", "aula-04.html", "aula-06.html", "aula-08.html", "aula-09.html"]
            for i in range(55):
                bank["questions"].append({
                    "id": f"fixture-{i:02d}",
                    "appearances": [{"lesson_id": lesson_ids[i % len(lesson_ids)], "year": "2020/1",
                                     "question_number": str(i + 1), "verbatim_text": f"Fixture question {i + 1}?",
                                     "topic": "Fixture", "kind": "case", "official_answer": "A",
                                     "verified_answer": "A", "citations": []}]
                })
            bank_path = tmp / "bank.json"
            bank_path.write_text(json.dumps(bank), encoding="utf-8")
            index_dir = tmp / "cpc"
            index_dir.mkdir()
            articles = ["321", "332", "125", "219", "336", "276"]
            index = {"capture_path": "capture.html", "chapters": [{"id": f"Art. {n}"} for n in articles]}
            index_path = index_dir / "index.json"
            index_path.write_text(json.dumps(index), encoding="utf-8")
            (index_dir / "capture.html").write_text("".join(f'<a name="art{n}"></a>Art. {n} fixture text. <a name="art{int(n)+1}"></a>' for n in articles), encoding="utf-8")
            previous = None
            for run in (1, 2):
                r = subprocess.run([sys.executable, str(builder), "--site", str(site), "--bank", str(bank_path), "--cpc-index", str(index_path)], cwd=ROOT, text=True, capture_output=True)
                if r.returncode:
                    print("FAIL build_s7 idempotence: " + (r.stderr.strip() or r.stdout.strip()))
                    return True
                current = {name: (site / "courses/processo-civil-i" / name).read_bytes() for name in ("revisao-p1.html", "cartoes.html")}
                if run == 2 and not outputs_are_idempotent(previous, current):
                    changed = ", ".join(name for name in current if current[name] != previous[name])
                    print(f"FAIL build_s7 idempotence: second-run output differs for {changed}")
                    return True
                previous = current
        print("PASS build_s7 idempotence: second run leaves review and cards byte-identical")
        return False
    except Exception as e:
        print(f"FAIL build_s7 idempotence: {e}")
        return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("course", help="course slug under courses/")
    ap.add_argument("--base", default=os.environ.get("COURSE_FLOOR_BASE", os.environ.get("PROC_FLOOR_BASE")))
    ap.add_argument("--head", help=argparse.SUPPRESS)
    ap.add_argument("--pages", nargs="*", help="explicit pages for a known-bad demonstration")
    ap.add_argument("--require-all-42", action="store_true", help="require all 22 Processo pages in the 4.2 completion ledger")
    ap.add_argument("--no-s7", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    global COURSE, LESSONS
    COURSE = args.course
    LESSONS = ROOT / "courses" / COURSE
    if not LESSONS.is_dir():
        print(f"FAIL course floors: unknown course {COURSE!r}")
        return 2
    if args.pages is not None:
        selected = [Path(x).resolve() for x in args.pages]
        structure_selected = selected
    elif args.base:
        changed = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", args.base], cwd=ROOT, text=True, capture_output=True)
        if changed.returncode:
            print(f"FAIL changed-page discovery: {changed.stderr.strip()}")
            return 1
        candidates = [ROOT / x for x in changed.stdout.splitlines() if x.startswith(f"courses/{COURSE}/") and x.endswith(".html") and (Path(x).name.startswith(("aula-", "unidade-", "revisao-"))) and (ROOT / x).is_file()]
        structure_selected = candidates
        selected = []
        for page in candidates:
            rel = page.relative_to(ROOT).as_posix()
            prior = subprocess.run(["git", "show", f"{args.base}:{rel}"], cwd=ROOT, text=True, capture_output=True)
            if prior.returncode or visible_text(prior.stdout) != visible_text(page): selected.append(page)
    else:
        selected = all_pages()
        structure_selected = selected
    require_all_42 = args.require_all_42 or os.environ.get("GITHUB_BASE_REF") == "main"
    failed = check_content(selected) | check_42(structure_selected, require_all_42, args.pages is not None) | check_images(args.base, args.head)
    if COURSE == "processo-civil-i" and not args.no_s7:
        failed = check_s7() or failed
    print(f"{COURSE} floors: FAIL" if failed else f"{COURSE} floors: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
