"""Direito Constitucional I · hero strips (1080 × 170). 33 pages opened on the same generic timeline
(1787 → 1988) whatever the lesson was about. Each now opens on a strip that answers its own question, from
facts printed on that page, in the house families (records and stamps, forms, tracks, rulers, measured bars).
Aulas 01–03 keep the timeline: it is their subject.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, t
from controle_heroes import stamp, tick

W, H = 1080, 170
INK, DIF, CONC, MUTED = 'var(--ink)', 'var(--dif)', 'var(--conc)', 'var(--ink-2)'


def frame(inner, label):
    return f'<svg class="hero-fork figkit" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">{inner}</svg>'


def sheet(x, y, w, h, title, dashed=False):
    # plain paper: these strips write on the sheet, so no filler lines
    st = 'fill:none;stroke:var(--ink-2);stroke-width:1.4;stroke-dasharray:6 5' if dashed else 'fill:var(--paper);stroke:var(--ink);stroke-width:1.4'
    return (f'<path d="M{x} {y}H{x + w - 12}L{x + w} {y + 12}V{y + h}H{x}Z" style="{st}"/>'
            + t(x + 12, y + 22, title, size=11, weight=700, caps=True))


def say(x, y, s, size=14, fill=INK, italic=False, anchor='start'):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a} style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def mono(x, y, s, fill=INK, size=11, anchor='start', bold=False):
    return t(x, y, s, size=size, caps=True, anchor=anchor, fill=fill, weight=700 if bold else 500)


def arrow(x1, x2, y, tone=INK, dash=False):
    d = ';stroke-dasharray:5 4' if dash else ''
    return (f'<path d="M{x1} {y} H{x2 - 6}" style="stroke:{tone};stroke-width:1.5{d}"/>'
            f'<path d="M{x2 - 8} {y - 5} l7 5 l-7 5" style="fill:none;stroke:{tone};stroke-width:1.5"/>')


def slip(x, y, w, head, sub, struck=False, dashed=False, tone=INK):
    st = 'fill:none;stroke:var(--ink-2);stroke-width:1.2;stroke-dasharray:4 4' if dashed else 'fill:var(--paper);stroke:var(--ink);stroke-width:1.2'
    o = f'<rect x="{x}" y="{y}" width="{w}" height="52" style="{st}"/>'
    o += mono(x + 10, y + 20, head, tone, 10.5, bold=True) + say(x + 10, y + 40, sub, 13)
    if struck:
        o += f'<line x1="{x - 4}" y1="{y + 26}" x2="{x + w + 4}" y2="{y + 26}" style="stroke:{CONC};stroke-width:2"/>'
    return o


def axis(x0, x1, y, y0, y1_, marks):
    o = f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" style="stroke:var(--ink);stroke-width:1.4"/>'
    X = lambda v: x0 + (x1 - x0) * (v - y0) / (y1_ - y0)
    for v, top, sub, tone in marks:
        x = X(v)
        o += f'<circle cx="{x:.1f}" cy="{y}" r="5" style="fill:{tone}"/>'
        o += mono(x, y - 16, top, tone, 10.5, 'middle', True) + t(x, y + 22, sub, size=10.5, anchor='middle', fill=MUTED)
    return o


H_ = {}


def hero(name):
    def deco(f):
        H_[name] = f
        return f
    return deco


@hero('aula-04-casos')
def _():
    o = mono(20, 30, 'STF', bold=True) + mono(560, 30, 'TSE', bold=True)
    o += '<line x1="540" y1="16" x2="540" y2="160" style="stroke:var(--ink-2);stroke-width:1"/>'
    o += sheet(20, 46, 230, 100, 'RE 197.917 · 24/03/2004') + say(30, 128, 'art. 29, IV: proporção à população', 12)
    o += stamp(390, 96, 'tese fixada', DIF)
    o += sheet(560, 46, 230, 100, 'Resolução 21.702/2004') + say(570, 128, 'aplica a tese às eleições de 2004', 12)
    o += mono(1060, 82, 'legislar ou explicitar?', MUTED, 11, 'end') + mono(1060, 104, 'e o art. 16?', CONC, 11, 'end')
    return frame(o, 'Duas colunas: o STF fixa no RE 197.917 a tese sobre vereadores proporcionais; o TSE a aplica às eleições de 2004 pela Resolução 21.702; a pergunta é se isso é legislar')


@hero('aula-04')
def _():
    o = mono(20, 28, 'quem certifica a inconstitucionalidade?', MUTED)
    o += ''.join(f'<circle cx="{40 + i * 26}" cy="78" r="9" style="fill:var(--ink)"/>' for i in range(10))
    o += mono(20, 120, 'difuso · qualquer juiz, no caso')
    o += f'<rect x="340" y="58" width="150" height="40" style="fill:var(--ink)"/>' + mono(415, 83, 'STF', 'var(--paper)', 12, 'middle', True)
    o += mono(340, 120, 'concentrado · um órgão')
    o += slip(560, 40, 220, 'ADI', 'lei posterior a 1988') + slip(800, 40, 260, 'ADPF', 'o que a ADI não alcança')
    o += mono(560, 120, 'concentrado ≠ abstrato · ADI ≠ ADPF', CONC)
    return frame(o, 'Assentos de juízes para o difuso, o STF para o concentrado, e duas fichas, ADI e ADPF: quem certifica a inconstitucionalidade e por qual ação')


@hero('aula-05')
def _():
    o = sheet(20, 26, 360, 128, 'Nova Constituição · originário')
    o += mono(36, 92, 'fundar uma ordem nova', size=10.5) + mono(36, 114, 'legitimidade: quem participou?', MUTED, 10.5)
    o += sheet(420, 26, 360, 128, 'Emenda · poder de reforma')
    o += mono(436, 92, 'exercente · Congresso, art. 60', size=10.5) + mono(436, 114, 'limites · § 4º, rito, circunstâncias', CONC, 10.5)
    o += mono(1060, 84, 'mesma origem? não', MUTED, 11, 'end') + mono(1060, 104, 'mesma competência? não', MUTED, 11, 'end')
    return frame(o, 'Duas folhas: a nova Constituição, do poder originário; a emenda, do poder de reforma, sujeita aos limites do art. 60')


@hero('aula-06-casos-precatorios')
def _():
    o = axis(60, 760, 100, 1985, 2003, [(1988, 'ADCT, art. 33', 'originário · parcelamento', INK), (2000, 'EC 30/2000', 'derivado · parcelamento', INK)])
    o += stamp(940, 96, 'cautelar', DIF, 14)
    o += mono(940, 140, 'não o mérito', CONC, 10.5, 'middle')
    return frame(o, 'Uma linha do tempo: o parcelamento de 1988 pelo constituinte originário e o de 2000 por emenda; contra este, uma cautelar')


@hero('aula-06-casos')
def _():
    o = sheet(20, 26, 300, 120, 'ADI 2.096') + say(32, 96, 'cláusula pétrea invocada contra a emenda', 12)
    o += stamp(170, 130, 'devolvida ao autor', INK, 11)
    o += sheet(380, 26, 420, 120, 'ADI 5.316-MC · EC 88')
    o += say(392, 96, 'texto da emenda … ', 13) + f'<rect x="510" y="82" width="170" height="20" style="fill:none;stroke:{CONC};stroke-width:1"/>'
    o += f'<line x1="512" y1="92" x2="678" y2="92" style="stroke:{DIF};stroke-width:2.4"/>' + say(686, 96, '…', 13)
    o += mono(1060, 82, 'barrada em', DIF, 11, 'end') + mono(1060, 102, 'uma só expressão', DIF, 11, 'end')
    return frame(o, 'Dois julgados do parágrafo 4º: na ADI 2.096 a cláusula pétrea é devolvida ao autor; na ADI 5.316 a emenda é barrada em uma só expressão')


@hero('aula-06')
def _():
    o = ''
    for i, s in enumerate(['rito do art. 60', 'limites expressos · § 4º', 'limites tácitos']):
        x = 20 + i * 300
        o += tick(x, 70) + say(x + 30, 70, s, 15)
    o += mono(20, 128, 'rito cumprido não basta', MUTED)
    o += mono(1060, 128, 'forma republicana e procedimento de emenda: fora do § 4º', CONC, 10.5, 'end')
    return frame(o, 'Três caixas que uma emenda precisa passar: o rito do art. 60, os limites expressos do parágrafo 4º e os limites tácitos')


@hero('aula-07-casos')
def _():
    o = axis(60, 700, 100, 2013, 2017, [(2015, 'EC 88/2015', 'aposentadoria aos 75', INK)])
    o += slip(740, 40, 320, 'ADI 5.316-MC', 'nova sabatina e regra transitória')
    o += stamp(900, 132, 'sabatina nova: barrada', DIF, 11)
    return frame(o, 'A EC 88 de 2015 leva a aposentadoria aos 75 anos; na ADI 5.316, o STF barra a nova sabatina')


@hero('aula-07')
def _():
    o = '<line x1="60" y1="96" x2="1020" y2="96" style="stroke:var(--ink);stroke-width:1.6"/>'
    for x, s, sub in [(60, 'plena', 'aplica-se já, inteira'), (540, 'contida', 'já, mas a lei pode restringir'), (1020, 'limitada', 'depende de lei · programática')]:
        o += f'<line x1="{x}" y1="86" x2="{x}" y2="106" style="stroke:var(--ink);stroke-width:1.6"/>'
        a = 'start' if x == 60 else ('end' if x == 1020 else 'middle')
        o += mono(x, 70, s, size=13, anchor=a, bold=True) + t(x, 130, sub, size=11, anchor=a, fill=MUTED)
    o += mono(540, 158, 'programática não é desculpa', CONC, 10.5, 'middle')
    return frame(o, 'A régua de José Afonso da Silva: eficácia plena, contida e limitada; contida e limitada não se confundem')


@hero('aula-08')
def _():
    o = '<line x1="60" y1="90" x2="1020" y2="90" style="stroke:var(--ink);stroke-width:1.6"/>'
    o += mono(60, 66, 'regra · tipo ideal', bold=True) + mono(1020, 66, 'princípio · tipo ideal', anchor='end', bold=True)
    o += f'<path d="M520 104 L540 104 L530 92 Z" style="fill:var(--ink)"/>' + arrow(560, 680, 98, CONC, dash=True)
    o += t(530, 130, 'a função na controvérsia', size=11, anchor='middle', fill=MUTED) + t(530, 146, 'pode mover a classificação', size=11, anchor='middle', fill=MUTED)
    o += mono(1020, 146, 'ponderar não dispensa as regras', CONC, 10.5, 'end')
    return frame(o, 'Uma régua entre regra e princípio como tipos ideais, com um marcador que a função na controvérsia pode deslocar')


@hero('aula-09')
def _():
    o = ''
    for i, s in enumerate(['triagem', 'adequação', 'necessidade', 'proporcionalidade estrita']):
        x = 20 + i * 250
        o += tick(x, 70) + say(x + 30, 70, s, 15)
    o += mono(20, 128, 'na resposta: o ganho, o sacrifício, a alternativa', DIF)
    o += mono(1060, 128, 'ponderação sem premissas: erro', CONC, 10.5, 'end')
    return frame(o, 'Quatro caixas do teste: triagem, adequação, necessidade e proporcionalidade em sentido estrito; a resposta nomeia ganho, sacrifício e alternativa')


@hero('aula-10')
def _():
    o = '<line x1="40" y1="90" x2="1040" y2="90" style="stroke:var(--ink-2);stroke-width:1"/>'
    o += '<line x1="540" y1="40" x2="540" y2="140" style="stroke:var(--ink);stroke-width:3"/>' + mono(540, 30, 'Constituição nova', anchor='middle', bold=True)
    o += mono(290, 66, 'norma anterior', anchor='middle') + say(290, 116, 'compatível: novada · incompatível: não recebida', 13, anchor='middle')
    o += mono(790, 66, 'norma posterior', anchor='middle') + say(790, 116, 'incompatível: inconstitucional', 13, anchor='middle')
    o += mono(290, 152, 'ADPF 153 · Lei de Anistia de 1979', MUTED, 10.5, 'middle')
    return frame(o, 'O marco da Constituição nova: normas anteriores são novadas ou não recebidas; posteriores, constitucionais ou não; a ADPF 153 como exemplo')


@hero('aula-11')
def _():
    o = ''
    for i, (a, b) in enumerate([('lei estrangeira', 'contra a sua Constituição'), ('lei estrangeira', 'contra a Constituição brasileira'), ('tratado', 'contra o direito interno')]):
        x = 20 + i * 360
        o += slip(x, 40, 330, f'conflito {i + 1} · {a}', b)
    o += mono(20, 136, 'três conflitos, três respostas', MUTED)
    o += mono(1060, 136, 'tratado de DH: supralegal · com rito do § 3º: emenda', DIF, 10.5, 'end')
    return frame(o, 'Três fichas de conflito: lei estrangeira contra sua Constituição, contra a brasileira, e tratado contra direito interno; a hierarquia dos tratados de direitos humanos')


@hero('aula-12')
def _():
    o = ''
    for i, s in enumerate(['1ª dimensão', '2ª dimensão', '3ª dimensão']):
        o += f'<rect x="{40 + i * 60}" y="{120 - i * 32}" width="{600 - i * 120}" height="28" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
        o += mono(52 + i * 60, 139 - i * 32, s, size=10.5, bold=True)
    o += say(700, 80, 'Cada dimensão acrescenta;', 16) + say(700, 104, 'nenhuma substitui a anterior.', 16, CONC)
    return frame(o, 'Três camadas de direitos empilhadas: as dimensões se acumulam e nenhuma substitui a anterior')


@hero('aula-13')
def _():
    o = mono(20, 30, 'art. 5º, § 2º · novo direito no catálogo', bold=True)
    for i, s in enumerate(['sede', 'conteúdo', 'regime']):
        x = 20 + i * 250
        o += tick(x, 84) + say(x + 30, 84, s, 16)
    o += mono(20, 140, 'cada inclusão pede justificativa', MUTED)
    o += mono(1060, 140, 'tratado aprovado sem ratificação: armadilha', CONC, 10.5, 'end')
    return frame(o, 'Formulário para incluir um direito pelo art. 5º, parágrafo 2º: sede, conteúdo e regime')


@hero('aula-14')
def _():
    o = mono(20, 30, 'que posição o titular invoca, e contra quem?', bold=True)
    o += slip(20, 52, 230, 'titular', 'quem invoca') + arrow(256, 316, 78) + slip(320, 52, 230, 'destinatário', 'contra quem')
    for i, s in enumerate(['animais', 'nascituro', 'pessoa jurídica']):
        o += slip(620 + i * 150, 52, 136, 'titular?', s, dashed=True)
    o += mono(620, 140, 'terreno de armadilhas', CONC, 10.5)
    return frame(o, 'Titular e destinatário de um direito, e três titulares discutidos: animais, nascituro e pessoa jurídica')


@hero('aula-15-casos')
def _():
    o = sheet(20, 24, 460, 130, 'ADPF 132 · acórdão')
    o += mono(36, 90, 'fundamentos · votos', MUTED, 10.5) + f'<rect x="32" y="108" width="436" height="28" style="fill:none;stroke:{DIF};stroke-width:2"/>' + mono(42, 127, 'dispositivo · união estável homoafetiva', DIF, 10.5)
    o += stamp(640, 84, 'unânime · vinculante', DIF, 12)
    o += mono(1060, 140, 'efeito horizontal: separar dispositivo e fundamentos', CONC, 10.5, 'end')
    return frame(o, 'O acórdão da ADPF 132 com o dispositivo marcado em azul e o carimbo unânime e vinculante')


@hero('aula-15')
def _():
    o = mono(20, 30, 'aplicação imediata · quem está obrigado, e como?', bold=True)
    for i, s in enumerate(['legislador', 'administração', 'juiz', 'particular']):
        o += slip(20 + i * 265, 52, 245, s, 'obrigado · modo próprio')
    o += mono(20, 140, 'não é eficácia idêntica para todos · não dispensa a lei', CONC, 10.5)
    return frame(o, 'Quatro destinatários dos direitos fundamentais, do legislador ao particular, cada um obrigado de modo próprio')


@hero('aula-16-casos')
def _():
    x0, px = 60, 4.6
    o = mono(20, 28, 'RE 778.889 · Tema 782', bold=True)
    o += f'<rect x="{x0}" y="50" width="{45 * px}" height="30" style="fill:var(--ink)"/>' + mono(x0 + 45 * px + 10, 70, 'recebeu: 30 + 15 = 45 dias')
    o += f'<rect x="{x0}" y="100" width="{180 * px}" height="30" style="fill:{DIF}"/>' + mono(x0 + 180 * px + 10, 120, '120 + 60 = 180', DIF)
    o += mono(x0, 156, 'adotante = gestante · a idade da criança não muda o prazo', DIF, 10.5)
    return frame(o, 'Duas barras em escala: os 45 dias que a servidora recebeu e os 180 dias da licença à gestante, que o Tema 782 estende à adotante, qualquer que seja a idade da criança')


@hero('aula-16')
def _():
    o = ''
    for i, s in enumerate(['âmbito', 'limite', 'fundamento', 'limites dos limites']):
        x = 20 + i * 265
        o += f'<rect x="{x}" y="50" width="240" height="44" style="fill:{"var(--ink)" if i < 3 else "var(--paper)"};stroke:var(--ink);stroke-width:1.3"/>'
        o += mono(x + 12, 77, s, 'var(--paper)' if i < 3 else CONC, 11.5, bold=True)
    o += mono(20, 136, 'restrição legítima ou erosão? a sequência decide', MUTED)
    return frame(o, 'Quatro passos em sequência: âmbito, limite, fundamento e limites dos limites')


@hero('aula-17')
def _():
    o = ''
    steps = [('dever geral', INK), ('objeção de consciência', INK), ('prestação alternativa', DIF), ('recusa também', CONC)]
    for i, (s, tone) in enumerate(steps):
        x = 20 + i * 240
        o += slip(x, 44, 210, s, '', tone=tone)
        if i < 3:
            o += arrow(x + 212, x + 238, 70)
    o += mono(20, 132, 'art. 5º, VIII', MUTED) + mono(980, 132, 'art. 15, IV', CONC, 11, 'middle')
    return frame(o, 'Quatro passos do art. 5º, VIII: dever geral, objeção de consciência, prestação alternativa; quem recusa também esta cai no art. 15, IV')


@hero('aula-18-casos')
def _():
    o = sheet(20, 26, 420, 120, 'Lei de Imprensa · 1967')
    o += ''.join(f'<line x1="26" y1="{70 + i * 14}" x2="434" y2="{70 + i * 14}" style="stroke:{DIF};stroke-width:2"/>' for i in range(5))
    o += stamp(600, 86, 'ADPF 130 · afastada por inteiro', DIF, 11)
    o += mono(1060, 74, 'censura prévia: vedada', CONC, 11, 'end') + mono(1060, 100, 'abuso: exame posterior', INK, 11, 'end')
    return frame(o, 'A Lei de Imprensa de 1967 riscada por inteiro pela ADPF 130: sem censura prévia, com exame posterior de abusos')


@hero('aula-18-limites')
def _():
    o = slip(20, 44, 260, 'Ellwanger', 'discurso de ódio') + arrow(284, 320, 70)
    o += slip(324, 44, 260, 'ADI 4.451 · 20–21/06/2018', 'sátira eleitoral')
    o += mono(620, 36, 'uma restrição precisa cumprir', bold=True)
    o += ''.join(tick(620 + i * 88, 90) for i in range(5)) + mono(620, 130, 'cinco condições', MUTED)
    return frame(o, 'De Ellwanger à ADI 4.451 e cinco caixas: as condições que uma restrição à expressão precisa cumprir')


@hero('aula-18')
def _():
    o = mono(60, 40, 'antes da expressão', bold=True) + mono(600, 40, 'depois da expressão', bold=True)
    o += '<line x1="540" y1="24" x2="540" y2="150" style="stroke:var(--ink);stroke-width:2.5"/>'
    o += f'<rect x="60" y="62" width="440" height="40" style="fill:none;stroke:{CONC};stroke-width:2"/>' + mono(76, 87, 'proibir · censura', CONC, 12, bold=True)
    o += '<rect x="600" y="62" width="440" height="40" style="fill:var(--ink)"/>' + mono(616, 87, 'responsabilizar · resposta, dano', 'var(--paper)', 12, bold=True)
    o += mono(60, 140, 'a Constituição trata os dois lados de modo oposto', MUTED)
    return frame(o, 'Uma linha no momento da expressão: antes, proibir é censura; depois, responsabilizar é possível')


@hero('aula-19-casos')
def _():
    o = sheet(20, 26, 420, 120, 'Notícia em circulação') + say(32, 100, 'jornalismo e o público que recebe', 13)
    o += stamp(520, 86, 'ADPF 130', DIF, 12)
    o += sheet(640, 26, 420, 120, 'Pedido de registro estatal') + say(652, 100, 'acesso individual: outra via', 13, CONC)
    return frame(o, 'Duas folhas: a notícia em circulação, protegida pela ADPF 130, e o pedido individual de registro estatal, que segue outra via')


@hero('aula-19')
def _():
    o = ''
    for i, (inc, s) in enumerate([('XIV', 'acesso à informação · sigilo da fonte'), ('XXXIII', 'informações de órgãos públicos'), ('LXXII', 'habeas data · dado pessoal')]):
        o += slip(20 + i * 355, 44, 335, f'art. 5º, {inc}', s)
    o += mono(20, 136, 'três pedidos, três incisos, três recusas possíveis', MUTED)
    o += mono(1060, 136, 'quando se pode negar?', CONC, 10.5, 'end')
    return frame(o, 'Três fichas: o inciso XIV, acesso à informação e sigilo da fonte; o XXXIII, informações de órgãos públicos; o LXXII, habeas data')


@hero('aula-20')
def _():
    o = mono(20, 30, 'propriedade · função social · que intervenção?', bold=True)
    for i, s in enumerate(['limitação', 'requisição', 'desapropriação', 'expropriação', 'usucapião']):
        o += slip(20 + i * 212, 52, 196, s, 'requisitos próprios')
    o += mono(20, 140, 'a prova cobra a modalidade certa', MUTED)
    return frame(o, 'Cinco fichas de intervenção na propriedade: limitação, requisição, desapropriação, expropriação e usucapião')


@hero('aula-21-casos')
def _():
    o = sheet(20, 26, 470, 120, 'ADPF 132') + say(32, 96, 'interpretação conforme · art. 1.723 do CC', 13)
    o += sheet(560, 26, 500, 120, 'RE 778.889') + say(572, 96, 'mutação constitucional · art. 7º, XVIII', 13)
    o += mono(540, 160, 'família, dignidade, igualdade · cada um com seus limites', MUTED, 10.5, 'middle')
    return frame(o, 'Dois julgados: a ADPF 132, por interpretação conforme do art. 1.723 do Código Civil; o RE 778.889, por mutação do art. 7º, XVIII')


@hero('aula-21')
def _():
    o = ''
    steps = ['art. 3º, IV', 'uso da sexualidade', 'silêncio como permissão', 'art. 226, § 3º']
    for i, s in enumerate(steps):
        x = 20 + i * 200
        o += slip(x, 40, 180, f'passo {i + 1}', s)
        if i < 3:
            o += arrow(x + 182, x + 198, 66)
    o += stamp(930, 66, 'união estável · igual', DIF, 11)
    o += mono(1060, 140, 'não trata de casamento nem de adoção', CONC, 10.5, 'end')
    return frame(o, 'Quatro passos do voto na ADPF 132, do art. 3º, IV ao art. 226, parágrafo 3º; o carimbo iguala a união estável; a decisão não trata de casamento nem de adoção')


@hero('aula-22-retrocesso')
def _():
    o = mono(60, 40, 'prestação existente', bold=True)
    o += '<rect x="60" y="56" width="420" height="30" style="fill:var(--ink)"/>'
    o += '<rect x="480" y="56" width="200" height="30" style="fill:var(--ink)"/><rect x="680" y="56" width="140" height="30" style="fill:none;stroke:var(--conc);stroke-width:1.6;stroke-dasharray:4 4"/>'
    o += mono(680, 108, 'redução', CONC, 10.5) + mono(680, 126, 'só justificada', CONC, 10.5)
    o += mono(60, 126, 'vale também para emenda · EC 95/2016, teto de gastos', MUTED, 10.5)
    return frame(o, 'Uma faixa de prestação existente com um trecho reduzido, tracejado: a redução precisa ser justificada, mesmo por emenda, como a do teto de gastos')


@hero('aula-22')
def _():
    o = slip(20, 44, 480, 'direito derivado', 'o medicamento da lista do SUS')
    o += slip(560, 44, 500, 'direito originário', 'o tratamento que nenhuma política oferece', tone=CONC)
    o += mono(540, 140, 'dois pedidos, dois problemas', MUTED, 11, 'middle')
    return frame(o, 'Dois pedidos de saúde: o medicamento da lista do SUS, direito derivado; o tratamento sem política, direito originário')


@hero('aula-23')
def _():
    o = mono(20, 28, 'penhora do único imóvel do fiador', bold=True)
    o += slip(20, 46, 300, 'RE 407.688 · 2006 · Plenário', 'penhora válida') + arrow(324, 356, 72)
    o += slip(360, 46, 330, 'RE 605.709 · 2018 · 1ª Turma', 'afastada na locação comercial') + arrow(694, 726, 72)
    o += slip(730, 46, 330, 'Tema 1127 · 2022 · Plenário', 'válida, residencial ou comercial', tone=DIF)
    o += mono(1060, 140, 'o resultado de 2018 não é o vigente', CONC, 10.5, 'end')
    return frame(o, 'Três precedentes em ordem: RE 407.688 em 2006, penhora válida; RE 605.709 em 2018, afastada na locação comercial; Tema 1127 em 2022, válida também na comercial')


@hero('aula-24')
def _():
    o = ''
    for i, s in enumerate(['direito de todos', 'deveres: Poder Público e coletividade', 'presentes e futuras gerações']):
        o += slip(20 + i * 300, 44, 280, 'art. 225', s)
    o += stamp(1000, 70, 'ADI 4.717', DIF, 12)
    o += mono(20, 140, 'que redução da proteção passa do limite?', CONC, 10.5)
    return frame(o, 'O art. 225 em três partes, direito, deveres e gerações futuras, e a ADI 4.717 como caso sobre redução da proteção')


@hero('aula-25')
def _():
    o = sheet(20, 26, 330, 120, 'RE 1.017.365 · tese') + say(32, 92, 'art. 231 · modo de vida e território', 13)
    o += stamp(530, 60, 'a demarcação declara', DIF, 11) + stamp(530, 116, 'marco temporal: afastado', DIF, 11)
    o += ''.join(f'<rect x="{720 + i * 84}" y="56" width="70" height="60" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>' + mono(755 + i * 84, 92, f'{i + 1}', size=14, anchor='middle', bold=True) for i in range(4))
    o += mono(720, 140, 'quatro regimes de indenização', MUTED, 10.5)
    return frame(o, 'A tese do RE 1.017.365: a demarcação declara, o marco temporal é afastado e há quatro regimes de indenização')


def apply(name):
    from inject import ROOT, element_span
    p = os.path.join(ROOT, 'courses', 'direito-constitucional-i', f'{name}.html')
    s = open(p).read()
    m = re.search(r'<svg\b[^>]*class="hero-fork[^"]*"', s)
    a, b = element_span(s, m.start())
    s = s[:a] + H_[name]() + s[b:]
    open(p, 'w').write(s)


if __name__ == '__main__':
    for name in H_:
        apply(name)
    print(len(H_), 'heroes;', '\n'.join(WARN) or 'no text warnings')
