#!/usr/bin/env python3
"""Check a lesson without a browser: python3 tools/lesson_check.py PAGE [--json].

Counts Unicode word runs (hyphens separate words), including headings and captions.
Every visible word belongs once to own prose, quotations or figures; figures take
precedence over quotations. Quotations include aside.fonte, blockquote, q and
explicitly verbatim exam material. Head, navigation, scripts, styles, templates
and hidden archives are excluded. Content outside chapters gets its own row.
The shell's length gate uses word_report()['totals']['own_prose'] too.

C<number> refers to the workshop COMPLAINTS.md. Style prompts, estimates of title
width and legacy rules contradicted by the approved lesson are warnings. Geometry,
meaning, source fidelity and working JavaScript require human/browser review.
"""
import argparse
import html
import json
import re
import sys
import tempfile
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

try:
    from .lint import marks_lint, slop_lint
except ImportError:  # direct CLI
    from lint import marks_lint, slop_lint

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
SKIP = {'head', 'script', 'style', 'nav', 'template', 'noscript'}
VERBATIM = {'verbatim', 'pergunta', 'bet-q', 'bet-opts', 'bet-options',
            'bet-case', 'exam-options'}
COUNTS = ('own_prose', 'quotations', 'figure_text')
BLOCK = set('p div section article aside figure figcaption blockquote li ol ul h1 h2 h3 h4 h5 h6 br td th summary'.split())
SCRIPTS = ('theme-toggle.js', 'offline.js', 'highlight.js', 'highlight-panel.js')


@dataclass(eq=False)
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    parent: object = None
    line: int = 1

    @property
    def classes(self):
        return set((self.attrs.get('class') or '').split())

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def text(self):
        return ''.join(c.text() if isinstance(c, Node) else c for c in self.children)

    def within(self, tag=None, classes=()):
        n = self
        while n:
            if n.tag == tag or n.classes.intersection(classes):
                return True
            n = n.parent
        return False


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node('document')
        self.current = self.root
        self.feed(source)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), parent=self.current, line=self.getpos()[0])
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        n = self.current
        while n.parent:
            if n.tag == tag:
                self.current = n.parent
                return
            n = n.parent

    def handle_data(self, data):
        self.current.children.append(data)


def excluded(node):
    return (node.tag in SKIP or 'hidden' in node.attrs
            or bool(re.search(r'(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)\b', node.attrs.get('style') or '', re.I)))


def category(node, inherited):
    if node.tag in {'figure', 'svg', 'canvas', 'figcaption'}:
        return 'figure_text'
    if inherited == 'figure_text':
        return inherited
    if (node.tag in {'blockquote', 'q'} or node.tag == 'aside' and 'fonte' in node.classes
            or node.classes.intersection(VERBATIM)):
        return 'quotations'
    return inherited


def _report(root):
    chapters = [n for n in root.walk() if n.tag == 'section' and 'chapter' in n.classes]
    rows = [{'id': n.attrs.get('id') or f'chapter-{i}',
             'title': next((c.text().strip() for c in n.walk() if c.tag == 'h2'), ''),
             **{k: [] for k in COUNTS}} for i, n in enumerate(chapters, 1)]
    outside = {'id': 'outside-chapters', 'title': 'Outside chapters', **{k: [] for k in COUNTS}}
    lookup = dict(zip(chapters, rows))

    def visit(node, row, group):
        if excluded(node):
            return
        row = lookup.get(node, row)
        group = category(node, group)
        if node.tag in BLOCK:
            row[group].append('\n')
        for child in node.children:
            if isinstance(child, Node):
                visit(child, row, group)
            else:
                row[group].append(child)
        if node.tag in BLOCK:
            row[group].append('\n')

    visit(root, outside, 'own_prose')
    for row in [*rows, outside]:
        for key in COUNTS:
            row[key] = len(re.findall(r'\b\w+\b', ''.join(row[key]), re.UNICODE))
        row['total'] = sum(row[k] for k in COUNTS)
    totals = {k: sum(row[k] for row in [*rows, outside]) for k in (*COUNTS, 'total')}
    return {'chapters': rows, 'outside_chapters': outside, 'totals': totals}


def word_report(source):
    """The single counting implementation, also used by the shell word gate."""
    return _report(Document(source).root)


def own_html(node, inherited='own_prose'):
    """Retain authored markup for marks_lint; prune quotations and figure text."""
    group = category(node, inherited)
    if excluded(node) or group != 'own_prose':
        return '\n'
    children = ''.join(own_html(c, group) if isinstance(c, Node) else html.escape(c)
                       for c in node.children)
    if node.tag == 'document':
        return children
    attrs = ''.join(f' {k}="{html.escape(v or "", quote=True)}"' for k, v in node.attrs.items())
    return f'<{node.tag}{attrs}>' + children + ('' if node.tag in VOID else f'</{node.tag}>')


