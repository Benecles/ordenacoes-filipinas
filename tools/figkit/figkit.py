"""Figure kit: instruments, not diagrams.

One implementation of the house drawing hand for lesson figures (the non-map counterpart of
latam-build/maps.py). A figure is a short script that puts real lesson content into a kit
component; the craft (stroke weights, mono labels, tones, ticks, gutters) lives here, once.

Colours are the course tokens (var(--ink) etc.), so every figure follows light/dark mode.
Panels are 600x600 (scrolly stage); heroes are 1080 wide.
"""

import calendar as _calendar


MONO = "font-family:var(--mono)"
TONE = {'ink': 'var(--ink)', 'conc': 'var(--conc)', 'dif': 'var(--dif)', 'mix': 'var(--mix)', 'muted': 'var(--ink-2)'}
WASH = {'ink': 'var(--paper-2)', 'conc': 'var(--conc-wash)', 'dif': 'var(--dif-wash)', 'mix': 'var(--mix-wash)', 'muted': 'var(--paper-2)'}
CH = 7.4  # mono 11px + .08em tracking, px per character (for gutters, not layout)
WARN = []  # text that would run into a line: fix the wording or the layout, never ship with warnings


def t(x, y, s, size=11, fill='var(--ink)', anchor='start', weight=500, caps=False, ls='.08em', italic=False, cls=''):
    st = f"{MONO};font-size:{size}px;font-weight:{weight};letter-spacing:{ls};fill:{fill}"
    if italic:
        st = f"font-family:var(--serif,serif);font-style:italic;font-size:{size + 2}px;fill:{fill}"
    if caps:
        s = s.upper()
    c = f' class="{cls}"' if cls else ''
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{x:g}" y="{y:g}"{a}{c} style="{st}">{s}</text>'


def line(x1, y1, x2, y2, tone='ink', w=1.5, dash=None, cls='', d=None):
    da = f";stroke-dasharray:{dash}" if dash else ''
    dl = f";--d:{d}s" if d is not None else ''
    c = f' class="{cls}"' if cls else ''
    return f'<path{c} d="M{x1:g} {y1:g}L{x2:g} {y2:g}" style="fill:none;stroke:{TONE[tone]};stroke-width:{w}{da}{dl}"/>'


def hatch_def(uid, tone='conc'):
    return (f'<pattern id="{uid}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="7" height="7" style="fill:{WASH[tone]}"/>'
            f'<path d="M0 0V7" style="stroke:{TONE[tone]};stroke-width:1.1;opacity:.55"/></pattern>')


def badge(x, y, ok, r=11):
    """A reading: ✓ inside the rule (dif), ✕ past it (conc)."""
    tone = 'dif' if ok else 'conc'
    mark = (f'M{x - 5} {y}l3.6 4 6.4-8' if ok else f'M{x - 4.5} {y - 4.5}l9 9m0-9l-9 9')
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{r}" style="fill:var(--paper);stroke:{TONE[tone]};stroke-width:1.6"/>'
            f'<path d="{mark}" style="fill:none;stroke:{TONE[tone]};stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round"/>')


