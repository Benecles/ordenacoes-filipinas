#!/usr/bin/env python3
"""Blocking floors for the Processo Civil I lesson pages (PROC-R3 A3)."""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "courses/processo-civil-i"
NEGATED = re.compile(r"\bnão\s+(?:se\s+)?(?:prova|provam|transforma|transformam|equivale|equivalem|basta|bastam|garante|garantem|substitui|substituem|encerra|encerram|resolve|resolvem|apaga|apagam|elimina|eliminam|esgota|esgotam|autoriza|autorizam|dispensa|dispensam|decide|decidem|significa|significam|cria|criam|converte|convertem|torna|tornam)\b", re.I)
BACKSTAGE = re.compile(
    r"\b(?:(?:os|nos|dos|pelos|segundo os?) slides?|materia(?:l|is) da disciplina|"
    r"nest[ae] leitura|dest[ae] leitura|prática autoral|relatad[oa]s? por|"
    r"localizador(?:es)?|fontes e (?:limites|localizadores)|C\d{1,2}\b|blueprint|cerca desta|"
    r"compêndio|compendio|arquivo-fonte|arquivo fonte|\d+-statute\.txt|"
    r"PDF\s+p(?:á?g(?:ina)?)?\.?\s*\d+|p(?:á?g(?:ina)?)?\.?\s*\d+\s+do PDF)\b", re.I)
TAG_SOUP = re.compile(r"<[a-z]+<")
IMAGE = re.compile(r"\.(?:png|jpe?g)$", re.I)


def visible_text(path):
    s = path.read_text(encoding="utf-8", errors="replace")
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?is)<(script|style|svg|head|nav)\b.*?</\1>", " ", s)
    s = re.sub(r"(?is)<div hidden\b.*?(?=</body>)", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</(?:p|li|h\d|td|th|div|figcaption|summary)>", "\n", s)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def all_pages():
    return sorted(p for p in LESSONS.glob("*.html") if p.name.startswith("aula-") or p.name == "revisao-p1.html")


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
            print(f"FAIL tag-soup {p.relative_to(ROOT)}: {len(soup)} match(es)")
            failed = True
    if not selected:
        print("PASS changed-page content floors: no changed Processo lesson/review pages")
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
                if run == 2 and current != previous:
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
    ap.add_argument("--base", default=os.environ.get("PROC_FLOOR_BASE"))
    ap.add_argument("--head", help=argparse.SUPPRESS)
    ap.add_argument("--pages", nargs="*", help="explicit pages for a known-bad demonstration")
    ap.add_argument("--no-s7", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.pages is not None:
        selected = [Path(x).resolve() for x in args.pages]
    elif args.base:
        changed = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", f"{args.base}...HEAD"], cwd=ROOT, text=True, capture_output=True)
        if changed.returncode:
            print(f"FAIL changed-page discovery: {changed.stderr.strip()}")
            return 1
        selected = [ROOT / x for x in changed.stdout.splitlines() if x.startswith("courses/processo-civil-i/") and x.endswith(".html") and (Path(x).name.startswith("aula-") or Path(x).name == "revisao-p1.html") and (ROOT / x).is_file()]
    else:
        selected = all_pages()
    failed = check_content(selected) | check_images(args.base, args.head)
    if not args.no_s7:
        failed = check_s7() or failed
    print("processo floors: FAIL" if failed else "processo floors: PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