def finding(check, message, node=None, severity='error'):
    return {'check': check, 'severity': severity, 'line': node.line if node else 1, 'message': message}


def contract(source):
    """Required on all shell pages, including non-lessons."""
    root = Document(source).root
    nodes = list(root.walk())
    paths = [urlsplit(n.attrs.get('src') or '').path for n in nodes if n.tag == 'script']
    out = [finding('SHELL-SCRIPTS', f'missing assets/{s}') for s in SCRIPTS
           if not any(p == f'assets/{s}' or p.endswith(f'/assets/{s}') for p in paths)]
    toggles = [n for n in nodes if 'theme-toggle' in n.classes]
    if len(toggles) != 1:
        out.append(finding('SHELL-TOGGLE', f'expected exactly one .theme-toggle; found {len(toggles)}'))
    return out


def media_parity(source):
    """Check every comma-separated max-width branch, not just the whole @media."""
    out = []
    for node in Document(source).root.walk():
        if node.tag != 'style':
            continue
        css = re.sub(r'/\*.*?\*/', '', node.text(), flags=re.S)
        for match in re.finditer(r'@media\s*([^{}]+)\{', css, re.I):
            for branch in match[1].split(','):
                if re.search(r'\(\s*max-width\s*:', branch, re.I) and not re.search(r'\band\s*\(\s*orientation\s*:\s*portrait\s*\)', branch, re.I):
                    out.append(finding('OFFLINE-PARITY', 'write phone CSS as @media (max-width:760px) and (orientation:portrait) { ... }; offline_build.py adds this qualifier', node))
    return out


def background_wash(declarations):
    """Resetting a background (as both approved lessons do) is not highlighting."""
    return any(value.strip().lower() not in {'none', 'transparent', 'initial', 'inherit', 'unset', 'revert'}
               for value in re.findall(r'\bbackground(?:-color|-image)?\s*:\s*([^;}]+)', declarations, re.I))


def mechanics(root):
    out = []
    nodes = list(root.walk())
    chapters = [n for n in nodes if n.tag == 'section' and 'chapter' in n.classes]
    first = nodes.index(chapters[0]) if chapters else len(nodes)
    last = nodes.index(chapters[-1]) if chapters else -1
    authored_inline = [n for n in nodes if n.tag in {'span', 'em', 'strong', 'b', 'i', 'mark'}
                       and all(not excluded(a) and category(a, 'own_prose') == 'own_prose' for a in ancestors(n))]
    for n in nodes:
        if any(excluded(a) for a in ancestors(n)):
            continue
        own = all(category(a, 'own_prose') == 'own_prose' for a in ancestors(n))
        if n.tag == 'title' and n.within('svg'):
            out.append(finding('C69', 'remove SVG <title>: it creates a browser hover tooltip', n))
        if n.tag in {'h1', 'h2'} and (len(n.text().strip()) > 100 or sum(c.tag == 'br' for c in n.walk()) > 1):
            out.append(finding('C50', 'title may exceed two lines; inspect at 1280px (text length is only a proxy)', n, 'warning'))
        if n.tag == 'p' and 'lede' in n.classes and '?' in n.text():
            out.append(finding('C20', 'a chapter lede must narrate, not ask a question', n))
        if n.within(classes={'hero'}) and (n.tag == 'button' or 'data-pick-group' in n.attrs or 'data-call' in n.attrs):
            out.append(finding('C31', 'hero question controls belong after the reading', n))
        if n.tag == 'animate' and n.within(classes={'hero'}) and (n.attrs.get('repeatcount') or '').lower() == 'indefinite':
            out.append(finding('C34', 'looping hero animation: review calm motion', n, 'warning'))
        if n.tag in {'h1', 'p'} and nodes.index(n) < first and '?' in n.text() and own:
            out.append(finding('C02', 'opening question precedes the first chapter', n))
        is_exam = bool(n.classes.intersection({'bet', 'exam-paper', 'exam-card'}))
        if is_exam and nodes.index(n) < last:
            out.append(finding('C62', 'exam card precedes the end of the reading', n))
        if n.tag in {'h3', 'header', 'summary'} and n.within(classes={'bet', 'exam-paper', 'exam-card'}) and re.search(r'\b(?:19|20)\d{2}(?:[/.-][12])?\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b', n.text()):
            out.append(finding('C61', 'past exam date in card label (approved Processo also has these)', n, 'warning'))
        if n.tag == 'details' and (is_exam or any(c.classes.intersection({'bet', 'exam-paper', 'exam-card'}) for c in n.walk())):
            out.append(finding('C82', 'exam card requires clicking open; expose it after the reading', n, 'warning'))
        if n.tag == 'button' and n.within('figure') and any(k in n.attrs for k in ('data-panel', 'data-slide', 'data-version')):
            out.append(finding('C73', 'figure version switch: use a static drawing or scroll state', n, 'warning'))
        if own and (n.tag == 'mark' or n.classes.intersection({'mark', 'highlight', 'highlighted'})):
            out.append(finding('C75', 'authored highlighter: reserve highlights for the reader', n))
        if own and n.tag in {'p', 'span', 'em', 'strong', 'b'} and background_wash(n.attrs.get('style') or ''):
            out.append(finding('C75', 'background wash in authored text: use emphasis or a house colour', n))
    # Inspect only CSS declarations / SVG paint attributes, never hashes in text or links.
    for n in nodes:
        blobs = [n.attrs.get('style') or '']
        if n.tag == 'style':
            css = re.sub(r'/\*.*?\*/', '', n.text(), flags=re.S)
            blobs += re.findall(r'(?:^|[;{])\s*[\w-]+\s*:\s*([^;{}]+)', css)
            for selector, declarations in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
                if background_wash(declarations):
                    for branch in selector.split(','):
                        # A conservative CSS subset: explicit inline tags/classes.
                        # Do not infer inherited paint, pseudo-elements or layout.
                        target = branch.strip().split()[-1] if branch.strip() else ''
                        if re.fullmatch(r'(?:span|em|strong|b|i|mark)?(?:\.[\w-]+)*', target) and target:
                            tag = re.match(r'^\w+', target)
                            classes = set(re.findall(r'\.([\w-]+)', target))
                            if any((not tag or n.tag == tag[0]) and classes <= n.classes for n in authored_inline):
                                out.append(finding('C75', f'CSS highlighter wash on authored text ({branch.strip()})', n))
                if re.search(r'(?<![\w-])\.(?:mark|highlight|highlighted)\b|\bmark\b', selector) and background_wash(declarations):
                    out.append(finding('C66', 'custom highlighter wash: review reader marker yellow', n, 'warning'))
                if re.search(r':(?:active|focus)(?![\w-])', selector) and re.search(r'(?:outline|box-shadow|background)\s*:', declarations):
                    out.append(finding('C68', 'mouse press/focus decoration: review visible traces', n, 'warning'))
        if n.within('svg'):
            blobs += [n.attrs.get(k) or '' for k in ('fill', 'stroke', 'stop-color', 'color')]
        if any(re.search(r'(?i)#[0-9a-f]{3,8}\b', b) for b in blobs):
            out.append(finding('C63', 'literal hex colour outside house tokens; use var(--ink), var(--dif), etc.', n))
    return out


