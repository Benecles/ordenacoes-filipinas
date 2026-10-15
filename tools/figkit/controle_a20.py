"""Controle Aula 20 · ADI: cabimento. Nine panels from the house families: a form for the formal test
(struck slips for what falls outside), art. 59 as text with an abstraction gauge, sorting trays for the
funnel's result, the three normative layers with the crack where the norm breaks, and the four temporal
scenarios as strips (parâmetro and norma as tracks in time). Ink carries everything; orange marks the
limit (outside the object, the broken layer); blue the rule the STF applies.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def say(x, y, s, size=16, fill='var(--ink)', italic=False, anchor='start'):
    a = '' if anchor == 'start' else f' text-anchor="{anchor}"'
    return f'<text x="{x}" y="{y}"{a} style="font-family:var(--serif,serif);font-size:{size}px;fill:{fill}{";font-style:italic" if italic else ""}">{s}</text>'


def tick(x, y):
    return (f'<rect x="{x}" y="{y - 17}" width="22" height="22" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>'
            f'<path d="M{x + 4} {y - 6} l6 6 l11 -15" style="fill:none;stroke:var(--ink);stroke-width:2.2"/>')


def struck_slip(x, y, w, tag, s):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="56" style="fill:var(--paper);stroke:var(--ink-2);stroke-width:1.2"/>'
    o += t(x + 12, y + 22, tag, size=10.5, weight=700, caps=True) + say(x + 12, y + 42, s, 14)
    o += f'<line x1="{x - 4}" y1="{y + 28}" x2="{x + w + 4}" y2="{y + 28}" style="stroke:var(--conc);stroke-width:2.2"/>'
    return o


# ── Fig. 1 · the funnel of cabimento ────────────────────────────────────────────────────────────────────
def a1():
    o = head('Teste 1 · forma')
    o += '<path d="M40 70H546L560 84V214H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(60, 98, 'Lei ou ato normativo', size=11, weight=700, caps=True)
    for i, s in enumerate(['já promulgado', 'já editado', 'já publicado']):
        o += tick(60, 136 + i * 30) + say(94, 136 + i * 30, s, 16)
    o += t(40, 256, 'Fora do objeto, mesmo com forma', size=10.5, caps=True, fill='var(--conc)')
    o += struck_slip(40, 272, 250, 'PEC', 'mera proposta, ainda não é EC')
    o += struck_slip(310, 272, 250, 'Lei municipal', 'não cabe ADI no STF')
    o += say(40, 400, 'Exceção: a PEC pode ser atacada por mandado')
    o += say(40, 424, 'de segurança, só do parlamentar, contra vício')
    o += say(40, 448, 'do processo legislativo.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-a1',
               label='Formulário do primeiro teste com três caixas marcadas: promulgado, editado, publicado; PEC e lei municipal riscadas, fora do objeto da ADI')


def a2():
    o = head('Teste 2 · espécie · art. 59')
    o += '<path d="M40 64H546L560 78V244H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    for i, s in enumerate(['I · emendas à Constituição', 'II · leis complementares', 'III · leis ordinárias', 'IV · leis delegadas',
                           'V · medidas provisórias', 'VI · decretos legislativos', 'VII · resoluções']):
        o += say(58, 90 + i * 22, s, 14)
    o += t(40, 282, 'Teste 3 · grau de abstração', size=11.5, weight=700, caps=True, ls='.12em')
    o += '<line x1="60" y1="356" x2="540" y2="356" style="stroke:var(--ink);stroke-width:2"/>'
    for x, s, a in ((60, 'concreto · pessoal', 'start'), (540, 'abstrato · geral', 'end')):
        o += f'<line x1="{x}" y1="348" x2="{x}" y2="364" style="stroke:var(--ink);stroke-width:1.5"/>' + t(x, 386, s, size=10.5, caps=True, anchor=a, fill='var(--ink-2)')
    o += '<path d="M466 332 L486 332 L476 348 Z" style="fill:var(--ink)"/>' + t(476, 322, 'ADI', size=11, anchor='middle', weight=700, caps=True, fill='var(--dif)')
    o += '<path d="M114 332 L134 332 L124 348 Z" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>' + t(124, 322, 'ADPF', size=11, anchor='middle', weight=700, caps=True, fill='var(--ink-2)')
    o += say(40, 440, 'Ato concreto e pessoal: ADPF. Abstrato e geral: ADI.')
    o += say(40, 466, 'Cinco dimensões no roteiro didático;', 15, 'var(--ink-2)', True)
    o += say(40, 488, 'impessoalidade e densidade normativa.', 15, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-a2',
               label='O art. 59 com suas sete espécies e uma régua do concreto e pessoal ao abstrato e geral: o ato abstrato vai à ADI, o concreto à ADPF')


def tray(x, y, w, title, items, tone):
    o = f'<path d="M{x} {y}V{y + 190}H{x + w}V{y}" style="fill:none;stroke:{tone};stroke-width:2"/>'
    o += t(x + 14, y - 12, title, size=11, weight=700, caps=True, fill=tone)
    for i, s in enumerate(items):
        o += f'<rect x="{x + 14}" y="{y + 150 - i * 40}" width="{w - 28}" height="32" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.1"/>'
        o += t(x + 26, y + 171 - i * 40, s, size=11.5, caps=True)
    return o


def a3():
    o = head('Resultado do funil')
    o += tray(40, 110, 240, 'Cabe ADI', ['Leis', 'MP · EC', 'DL · resoluções'], 'var(--dif)')
    o += tray(320, 110, 240, 'Não cabe', ['PEC', 'decreto regulamentar', 'norma pré-CF'], 'var(--conc)')
    o += say(40, 400, 'Cada ato cai numa das bandejas pelos três testes:')
    o += say(40, 424, 'forma, espécie, abstração.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-a3',
               label='Duas bandejas: na do cabimento, leis, medidas provisórias, emendas, decretos legislativos e resoluções; na outra, PEC, decreto regulamentar e norma anterior à Constituição')


# ── Fig. 2 · the three layers and the crack ─────────────────────────────────────────────────────────────
def layers(ident, title, crack, law_absent=False, notes=(), label=''):
    o = head(title)
    names = [('Constituição', 92), ('Lei', 184), ('Decreto', 276)]
    for name, y in names:
        if name == 'Lei' and law_absent:
            o += f'<rect x="80" y="{y}" width="440" height="70" style="fill:none;stroke:var(--ink-2);stroke-width:1.2;stroke-dasharray:5 5"/>'
            o += t(100, y + 40, 'Lei · camada não percorrida', size=11.5, weight=700, caps=True, fill='var(--ink-2)')
            continue
        o += f'<rect x="80" y="{y}" width="440" height="70" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
        o += t(100, y + 40, name, size=12.5, weight=700, caps=True)
    if crack == 'lei':          # the decree breaks the law: a crack between decreto and lei
        o += '<path d="M300 254 l12 10 l-16 8 l14 10" style="fill:none;stroke:var(--conc);stroke-width:2.4"/>'
    elif crack == 'cf':         # the autonomous decree reaches the Constitution directly
        o += '<path d="M460 276 V170 l10 -8 l-12 -10 l10 -10" style="fill:none;stroke:var(--conc);stroke-width:2.4"/>'
    for i, (s, fill) in enumerate(notes):
        o += say(40, 420 + i * 26, s, 16, fill)
    return svg('0 0 600 600', o, cls='panel fig on', ident=ident, label=label)


def b1():
    return layers('p-b1', 'Camadas normativas', None, notes=[('A Constituição funda a lei; a lei funda o decreto.', 'var(--ink)'), ('O decreto é ato secundário.', 'var(--ink-2)')],
                  label='Três camadas empilhadas: Constituição, lei e decreto; cada uma funda a de baixo')


def b2():
    return layers('p-b2', 'O decreto extrapola a lei', 'lei', notes=[('A ruptura é entre decreto e lei: crise de legalidade.', 'var(--ink)'), ('A Constituição só é ofendida por via indireta.', 'var(--conc)')],
                  label='A rachadura fica entre o decreto e a lei: o decreto ultrapassa a lei, uma crise de legalidade, e a Constituição é ofendida só indiretamente')


def b3():
    return layers('p-b3', 'Decreto autônomo', 'cf', law_absent=True, notes=[('Sem lei entre eles, o decreto toca a Constituição.', 'var(--ink)'), ('Ofensa direta: cabe ADI.', 'var(--dif)')],
                  label='A camada da lei não existe; o decreto autônomo alcança diretamente a Constituição: ofensa direta, cabe ADI')


def b4():
    o = head('Qual camada foi rompida?')
    rows = [('Indireta', 'decreto → lei → CF', 'ADPF', 'var(--ink-2)'), ('Direta', 'decreto → CF', 'ADI', 'var(--dif)')]
    for i, (k, path, via, tone) in enumerate(rows):
        y = 110 + i * 130
        o += f'<rect x="40" y="{y}" width="520" height="100" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.3"/>'
        o += t(60, y + 32, k, size=11, weight=700, caps=True) + say(60, y + 70, path, 22)
        o += t(530, y + 70, via, size=18, weight=700, caps=True, anchor='end', fill=tone)
    o += say(40, 420, 'O caminho da ofensa decide a ação.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-b4',
               label='Duas fichas: ofensa indireta, do decreto à lei e à Constituição, vai à ADPF; ofensa direta, do decreto à Constituição, à ADI')


# ── Fig. 3 · the time mark and four scenarios ──────────────────────────────────────────────────────────
def tempo1():
    o = head('Constituição de 1988')
    o += '<line x1="40" y1="150" x2="560" y2="150" style="stroke:var(--ink);stroke-width:1.6"/>'
    o += '<line x1="300" y1="110" x2="300" y2="190" style="stroke:var(--ink);stroke-width:3"/>' + t(300, 100, '05/10/1988', size=11, anchor='middle', weight=700)
    o += t(170, 180, 'Antes', size=11, caps=True, anchor='middle') + t(430, 180, 'Depois', size=11, caps=True, anchor='middle')
    o += say(40, 240, 'Norma anterior:', 17) + say(40, 266, 'recepção ou não recepção.', 16, 'var(--ink-2)')
    o += say(320, 240, 'Norma posterior:', 17) + say(320, 266, 'constitucional ou não.', 16, 'var(--ink-2)')
    o += say(40, 330, 'Compatível → recebida. Incompatível → não recebida.', 15)
    o += say(320, 380, 'Vício de origem:', 15, 'var(--dif)') + say(320, 402, 'inconstitucional, cabe ADI.', 15, 'var(--dif)')
    o += say(40, 470, 'Não há inconstitucionalidade superveniente.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-tempo1',
               label='Uma linha do tempo cortada em 5 de outubro de 1988: normas anteriores são recebidas ou não; posteriores nascem constitucionais ou não')


def scenario(y, n, title, order, verdict, case, tone, invalid=False):
    """order: which comes first on the time line, 'P' (parâmetro) or 'N' (norma), with an incompatibility mark."""
    o = t(40, y, f'{n} · {title}', size=10.5, weight=700, caps=True)
    first, second = order
    xs = {first: 70, second: 230}
    o += f'<line x1="60" y1="{y + 26}" x2="330" y2="{y + 26}" style="stroke:var(--ink-2);stroke-width:1"/>'
    for k, x in xs.items():
        lab = {'P': 'parâmetro', 'N': 'norma', 'E': 'EC'}[k]
        o += f'<rect x="{x}" y="{y + 14}" width="84" height="24" style="fill:{"var(--ink)" if k != "N" else "var(--paper)"};stroke:var(--ink);stroke-width:1.2"/>'
        o += t(x + 42, y + 30, lab, size=9.5, anchor='middle', caps=True, fill='var(--paper)' if k != 'N' else 'var(--ink)')
    if invalid:
        x = xs['N']; o += f'<line x1="{x - 4}" y1="{y + 26}" x2="{x + 88}" y2="{y + 26}" style="stroke:var(--conc);stroke-width:2.2"/>'
    o += t(350, y + 22, verdict, size=10.5, weight=700, caps=True, fill=tone) + t(350, y + 38, case, size=10, fill='var(--ink-2)')
    return o


def tempo2():
    o = head('Quatro cenários · norma e parâmetro')
    o += scenario(90, 1, 'lei posterior já nasce incompatível', 'PN', 'inconstitucional', 'ADI 7.739/DF*', 'var(--dif)')
    o += scenario(180, 2, 'Constituição nova, lei anterior', 'NP', 'não recepção', 'ADI 2/DF', 'var(--ink)')
    o += scenario(270, 3, 'EC posterior cria incompatibilidade', 'NE', 'perda de validade', 'ADPF 836 · Tema 1.053', 'var(--ink)')
    o += scenario(360, 4, 'EC posterior admite lei inválida', 'NE', 'sem convalidação', 'ADIs 2.158/2.189', 'var(--conc)', invalid=True)
    o += say(40, 480, 'A ordem no tempo decide a figura.')
    o += say(40, 506, 'A emenda pode retirar validade; o vício de origem fica.', 15, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-tempo2',
               label='Quatro faixas no tempo, cada uma com a ordem entre norma e parâmetro e o resultado: inconstitucional, não recepção, perda de validade, sem convalidação')


def panels():
    return [a1(), a2(), a3(), b1(), b2(), b3(), b4(), tempo1(), tempo2()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-20.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
