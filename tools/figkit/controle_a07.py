"""Controle Aula 07 · Fig. 1 · marcos temporais do juízo."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Timeline, svg


def linha_temporal():
    # Only the three dates stated in the lesson's sources appear as events.
    tl = Timeline("a07-recepcao", 44, 356, 270, 1969, 1988, step=1000)
    tl.event(1969, 130, "CF · 1969", tone="dif", sub="parâmetro de origem", anchor="start")
    tl.event(1980, 200, "Lei · 1980", tone="ink", sub="hipótese do exemplo", anchor="middle")
    tl.event(1988, 130, "CF/88", tone="conc", sub="parâmetro de recepção", anchor="end")
    return svg(
        "28 23 344 264",
        tl.svg(),
        cls="panel fig on",
        label="Constituição de 1969, lei hipotética de 1980 e Constituição de 1988 em ordem temporal",
        ident="p-recepcao-tempo",
    )


if __name__ == "__main__":
    print(linha_temporal())