def ancestors(node):
    while node:
        yield node
        node = node.parent


def check(source, path='<memory>', lang=None, shell_contract=True):
    root = Document(source).root
    language = lang or next((('en' if (n.attrs.get('lang') or '').lower().startswith('en') else 'pt')
                             for n in root.walk() if n.tag == 'html'), 'pt')
    findings = mechanics(root)
    if shell_contract:
        findings += contract(source)
    findings += media_parity(source)
    with tempfile.TemporaryDirectory(prefix='lesson-check-') as tmp:
        projected = Path(tmp) / 'own.html'
        projected.write_text(own_html(root), encoding='utf-8')
        slop = slop_lint.lint(str(projected), None, language)
        for f in slop['findings']:
            findings.append(finding('C13/' + f['rule'], f['span'] + ': ' + f['fix'], severity='warning'))
        for line, rule, message in marks_lint.check(str(projected)):
            # #75 explicitly permits bold; the older linter retired it.
            severity = 'warning' if rule in {'plain-bold', 'mark-per-chapter', 'mark-in-fonte',
                                           'held-too-long', 'limit-too-long'} else 'error'
            f = finding('C24/' + rule, message, severity=severity)
            f['line'] = line
            findings.append(f)
    return {'page': str(path), 'language': language, **_report(root),
            'status': 'FAIL' if any(f['severity'] == 'error' for f in findings) else 'PASS',
            'findings': findings}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('page', type=Path)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--lang', choices=('pt', 'en'))
    args = parser.parse_args(argv)
    try:
        result = check(args.page.read_text(encoding='utf-8'), args.page, args.lang)
    except (OSError, UnicodeError) as exc:
        parser.exit(2, f'lesson_check: {exc}\n')
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f'{result["status"]} lesson_check: {args.page} ({result["language"]})')
        print('chapter                         own prose   quotations  figure text   total')
        for row in [*result['chapters'], result['outside_chapters'], {'id': 'TOTAL', **result['totals']}]:
            print(f'{row["id"]:30} {row["own_prose"]:10} {row["quotations"]:12} {row["figure_text"]:12} {row["total"]:7}')
        for f in result['findings']:
            print(f'{f["severity"].upper()} {f["check"]} line {f["line"]}: {f["message"]}')
    return int(result['status'] == 'FAIL')


if __name__ == '__main__':
    sys.exit(main())
