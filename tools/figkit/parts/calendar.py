"""calendar: the prazo counted on a real calendar (from the chairman-praised specimen, 07/10).

params:
  heading      str   top line, e.g. "Abril de 2015 · prazo de 15 dias úteis (CPC, arts. 219 e 1.003, § 5º)"
  start        date  the day the prazo is triggered (publicação, juntada do AR...); it never counts (art. 224)
  start_label  str   what happened that day, e.g. "publicada"
  days         int   length of the prazo
  rule         "business" (dias úteis, art. 219) | "calendar" (dias corridos)
  holidays     {date: name}   non-business days inside the span
  marks        {date: label}  other dated events to write in their cell (e.g. "disponibilizada")
  notes        {object_id: sentence}  optional overrides for the pressed sentence (ids: inicio, fim, feriado-YYYY-MM-DD)
The part computes every count itself; the writer supplies facts, never positions.
Under "calendar", a last day that falls on a non-business day moves to the next business day (art. 224, § 1º).
"""
from __future__ import annotations

import datetime as dt

from . import svg as S

WEEK = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
MONTHS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def _d(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def count_days(start: dt.date, days: int, rule: str, holidays: set) -> tuple[dict, dt.date]:
    def business(d):
        return d.weekday() < 5 and d not in holidays
    counted, d, n = {}, start, 0
    while n < days:
        d += dt.timedelta(1)
        if rule == "calendar" or business(d):
            n += 1
            counted[d] = n
    end = d
    if rule == "calendar":
        while not business(end):
            end += dt.timedelta(1)
    return counted, end


def build(p: dict) -> tuple[str, list[dict]]:
    start, days, rule = _d(p["start"]), int(p["days"]), p.get("rule", "business")
    if rule not in ("business", "calendar"):
        raise ValueError("calendar: rule must be business or calendar")
    hol = {_d(k): v for k, v in (p.get("holidays") or {}).items()}
    marks = {_d(k): v for k, v in (p.get("marks") or {}).items()}
    notes = p.get("notes") or {}
    counted, end = count_days(start, days, rule, set(hol))
    first = min([start, *marks]) - dt.timedelta(days=min([start, *marks]).weekday())
    last = end + dt.timedelta(days=6 - end.weekday())
    weeks = ((last - first).days + 1) // 7
    if weeks > 7:
        raise ValueError("calendar: span over 7 weeks; split the prazo or use another part")

    W, X0, Y0, CW = 1080, 40, 96, 142
    CH = 84 if weeks <= 5 else 70
    grid_bottom = Y0 + weeks * CH
    band_y = grid_bottom + 18
    H = band_y + 62
    b: list[str] = [S.text(X0, 36, p["heading"], size=12, fill=S.INK2)]
    for i, w in enumerate(WEEK):
        b.append(S.text(X0 + i * CW + 10, Y0 - 14, w, size=11, fill=S.INK2))

    cells = {}
    for k in range(weeks * 7):
        day = first + dt.timedelta(k)
        r, c = divmod(k, 7)
        x, y = X0 + c * CW, Y0 + r * CH
        cells[day] = (x, y)
        weekend, inside = day.weekday() >= 5, first <= day <= last
        b.append(S.rect(x, y, CW - 6, CH - 6, fill=S.PAPER2 if weekend else S.PAPER, stroke=S.GRID, stroke_width=1))
        if day in hol:
            b += S.hatch(x, y, CW - 6, CH - 6, stroke=S.CONC, stroke_width=1.5, opacity="0.4")
        dim = weekend or day in hol
        label = f"{day.day:02d}" + (f" {MONTHS[day.month - 1]}" if day.day == 1 or k == 0 else "")
        b.append(S.text(x + 10, y + 22, label, size=15, fill=S.MUTED if dim else S.INK, weight="500"))
        word = hol.get(day) or marks.get(day) or (p.get("start_label") if day == start else None)
        if word:
            for j, part in enumerate(S.wrap(word, 16)[:2][::-1]):
                b.append(S.text(x + 10, y + CH - 16 - j * 14, part, size=11, fill=S.CONC if day in hol else S.INK2))
        if day in counted:
            n, is_end = counted[day], day == end
            col = S.CONC if is_end else S.DIF
            b.append(S.circle(x + CW - 30, y + CH / 2 - 3, 17, fill=S.CONC if is_end else "none", stroke=col, stroke_width=2))
            b.append(S.text(x + CW - 30, y + CH / 2 + 2, str(n), size=13, fill=S.PAPER if is_end else col, anchor="middle", weight="600"))
        elif day == end:  # calendar rule, moved to the next business day
            b.append(S.circle(x + CW - 30, y + CH / 2 - 3, 17, fill=S.CONC, stroke=S.CONC, stroke_width=2))
            b.append(S.text(x + CW - 30, y + CH / 2 + 2, "fim", size=11, fill=S.PAPER, anchor="middle", weight="600"))

    b += S.callout_band(X0, band_y, 7 * CW - 6, "Toque no dia da publicação, num feriado ou no último dia para ver por que conta ou não.")

    def fmt(d):
        return f"{d.day:02d}/{d.month:02d}"

    objects, targets, states = [], [], []

    def add(oid, day, label, sentence):
        x, y = cells[day]
        objects.append({"id": oid, "label": label, "description": sentence})
        targets.append(f'<g data-object="{oid}">{S.hit(x, y, CW - 6, CH - 6)}</g>')
        ring = S.rect(x - 3, y - 3, CW, CH, fill="none", stroke=S.CONC, stroke_width=3)
        states.append(f'<g data-object-state="{oid}" data-state="active">{ring}{"".join(S.callout(X0, band_y, 7 * CW - 6, sentence))}</g>')

    unit = "dia útil" if rule == "business" else "dia"
    first_counted = min(counted)
    add("inicio", start, f"{fmt(start)}, {p.get('start_label', 'início')}",
        notes.get("inicio") or f"{fmt(start)} · {p.get('start_label', 'início')}: o dia do começo não conta (art. 224); "
                               f"a contagem começa no {unit} seguinte, {fmt(first_counted)}.")
    for day, name in sorted(hol.items()):
        if day in cells:
            oid = f"feriado-{day.isoformat()}"
            add(oid, day, f"{fmt(day)}, {name}",
                notes.get(oid) or (f"{fmt(day)} · {name}: não é dia útil, então não entra na contagem (art. 219)."
                                   if rule == "business" else f"{fmt(day)} · {name}: em dias corridos, conta como qualquer outro."))
    moved = rule == "calendar" and end not in counted
    add("fim", end, f"{fmt(end)}, último dia",
        notes.get("fim") or (f"{fmt(end)} · o prazo acaba aqui: é o {days}º {unit} depois de {fmt(start)}."
                             if not moved else f"{fmt(end)} · o {days}º dia caiu em dia não útil; o último dia passa para o primeiro dia útil seguinte (art. 224, § 1º)."))

    title = p.get("title") or f"Calendário com a contagem de {days} {'dias úteis' if rule == 'business' else 'dias'} a partir de {fmt(start)}"
    return S.svg(W, H, title, b + targets + states), objects