class Ruler:
    """A graduated rule: the parameter as a measuring instrument.

    stops: labels at equal steps (each a str or a (line1, line2) tuple).
    limit: the step value where the rule stops allowing (everything past it is hatched).
    Acts are laid against it with .strip(); each strip projects its end back onto the rule.
    """

    def __init__(self, uid, x, y, w, stops, title='', source='', limit=None, h=74, minor=5, tone='ink'):
        self.uid, self.x, self.y, self.w, self.h = uid, x, y, w, h
        self.stops, self.title, self.source, self.limit, self.minor = stops, title, source, limit, minor
        self.n = len(stops) - 1
        self.parts = []

    def pos(self, v):
        return self.x + 14 + (self.w - 28) * v / self.n

    def defs(self):
        return hatch_def(f'{self.uid}-h')

    def body(self, d=0):
        x, y, w, h = self.x, self.y, self.w, self.h
        o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
        if self.limit is not None:  # the forbidden reach of the scale
            lx = self.pos(self.limit)
            o += f'<rect x="{lx:g}" y="{y + 20}" width="{x + w - lx:g}" height="{h - 20}" style="fill:url(#{self.uid}-h);stroke:none"/>'
        o += line(x, y + 20, x + w, y + 20, w=1)
        o += t(x + 10, y + 14, self.title, size=10, fill='var(--ink-2)', caps=True, weight=600)
        if self.source:
            o += t(x + w - 10, y + 14, self.source, size=10, fill='var(--ink)', anchor='end', weight=700, caps=True)
        step = (self.w - 28) / self.n / self.minor
        for i in range(self.n * self.minor + 1):  # graduations, cut into the bottom edge
            tx = self.x + 14 + i * step
            major = i % self.minor == 0
            ln = 15 if major else 6
            o += line(tx, y + h, tx, y + h - ln, w=1.3 if major else .8)
        for i, s in enumerate(self.stops):
            px = self.pos(i)
            a = 'start' if i == 0 else ('end' if i == self.n else 'middle')
            ax = px - 4 if i == 0 else (px + 4 if i == self.n else px)
            if self.limit is not None and i == self.limit and 0 < i < self.n:  # never under the limit line
                a, ax = 'end', px - 7
            ls = s if isinstance(s, tuple) else (s,)
            y0 = y + 38 if len(ls) == 2 else y + 46
            beyond = self.limit is not None and i > self.limit
            for k, part in enumerate(ls):
                o += t(ax, y0 + 14 * k, part, size=11, anchor=a, fill='var(--conc)' if beyond else 'var(--ink)',
                       weight=600 if beyond else 500)
        return f'<g>{o}</g>'

    def limit_mark(self, reach_to, label='', sub='', d=None):
        """The rule's own limit: a red line through the scale and down past the acts."""
        lx = self.pos(self.limit)
        o = line(lx, self.y - 16, lx, self.y, tone='conc', w=2.2) + line(lx, self.y + 20, lx, reach_to, tone='conc', w=2.2, cls='grow' if d is not None else '', d=d)
        o += f'<path d="M{lx - 6:g} {self.y - 16}H{lx + 6:g}" style="stroke:var(--conc);stroke-width:2.2"/>'
        if label:
            o += t(lx + 9, self.y - 20, label, size=10.5, fill='var(--conc)', weight=700, caps=True)
        if sub:
            o += t(lx + 9, self.y - 7, sub, size=10, fill='var(--conc)')
        return o

    def strip(self, sy, to, label, note='', tone=None, d=None, reading=True):
        """An act laid against the rule, from 0 to `to`, with its end projected onto the scale."""
        over = self.limit is not None and to > self.limit
        tone = tone or ('conc' if over else 'dif')
        x0, x1 = self.x + 14, self.pos(to)
        anim = ' class="grow"' if d is not None else ''
        dl = f';--d:{d}s' if d is not None else ''
        name, desc = label if isinstance(label, tuple) else ('', label)
        room = (self.pos(self.limit) if self.limit is not None else self.x + self.w) - x0 - 8
        for s_ in (desc, note):
            if s_ and len(s_) * CH > room:
                WARN.append(f'{self.uid}: "{s_}" ~{len(s_) * CH:.0f}px > {room:.0f}px before the limit')
        o = (t(x0, sy - 22, name, size=10.5, weight=700, caps=True) if name else '') + t(x0, sy - 8, desc, size=11)
        o += f'<rect x="{x0:g}" y="{sy}" width="{x1 - x0:g}" height="14" style="fill:{WASH[tone]};stroke:{TONE[tone]};stroke-width:1.3"/>'
        if over:  # the part that the rule does not allow
            lx = self.pos(self.limit)
            o += f'<rect x="{lx:g}" y="{sy}" width="{x1 - lx:g}" height="14" style="fill:var(--conc);stroke:var(--conc);stroke-width:1.3"/>'
        o += f'<path d="M{x1:g} {sy - 4}V{self.y + self.h}" style="fill:none;stroke:{TONE[tone]};stroke-width:1.2;stroke-dasharray:3 3"/>'
        o += f'<circle cx="{x1:g}" cy="{self.y + self.h}" r="3.2" style="fill:{TONE[tone]}"/>'
        if reading:
            o += badge(x1 + 22, sy + 7, not over)
        if note:
            o += t(x0, sy + 30, note, size=10.5, fill=TONE[tone], weight=600)
        return o


def svg(view, inner, cls='', label='', ident=''):
    i = f' id="{ident}"' if ident else ''
    cls = f'{cls} figkit'.strip()  # kit figures opt out of the course's blanket label-size override
    c = f' class="{cls}"'
    a = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return f'<svg{i}{c} viewBox="{view}"{a}>{inner}</svg>'


