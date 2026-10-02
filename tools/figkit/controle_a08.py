"""Controle Aula 08: ordinal timeline for the RE 197.917 modulation example."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Timeline, svg, t


def re_197917_timeline():
    # The three marks are ordered events, not measured durations. No dates are
    # assigned to the law's origin or the following legislature.
    timeline = Timeline("a08-re197917", 52, 548, 250, 1, 3, step=10)
    timeline.event(1, 75, "", tone="muted", mark="circle")
    timeline.event(2, 110, "", tone="conc")
    timeline.event(3, 75, "", tone="dif", mark="circle")
    timeline.span(302, 1, 2, "", tone="ink")

    marks = timeline.svg()
    marks += t(52, 43, "MIRA ESTRELA", size=22, caps=True, weight=700)
    marks += t(548, 43, "SEM ESCALA", size=22, caps=True, weight=600,
               anchor="end", fill="var(--ink-2)")

    marks += t(52, 131, "LEI", size=22, caps=True, weight=700)
    marks += t(52, 164, "ORIGEM", size=22, caps=True, fill="var(--ink-2)")
    marks += t(300, 70, "JULGAMENTO STF", size=22, caps=True, weight=700, anchor="middle",
               fill="var(--conc)")
    marks += t(300, 99, "06 JUN. 2002", size=22, caps=True, anchor="middle", fill="var(--ink-2)")
    marks += t(548, 131, "LEGISLATURA", size=22, caps=True, weight=700, anchor="end", fill="var(--dif)")
    marks += t(548, 164, "SEGUINTE", size=22, caps=True, anchor="end", fill="var(--ink-2)")

    marks += t(52, 288, "MODELO CLÁSSICO", size=22, caps=True, weight=700)
    marks += t(52, 340, "EX TUNC · ORIGEM", size=22, caps=True, weight=700)
    marks += t(52, 370, "EFEITO", size=22, caps=True, weight=700,
               fill="var(--conc)")
    marks += t(548, 370, "11 → 9 VEREADORES", size=22, caps=True, weight=700,
               anchor="end", fill="var(--conc)")
    marks += t(548, 402, "LEGISLATURA SEGUINTE", size=22, caps=True, anchor="end",
               fill="var(--ink-2)")

    return svg("36 16 528 407", marks, cls="panel fig on", ident="p08-re197917",
               label="Linha temporal ordinal: regra ex tunc e efeitos do RE 197.917 na legislatura seguinte")


if __name__ == "__main__":
    print(re_197917_timeline())
