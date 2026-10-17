"""Direito Constitucional I Aula 11 · where a treaty sits, as strata, with the lift that decides it.

  object   a section through the legal order, like rock strata: the Constitution on top, a thin supralegal stratum
           (since the STF's December 2008 rulings), and the stratum of statutes, where ordinary treaties sit level with
           the law (RE 80.004, 1977). To the right, a lift: a human-rights treaty enters at the bottom; without the
           § 3º vote it stops at the supralegal stratum, with it (each House, two rounds, three fifths) it rises to the
           Constitution's level, equivalent to an amendment. The depositário infiel case is drawn in place: the
           supralegal stratum presses on the statute that authorised the prison, which becomes inapplicable.
  behaves  hover the lift: the car rides up to the top stop and back
  states   ink = the order · hatch = a stratum's material · orange = the statute set aside (a limit)
  facts    all in the lesson (Sarlet; art. 5º §§ 2º and 3º; RE 80.004; RE 466.343, RE 349.703, HC 87.585)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from figkit import t, svg

L, R = 60, 640                 # the strata's extent
S1, S2, S3, S4 = 70, 150, 250, 360   # stratum boundaries: Constitution | supralegal | statutes | bottom
XL = 760                       # the lift shaft


def stack(x, y, lines, anchor='start', size=9.5, lead=13, fill='var(--ink-2)', weight=500):
    return ''.join(t(x, y + k * lead, s, size, fill=fill, anchor=anchor, weight=weight) for k, s in enumerate(lines))


def figure():
    g = ['<defs>'
         '<pattern id="dci11-a" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><path d="M0 0V9" style="stroke:var(--ink-2);stroke-width:.6;opacity:.45"/></pattern>'
         '<pattern id="dci11-b" width="6" height="6" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r=".8" style="fill:var(--ink-2);opacity:.55"/></pattern>'
         '<pattern id="dci11-c" width="12" height="6" patternUnits="userSpaceOnUse"><path d="M0 3H7" style="stroke:var(--ink-2);stroke-width:.6;opacity:.5"/></pattern>'
         '</defs>']
    # strata: drawn as a section with a slightly uneven surface, each with its material
    g.append(f'<path d="M{L} {S1}C200 {S1 - 4} 420 {S1 + 4} {R} {S1}V{S2}H{L}Z" style="fill:url(#dci11-a);stroke:var(--ink);stroke-width:1.6"/>')
    g.append(f'<path d="M{L} {S2}H{R}V{S3}H{L}Z" style="fill:url(#dci11-b);stroke:var(--ink);stroke-width:1.2"/>')
    g.append(f'<path d="M{L} {S3}H{R}V{S4}H{L}Z" style="fill:url(#dci11-c);stroke:var(--ink);stroke-width:1.2"/>')
    g.append(t(L + 14, S1 + 26, 'CONSTITUIÇÃO E EMENDAS', 11, weight=600))
    g.append(t(L + 14, S2 + 22, 'SUPRALEGAL', 11, weight=600))
    g.append(stack(L + 14, S2 + 38, ['tratados de direitos humanos sem o rito do § 3º', 'STF, dez. 2008: RE 466.343 · RE 349.703 · HC 87.585']))
    g.append(t(L + 14, S3 + 22, 'LEIS', 11, weight=600))
    g.append(stack(L + 14, S3 + 38, ['tratados comuns no mesmo nível da lei', 'RE 80.004, 1977']))
    # the depositário case: the supralegal stratum sets aside the statute that allowed the prison
    sx, sy = 470, S3 + 46
    g.append(f'<path d="M{sx - 92} {sy - 18}h184v40h-184z" style="fill:var(--paper);stroke:var(--conc);stroke-width:1.6"/>')
    g.append(stack(sx, sy - 2, ['lei que autorizava a prisão', 'do depositário infiel'], anchor='middle', fill='var(--ink)'))
    g.append(f'<path d="M{sx + 40} {S2 + 60}V{sy - 24}" style="stroke:var(--ink);stroke-width:1.6"/><path d="M{sx + 40} {sy - 20}l-5 -9h10z" style="fill:var(--ink)"/>')
    g.append(t(sx, sy + 40, 'inaplicável', 10, fill='var(--conc)', anchor='middle', weight=600))
    # the lift: a human-rights treaty enters at the bottom; the § 3º vote decides the stop
    g.append(f'<path d="M{XL - 20} {S1 - 14}V{S4}M{XL + 20} {S1 - 14}V{S4}" style="stroke:var(--ink);stroke-width:1.6"/>')
    for y in (S1 + 20, S2 + 30, S3 + 54):
        g.append(f'<path d="M{R} {y}H{XL - 20}" style="stroke:var(--ink-2);stroke-width:.9;stroke-dasharray:2 4"/>')
    g.append(f'<g class="lift"><rect x="{XL - 34}" y="{S1 - 14}" width="68" height="{S4 - S1 + 14}" style="fill:transparent"/>'
             f'<g class="car"><path d="M{XL - 16} {S3 + 38}h32v32h-32z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.8"/>'
             f'<path d="M{XL - 9} {S3 + 48}h18M{XL - 9} {S3 + 55}h18M{XL - 9} {S3 + 62}h12" style="stroke:var(--ink-2);stroke-width:1"/></g></g>')
    g.append(stack(XL, S4 + 22, ['tratado de', 'direitos humanos'], anchor='middle', fill='var(--ink)', weight=600))
    g.append(stack(XL + 34, S2 + 24, ['sem o rito do § 3º:', 'para aqui'], fill='var(--ink)'))
    g.append(stack(XL + 34, S1 + 8, ['com o rito do § 3º:', 'cada Casa, 2 turnos, 3/5', '= equivalente a emenda'], fill='var(--ink)'))
    return svg('0 0 1000 400', ''.join(g), label='A posição dos tratados como estratos, com o elevador do § 3º', ident='dci-a11-estratos')


def block():
    return ('<figure class="instr" id="fig-dci-a11-estratos">' + figure() +
            '<figcaption>O conteúdo diz se é tratado de direitos humanos; o rito do § 3º decide em que andar ele para.</figcaption></figure>')


ANCHOR = ('courses/direito-constitucional-i/aula-11.html', 'Para aplicar o § 3º, identifique primeiro o conteúdo do tratado.')