class Field:
    """A two-axis classifier: locate a case by two questions at once.

    x / y: lists of (position, (line1, line2)) ticks on the bottom and left axes.
    Regions and a border split the plane into legal categories; marks are the doctrinal forms
    (points or bars) and cases (ranges that may straddle the border). Label placement is
    explicit per mark (dx, dy, anchor): the kit draws, the author composes.
    """

    def __init__(self, uid, x0=200, x1=570, y0=100, y1=470):
        self.uid, self.x0, self.x1, self.y0, self.y1 = uid, x0, x1, y0, y1
        self.o = []

    def axes(self, xticks, yticks, xtitle='', ytitle=''):
        x0, x1, y0, y1 = self.x0, self.x1, self.y0, self.y1
        o = line(x0, y0 - 10, x0, y1) + line(x0, y1, x1 + 10, y1)
        o += f'<path d="M{x1 + 10} {y1}l-7 -4v8z" style="fill:var(--ink)"/><path d="M{x0} {y0 - 10}l-4 7h8z" style="fill:var(--ink)"/>'
        for px, (a, b) in xticks:
            o += line(px, y1, px, y1 + 6, w=1.2)
            o += t(px, y1 + 22, a, size=10.5, anchor='middle') + t(px, y1 + 35, b, size=10.5, anchor='middle', fill='var(--ink-2)')
        for py, (a, b) in yticks:
            o += line(x0 - 6, py, x0, py, w=1.2)
            o += t(x0 - 12, py - 2, a, size=10.5, anchor='end') + t(x0 - 12, py + 11, b, size=10.5, anchor='end', fill='var(--ink-2)')
        if xtitle:
            o += t((x0 + x1) / 2, y1 + 62, xtitle, size=10.5, anchor='middle', caps=True, weight=700, fill='var(--ink-2)')
        if ytitle:
            o += t(x0 - 12, y0 - 26, ytitle, size=10.5, anchor='end', caps=True, weight=700, fill='var(--ink-2)')
        self.o.append(o)

    def region(self, ya, yb, tone, opacity=.5):
        self.o.insert(0, f'<rect x="{self.x0}" y="{ya}" width="{self.x1 - self.x0}" height="{yb - ya}" '
                         f'style="fill:{WASH[tone]};opacity:{opacity}"/>')

    def border(self, y, above, below, tone='conc'):
        o = line(self.x0, y, self.x1, y, tone=tone, w=1.6, dash='6 4')
        o += t(self.x0 + 8, y - 7, above, size=10.5, weight=700, fill=TONE[tone], caps=True)
        o += t(self.x0 + 8, y + 15, below, size=10.5, weight=700, fill='var(--dif)', caps=True)
        self.o.append(o)

    def point(self, x, y, label, active=False, tone='ink', dx=12, dy=4, anchor='start', sub=''):
        c = TONE[tone]
        fill = c if active else 'var(--paper)'
        o = f'<circle cx="{x}" cy="{y}" r="{8 if active else 6.5}" style="fill:{fill};stroke:{c};stroke-width:1.8"/>'
        o += t(x + dx, y + dy, label, size=11, weight=700 if active else 500, caps=True,
               fill=c if active else 'var(--ink-2)', anchor=anchor)
        if sub and active:
            o += t(x + dx, y + dy + 14, sub, size=10.5, anchor=anchor, fill='var(--ink)')
        self.o.append(o)

    def bar(self, xa, xb, y, label, active=False, tone='ink', dy=-14, sub=''):
        c = TONE[tone]
        o = f'<rect x="{xa}" y="{y - 5}" width="{xb - xa}" height="10" rx="5" style="fill:{c if active else "var(--paper)"};stroke:{c};stroke-width:1.8"/>'
        o += t((xa + xb) / 2, y + dy, label, size=11, weight=700 if active else 500, caps=True,
               fill=c if active else 'var(--ink-2)', anchor='middle')
        if sub and active:
            o += t((xa + xb) / 2, y + 22, sub, size=10.5, anchor='middle')
        self.o.append(o)

    def range(self, x, ya, yb, l1, l2, tone='mix', dx=12):
        c = TONE[tone]
        o = f'<path d="M{x} {ya}V{yb}" style="stroke:{c};stroke-width:4;stroke-linecap:round;opacity:.85"/>'
        o += f'<path d="M{x - 7} {ya}h14M{x - 7} {yb}h14" style="stroke:{c};stroke-width:2"/>'
        o += t(x + dx, (ya + yb) / 2 + 14, l1, size=10.5, weight=700, fill=c, caps=True)
        o += t(x + dx, (ya + yb) / 2 + 27, l2, size=10.5, fill=c)
        self.o.append(o)

    def svg(self):
        return ''.join(self.o)


SERIF = "font-family:var(--serif,serif)"
SCH = 6.25  # serif 12px, px per character (wrap estimate)


def wrap(s, width, ch=SCH):
    words, lines, cur = s.split(), [], ''
    for w in words:
        if cur and (len(cur) + 1 + len(w)) * ch > width:
            lines.append(cur); cur = w
        else:
            cur = f'{cur} {w}'.strip()
    return lines + ([cur] if cur else [])


