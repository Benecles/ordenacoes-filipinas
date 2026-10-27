"""Drawing helpers shared by the parts. Output obeys tools/lesson_renderer.py's SVG whitelist: presentation attributes
only (no style, class, defs or patterns). Colours are the house tokens via var(), which SVG attributes resolve, so
every part follows light and dark with the page (verified in the browser, 27/10)."""
from __future__ import annotations

from html import escape

INK, INK2, MUTED, PAPER, PAPER2 = "var(--ink)", "var(--ink-2)", "var(--muted)", "var(--paper)", "var(--paper-2)"
GRID, CONC, DIF = "var(--grid-major)", "var(--conc)", "var(--dif)"
MONO = "var(--mono, 'IBM Plex Mono', ui-monospace, monospace)"
SERIF = "var(--serif, 'Spectral', Georgia, serif)"
SANS = "var(--sans, 'Archivo', system-ui, sans-serif)"


def esc(s: str) -> str:
    return escape(str(s), quote=True)


def attrs(**kw) -> str:
    out = []
    for k, v in kw.items():
        if v is None:
            continue
        k = k.rstrip("_").replace("_", "-")
        if isinstance(v, float):
            v = f"{v:.1f}".rstrip("0").rstrip(".")
        out.append(f'{k}="{esc(v)}"')
    return " ".join(out)


def rect(x, y, w, h, **kw) -> str:
    return f"<rect {attrs(x=x, y=y, width=w, height=h, **kw)}/>"


def line(x1, y1, x2, y2, **kw) -> str:
    return f"<line {attrs(x1=x1, y1=y1, x2=x2, y2=y2, **kw)}/>"


def circle(cx, cy, r, **kw) -> str:
    return f"<circle {attrs(cx=cx, cy=cy, r=r, **kw)}/>"


def path(d, **kw) -> str:
    return f"<path {attrs(d=d, **kw)}/>"


def text(x, y, s, size=13, family=MONO, fill=INK, weight=None, anchor=None, **kw) -> str:
    a = attrs(x=x, y=y, font_size=size, font_family=family, font_weight=weight, fill=fill, text_anchor=anchor, **kw)
    return f"<text {a}>{esc(s)}</text>"


def hatch(x, y, w, h, step=9, **kw) -> list[str]:
    """45° hatching clipped to a rectangle by arithmetic (patterns are not allowed)."""
    out, k = [], -h
    while k < w:
        t0, t1 = max(0.0, -k / h), min(1.0, (w - k) / h)
        if t0 < t1:
            out.append(line(x + k + t0 * h, y + h - t0 * h, x + k + t1 * h, y + h - t1 * h, **kw))
        k += step
    return out


def hit(x, y, w, h) -> str:
    """An invisible but clickable target (opacity 0 still receives pointer events)."""
    return rect(x, y, w, h, fill="#000", opacity="0")


def wrap(s: str, width: int) -> list[str]:
    words, lines, cur = s.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + ([cur] if cur else [])


def callout_band(x, y, w, hint: str) -> list[str]:
    """The fixed strip where a pressed object's sentence appears; idle, it carries the hint."""
    return [line(x, y, x + w, y, stroke=GRID, stroke_width=1),
            text(x, y + 30, hint, size=14, family=SERIF, fill=MUTED)]


def callout(x, y, w, sentence: str) -> list[str]:
    """Covers the hint and writes the sentence, at most two lines, in the same place every time (text never moves)."""
    lines = wrap(sentence, 96)[:2]
    out = [rect(x, y + 1, w, 52, fill=PAPER2)]
    for i, ln in enumerate(lines):
        out.append(text(x, y + 26 + i * 22, ln, size=16, family=SERIF, fill=INK))
    return out


def svg(width, height, title: str, body: list[str]) -> str:
    return (f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            + "".join(body) + "</svg>")
