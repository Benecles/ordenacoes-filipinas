"""Aula 11: party positions and the reach of a no-merit decision.

The figures use Jesse Valadão's 2015 P2 question 4 and only the labelled
variations approved in the Aula 11 blueprint.
"""

from figkit import line, svg, t


EXAM_THREAD = "exam-2015-1-avaliacao-2-q4"
SOURCE = "EX, Avaliação 2 2015, questão 4; CPC, Lei 13.105/2015."


def _dot(x, y, tone="ink", r=7, open_=False):
    fill = "var(--paper)" if open_ else f"var(--{tone})"
    return (f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" '
            f'style="fill:{fill};stroke:var(--{tone});stroke-width:2"/>')


def hero_panel():
    """Seat the one claimant opposite the two distinct defendants."""
    o = t(38, 43, "JESSE VALADÃO · COBRANÇA SOLIDÁRIA", size=16, weight=700)
    o += t(762, 43, "R$ 100.000,00", size=15, weight=700, anchor="end",
           fill="var(--ink)")
    o += line(38, 59, 762, 59, w=1.4)
    o += t(114, 105, "AUTOR", size=14, weight=700, anchor="middle",
           fill="var(--ink-2)")
    o += t(585, 105, "RÉUS · POSIÇÕES DISTINTAS", size=14, weight=700,
           anchor="middle", fill="var(--ink-2)")
    o += _dot(114, 154, "ink", 10)
    o += t(114, 185, "JESSE", size=15, weight=700, anchor="middle")
    o += t(114, 207, "VALADÃO", size=14, anchor="middle")
    o += line(126, 154, 318, 154, w=2.3)
    o += line(318, 128, 318, 180, w=2.3)
    o += line(318, 128, 471, 128, w=2.3)
    o += line(318, 180, 471, 180, w=2.3)
    o += _dot(471, 128, "ink", 9, open_=True)
    o += _dot(471, 180, "ink", 9, open_=True)
    o += t(495, 133, "DALVO FRITZ", size=15, weight=700)
    o += t(495, 185, "SEROTONINA DA SILVA", size=15, weight=700)
    o += t(495, 155, "RÉU 1", size=14, fill="var(--ink-2)")
    o += t(495, 207, "RÉ 2", size=14, fill="var(--ink-2)")
    o += line(38, 242, 762, 242, tone="muted", w=1)
    o += t(38, 268, "P2 · AVALIAÇÃO 2 · 2015 · QUESTÃO 4", size=14,
           weight=700, fill="var(--ink-2)")
    o += t(38, 296, "HIPÓTESE DE ILEGITIMIDADE AINDA SERÁ TESTADA",
           size=14, weight=700, fill="var(--ink)")
    return svg("20 20 760 300", o, cls="fig hero-fork",
               ident="pci-a11-hero",
               label="Jesse Valadão cobra solidariamente cem mil reais de Dalvo Fritz e Serotonina da Silva, que ocupam posições distintas no polo passivo").replace(
                   "<svg", '<svg data-family="figure.seating"', 1)


def scope_panel(stage):
    """One of three decision-scope states for the same Q4 record."""
    o = t(34, 38, "QUESTÃO 4 · ALCANCE DA DECISÃO", size=15, weight=700)
    o += line(34, 54, 686, 54, w=1.3)
    o += t(34, 82, "JESSE · R$ 100.000 · COBRANÇA SOLIDÁRIA", size=14,
           weight=700)
    o += t(686, 82, f"ESTADO {stage}/3", size=13, weight=700,
           anchor="end", fill="var(--ink-2)")
    o += line(360, 100, 360, 135, w=2)
    if stage == 1:
        o += line(165, 135, 555, 135, w=2)
        o += line(165, 135, 165, 210, w=2)
        o += line(555, 135, 555, 210, w=2)
        o += _dot(165, 211, "ink", 8, open_=True)
        o += _dot(555, 211, "ink", 8, open_=True)
        o += t(165, 182, "DALVO", size=14, weight=700, anchor="middle")
        o += t(555, 182, "SEROTONINA", size=14, weight=700, anchor="middle")
        o += t(360, 254, "REGISTRO DA QUESTÃO", size=14, weight=700,
               anchor="middle", fill="var(--ink-2)")
        o += t(360, 278, "Dois réus · nenhum resultado judicial afirmado", size=13,
               anchor="middle")
        o += t(360, 344, "O ENUNCIADO APRESENTA UMA HIPÓTESE", size=13,
               weight=700, anchor="middle", fill="var(--ink)")
    elif stage == 2:
        o += line(165, 135, 555, 135, w=2)
        o += line(165, 135, 165, 210, tone="dif", w=3)
        o += line(555, 135, 555, 253, tone="dif", w=3)
        o += line(155, 198, 175, 218, tone="dif", w=2.5)
        o += line(155, 218, 175, 198, tone="dif", w=2.5)
        o += _dot(555, 253, "dif", 8, open_=True)
        o += t(165, 182, "DALVO", size=14, weight=700,
               anchor="middle", fill="var(--ink)")
        o += t(555, 182, "SEROTONINA", size=14, weight=700,
               anchor="middle", fill="var(--ink)")
        o += t(165, 249, "EXCLUÍDO", size=13, weight=700,
               anchor="middle", fill="var(--ink)")
        o += t(555, 288, "A COBRANÇA SEGUE", size=13, weight=700,
               anchor="middle", fill="var(--ink)")
        o += t(360, 344, "PARCELA · DECISÃO INTERLOCUTÓRIA · AGRAVO", size=13,
               weight=700, anchor="middle", fill="var(--ink)")
    else:
        o += line(360, 135, 360, 210, tone="dif", w=3)
        o += line(350, 198, 370, 218, tone="dif", w=2.5)
        o += line(350, 218, 370, 198, tone="dif", w=2.5)
        o += _dot(360, 135, "ink", 8, open_=True)
        o += t(360, 182, "DALVO · ÚNICO RÉU", size=14, weight=700,
               anchor="middle")
        o += t(360, 249, "A FASE COGNITIVA SE ENCERRA", size=14,
               weight=700, anchor="middle", fill="var(--ink)")
        o += t(360, 279, "TOTAL · SENTENÇA · APELAÇÃO", size=13,
               weight=700, anchor="middle", fill="var(--ink)")
        o += t(360, 344, "VARIAÇÃO DE UM FATO · SEROTONINA SAI DO POLO PASSIVO",
               size=13, weight=700, anchor="middle", fill="var(--ink-2)")
    return svg("16 12 688 360", o,
               cls="panel fig" + (" on" if stage == 1 else ""),
               ident=f"pci-a11-scope-{stage}",
               label=("Questão 4: registro com Jesse, Dalvo e Serotonina; nenhuma decisão afirmada" if stage == 1 else
                      "Hipótese da questão 4: Dalvo é excluído, a cobrança segue contra Serotonina e a decisão é parcial, interlocutória e agravável" if stage == 2 else
                      "Variação de um fato: Dalvo é o único réu, sua exclusão encerra a fase cognitiva e gera sentença apelável")).replace(
                          "<svg", '<svg data-family="figure.form"', 1)


