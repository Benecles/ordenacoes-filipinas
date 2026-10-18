#!/usr/bin/env python3
"""Build the three approved PROC-R3 Aula 04 rebuild-2 figure panels.

The prose remains authored in aula-04.html. This script owns only the inline SVG
between each stable FIGn marker, so regeneration cannot replace lesson text.
"""
from pathlib import Path
import re
import sys

from figkit import line, svg, t

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "courses/processo-civil-i/aula-04.html"


def node(x, y, tone="ink", r=7):
    stroke = {"ink": "var(--ink)", "conc": "var(--conc)", "dif": "var(--dif)"}[tone]
    return f'<circle cx="{x}" cy="{y}" r="{r}" style="fill:var(--paper);stroke:{stroke};stroke-width:2.4"/>'


def arrow(x, y, tone="dif"):
    color = {"ink": "var(--ink)", "conc": "var(--conc)", "dif": "var(--dif)"}[tone]
    return f'<path d="M{x-8} {y-6}L{x} {y}L{x-8} {y+6}" style="fill:none;stroke:{color};stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round"/>'


def fig1():
    o = t(300, 36, "DUAS RELAÇÕES", size=20, anchor="middle", weight=700, fill="var(--ink-2)")
    o += t(300, 83, "DESPEJO", size=22, anchor="middle", weight=700)
    o += t(145, 119, "LOCADOR", size=22, anchor="middle", weight=600)
    o += t(455, 119, "LOCATÁRIO", size=22, anchor="middle", weight=600)
    o += line(170, 142, 430, 142, tone="conc", w=3)
    o += node(170, 142, "conc") + node(430, 142, "conc")
    o += t(300, 172, "RELAÇÃO DISCUTIDA", size=18, anchor="middle", fill="var(--conc)", weight=700)
    o += line(34, 192, 566, 192, tone="ink", w=1)
    o += t(300, 226, "SUBLOCAÇÃO", size=20, anchor="middle", weight=700, fill="var(--ink-2)")
    o += t(198, 265, "LOCATÁRIO", size=22, anchor="middle", weight=600)
    o += t(418, 265, "SUBLOCATÁRIO", size=22, anchor="middle", weight=600)
    o += line(225, 286, 391, 286, tone="ink", w=2)
    o += node(225, 286) + node(391, 286)
    o += t(300, 320, "o direito do sublocatário depende da preservação", size=16, anchor="middle", fill="var(--ink-2)")
    o += t(300, 344, "do direito do locatário", size=18, anchor="middle", fill="var(--ink-2)")
    o += t(300, 383, "INTERESSE REFLEXO · ASSISTÊNCIA SIMPLES", size=20, anchor="middle", fill="var(--dif)", weight=700)
    return svg("0 0 600 405", o, label="Relação de despejo entre locador e locatário e relação de sublocação entre locatário e sublocatário; a segunda dá o interesse reflexo para assistência simples.")


