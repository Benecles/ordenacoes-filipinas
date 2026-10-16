"""Direito Constitucional I Aula 06 · the six questions a PEC must clear, as a canal with gates.

  object   a canal from the proposal (left) to the amendment (right). The boat is the PEC; every question in the
           lesson's list is a structure on the water, numbered as in the list: (1) a storm gate shut during
           intervention or a state of exception; (2) three streams that may feed the canal (the only initiatives);
           (3) the gate of § 4º; (4) a gate nobody wrote down (dashed); (5) two locks, Câmara and Senado, each lifting
           twice at three fifths; (6) a spillway where a rejected proposal leaves and cannot return in the same
           session. At the end the Mesas promulgate it with a number.
  behaves  hover a gate: it swings as if tested. The canal never moves
  states   orange = a limit (the gates that bar: §1, §4, tacit) · dashed = unwritten · ink = the procedure
  facts    all from the lesson's own list (art. 60, I–III, §§ 1º–5º; tacit limits per Bonavides as the lesson gives them)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import t, svg

YT, YB = 196, 232            # the banks
X0, X1 = 26, 976


def gate(x, tone='ink', dash=None, num=None):
    c = 'var(--conc)' if tone == 'conc' else 'var(--ink)'
    d = f';stroke-dasharray:{dash}' if dash else ''
    out = (f'<g class="gate"><rect x="{x - 14}" y="{YT - 18}" width="28" height="{YB - YT + 36}" style="fill:transparent"/>'
           f'<path d="M{x} {YT - 12}V{YT}M{x} {YB}V{YB + 12}" style="stroke:{c};stroke-width:3"/>'
           f'<path class="leaf" d="M{x} {YT}V{YB}" style="stroke:{c};stroke-width:4{d};transform-origin:{x}px {YT}px"/></g>')
    if num:
        out += (f'<circle cx="{x}" cy="{YT - 30}" r="9" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
                + t(x, YT - 26.5, str(num), 10, anchor='middle', weight=600))
    return out


def stack(x, y, lines, anchor='middle', size=9.5, lead=13, fill='var(--ink-2)'):
    return ''.join(t(x, y + k * lead, s, size, fill=fill, anchor=anchor) for k, s in enumerate(lines))


def figure():
    g = []
    # the canal
    g.append(f'<path d="M{X0} {YT}H{X1}M{X0} {YB}H{X1}" style="stroke:var(--ink);stroke-width:1.8"/>')
    g.append(f'<path d="M{X0} {(YT + YB) / 2}H{X1}" style="stroke:var(--ink-2);stroke-width:.7;stroke-dasharray:2 6"/>')
    # the boat: the PEC
    g.append(f'<path d="M44 {YT + 22}h34l-6 7h-22z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
             f'<path d="M61 {YT + 22}V{YT + 6}l11 9h-11" style="fill:none;stroke:var(--ink);stroke-width:1.3"/>')
    g.append(t(60, YB + 26, 'PEC', 10.5, anchor='middle', weight=600))
    # 1 circumstance: the storm gate
    g.append(gate(140, 'conc', num=1))
    g.append(t(140, YT - 48, '§ 1º', 9.5, fill='var(--conc)', anchor='middle', weight=600))
    g.append(stack(140, YB + 30, ['intervenção federal', 'estado de defesa', 'estado de sítio']))
    # 2 initiative: three streams that may feed the canal
    for k, (lab, x) in enumerate([('1/3 da Câmara ou do Senado', 236), ('Presidente', 282), ('+ ½ das Assembleias', 328)]):
        g.append(f'<path d="M{x} {58 + k * 34}C{x} {150} {x + 34} {YT - 22} {x + 40} {YT}" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>')
        g.append(t(x + 7, 61 + k * 34, lab, 9.5, fill='var(--ink-2)'))
    g.append(f'<circle cx="306" cy="{YT - 30}" r="9" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>' + t(306, YT - 26.5, '2', 10, anchor='middle', weight=600))
    g.append(t(306, YB + 30, 'I a III', 9.5, fill='var(--ink-2)', anchor='middle'))
    # 3 express matter: the gate of § 4º
    g.append(gate(420, 'conc', num=3))
    g.append(t(420, YT - 48, '§ 4º', 9.5, fill='var(--conc)', anchor='middle', weight=600))
    g.append(stack(420, YB + 30, ['forma federativa', 'voto direto, secreto,', 'universal e periódico', 'separação de Poderes', 'direitos e garantias', 'individuais']))
    # 4 tacit matter: the gate nobody wrote down
    g.append(gate(586, 'conc', dash='4 4', num=4))
    g.append(t(586, YT - 48, 'tácito', 9.5, fill='var(--conc)', anchor='middle', weight=600))
    g.append(stack(586, YB + 30, ['regras da própria', 'reforma', 'pluripartidarismo', 'soberania nacional']))
    # 5 the vote: two locks, each lifting twice at three fifths
    for x, house in [(724, 'Câmara'), (836, 'Senado')]:
        g.append(gate(x - 22) + gate(x + 22))
        g.append(f'<path d="M{x - 18} {YB - 10}h36M{x - 18} {YB - 18}h36" style="stroke:var(--ink-2);stroke-width:1"/>')
        g.append(t(x, YT - 48, house, 10, anchor='middle', weight=600))
        g.append(stack(x, YB + 30, ['2 turnos', '3/5 dos membros']))
    g.append(f'<circle cx="780" cy="{YT - 30}" r="9" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>' + t(780, YT - 26.5, '5', 10, anchor='middle', weight=600))
    # 6 the spillway: rejected or prejudiced matter leaves and can't come back this session
    g.append(f'<path d="M888 {YB}C888 {YB + 40} 894 {YB + 70} 910 {YB + 96}M912 {YB}C912 {YB + 36} 918 {YB + 66} 934 {YB + 96}" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>')
    g.append(f'<circle cx="946" cy="{YB + 108}" r="9" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>' + t(946, YB + 111.5, '6', 10, anchor='middle', weight=600))
    g.append(stack(920, YB + 136, ['rejeitada ou prejudicada:', 'não volta na mesma', 'sessão legislativa · § 5º'], anchor='middle'))
    # the end: promulgated by the Mesas, with a number
    g.append(f'<path d="M990 {YT - 6}h26l8 8v38h-34z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.5"/>'
             f'<path d="M996 {YT + 12}h20M996 {YT + 20}h20M996 {YT + 28}h14" style="stroke:var(--ink-2);stroke-width:1"/>')
    g.append(t(1004, YT - 18, 'EMENDA', 9.5, anchor='middle', weight=600))
    g.append(stack(1004, YB + 30, ['as Mesas', 'promulgam', 'com número', '§ 3º']))
    return svg('0 0 1050 410', ''.join(g), label='As seis perguntas do art. 60 como um canal com comportas', ident='dci-a06-canal')


def block():
    return ('<figure class="instr" id="fig-dci-a06-canal">' + figure() +
            '<figcaption>Os números seguem o roteiro: uma PEC aprovada por três quintos em dois turnos ainda para na comporta 1 '
            'se for votada em estado de sítio.</figcaption></figure>')


ANCHOR = ('courses/direito-constitucional-i/aula-06.html', 'A ordem das perguntas que uma PEC precisa vencer segue esse desenho:', '</ol>')
