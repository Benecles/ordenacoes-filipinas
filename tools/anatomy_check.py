"""Lesson anatomy check: layout mistakes that already shipped once (FLIGHT-LOG F-014..F-016).

  LOOSE-PROSA  a .prosa block not inside .wide (or a chapter/card): it renders at x=0, off the page grid
  LATE-PANEL   the only panel of a one-step scrolly lacks class "on": it fades in late, or never
  SQUARE-KIT   a kit panel alone in its scrolly keeps the default 600x600 viewBox: crop it to the drawing
  REF-LEAK     a page other than the reference lesson carries `REF ·` agent comments: they were copied, delete them
  TITLEBLOCK-DUPLICATE  a hero titleblock has more than one Leitura, Antes or Depois item

Run: python3 tools/anatomy_check.py [files...]   (default: every courses/*/*.html). Exit 1 on any hit.
"""
import glob, os, re, sys
from html.parser import HTMLParser

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
HOLDERS = {'wide', 'chapter', 'card', 'step', 'quiz', 'note'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.hits = [], []
        self.scrolly = None  # {'steps': n, 'panels': [(cls, viewBox)]}
        self.titleblock = None  # {'counts': {}, 'line': n, 'item': None}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = set((a.get('class') or '').split())
        line = self.getpos()[0]
        if tag == 'div' and 'prosa' in cls and not any(c & HOLDERS for _, c, _ in self.stack):
            self.hits.append(f'LOOSE-PROSA line {line}: wrap it in <div class="wide">')
        if tag == 'div' and 'titleblock' in cls:
            self.titleblock = {'counts': {}, 'line': line, 'item': None}
        if self.titleblock is not None and a.get('role') == 'listitem':
            self.titleblock['item'] = []
        if 'scrolly' in cls:
            self.scrolly = {'steps': 0, 'panels': [], 'line': line, 'depth': len(self.stack)}
        if self.scrolly is not None:
            if 'step' in cls:
                self.scrolly['steps'] += 1
            if tag == 'svg' and 'panel' in cls:
                self.scrolly['panels'].append((cls, a.get('viewBox', ''), a.get('id', '')))
        if tag not in VOID and not tag.endswith('/'):
            self.stack.append((tag, cls, a.get('role')))

    def handle_data(self, data):
        if self.titleblock is not None and self.titleblock['item'] is not None:
            self.titleblock['item'].append(data)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        closed = []
        while self.stack:
            t, cls, role = self.stack.pop()
            closed.append((t, cls, role))
            if t == tag:
                break
        for t, cls, role in closed:
            if t == 'div' and role == 'listitem' and self.titleblock is not None and self.titleblock['item'] is not None:
                label = ''.join(self.titleblock['item']).strip()
                match = re.match(r'(Leitura|Antes|Depois)\b', label, re.I)
                if match:
                    key = match.group(1).capitalize()
                    self.titleblock['counts'][key] = self.titleblock['counts'].get(key, 0) + 1
                self.titleblock['item'] = None
            if t == 'header' and 'hero' in cls and self.titleblock is not None:
                for key, count in self.titleblock['counts'].items():
                    if count > 1:
                        self.hits.append(f'TITLEBLOCK-DUPLICATE line {self.titleblock["line"]}: {count} {key} items (maximum 1)')
                self.titleblock = None
        s = self.scrolly
        if s is not None and len(self.stack) <= s['depth']:
            if s['steps'] == 1 and len(s['panels']) == 1:
                cls, vb, ident = s['panels'][0]
                if 'on' not in cls:
                    self.hits.append(f'LATE-PANEL line {s["line"]} #{ident}: add class "on"')
                if 'figkit' in cls and re.sub(r'\s+', ' ', vb.strip()) == '0 0 600 600':
                    self.hits.append(f'SQUARE-KIT line {s["line"]} #{ident}: crop the viewBox to the drawing')
            self.scrolly = None


REFERENCE = os.path.join('courses', 'controle-de-constitucionalidade', 'aula-01.html')


def check(path):
    src = open(path, encoding='utf-8').read()
    p = Page()
    p.feed(src)
    if not os.path.abspath(path).endswith(REFERENCE) and re.search(r'<!--\s*REF ·', src):
        p.hits.append('REF-LEAK: agent comments copied from the reference lesson; remove every <!-- REF · … --> block')
    return p.hits


if __name__ == '__main__':
    root = os.path.join(os.path.dirname(__file__), '..')
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(root, 'courses', '*', '*.html')))
    bad = 0
    for f in files:
        for h in check(f):
            print(f'{os.path.relpath(f, root)}: {h}')
            bad += 1
    print(f'anatomy: {"FAIL" if bad else "PASS"} ({bad} hits, {len(files)} pages)')
    sys.exit(1 if bad else 0)
