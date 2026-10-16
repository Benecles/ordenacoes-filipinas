"""Aula 02: measured docket for the Art. 334 hearing intervals."""
import os
import re
from pathlib import Path

from figkit import Timeline, line, svg, t
import figkit


def panel():
    scale = Timeline("pci-a02-s5", 95, 1005, 160, -30, 0, step=10)
    scale.event(-30, 78, "designação", tone="ink", sub="juiz · audiência", anchor="start")
    scale.event(-20, 60, "citação", tone="ink", sub="juízo · réu", anchor="middle", mark="circle")
    scale.event(-10, 78, "petição", tone="ink", sub="réu · desinteresse", anchor="middle", mark="circle")
    scale.event(0, 60, "audiência", tone="ink", sub="dia zero", anchor="end")

    o = t(550, 39, "ART. 334 · MARCOS EM RELAÇÃO À AUDIÊNCIA", size=12,
          fill="var(--ink-2)", anchor="middle", weight=600, caps=True)
    o += scale.svg()

    x30, x20, x0 = scale.x(-30), scale.x(-20), scale.x(0)
    o += line(x30, 226, x0, 226, tone="ink", w=1.8)
    o += line(x30, 219, x30, 233, tone="ink", w=1.8)
    o += line(x0, 219, x0, 233, tone="ink", w=1.8)
    o += t((x30 + x0) / 2, 218, "designação · mínimo 30 dias",
           size=11.5, fill="var(--conc)", anchor="middle", weight=700, ls=".02em")

    o += line(x20, 270, x0, 270, tone="ink", w=1.8)
    o += line(x20, 263, x20, 277, tone="ink", w=1.8)
    o += line(x0, 263, x0, 277, tone="ink", w=1.8)
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
    ).replace('<svg ', '<svg data-family="figure.calendar" ', 1)