def fig2():
    o = t(300, 32, "MESMO DESPEJO · PRAZO RECURSAL ENCERRADO", size=18, anchor="middle", weight=700, fill="var(--ink-2)")
    # First unboxed impression: blank disposition field, route remains open.
    o += t(32, 77, "CAMPO EM BRANCO", size=19, weight=700, fill="var(--dif)")
    o += t(34, 104, "DISPOSIÇÃO DO LOCATÁRIO", size=16, fill="var(--ink-2)")
    o += line(34, 136, 220, 136, tone="ink", w=1.5)
    o += t(34, 164, "RECURSO", size=18, weight=700)
    o += line(150, 158, 295, 158, tone="dif", w=3) + arrow(295, 158, "dif")
    o += node(315, 158, "dif", r=10)
    o += t(344, 165, "ASSISTENTE RECORRE", size=18, weight=700, fill="var(--dif)")
    o += line(34, 190, 566, 190, tone="ink", w=1)
    # Second impression: a generic signature mark crosses the same appeal line.
    o += t(32, 229, "RENÚNCIA EXPRESSA", size=19, weight=700, fill="var(--conc)")
    o += t(34, 256, "DISPOSIÇÃO DO LOCATÁRIO", size=16, fill="var(--ink-2)")
    o += line(34, 288, 220, 288, tone="ink", w=1.5)
    o += t(34, 318, "RECURSO", size=18, weight=700)
    o += line(150, 312, 190, 312, tone="conc", w=3) + arrow(190, 312, "conc")
    o += node(210, 312, "dif", r=10)
    o += f'<path d="M192 309c7-17 12 17 19-2 6-15 11 9 17 2 6-7 10-4 15 0" style="fill:none;stroke:var(--ink);stroke-width:2.5;stroke-linecap:round"/>'
    o += line(228, 312, 250, 312, tone="conc", w=3)
    o += line(266, 296, 266, 328, tone="conc", w=4)
    o += t(288, 317, "A ESCOLHA VINCULA", size=18, weight=700, fill="var(--conc)")
    o += t(288, 348, "O ASSISTENTE", size=18, weight=700, fill="var(--conc)")
    return svg("0 0 600 360", o, label="Duas impressões do mesmo processo de despejo com prazo recursal encerrado: campo de disposição em branco deixa aberta a via do assistente; renúncia expressa do locatário encerra a via.")


def fig3():
    o = t(150, 38, "DESPEJO", size=20, anchor="middle", weight=700, fill="var(--ink-2)")
    o += t(94, 81, "LOCADOR", size=20, anchor="middle", weight=600)
    o += t(300, 81, "LOCATÁRIO", size=20, anchor="middle", weight=600)
    o += t(500, 81, "SUBLOCATÁRIO", size=20, anchor="middle", weight=600)
    o += line(120, 103, 274, 103, tone="conc", w=2.7) + node(120, 103, "conc") + node(274, 103, "conc")
    o += line(326, 103, 470, 103, tone="ink", w=2) + node(326, 103) + node(470, 103)
    o += t(300, 140, "REFLEXO · SIMPLES", size=18, anchor="middle", weight=700, fill="var(--dif)")
    o += line(28, 163, 572, 163, tone="ink", w=1)
    o += t(300, 197, "AÇÃO DE UM CONDÔMINO", size=20, anchor="middle", weight=700, fill="var(--ink-2)")
    o += t(150, 246, "UM CONDÔMINO", size=20, anchor="middle", weight=600)
    o += t(440, 246, "OUTRO CONDÔMINO", size=20, anchor="middle", weight=600)
    o += line(176, 268, 414, 268, tone="conc", w=2.7) + node(176, 268, "conc") + node(414, 268, "conc")
    o += t(300, 301, "COTITULAR DA SITUAÇÃO DISCUTIDA", size=18, anchor="middle", fill="var(--conc)", weight=700)
    o += t(300, 332, "sentença pode influir na relação com o adversário", size=16, anchor="middle", fill="var(--conc)")
    o += t(300, 371, "RELAÇÃO DIRETA · ASSISTÊNCIA LITISCONSORCIAL", size=17, anchor="middle", fill="var(--dif)", weight=700)
    return svg("0 0 600 394", o, label="Mapa comparativo: a sublocação liga o interesse reflexo do sublocatário à assistência simples; o condômino é cotitular da situação discutida e a sentença pode influir na relação com o adversário.")


FIGURES = {"FIG1": fig1, "FIG2": fig2, "FIG3": fig3}


def build():
    s = PAGE.read_text(encoding="utf-8")
    for key, maker in FIGURES.items():
        start, end = f"<!-- {key}-BEGIN -->", f"<!-- {key}-END -->"
        if s.count(start) != 1 or s.count(end) != 1:
            raise ValueError(f"expected exactly one stable marker pair for {key}")
        a = s.index(start) + len(start)
        b = s.index(end, a)
        s = s[:a] + "\n" + maker() + "\n" + s[b:]
    PAGE.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    try:
        build()
    except Exception as exc:
        print(f"processo_a04_r3: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print(f"wrote three inline panels to {PAGE.relative_to(ROOT)}")
