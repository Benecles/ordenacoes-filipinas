"""Controle Aula 26 · repristinação, as the tracks family (controle_a16): Lei 1 and Lei 2 as tracks in time.
Revocation ends Lei 1's track and LINDB keeps it ended; the ADI cautelar cuts Lei 2 and, by art. 11, § 2º of
Lei 9.868/1999, Lei 1's track resumes (blue: what the decision does), unless the STF says otherwise (orange).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import track, say

X0, X1, T1, T2 = 60, 540, 220, 380


def frame(title, step):
    o = t(40, 44, title, size=11.5, weight=700, caps=True, ls='.12em')
    o += f'<line x1="{X0}" y1="300" x2="{X1}" y2="300" style="stroke:var(--ink-2);stroke-width:1"/>' + t(X1, 320, 'o tempo segue →', size=10, anchor='end', fill='var(--ink-2)')
    if step >= 1:
        o += f'<line x1="{T1}" y1="140" x2="{T1}" y2="306" style="stroke:var(--ink);stroke-width:1;stroke-dasharray:2 4"/>' + t(T1, 336, 'Lei 2 revoga', size=10, anchor='middle', caps=True)
    if step >= 2:
        o += f'<line x1="{T2}" y1="140" x2="{T2}" y2="306" style="stroke:var(--dif);stroke-width:1.4"/>' + t(T2, 336, 'cautelar na ADI', size=10, anchor='middle', caps=True, fill='var(--dif)')
    return o


def p_vigor():
    o = frame('Repristinação · três normas no tempo', 0)
    o += track(140, [(X0, X1, 'on')], 'Lei 1 · em vigor')
    o += say(40, 400, 'No início, a Lei 1 vale sozinha.')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p26-vigor', label='A Lei 1 como uma faixa contínua no tempo, em vigor, sozinha')


def p_revoga():
    o = frame('A regra geral', 1)
    o += track(140, [(X0, T1, 'on'), (T1, X1, 'off')], 'Lei 1')
    o += track(220, [(T1, X1, 'on')], 'Lei 2')
    o += say(40, 400, 'A Lei 2 revoga a Lei 1.')
    o += say(40, 436, 'LINDB, art. 2º, § 3º: a lei revogada não volta,', 16, 'var(--conc)', True)
    o += say(40, 460, 'salvo previsão expressa.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p26-revoga',
               label='A faixa da Lei 1 termina quando a Lei 2 a revoga; pela LINDB, ela não volta sozinha')


def p_cautelar():
    o = frame('A cautelar suspende a Lei 2', 2)
    o += track(140, [(X0, T1, 'on'), (T1, X1, 'off')], 'Lei 1')
    o += track(220, [(T1, T2, 'on'), (T2, X1, 'off')], 'Lei 2 · impugnada')
    o += say(40, 400, 'Na ADI contra a Lei 2, o STF concede a cautelar:')
    o += say(40, 424, 'suspensão provisória, ainda não o mérito.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p26-cautelar',
               label='A cautelar na ADI corta a faixa da Lei 2; a da Lei 1 continua interrompida')


def p_repristina():
    o = frame('Efeito repristinatório', 2)
    o += track(140, [(X0, T1, 'on'), (T1, T2, 'off'), (T2, X1, 'decided')], 'Lei 1 · volta a ser aplicável')
    o += track(220, [(T1, T2, 'on'), (T2, X1, 'off')], 'Lei 2 · suspensa')
    o += say(40, 400, 'Lei 9.868/1999, art. 11, § 2º: a cautelar torna')
    o += say(40, 424, 'aplicável a legislação anterior.', 16, 'var(--dif)')
    o += say(40, 466, 'Salvo manifestação expressa em sentido contrário.', 16, 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p26-repristina',
               label='Depois da cautelar, a faixa da Lei 1 volta, em azul: o efeito repristinatório, salvo decisão expressa em contrário')


def panels():
    return [p_vigor(), p_revoga(), p_cautelar(), p_repristina()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-26.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