class Map:
    """Geography as regions, routes and places.

    Geometry is supplied by the lesson script from its real places; this component owns the
    shared land, route, pin and label grammar. Route labels are placed explicitly by the caller
    so they can sit in water or a clear gutter instead of crossing a country or another label.
    """

    def __init__(self, uid):
        self.uid, self.o, self.markers = uid, [], set()

    def region(self, d, tone='muted', opacity=1):
        """Draw one real area from SVG path data, filled by its map key."""
        self.o.append(f'<path d="{d}" style="fill:{WASH[tone]};fill-opacity:{opacity};stroke:{TONE["ink"]};stroke-width:1.25;stroke-linejoin:round"/>')

    def route(self, d, tone='mix', dash=False, arrow=True):
        """Trace a documented route. `d` is path geometry in the map's viewBox."""
        marker = ''
        if arrow:
            marker_id = f'{self.uid}-arrow-{tone}'
            marker = f' marker-end="url(#{marker_id})"'
            self.markers.add((marker_id, tone))
        da = ';stroke-dasharray:5 4' if dash else ''
        self.o.append(f'<path d="{d}"{marker} style="fill:none;stroke:{TONE[tone]};stroke-width:2{da};stroke-linecap:round;stroke-linejoin:round"/>')

    def pin(self, x, y, label='', tone='conc', dx=10, dy=4, anchor='start', sub=''):
        """Mark a named place; dx/dy/anchor explicitly place its label."""
        self.o.append(f'<circle cx="{x:g}" cy="{y:g}" r="4.2" style="fill:var(--paper);stroke:{TONE[tone]};stroke-width:2"/>')
        if label:
            self.o.append(t(x + dx, y + dy, label, size=10.5, anchor=anchor, weight=700, fill=TONE[tone], caps=True))
        if sub:
            self.o.append(t(x + dx, y + dy + 14, sub, size=10, anchor=anchor, fill='var(--ink-2)'))

    def label(self, x, y, text, tone='ink', anchor='middle', sub=''):
        """Place a geographic or time label at an explicit map gutter position."""
        self.o.append(t(x, y, text, size=10.5, anchor=anchor, weight=700, fill=TONE[tone], caps=True))
        if sub:
            self.o.append(t(x, y + 14, sub, size=10, anchor=anchor, fill='var(--ink-2)'))

    def svg(self):
        defs = ''.join(f'<marker id="{ident}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0L8 4L0 8Z" style="fill:{TONE[tone]}"/></marker>' for ident, tone in sorted(self.markers))
        return (f'<defs>{defs}</defs>' if defs else '') + ''.join(self.o)


