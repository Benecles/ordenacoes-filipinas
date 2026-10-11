"""Aula 02: measured docket for the Art. 334 hearing intervals."""
import os
import re
from pathlib import Path

from figkit import Timeline, line, svg, t
import figkit


def panel():
    scale = Timeline("pci-a02-s5", 95, 1005, 160, -30, 0, step=10)
    scale.event(-30, 78, "designação", tone="dif", sub="juiz · audiência", anchor="start")
    scale.event(-20, 60, "citação", tone="ink", sub="juízo · réu", anchor="middle", mark="circle")
    scale.event(-10, 78, "petição", tone="conc", sub="réu · desinteresse", anchor="middle", mark="circle")
    scale.event(0, 60, "audiência", tone="ink", sub="dia zero", anchor="end")

    o = t(550, 27, "ART. 334 · MARCOS EM RELAÇÃO À AUDIÊNCIA", size=12,
          fill="var(--ink-2)", anchor="middle", weight=600, caps=True)
    o += scale.svg()

    x30, x20, x0 = scale.x(-30), scale.x(-20), scale.x(0)
    o += line(x30, 226, x0, 226, tone="dif", w=1.8)
    o += line(x30, 219, x30, 233, tone="dif", w=1.8)
    o += line(x0, 219, x0, 233, tone="dif", w=1.8)
    o += t((x30 + x0) / 2, 218, "designação · mínimo 30 dias",
           size=11.5, fill="var(--dif)", anchor="middle", weight=700, ls=".02em")

    o += line(x20, 270, x0, 270, tone="conc", w=1.8)
    o += line(x20, 263, x20, 277, tone="conc", w=1.8)
    o += line(x0, 263, x0, 277, tone="conc", w=1.8)
    o += t((x20 + x0) / 2, 262, "citação · mínimo 20 dias",
           size=11.5, fill="var(--conc)", anchor="middle", weight=700, ls=".02em")

    return svg(
        "35 10 1030 290",
        o,
        cls="fig",
        ident="pci-a02-s5",
        label=(
            "Escala relativa ao dia da audiência, em zero. O juiz designa com pelo menos "
            "30 dias de antecedência; o réu é citado pelo menos 20 dias antes; o réu "
            "pode protocolar o desinteresse com 10 dias de antecedência."
        ),
    )


def q8():
    """Comparison instrument for the actual 2018/2 P1 question 8."""
    o = t(490, 28, "P1 · 2018/2 · QUESTÃO 8 · EFEITO FUTURO", size=12,
          fill="var(--ink-2)", anchor="middle", weight=600, caps=True)
    o += line(110, 158, 870, 158, tone="ink", w=1.6)
    for x, tone in ((280, "conc"), (700, "dif")):
        o += line(x, 143, x, 175, tone=tone, w=1.8)
        o += f'<circle cx="{x}" cy="158" r="7" style="fill:var(--paper);stroke:{figkit.TONE[tone]};stroke-width:2"/>'
    o += t(280, 112, "INDEFERIMENTO DA INICIAL", size=12, fill="var(--conc)",
           anchor="middle", weight=700, caps=True)
    o += t(700, 112, "IMPROCEDÊNCIA LIMINAR", size=12, fill="var(--dif)",
           anchor="middle", weight=700, caps=True)
    o += t(280, 218, "sem resolução do mérito", size=18, fill="var(--ink)",
           anchor="middle", weight=500, ls="0")
    o += t(280, 246, "possibilidade de repropositura", size=12, fill="var(--ink-2)",
           anchor="middle", weight=500, ls=".02em")
    o += t(700, 218, "com resolução do mérito", size=18, fill="var(--ink)",
           anchor="middle", weight=500, ls="0")
    o += t(700, 246, "coisa julgada", size=12, fill="var(--ink-2)",
           anchor="middle", weight=600, ls=".02em")
    o += t(490, 302, "CLASSIFIQUE O RESULTADO, NÃO APENAS O MOMENTO DA DECISÃO",
           size=11, fill="var(--ink-2)", anchor="middle", weight=600, caps=True)
    return svg(
        "70 10 910 315", o, ident="pci-a02-q8",
        label=("Instrumento para a questão 8 da P1 de 2018/2. O indeferimento da inicial "
               "é sem resolução do mérito; a improcedência liminar resolve o mérito e pode "
               "produzir coisa julgada. A questão pergunta pelo efeito futuro."),
    )


def q8_card():
    return f'''<figure class="figure-card">{q8()}<figcaption>Fig. 1 · A diferença que a questão 8 da P1 de 2018/2 pede para o futuro.</figcaption><span class="src" hidden data-src="exam-bank.json, exam-2018-2-p1-v1-q8, provas 2018-2 P1 v1 e v2, PDF p. 2; CPC, arts. 330, 332, 485, I, 486, 487, I"></span></figure>'''


def probe_page():
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Figkit · Processo Aula 02</title>
<link rel="stylesheet" href="../courses/processo-civil-i/assets/curso.css"><link rel="stylesheet" href="../assets/casa.css">
<style>body{{margin:0;background:var(--paper);color:var(--ink)}}.figure-card{{width:min(1083px,calc(100vw - 96px));margin:34px auto;padding:16px 20px 12px;background:var(--paper);border:1.5px solid var(--ink);box-shadow:6px 6px 0 var(--grid-major)}}.figure-card svg{{display:block;width:100%;height:auto}}.figure-card figcaption{{max-width:70ch;margin:10px auto 0;font:500 12px/1.5 var(--mono);color:var(--ink-2)}}@media(max-width:1099px) and (orientation:portrait){{.figure-card{{width:calc(100vw - 32px)}}}}</style></head><body>
<figure class="figure-card">{panel()}<figcaption>A audiência tem prazos mínimos diferentes para designação, citação e manifestação do réu.</figcaption></figure>
</body></html>"""


def inject_page():
    root = Path(__file__).resolve().parents[2]
    page = root / "courses/processo-civil-i/aula-02.html"
    text = page.read_text(encoding="utf-8")
    marker = "<!-- FIGURE: PCI-A02 -->"
    if text.count(marker) == 1:
        text = text.replace(marker, panel())
    else:
        text, count = re.subn(r'<svg id="pci-a02-s5".*?</svg>', panel(), text, count=1, flags=re.S)
        if count != 1:
            raise SystemExit(f"Expected one figure marker or SVG in {page}")
    q8_marker = "<!-- FIGURE: PCI-A02-Q8 -->"
    if text.count(q8_marker) == 1:
        text = text.replace(q8_marker, q8_card())
    else:
        text, count = re.subn(
            r'<figure class="figure-card"><svg id="pci-a02-q8"[\s\S]*?</figure>',
            lambda _: q8_card(), text, count=1)
        if count != 1:
            raise SystemExit(f"Expected one Q8 comparison figure in {page}")
    page.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    figkit.WARN.clear()
    probe = os.environ.get("FIGKIT_PROBE")
    if probe:
        Path(probe).write_text(probe_page(), encoding="utf-8")
        print(probe)
    else:
        inject_page()
    print("\n".join(figkit.WARN) or "no text warnings")