def q8():
    """Comparison instrument for the actual 2018/2 P1 question 8."""
    o = t(490, 28, "P1 · 2018/2 · QUESTÃO 8 · EFEITO FUTURO", size=12,
          fill="var(--ink-2)", anchor="middle", weight=600, caps=True)
    o += line(110, 158, 870, 158, tone="ink", w=1.6)
    for x in (280, 700):
        tone = "ink"
        o += line(x, 143, x, 175, tone=tone, w=1.8)
        o += f'<circle cx="{x}" cy="158" r="7" style="fill:var(--paper);stroke:{figkit.TONE[tone]};stroke-width:2"/>'
    o += t(280, 112, "INDEFERIMENTO DA INICIAL", size=12, fill="var(--ink)",
           anchor="middle", weight=700, caps=True)
    o += t(700, 112, "IMPROCEDÊNCIA LIMINAR", size=12, fill="var(--ink)",
           anchor="middle", weight=700, caps=True)
    o += t(280, 218, "sem resolução do mérito", size=18, fill="var(--ink)",
           anchor="middle", weight=500, ls="0")
    o += t(280, 246, "possibilidade de repropositura", size=12, fill="var(--ink-2)",
           anchor="middle", weight=500, ls=".02em")
    o += t(700, 218, "com resolução do mérito", size=18, fill="var(--ink)",
           anchor="middle", weight=500, ls="0")
    o += t(700, 246, "coisa julgada", size=12, fill="var(--ink)",
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


def hero_dossier():
    """Draw the source-located Faustina record without implying a legal result."""
    o = t(34, 40, "AUTOS · FATOS LOCALIZADOS", size=12,
          fill="var(--ink-2)", weight=700)
    o += line(34, 54, 966, 54, tone="ink", w=1.4)
    o += t(56, 84, "FAUSTINA", size=18, fill="var(--ink)", weight=700)
    o += t(56, 108, "contra Antonino · pedido de entrega de projeto arquitetônico", size=16,
           fill="var(--ink)")
    o += line(56, 132, 944, 132, tone="ink", w=1)
    o += t(56, 172, "CONTRATO", size=11, fill="var(--ink-2)", weight=700)
    o += t(56, 204, "entrega em até 30 dias após o pagamento", size=16,
           fill="var(--ink)")
    o += t(56, 260, "RECIBO", size=11, fill="var(--ink-2)", weight=700)
    o += t(56, 292, "pagamento integral", size=16, fill="var(--ink)")
    o += t(56, 348, "PROVA", size=11, fill="var(--ink-2)", weight=700)
    o += t(56, 380, "dispensa de outras provas", size=16, fill="var(--ink)")
    o += t(944, 172, "30", size=24, fill="var(--ink)", anchor="end", weight=700)
    o += t(944, 204, "dias após pagamento", size=11, fill="var(--ink-2)", anchor="end")
    o += t(944, 348, "PEDIDO", size=11, fill="var(--ink-2)", anchor="end", weight=700)
    o += t(944, 380, "entrega do projeto", size=11, fill="var(--ink)", anchor="end")
    return svg("20 8 960 410", o, ident="pci-a02-hero", label=(
        "Dossiê dos fatos localizados: Faustina pede a Antonino a entrega de projeto arquitetônico; o contrato "
        "prevê entrega em até 30 dias após o pagamento; há recibo de pagamento integral "
        "e dispensa de outras provas."))


def hero_card():
    drawing = hero_dossier().replace('<svg ', '<svg data-family="figure.autos" ', 1)
    return f'''<figure class="hero-drawing">{drawing}<figcaption>Faustina pede a entrega do projeto; contrato, recibo e dispensa de outras provas compõem o registro.</figcaption></figure>'''


def decision_scope():
    """Two-stage scrolly keeps the located record separate from the legal gate."""
    p1 = svg("0 0 600 600", (
        t(38, 60, "FATOS LOCALIZADOS", size=13, fill="var(--ink-2)", weight=700)
        + line(38, 80, 562, 80, tone="ink")
        + '<path d="M54 126H526L546 146V245H54Z M526 126V146H546" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
        + t(78, 166, "CONTRATO", size=12, fill="var(--ink-2)", weight=700)
        + t(78, 207, "entrega em até 30 dias após pagamento", size=16, fill="var(--ink)")
        + '<path d="M54 274H526L546 294V392H54Z M526 274V294H546" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
        + t(78, 316, "RECIBO", size=12, fill="var(--ink-2)", weight=700)
        + t(78, 357, "pagamento integral", size=16, fill="var(--ink)")
        + '<path d="M54 422H526L546 442V536H54Z M526 422V442H546" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
        + t(78, 464, "PROVA", size=12, fill="var(--ink-2)", weight=700)
        + t(78, 505, "Faustina dispensa outras provas", size=16, fill="var(--ink)")
    ), cls="panel on", ident="pci-a02-gate-record", label="Fatos localizados no trecho sobre Faustina.")
    p2 = svg("0 0 600 600", (
        t(38, 60, "TESTE DO ART. 332", size=13, fill="var(--ink-2)", weight=700)
        + line(38, 80, 562, 80, tone="ink")
        + '<path d="M54 126H526L546 146V300H54Z M526 126V146H546" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
        + t(78, 166, "CAUSA", size=12, fill="var(--ink-2)", weight=700)
        + t(78, 208, "dispensa de instrução?", size=17, fill="var(--ink)")
        + line(78, 242, 520, 242, tone="ink", w=1)
        + t(78, 275, "avaliação jurídica", size=14, fill="var(--ink-2)")
        + '<path d="M54 330H526L546 350V536H54Z M526 330V350H546" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
        + t(78, 370, "FUNDAMENTO LEGAL", size=12, fill="var(--ink-2)", weight=700)
        + t(78, 414, "enquadramento legal identificado?", size=16, fill="var(--ink)")
        + line(78, 452, 520, 452, tone="ink", w=1)
        + t(78, 477, "Variação: se o pedido", size=13, fill="var(--ink)", weight=600)
        + t(78, 499, "contrariasse súmula do STJ…", size=13, fill="var(--ink)", weight=600)
    ), cls="panel", ident="pci-a02-gate-law", label="O teste distingue a dispensa de instrução e o fundamento legal.")
    p1 = p1.replace('<svg ', '<svg data-family="figure.form" ', 1)
    p2 = p2.replace('<svg ', '<svg data-family="figure.form" ', 1)
    return f'''<div class="scrolly"><div class="stage" aria-hidden="true"><figure>{p1}{p2}<figcaption><span>Faustina · fatos e enquadramento</span><span class="stage-count">1 / 2</span></figcaption></figure></div><div class="steps"><section class="step on" data-panel="pci-a02-gate-record" data-slides="Fatos localizados"><div class="card"><span class="label">Etapa 1</span><h3>Leia os fatos apresentados</h3><p>Contrato com prazo de entrega após o pagamento, recibo de pagamento integral e dispensa de outras provas.</p></div></section><section class="step" data-panel="pci-a02-gate-law" data-slides="Fundamento legal"><div class="card"><span class="label">Etapa 2</span><h3>Separe prova e fundamento</h3><p>O teste do art. 332 tem dois campos: necessidade de instrução e enquadramento legal. Aqui, o campo do fundamento fica em aberto.</p></div></section></div></div>'''


def bet_card():
    return '''<div class="bet"><div><span class="bet-k">Antes de ler · primeira resposta</span><p class="bet-q">Os fatos apresentados permitem afirmar que os requisitos da improcedência liminar estão presentes?</p><div class="bet-opts"><button type="button" data-opt="a">A · Sim: contrato e recibo bastam para apontar um fundamento legal.</button><button type="button" data-opt="b">B · Sim: qualquer decisão antes da citação é improcedência liminar.</button><button type="button" data-opt="c" data-court>C · O fundamento legal ainda precisa ser identificado.</button></div><div class="bet-reveal"><p><span class="held">Resposta: C.</span> Faustina tem contrato com prazo contado do pagamento, recibo de quitação integral e dispensa de outras provas. A improcedência liminar exige também o enquadramento em hipótese legal; esse campo permanece em aberto com os fatos narrados. A conclusão não resolve se o caso poderia vir a preencher a hipótese.</p></div></div></div>'''


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
    generated_hero = hero_card()
    if 'id="pci-a02-hero"' in text:
        text, count = re.subn(r'<figure class="hero-drawing">.*?id="pci-a02-hero".*?</figure>', generated_hero, text, count=1, flags=re.S)
        if count != 1: raise SystemExit("Could not refresh the A02 hero figure")
    else:
        text = text.replace('<div class="titleblock label"', generated_hero + '\n  <div class="titleblock label"', 1)
    bet = bet_card()
    start = text.find('<div class="bet">')
    if start >= 0:
        end = text.find('<section class="chapter"', start)
        text = text[:start] + bet + '\n\n' + text[end:]
    else:
        text = text.replace('<section class="chapter" aria-labelledby="c1">', bet + '\n<section class="chapter" aria-labelledby="c1">', 1)
    scope = decision_scope()
    if 'id="pci-a02-gate-record"' in text:
        for ident in ("pci-a02-gate-record", "pci-a02-gate-law"):
            fresh = re.search(r'<svg\b[^>]*\bid="' + ident + r'"[^>]*>.*?</svg>', scope, re.S).group(0)
            text, count = re.subn(r'<svg\b[^>]*\bid="' + ident + r'"[^>]*>.*?</svg>', lambda _: fresh, text, count=1, flags=re.S)
            if count != 1: raise SystemExit(f"Could not refresh the A02 panel {ident}")
        text = text.replace("Faustina · registro e enquadramento", "Faustina · fatos e enquadramento")
        text = text.replace("data-slides=\"Registro localizado\"", "data-slides=\"Fatos localizados\"")
        text = text.replace("Leia o que o registro contém", "Leia os fatos apresentados")
        text = text.replace("O trecho não identifica um fundamento do art. 332. Não é possível afirmar os dois requisitos com os dados localizados.", "O teste do art. 332 tem dois campos: necessidade de instrução e enquadramento legal. Aqui, o campo do fundamento fica em aberto.")
        text = text.replace("O teste do art. 332 tem dois campos: necessidade de instrução e enquadramento legal. Aqui, o campo do fundamento fica em aberto.", "O teste jurídico tem dois campos: necessidade de instrução e enquadramento legal. A variação abaixo mostra um fundamento do art. 332.")
    else:
        text = text.replace('<div class="wide"><div class="prose">\n<p><span class="term"', '<div class="wide">' + scope + '</div>\n<div class="wide"><div class="prose">\n<p><span class="term"', 1)
    marker = "<!-- FIGURE: PCI-A02 -->"
    if text.count(marker) == 1:
        text = text.replace(marker, panel())
    else:
        text, count = re.subn(r'<svg\b(?=[^>]*\bid="pci-a02-s5")[^>]*>.*?</svg>', panel(), text, count=1, flags=re.S)
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