class Tally:
    """Count and compare real units as dots, one mark per item.

    Each row names the class of items. `items` is a sequence of source-grounded items, either
    plain labels (all use the row tone) or `(label, tone)` pairs. The labels are retained as data
    for authorship, while the marks let students count the distribution by eye.
    """

    def __init__(self, uid, x0=32, x1=568, y0=96, columns=18, step=18, dot=4.2):
        self.uid, self.x0, self.x1, self.cursor = uid, x0, x1, y0
        self.columns, self.step, self.dot = columns, step, dot
        self.o = []

    def row(self, label, items, tone='dif', sub=''):
        if isinstance(items, int):
            items = [None] * items
        items = list(items)
        if not items:
            raise ValueError('a tally row needs at least one real item')
        y = self.cursor
        self.o.append(t(self.x0, y, label, size=10.5, weight=700, fill=TONE[tone], caps=True))
        if sub:
            self.o.append(t(self.x0, y + 14, sub, size=10, fill='var(--ink-2)'))
        dot_x0 = self.x0 + 164
        available = self.x1 - dot_x0
        cols = max(1, min(self.columns, int(available // self.step) + 1))
        for i, item in enumerate(items):
            item_tone = tone
            if isinstance(item, tuple) and len(item) == 2 and item[1] in TONE:
                item_tone = item[1]
            col, row = i % cols, i // cols
            cx = dot_x0 + col * self.step + self.dot
            cy = y - 4 + row * 14
            self.o.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{self.dot:g}" style="fill:{TONE[item_tone]};stroke:var(--paper);stroke-width:1"/>')
        lines = (len(items) + cols - 1) // cols
        self.cursor += max(38, lines * 14 + 20)
        return self

    def legend(self, entries, y=None):
        """Add a compact key as `(tone, label)` entries, wrapping into a second line if needed."""
        cx = self.x0
        cy = self.cursor if y is None else y
        for tone, label in entries:
            width = 18 + len(label) * CH + 12
            if cx + width > self.x1:
                cx, cy = self.x0, cy + 18
            self.o.append(f'<circle cx="{cx + 4:g}" cy="{cy - 4:g}" r="3.6" style="fill:{TONE[tone]}"/>')
            self.o.append(t(cx + 14, cy, label, size=10, fill='var(--ink-2)'))
            cx += width
        self.cursor = max(self.cursor, cy + 22)
        return self

    def svg(self):
        return ''.join(self.o)


class Document:
    """A real legal document drawn as paper: the object the law produces, opened up.

    lines: (kind, text, key) with kind in title | party | clause | place | sign.
    After layout, self.box[key] = (x0, y0, x1, y1) so steps can bracket, highlight or stamp
    exactly the clauses they read.
    """

    def __init__(self, uid, x, y, w, lines, lead=18, indent=78, foot=0):
        self.uid, self.x, self.y, self.w, self.lead, self.indent = uid, x, y, w, lead, indent
        self.box, self.parts = {}, []
        cy, pad = y + 30, 16
        for kind, text, key in lines:
            if kind == 'title':
                self.parts.append(t(x + w / 2, cy, text, size=11.5, anchor='middle', caps=True, weight=700, ls='.12em'))
                self.box[key] = (x + pad, cy - 12, x + w - pad, cy + 4); cy += 26
            elif kind == 'sign':
                a, b = text
                cy += 18
                half = (w - 3 * pad) / 2
                for i, name in enumerate((a, b)):
                    sx = x + pad + i * (half + pad)
                    self.parts.append(line(sx, cy, sx + half, cy, w=1))
                    self.parts.append(t(sx + half / 2, cy + 14, name, size=10, anchor='middle', fill='var(--ink-2)'))
                    self.box[f'{key}{i}'] = (sx, cy - 18, sx + half, cy + 18)
                cy += 26
            else:
                label, body = text if isinstance(text, tuple) else ('', text)
                y0 = cy - 11
                indent = 0
                if label:
                    self.parts.append(t(x + pad, cy, label, size=10, weight=700, caps=True, fill='var(--ink-2)'))
                    indent = self.indent
                for i, ln in enumerate(wrap(body, w - 2 * pad - indent)):
                    st = f"{SERIF};font-size:12px;fill:var(--ink)" + (';font-style:italic' if kind == 'place' else '')
                    self.parts.append(f'<text x="{x + pad + indent:g}" y="{cy:g}" style="{st}">{ln}</text>')
                    cy += self.lead
                self.box[key] = (x + pad, y0, x + w - pad, cy - self.lead + 5)
                cy += 6 if kind == 'clause' else 4
        self.h = cy - y + 8 + foot

    def paper(self):
        x, y, w, h = self.x, self.y, self.w, self.h
        return (f'<path d="M{x} {y}H{x + w - 18}L{x + w} {y + 18}V{y + h}H{x}Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
                f'<path d="M{x + w - 18} {y}V{y + 18}H{x + w}" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1"/>')

    def highlight(self, keys, tone='conc'):
        o = ''
        for k in keys:
            x0, y0, x1, y1 = self.box[k]
            o += f'<rect x="{x0 - 5:g}" y="{y0 - 3:g}" width="{x1 - x0 + 10:g}" height="{y1 - y0 + 6:g}" style="fill:{WASH[tone]};stroke:none"/>'
        return o

    def bracket(self, keys, side, label, sub='', tone='conc', gap=12):
        ys = [self.box[k][1] for k in keys] + [self.box[k][3] for k in keys]
        y0, y1 = min(ys) - 2, max(ys) + 2
        c = TONE[tone]
        if side == 'left':
            bx = self.x - gap
            o = f'<path d="M{bx + 6} {y0}H{bx}V{y1}H{bx + 6}" style="fill:none;stroke:{c};stroke-width:1.8"/>'
            o += t(bx - 8, (y0 + y1) / 2, label, size=10.5, anchor='end', caps=True, weight=700, fill=c)
            if sub:
                o += t(bx - 8, (y0 + y1) / 2 + 14, sub, size=10, anchor='end', fill='var(--ink-2)')
        else:
            bx = self.x + self.w + gap
            o = f'<path d="M{bx - 6} {y0}H{bx}V{y1}H{bx - 6}" style="fill:none;stroke:{c};stroke-width:1.8"/>'
            o += t(bx + 8, (y0 + y1) / 2, label, size=10.5, caps=True, weight=700, fill=c)
            if sub:
                o += t(bx + 8, (y0 + y1) / 2 + 14, sub, size=10, fill='var(--ink-2)')
        return o

    def stamp(self, text, cx, cy, tone='dif', angle=-8):
        c = TONE[tone]
        wpx = len(text) * 9.6 + 24
        return (f'<g transform="rotate({angle} {cx} {cy})"><rect x="{cx - wpx / 2:g}" y="{cy - 17}" width="{wpx:g}" height="30" rx="3" '
                f'style="fill:none;stroke:{c};stroke-width:2.2;opacity:.9"/>'
                f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" style="{MONO};font-size:15px;font-weight:700;letter-spacing:.14em;fill:{c};opacity:.9">{text}</text></g>')


def statute(x, y, w, art, parts, source='', tone='conc'):
    """A statute cut: the article's own words, with the operative phrase marked.
    parts: list of (text, marked) runs, wrapped together."""
    words = []
    for txt, marked in parts:
        words += [(wd, marked) for wd in txt.split()]
    lines, cur, cw = [], [], 0
    width = w - 24
    for wd, m in words:
        ln = (len(wd) + 1) * SCH
        if cur and cw + ln > width:
            lines.append(cur); cur, cw = [], 0
        cur.append((wd, m)); cw += ln
    if cur:
        lines.append(cur)
    h = 34 + 18 * len(lines)
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
    o += f'<rect x="{x}" y="{y}" width="4" height="{h}" style="fill:{TONE[tone]}"/>'
    o += t(x + 14, y + 17, art, size=10.5, caps=True, weight=700)
    if source:
        o += t(x + w - 10, y + 17, source, size=10, anchor='end', fill='var(--ink-2)')
    cy = y + 36
    for ln in lines:
        runs, prev = [], None
        for wd, m in ln:
            if runs and runs[-1][1] == m:
                runs[-1][0].append(wd)
            else:
                runs.append(([wd], m))
        spans = ''
        for k, (wds, m) in enumerate(runs):
            txt = (' ' if k else '') + ' '.join(wds)
            spans += (f'<tspan style="fill:{TONE[tone]};font-weight:700">{txt}</tspan>' if m else f'<tspan>{txt}</tspan>')
        if any(m for _, m in ln):
            o += f'<path d="M{x + 8} {cy - 10}V{cy + 3}" style="stroke:{TONE[tone]};stroke-width:2"/>'
        o += f'<text x="{x + 14}" y="{cy}" xml:space="preserve" style="{SERIF};font-size:12px;fill:var(--ink)">{spans}</text>'
        cy += 18
    return o, h


class Clock:
    """A procedural clock: real days as columns, scenarios as lanes, incidents as marks on the day they happen.

    days: list of (name, label, workday). Lanes are drawn top to bottom; each lane is a thin line
    with marks placed at day indexes (fractions allowed). Weekend columns are shaded through every lane.
    """

    def __init__(self, uid, x0, x1, y0, days, pre=None):
        self.uid, self.x0, self.x1, self.y0, self.days, self.pre = uid, x0, x1, y0, days, pre
        self.cw = (x1 - x0) / len(days)
        self.o, self.lanes_y = [], []

    def cx(self, d):
        return self.x0 + self.cw * (d + .5)

    def header(self, bottom):
        o = ''
        for i, (name, lab, work) in enumerate(self.days):
            x = self.x0 + i * self.cw
            if not work:
                o += f'<rect x="{x:g}" y="{self.y0}" width="{self.cw:g}" height="{bottom - self.y0}" style="fill:var(--paper-2);opacity:.9"/>'
            o += f'<rect x="{x:g}" y="{self.y0}" width="{self.cw:g}" height="40" style="fill:none;stroke:var(--ink);stroke-width:1"/>'
            o += t(x + self.cw / 2, self.y0 + 16, name, size=10, anchor='middle', caps=True, fill='var(--ink-2)')
            o += t(x + self.cw / 2, self.y0 + 32, lab, size=11.5, anchor='middle', weight=700, fill='var(--ink)' if work else 'var(--muted)')
        if self.pre:
            px0 = self.x0 - self.pre[0]
            o += f'<rect x="{px0}" y="{self.y0}" width="{self.pre[0]}" height="40" style="fill:var(--conc-wash);stroke:var(--conc);stroke-width:1"/>'
            o += t(px0 + self.pre[0] / 2, self.y0 + 25, self.pre[1], size=11, anchor='middle', weight=700, fill='var(--conc)')
        self.o.insert(0, o)

    def lane(self, y, title, sub=''):
        o = t(self.x0, y - 20, title, size=10.5, caps=True, weight=700)
        if sub:
            o += t(self.x1, y - 20, sub, size=10, anchor='end', fill='var(--ink-2)')
        o += line(self.x0, y, self.x1, y, tone='muted', w=1)
        self.o.append(o)

    def votes(self, y, at, hollow=(), tone='ink'):
        """at: list of day indexes, one per vote; several on a day stack sideways."""
        seen = {}
        o = ''
        for d in at:
            k = seen.get(d, 0); seen[d] = k + 1
            x = self.cx(d) - self.cw / 2 + 8 + (k % 5) * 9
            yy = y - 6 + (k // 5) * 12
            o += f'<circle cx="{x:g}" cy="{yy}" r="3.6" style="fill:{TONE[tone]}"/>'
        for d in hollow:
            x = self.cx(d) + self.cw / 2 - 12
            o += f'<circle cx="{x:g}" cy="{y - 6}" r="4.2" style="fill:var(--paper);stroke:{TONE["conc"]};stroke-width:1.6"/>'
        self.o.append(o)

    def event(self, y, d, label, sub='', tone='conc', below=24, anchor='middle'):
        x = self.cx(d)
        o = f'<path d="M{x:g} {y - 14}V{y + 8}" style="stroke:{TONE[tone]};stroke-width:2.4"/>'
        o += f'<path d="M{x - 5:g} {y - 14}h10l-5 7z" style="fill:{TONE[tone]}"/>'
        o += t(x, y + below, label, size=10.5, weight=700, caps=True, fill=TONE[tone], anchor=anchor)
        if sub:
            o += t(x, y + below + 14, sub, size=10.5, anchor=anchor)
        self.o.append(o)

    def run(self, y, d0, x_end, label, tone='mix', dash=False):
        x = self.cx(d0)
        da = ';stroke-dasharray:6 4' if dash else ''
        o = f'<path d="M{x:g} {y}H{x_end - 8:g}" style="stroke:{TONE[tone]};stroke-width:3{da}"/><path d="M{x_end:g} {y}l-9 -5v10z" style="fill:{TONE[tone]}"/>'
        o += t(x_end, y - 8, label, size=10.5, anchor='end', weight=700, fill=TONE[tone])
        self.o.append(o)

    def svg(self):
        return ''.join(self.o)


class Calendar:
    """A real Gregorian month laid out as a countable date grid.

    Weekends are shaded; exact dates, holidays and deadlines come from the lesson script via
    `mark()`. Long event names belong in a separate gutter or legend, not squeezed into cells.
    """

    WEEKDAYS = ('SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SÁB', 'DOM')

    def __init__(self, uid, year, month, x=42, y=80, w=516, h=430, weekdays=None):
        self.uid, self.year, self.month = uid, year, month
        self.x, self.y, self.w, self.h = x, y, w, h
        self.weekdays = weekdays or self.WEEKDAYS
        self.weeks = _calendar.Calendar(firstweekday=0).monthdayscalendar(year, month)
        self.marks = {}

    def mark(self, day, label='', tone='conc'):
        if day < 1 or day > _calendar.monthrange(self.year, self.month)[1]:
            raise ValueError(f'{self.year}-{self.month:02d} has no day {day}')
        self.marks[day] = (label, tone)
        return self

    def svg(self):
        head_h = 24
        cell_w = self.w / 7
        cell_h = (self.h - head_h) / len(self.weeks)
        o = ''
        for col, name in enumerate(self.weekdays):
            xx = self.x + col * cell_w
            fill = 'var(--paper-2)' if col >= 5 else 'var(--paper)'
            o += f'<rect x="{xx:g}" y="{self.y:g}" width="{cell_w:g}" height="{head_h:g}" style="fill:{fill};stroke:var(--ink);stroke-width:1"/>'
            o += t(xx + cell_w / 2, self.y + 16, name, size=9.5, anchor='middle', weight=700, fill='var(--ink-2)')
        for row, week in enumerate(self.weeks):
            for col, day in enumerate(week):
                xx, yy = self.x + col * cell_w, self.y + head_h + row * cell_h
                fill = 'var(--paper-2)' if col >= 5 else 'var(--paper)'
                o += f'<rect x="{xx:g}" y="{yy:g}" width="{cell_w:g}" height="{cell_h:g}" style="fill:{fill};stroke:var(--ink);stroke-width:.8"/>'
                if day:
                    o += t(xx + 5, yy + 14, str(day), size=10.5, weight=600, fill='var(--ink-2)')
                    if day in self.marks:
                        label, tone = self.marks[day]
                        cx, cy = xx + cell_w / 2, yy + cell_h / 2 + 2
                        o += f'<circle cx="{cx:g}" cy="{cy:g}" r="4.2" style="fill:{TONE[tone]}"/>'
                        if label:
                            room = cell_w - 8
                            if len(label) * CH > room:
                                WARN.append(f'{self.uid} day {day}: calendar label "{label}" exceeds the cell; move it to a gutter legend')
                            else:
                                o += t(cx, yy + cell_h - 5, label, size=8.5, anchor='middle', weight=600, fill=TONE[tone])
        return o


class Path:
    """A decision path: questions on a trunk, each exit a named legal consequence.

    Questions sit left of the trunk (right-aligned); exits leave to the right and end in a card;
    the 'continue' answer is written beside the trunk. The active question is inked, the rest muted.
    """

    def __init__(self, uid, trunk=232, card_x=330, card_w=240):
        self.uid, self.tx, self.cx, self.cw = uid, trunk, card_x, card_w
        self.o = []

    def card(self, x, y, w, head, lines, tone, active=True):
        c = TONE[tone] if active else 'var(--ink-2)'
        h = 26 + 15 * len(lines)
        o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="fill:{WASH[tone] if active else "var(--paper)"};stroke:{c};stroke-width:1.4"/>'
        o += t(x + 12, y + 18, head, size=10.5, caps=True, weight=700, fill=c)
        for i, ln in enumerate(lines):
            o += t(x + 12, y + 34 + 15 * i, ln, size=10.5, fill='var(--ink)' if active else 'var(--ink-2)')
        return o, h

    def question(self, y, q, exit_label, head, lines, tone='conc', go='', active=True, next_y=None):
        ink = 'var(--ink)' if active else 'var(--ink-2)'
        o = ''
        if next_y is not None:
            o += line(self.tx, y + 9, self.tx, next_y - 9, w=2.2 if active else 1.4)
            if go:
                o += t(self.tx - 14, y + 36, go, size=10.5, anchor='end', weight=700 if active else 500, fill=ink)
        o += line(self.tx + 9, y, self.cx, y, tone=tone if active else 'muted', w=2 if active else 1.2)
        o += t(self.tx + 14, y - 8, exit_label, size=10.5, weight=700, fill=TONE[tone] if active else 'var(--ink-2)')
        o += f'<circle cx="{self.tx}" cy="{y}" r="9" style="fill:{"var(--ink)" if active else "var(--paper)"};stroke:var(--ink);stroke-width:2"/>'
        for i, ln in enumerate(q):
            o += t(self.tx - 18, y - 3 + 15 * i - 7 * (len(q) - 1), ln, size=11.5, anchor='end', weight=700 if active else 500, fill=ink)
        c, h = self.card(self.cx, y - 18, self.cw, head, lines, tone, active)
        self.o.append(o + c)

    def svg(self):
        return ''.join(self.o)


class Timeline:
    """Real dates on a real axis. Events are stems above the axis (tone = what kind of event);
    spans are bands; links are arcs below the axis that tie one event to an earlier one."""

    def __init__(self, uid, x0, x1, y, a, b, step=10):
        self.uid, self.x0, self.x1, self.y, self.a, self.b = uid, x0, x1, y, a, b
        self.o = []
        o = line(x0, y, x1, y, w=1.6)
        for yr in range((a // step + 1) * step if a % step else a, b + 1, step):
            x = self.x(yr)
            o += line(x, y, x, y + 6, w=1)
            o += t(x, y + 20, str(yr), size=10, anchor='middle', fill='var(--muted)')
        self.o.append(o)

    def x(self, yr):
        return self.x0 + (self.x1 - self.x0) * (yr - self.a) / (self.b - self.a)

    def event(self, yr, h, label, tone='conc', sub='', anchor='middle', mark='tri'):
        x = self.x(yr)
        top = self.y - h
        o = f'<path d="M{x:g} {self.y}V{top + 6}" style="stroke:{TONE[tone]};stroke-width:2"/>'
        if mark == 'tri':
            o += f'<path d="M{x - 6:g} {top + 8}h12l-6 -11z" style="fill:{TONE[tone]}"/>'
        else:
            o += f'<circle cx="{x:g}" cy="{top + 2}" r="5" style="fill:{TONE[tone]}"/>'
        o += t(x, top - 9, label, size=11, weight=700, anchor=anchor, fill=TONE[tone])
        if sub:
            o += t(x, top - 23, sub, size=10, anchor=anchor, fill='var(--ink-2)')
        self.o.append(o)

    def span(self, y0, a, b, label, tone='mix', open_end=False):
        xa, xb = self.x(a), self.x(b)
        o = f'<rect x="{xa:g}" y="{y0}" width="{xb - xa:g}" height="16" style="fill:{WASH[tone]};stroke:{TONE[tone]};stroke-width:1.2"/>'
        if open_end:
            o += f'<path d="M{xb:g} {y0 + 8}l8 -6v12z" style="fill:{TONE[tone]}"/>'
        o += t(xa + 8, y0 + 12, label, size=10.5, weight=700, fill=TONE[tone])
        self.o.append(o)

    def link(self, from_yr, to_yr, depth, label, tone='mix', sub=''):
        xa, xb = self.x(from_yr), self.x(to_yr)
        y = self.y + 30
        o = f'<path d="M{xa:g} {y}C{xa:g} {y + depth} {xb:g} {y + depth} {xb:g} {y + 6}" style="fill:none;stroke:{TONE[tone]};stroke-width:1.8;stroke-dasharray:5 3"/>'
        o += f'<path d="M{xb:g} {y}l-5 9h10z" style="fill:{TONE[tone]}"/>'
        o += f'<circle cx="{xa:g}" cy="{y}" r="5" style="fill:{TONE[tone]}"/>'
        lx = (xa + xb) / 2
        o += t(lx, y + depth * .75 + 22, label, size=10.5, weight=700, anchor='middle', fill=TONE[tone])
        if sub:
            o += t(lx, y + depth * .75 + 36, sub, size=10.5, anchor='middle')
        self.o.append(o)

    def svg(self):
        return ''.join(self.o)


class Strata:
    """Named, dated layers shown as a section through the history of a legal idea.

    Periods stay at the precision supplied by the lesson (for example, "anos 1990"). Layers
    stack without arrows; dates occupy a fixed left gutter and the legal material sits in bands.
    """

    def __init__(self, uid, x=56, y=76, w=488, date_w=124, layer_h=48, gap=2):
        self.uid, self.x, self.y, self.w = uid, x, y, w
        self.date_w, self.layer_h, self.gap = date_w, layer_h, gap
        self.cursor, self.o = y, []

    def layer(self, period, label, tone='muted', sub=''):
        date_lines = wrap(period, self.date_w - 14, ch=CH)
        label_lines = wrap(label, self.w - self.date_w - 26, ch=CH)
        sub_lines = wrap(sub, self.w - self.date_w - 26, ch=CH) if sub else []
        height = max(self.layer_h, 22 + max(len(date_lines), len(label_lines)) * 14 + len(sub_lines) * 13)
        y = self.cursor
        self.o.append(f'<rect x="{self.x:g}" y="{y:g}" width="{self.w:g}" height="{height:g}" style="fill:{WASH[tone]};stroke:{TONE["ink"]};stroke-width:1"/>')
        self.o.append(line(self.x + self.date_w, y, self.x + self.date_w, y + height, tone='ink', w=1))
        for i, part in enumerate(date_lines):
            self.o.append(t(self.x + 8, y + 18 + 14 * i, part, size=10, weight=700, fill=TONE[tone]))
        for i, part in enumerate(label_lines):
            self.o.append(t(self.x + self.date_w + 12, y + 18 + 14 * i, part, size=10.5, weight=700 if i == 0 else 500, fill='var(--ink)'))
        for i, part in enumerate(sub_lines):
            self.o.append(t(self.x + self.date_w + 12, y + 20 + 14 * len(label_lines) + 13 * i, part, size=9.5, fill='var(--ink-2)'))
        self.cursor += height + self.gap
        return self

    def svg(self):
        return ''.join(self.o)