def refiling_panel():
    """Mark three statutory states of Jesse's same unresolved demand."""
    o = t(34, 39, "A MESMA PRETENSÃO DE JESSE · R$ 100.000", size=16,
          weight=700)
    o += line(34, 56, 686, 56, w=1.3)
    o += t(34, 91, "DEPOIS DA DECISÃO SEM MÉRITO", size=13,
           weight=700, fill="var(--ink-2)")
    o += line(70, 157, 650, 157, tone="dif", w=5)
    o += _dot(70, 157, "ink", 10)
    o += _dot(650, 157, "dif", 9, open_=True)
    o += t(70, 134, "PEDIDO SEM JULGAMENTO", size=14, weight=700)
    o += t(650, 134, "POSSÍVEL NOVA AÇÃO", size=14, weight=700,
           anchor="end", fill="var(--ink)")
    marks = [(128, "ABANDONO OU", "DESISTÊNCIA", "CUSTAS E HONORÁRIOS", "dif"),
             (360, "VÍCIO INDICADO", "CORRIGIR ANTES", "PROVA DAS DESPESAS", "conc"),
             (592, "3 ABANDONOS", "MESMO OBJETO", "DIREITO · DEFESA", "conc")]
    for x, a, b, c, tone in marks:
        o += line(x, 157, x, 222, tone=tone, w=2.4)
        o += _dot(x, 222, tone, 7, open_=(tone == "dif"))
        o += t(x, 258, a, size=13, weight=700, anchor="middle",
               fill="var(--ink)")
        o += t(x, 280, b, size=13, weight=700, anchor="middle")
        o += line(x - 75, 297, x + 75, 297, tone="muted", w=1)
        o += t(x, 323, c, size=13, weight=600, anchor="middle",
               fill="var(--ink-2)")
    o += t(592, 350, "NOVA AÇÃO BARRADA", size=13, weight=700,
           anchor="middle", fill="var(--ink)")
    return svg("16 12 688 368", o, cls="fig",
               ident="pci-a11-refiling",
               label="A mesma pretensão de Jesse permanece sem julgamento; abandono ou desistência permitem nova ação com despesas comprovadas, vício indicado exige correção e três abandonos barram ação idêntica, preservado o direito como defesa").replace(
                   "<svg", '<svg data-family="figure.form"', 1)


def panels():
    return hero_panel(), tuple(scope_panel(n) for n in (1, 2, 3)), refiling_panel()


def specimen_sections():
    hero, scopes, refile = panels()
    scrolly = ''.join(f'<div class="s">{panel}</div>' for panel in scopes)
    return f'''<section class="ref" data-exam-thread="{EXAM_THREAD}"><header><span class="g">Partes · posições</span><span class="v">verbo · localizar</span></header>
<h2>Processo · Aula 11 · cobrança e litisconsortes</h2><p>O mesmo pedido solidário ocupa duas posições distintas no polo passivo.</p><p class="r">thread · {EXAM_THREAD}</p><div class="wide"><div class="s">{hero}</div></div></section>
<section class="ref" data-exam-thread="{EXAM_THREAD}"><header><span class="g">Decisão · alcance</span><span class="v">verbo · delimitar</span></header>
<h2>Processo · Aula 11 · término total e parcial</h2><p>A exclusão hipotética de Dalvo deixa Serotonina no processo; retirado o único réu, a mesma decisão alcança a fase inteira.</p><p class="r">thread · {EXAM_THREAD}</p><div class="grid">{scrolly}</div></section>
<section class="ref" data-exam-thread="{EXAM_THREAD}"><header><span class="g">Pretensão · estado após a decisão</span><span class="v">verbo · decidir</span></header>
<h2>Processo · Aula 11 · a mesma demanda depois do não mérito</h2><p>A pretensão de Jesse continua sem julgamento, mas o art. 486 condiciona sua nova propositura à correção, às despesas e ao limite da perempção.</p><p class="r">thread · {EXAM_THREAD}</p><div class="wide"><div class="s">{refile}</div></div></section>'''
