"""Metodologia Jurídica · hero strips (1080 × 150). One course axis, centuries XII → XX, with every lesson's span
drawn in ink and this lesson's span in blue, so each page shows where its text sits in the course. Replaces
the repeated generic timeline (01–04) and gives 05–15 a strip. Spans follow each lesson's text: centuries
named on the page where given (05: XVI–XVII; 09: XVIII; 14: XIX; 15: 1958), otherwise placed by subject.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, t

W, H = 1080, 150
C0, C1, X0, X1 = 12, 21, 30, 1050
ROMAN = {12: 'XII', 13: 'XIII', 14: 'XIV', 15: 'XV', 16: 'XVI', 17: 'XVII', 18: 'XVIII', 19: 'XIX', 20: 'XX'}
LESSONS = {   # page: (from century, to century, short label)
    'aula-01': (12, 15.5, 'escolas medievais'), 'aula-02': (15, 16.5, 'Portugal'), 'aula-03': (16, 18.9, 'casuísmo I'),
    'aula-04': (16, 17.9, 'América colonial'), 'aula-05': (16, 17.95, 'literatura pragmática'), 'aula-06': (17, 17.9, 'Solórzano'),
    'aula-07': (16.2, 18.8, 'costume indiano'), 'aula-08': (16.4, 18.7, 'casuísmo II'), 'aula-09': (18, 18.95, 'ordem'),
    'aula-14': (19, 19.95, 'cursos jurídicos'), 'aula-15': (20.5, 20.62, 'Cirne Lima, 1958'),
}
X = lambda c: X0 + (X1 - X0) * (c - C0) / (C1 - C0)


def strip(page):
    o = f'<line x1="{X0}" y1="112" x2="{X1}" y2="112" style="stroke:var(--ink);stroke-width:1.2"/>'
    for c in range(C0, C1):
        o += f'<line x1="{X(c):.0f}" y1="106" x2="{X(c):.0f}" y2="118" style="stroke:var(--ink);stroke-width:1"/>'
        o += t(X(c + .5), 136, ROMAN[c], size=10.5, anchor='middle', fill='var(--ink-2)')
    rows = {}
    for p, (a, b, label) in LESSONS.items():
        r = next(k for k in range(6) if all(not (a < rb and ra < b) for ra, rb in rows.get(k, [])))
        rows.setdefault(r, []).append((a, b))
        y = 92 - r * 14
        me = p == page
        o += f'<rect x="{X(a):.0f}" y="{y}" width="{max(6, X(b) - X(a)):.0f}" height="8" style="fill:{"var(--dif)" if me else "var(--ink-2)"};opacity:{1 if me else .55}"/>'
        if me:
            o += t(X(a), 20, label, size=12, weight=700, caps=True, fill='var(--dif)', anchor='end' if X(a) > 800 else 'start') + f'<line x1="{X(a):.0f}" y1="26" x2="{X(a):.0f}" y2="{y}" style="stroke:var(--dif);stroke-width:1"/>'
    label = f'O curso em séculos, do XII ao XX, com o texto desta aula marcado: {LESSONS[page][2]}'
    return f'<svg class="hero-fork figkit" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">{o}</svg>'


def apply(page):
    from inject import ROOT, element_span
    p = os.path.join(ROOT, 'courses', 'metodologia-juridica', f'{page}.html')
    s = open(p).read()
    new = strip(page)
    m = re.search(r'<svg\b[^>]*class="hero-fork[^"]*"', s)
    if m:
        a, b = element_span(s, m.start())
        s = s[:a] + new + s[b:]
    else:
        d = re.search(r'(?s)<p class="deck">.*?</p>', s)
        s = s[:d.end()] + '\n  ' + new + s[d.end():]
    open(p, 'w').write(s)


if __name__ == '__main__':
    for page in LESSONS:
        apply(page)
    print(len(LESSONS), 'heroes;', '\n'.join(WARN) or 'no text warnings')
