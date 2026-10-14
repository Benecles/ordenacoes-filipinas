"""Controle Aula 14 · Fig. 1: arrastamento drawn on the norms themselves. The declared article is struck
(blue: what the STF decided); the dependent norm is struck with it, dashed (the extension); a norm on the
same subject, or a provision that keeps its own sense, stays whole, with the limit in orange.
The facts are the lesson's own test: Lei X authorises a licence; Decreto Y only sets the form and the deadline.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import WARN, svg, t

SER = 'font-family:var(--serif,serif);font-size:14px;fill:var(--ink)'


def sheet(x, y, w, title, rows, struck=(), dashed=()):
    """rows: list of strings; struck / dashed: row indexes. Returns (svg, height)."""
    h = 44 + len(rows) * 26 + 10
    o = (f'<path d="M{x} {y}H{x + w - 14}L{x + w} {y + 14}V{y + h}H{x}Z" style="fill:var(--paper);stroke:var(--ink);stroke-width:1.4"/>'
         f'<path d="M{x + w - 14} {y}V{y + 14}H{x + w}" style="fill:var(--paper-2);stroke:var(--ink);stroke-width:1"/>')
    o += t(x + 14, y + 26, title, size=11.5, weight=700, caps=True, ls='.12em')
    for i, r in enumerate(rows):
        yy = y + 52 + i * 26
        o += f'<text x="{x + 14}" y="{yy}" style="{SER}">{r}</text>'
        if i in struck or i in dashed:
            dash = ';stroke-dasharray:7 5' if i in dashed else ''
            o += f'<line x1="{x + 10}" y1="{yy - 5}" x2="{x + w - 12}" y2="{yy - 5}" style="stroke:var(--dif);stroke-width:2.2{dash}"/>'
    return o, h


def note(x, y, s, fill='var(--ink)', italic=False):
    st = f'font-family:var(--serif,serif);font-size:15px;fill:{fill}' + (';font-style:italic' if italic else '')
    return f'<text x="{x}" y="{y}" style="{st}">{s}</text>'


def vertical():
    o = t(40, 40, 'Vertical · lei e decreto', size=11.5, weight=700, caps=True, ls='.12em')
    s1, h1 = sheet(40, 64, 330, 'Lei X', ['Art. 1º Fica autorizada a licença L.'], struck=[0])
    o += s1 + t(380, 116, 'declarada', size=10.5, caps=True, fill='var(--dif)') + t(380, 130, 'inconstitucional', size=10.5, caps=True, fill='var(--dif)')
    y2 = 64 + h1 + 52
    o += f'<path d="M110 {64 + h1} V{y2}" style="stroke:var(--ink);stroke-width:1.2"/>' + t(120, 64 + h1 + 30, 'regulamenta', size=10.5, caps=True, fill='var(--ink-2)')
    s2, h2 = sheet(40, y2, 330, 'Decreto Y', ['Art. 1º O pedido da licença L usa o', 'formulário F.', 'Art. 2º Fixa o prazo do pedido.'], dashed=[0, 1, 2])
    o += s2 + t(380, y2 + 60, 'arrastado', size=10.5, caps=True, fill='var(--dif)')
    o += note(380, y2 + 84, 'sem a Lei X,', 'var(--ink-2)', True) + note(380, y2 + 104, 'não tem fundamento', 'var(--ink-2)', True)
    y3 = y2 + h2 + 34
    s3, h3 = sheet(40, y3, 330, 'Lei W', ['Art. 1º Também trata de licenças.'])
    o += s3 + t(380, y3 + 46, 'fica', size=10.5, caps=True, fill='var(--conc)')
    o += note(380, y3 + 70, 'mesmo assunto,', 'var(--conc)', True) + note(380, y3 + 90, 'sem dependência', 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-vertical',
               label='Lei X riscada como inconstitucional; o Decreto Y, que só a regulamenta, riscado com ela, tracejado; a Lei W, sobre o mesmo assunto, fica inteira')


def horizontal():
    o = t(40, 40, 'Horizontal · dentro da mesma lei', size=11.5, weight=700, caps=True, ls='.12em')
    rows = ['Art. A Fica autorizada a licença L.', 'Art. B Nos termos do art. A, o pedido', 'usa o formulário F.', 'Art. C A repartição publica seus', 'horários de atendimento.']
    s, h = sheet(40, 64, 360, 'Lei X', rows, struck=[0], dashed=[1, 2])
    o += s
    o += t(412, 116, 'impugnado', size=10.5, caps=True, fill='var(--dif)')
    o += t(412, 154, 'remete a A:', size=10.5, caps=True, fill='var(--dif)') + t(412, 168, 'cai junto', size=10.5, caps=True, fill='var(--dif)')
    o += t(412, 206, 'sentido próprio:', size=10.5, caps=True, fill='var(--conc)') + t(412, 220, 'fica', size=10.5, caps=True, fill='var(--conc)')
    y = 64 + h + 60
    o += note(40, y, 'A extensão segue a dependência, e ela tem de ser demonstrada.')
    o += note(40, y + 28, 'O mesmo assunto, sem dependência, deixa a norma de pé.', 'var(--conc)', True)
    return svg('0 0 600 600', o, cls='panel fig on', ident='p-horizontal',
               label='Na mesma lei, o art. A é declarado inconstitucional; o art. B, que remete a ele, cai junto; o art. C, com sentido próprio, fica')


def panels():
    return [vertical(), horizontal()]


if __name__ == '__main__':
    import re
    from inject import inject
    WARN.clear()
    n = inject('courses/controle-de-constitucionalidade/aula-14.html', {re.search(r'id="([^"]+)"', s).group(1): s for s in panels()})
    print(n, 'figures;', '\n'.join(WARN) or 'no text warnings')
