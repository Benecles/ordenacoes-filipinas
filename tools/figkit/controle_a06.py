"""Controle Aula 06 · tipos de inconstitucionalidade. Conduct as two records (a law edited / a law never
edited, the greve dos servidores), formal vs material as where the defect sits on a law's sheet (its path
vs its content), and the three formal sub-species as stamps on the act. The old caption named the kinds by
colour (azul / vermelhão); position now does it, and the caption is rewritten.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t
from controle_a16 import say
from controle_a09 import stamp, paper


def head(s):
    return t(40, 44, s, size=11.5, weight=700, caps=True, ls='.12em')


def conduta():
    o = head('Quanto à conduta')
    o += paper(40, 70, 240, 140, 'Lei editada')
    o += stamp(160, 186, 'por ação', 'var(--ink)')
    o += f'<path d="M320 70H506L520 84V210H320Z" style="fill:none;stroke:var(--ink-2);stroke-width:1.4;stroke-dasharray:6 5"/>'
    o += t(334, 96, 'Lei que não veio', size=10.5, weight=700, caps=True, fill='var(--ink-2)')
    o += stamp(420, 186, 'por omissão', 'var(--conc)')
    o += say(40, 270, 'Por ação: o legislador edita lei incompatível.')
    o += say(40, 300, 'Por omissão: falta a norma que a Constituição exigia.')
    o += say(40, 344, 'Ex.: greve dos servidores (art. 37, VII), sem a lei', 15, 'var(--ink-2)', True)
    o += say(40, 366, 'específica. A omissão pode ser total ou parcial.', 15, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-conduta',
               label='Duas folhas: uma lei editada, carimbada por ação; uma lei que não veio, tracejada, carimbada por omissão')


def sheet_with(where):
    """A law's sheet: top band = the path (iniciativa, votação, sanção), body = the content. where: 'path' | 'content'."""
    o = '<path d="M40 70H506L520 84V300H40Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
    o += t(56, 96, 'Lei X', size=11, weight=700, caps=True)
    o += t(56, 124, 'iniciativa · votação · sanção · publicação', size=10, caps=True, fill='var(--ink-2)')
    o += '<line x1="40" y1="140" x2="520" y2="140" style="stroke:var(--ink);stroke-width:1"/>'
    o += ''.join(f'<line x1="56" y1="{170 + i * 22}" x2="{490 - (i % 3) * 50}" y2="{170 + i * 22}" style="stroke:var(--ink-2);stroke-width:1"/>' for i in range(6))
    if where == 'path':
        o += '<rect x="48" y="106" width="464" height="28" style="fill:none;stroke:var(--conc);stroke-width:2.2"/>'
    else:
        o += '<rect x="48" y="152" width="464" height="136" style="fill:none;stroke:var(--conc);stroke-width:2.2"/>'
    return o


def formal():
    o = head('Vício formal · nomodinâmico') + sheet_with('path')
    o += say(40, 350, 'O defeito está no caminho: como a norma nasceu.')
    o += say(40, 380, 'Competência, forma, prazos, rito.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-formal', label='A folha de uma lei com o defeito marcado na faixa do caminho: iniciativa, votação, sanção, publicação')


def material():
    o = head('Vício material · nomoestático') + sheet_with('content')
    o += say(40, 350, 'O defeito está no conteúdo: o que a norma diz.')
    o += say(40, 380, 'Ex.: violação a direitos fundamentais.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-material', label='A mesma folha com o defeito marcado no corpo, o conteúdo da norma')


def arvore():
    o = head('Vício formal · três subespécies') + sheet_with('path')
    for i, (s, sub) in enumerate([('orgânica', 'competência'), ('propriamente dita', 'iniciativa e rito'), ('pressupostos objetivos', 'requisito do ato')]):
        x = 40 + i * 176
        o += f'<rect x="{x}" y="340" width="160" height="70" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.2"/>'
        o += t(x + 10, 366, s, size=10, weight=700, caps=True) + say(x + 10, 394, sub, 14, 'var(--ink-2)')
    o += say(40, 460, 'Todas independem do conteúdo.', 16, 'var(--ink-2)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-arvore', label='A faixa do caminho e as três subespécies do vício formal: orgânica, propriamente dita e pressupostos objetivos')


def organica():
    o = head('Orgânica · quem podia legislar')
    o += paper(40, 70, 300, 130, 'Lei municipal')
    o += stamp(190, 180, 'matéria da União', 'var(--conc)')
    o += say(40, 270, 'O Município edita lei sobre matéria federal:')
    o += say(40, 294, 'invade a competência da União.', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-organica', label='Uma lei municipal carimbada matéria da União: vício orgânico, de competência')


def propria():
    o = head('Formal propriamente dita')
    o += paper(40, 70, 240, 130, 'Projeto · iniciativa')
    o += stamp(160, 180, 'só o Executivo', 'var(--conc)')
    o += t(40, 236, 'subjetivo · iniciativa', size=10, caps=True)
    o += paper(320, 70, 240, 130, 'Votação')
    o += stamp(440, 170, 'LC por maioria simples', 'var(--conc)', -5)
    o += t(320, 236, 'objetivo · rito', size=10, caps=True)
    o += say(40, 300, 'Subjetivo: violou a regra de iniciativa.')
    o += say(40, 324, 'Objetivo: violou o rito depois dela; ex.: PEC com um', 16)
    o += say(40, 348, 'só turno em cada Casa.', 16)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-propria',
               label='Dois papéis: um projeto carimbado só o Executivo, vício de iniciativa; uma votação carimbada lei complementar por maioria simples, vício de rito')


def pressupostos():
    o = head('Pressupostos objetivos do ato')
    o += paper(40, 70, 240, 130, 'Lei estadual · novo Município')
    o += stamp(160, 180, 'sem estudo de viabilidade', 'var(--conc)', -5)
    o += paper(320, 70, 240, 130, 'Medida provisória')
    o += stamp(440, 180, 'sem urgência', 'var(--conc)')
    o += say(40, 270, 'Faltou a formalidade que a Constituição exige')
    o += say(40, 294, 'para aquele ato (art. 18, § 4º; relevância e urgência).', 16, 'var(--ink-2)')
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-pressupostos',
               label='Uma lei estadual que cria Município, carimbada sem estudo de viabilidade; uma medida provisória carimbada sem urgência')


TEXT = [('Fig. 2 · Formal (azul) × material (vermelhão)', 'Fig. 2 · Formal × material: o caminho e o conteúdo')]


def panels():
    return [conduta(), formal(), material(), arvore(), organica(), propria(), pressupostos()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    path = 'courses/controle-de-constitucionalidade/aula-06.html'
    n = inject(path, {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    p = os.path.join(os.path.dirname(__file__), '..', '..', path)
    h = open(p).read()
    for a, b in TEXT:
        if a not in h and b not in h:
            raise SystemExit(f'text not found: {a}')
        h = h.replace(a, b)
    open(p, 'w').write(h)
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
