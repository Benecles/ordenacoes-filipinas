"""Aula 02 force rose, cast through the planta part.

mode: 'rosa' (default). Five traceable rays relate Zeca's existing exclusivity
contract to freedom, binding force, relativity, social function and objective
good faith. Selecting a ray highlights its relation and changes the legal explanation below; no
numerical weight is assigned to a principle. No arbitrary facts or legal rankings.
The desktop rose has a compact phone variant with the same topology.
"""
from __future__ import annotations
import math
import re
from . import svg as S
from . import planta

FORCES = [
 ('liberdade','Liberdade contratual','escolher e autovincular-se',-150,
  'A liberdade permite assumir o compromisso de exclusividade; a oportunidade posterior de contratar não o desfaz.'),
 ('forca','Força obrigatória','exigir o compromisso',-30,
  'Fischer e All-E podiam contar com o compromisso vigente: o descumprimento permitia exigir reparação.'),
 ('relatividade','Relatividade','a prestação cabe às partes',42,
  'A África não devia a prestação artística prometida por Zeca; a relatividade não afasta responsabilidade por interferência ilícita própria.'),
 ('social','Função social','respeitar o vínculo alheio',138,
  'A função social situa o vínculo no meio que ele afeta; o dever de reparar a interferência ilícita depende do caso.'),
 ('conduta','Boa-fé objetiva','agir com lealdade',90,
  'A lealdade de conduta fundamenta o dever de respeito: conhecer a exclusividade e induzir sua ruptura pode constituir ilícito.')]

def rose(narrow=False):
    if narrow:
        w, h = 340, 420
        cx, cy = 170, 190
        o = []
        for key, label, note, angle, answer in FORCES:
            a = math.radians(angle); radius = 76
            x, y = cx + radius * math.cos(a), cy + radius * math.sin(a)
            o.append(f'<g data-thread="{key}" data-fio="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">')
            o.append(S.line(cx, cy, x, y, stroke=S.INK, stroke_width=1.7))
            pos = {'liberdade': (10, 69), 'forca': (184, 69), 'relatividade': (184, 310), 'social': (10, 310), 'conduta': (170, 385)}
            tx, ty = pos[key]; anchor = 'middle' if key == 'conduta' else 'start'
            words = label.split(); lines = [' '.join(words[:-1]), words[-1]] if len(words) > 1 else [label]
            for i, line in enumerate(lines):
                o.append(S.text(tx, ty + i * 17, line, size=13, family=S.SANS, anchor=anchor, weight='600'))
            o.append(S.circle(x, y, 3.5, fill=S.PAPER, stroke=S.INK, stroke_width=1.4))
            o.append('</g>')
        bw, bh = 118, 68
        o.append(S.rect(cx - bw / 2, cy - bh / 2, bw, bh, fill=S.PAPER, stroke=S.INK, stroke_width=1.5, data_lk='liberdade forca relatividade social conduta'))
        o.append(S.text(cx, cy - 8, 'Zeca · Nova Schin', size=13, family=S.SANS, anchor='middle', weight='600'))
        o.append(S.line(cx - bw / 2 + 12, cy + 2, cx + bw / 2 - 12, cy + 2, stroke=S.GRID, stroke_width=1))
        o.append(S.text(cx, cy + 22, 'exclusividade vigente', size=12, family=S.SERIF, anchor='middle'))
        return S.svg(w, h, 'Cinco forças incidentes no mesmo contrato de exclusividade', o)

    # Desktop: the Zeca case as a wiring plan with five traceable forces and a measured calendar of the decisions
    w, h = 1080, 420
    o = []
    T = S.text
    yr = 190
    FA, NS, ZE, AF, BR = 110, 330, 560, 800, 990

    def grp(key, label, parts):
        return (f'<g data-thread="{key}" data-fio="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">'
                + ''.join(parts) + '</g>')

    def hollow(x, y, col=S.INK, r=8):
        return S.circle(x, y, r, fill=S.PAPER, stroke=col, stroke_width=2.2)

    def hitbox(x, y, bw, bh):
        return S.rect(x, y, bw, bh, fill=S.PAPER, opacity='0')

    sx = lambda yr_: 140 + (yr_ - 2005) * 94
    x2005, x2011, x2014 = sx(2005), sx(2011), sx(2014.42)

    # wider boundary first (função social), then the parties' boundary (relatividade)
    o += [grp('social', 'Função social', [
              S.rect(24, 52, 1032, 278, fill='none', stroke=S.INK2, stroke_width=1.4, stroke_dasharray='2 6'),
              S.rect(17, 45, 14, 14, fill=S.PAPER, stroke=S.INK2, stroke_width=1.6),
              hitbox(34, 306, 440, 22),
              T(38, 322, 'Função social', size=13, family=S.SANS, weight=650),
              T(134, 322, 'o vínculo respeita o meio que ele afeta', size=12.5, family=S.SERIF, fill=S.INK2)]),
          grp('relatividade', 'Relatividade', [
              S.rect(50, 124, 570, 176, fill='none', stroke=S.INK, stroke_width=1.8, stroke_dasharray='8 5'),
              hitbox(56, 276, 330, 22),
              T(62, 292, 'Relatividade', size=13, family=S.SANS, weight=650),
              T(152, 292, 'a prestação cabe só às partes', size=12.5, family=S.SERIF, fill=S.INK2)]),
          grp('liberdade', 'Liberdade contratual', [
              S.line(ZE, yr - 8, ZE, 72, stroke=S.DIF, stroke_width=1.8),
              S.path(f'M{ZE},72 H{ZE - 12} L{ZE - 6},78 L{ZE - 12},84 H{ZE}', fill=S.PAPER, stroke=S.DIF, stroke_width=1.8),
              hitbox(ZE - 14, 60, 190, 40),
              T(ZE + 12, 76, 'Liberdade contratual', size=13, family=S.SANS, weight=650, fill=S.DIF),
              T(ZE + 12, 92, 'escolher e autovincular-se', size=12.5, family=S.SERIF, fill=S.INK2)]),
          grp('forca', 'Força obrigatória', [
              S.rect(ZE - 121, yr - 18, 12, 36, fill=S.INK, stroke=S.INK, stroke_width=1.2),
              hitbox(ZE - 190, yr + 22, 150, 44),
              T(ZE - 115, yr + 38, 'Força obrigatória', size=13, family=S.SANS, weight=650, anchor='middle'),
              T(ZE - 115, yr + 54, 'exigir o compromisso', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle')]),
          grp('conduta', 'Boa-fé objetiva', [
              S.line(AF - 10, yr, ZE + 10, yr, stroke=S.CONC, stroke_width=2, stroke_dasharray='3 5'),
              S.path('M660,%d V%d M660,%d L646,%d L656,%d L646,%d L660,%d' % (yr - 12, yr + 12, yr - 12, yr - 6, yr, yr + 6, yr + 12), fill='none', stroke=S.CONC, stroke_width=2),
              S.path(f'M{AF},{yr + 8} V334 H{x2014}', fill='none', stroke=S.CONC, stroke_width=1.8, stroke_dasharray='3 5'),
              hollow(x2014, 334, S.CONC, 6),
              hitbox(AF + 8, 238, 232, 64),
              T(AF + 14, 256, 'Boa-fé objetiva', size=13, family=S.SANS, weight=650, fill=S.CONC),
              T(AF + 14, 272, 'respeitar o contrato alheio', size=12.5, family=S.SERIF, fill=S.INK2),
              T(AF + 14, 288, 'concorrência desleal · Lei 9.279/96', size=12, family=S.SERIF, fill=S.INK2),
              T(695, yr - 14, 'aliciamento', size=12.5, family=S.SERIF, fill=S.CONC, anchor='middle')])]
    # the contract wiring: agencies, Nova Schin, Zeca; África and Brahma outside the boundary
    o += [S.line(FA, yr, ZE, yr, stroke=S.INK, stroke_width=2.6, data_lk='liberdade forca relatividade social conduta'),
          S.line(AF, yr, BR, yr, stroke=S.INK2, stroke_width=1.6),
          hollow(FA, yr), hollow(NS, yr), hollow(ZE, yr), hollow(AF, yr, S.CONC), hollow(BR, yr, S.INK2),
          T(220, yr - 14, 'criam a campanha', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle'),
          T(385, yr - 14, 'exclusividade', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle'),
          T(895, yr - 14, 'anuncia a Brahma', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle'),
          T(FA, yr + 28, 'Fischer · All-E', size=13, family=S.SANS, anchor='middle', weight=650),
          T(NS, yr + 28, 'Nova Schin', size=13, family=S.SANS, anchor='middle', weight=650),
          T(ZE, yr + 28, 'Zeca', size=13, family=S.SANS, anchor='middle', weight=650),
          T(AF - 12, yr + 28, 'África', size=13, family=S.SANS, anchor='end', weight=650),
          T(BR, yr + 28, 'Brahma', size=13, family=S.SANS, anchor='middle', weight=650)]
    # the agencies' investment, measured along the campaign
    o += [S.path(f'M{FA},{yr + 54} V{yr + 60} H{ZE} V{yr + 54}', fill='none', stroke=S.INK2, stroke_width=1.1),
          T((FA + ZE) / 2 - 110, yr + 78, 'investimento enquanto o compromisso corria', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle')]
    # the case in time: scale in years (measured), three decisions flagged
    ys = 392
    o += [S.rect(40, ys, 1010, 26, fill=S.PAPER, stroke=S.INK, stroke_width=1.4)]
    o += S.hatch(x2005, ys + 1, x2014 - x2005, 24, step=7, stroke=S.GRID, stroke_width=1)
    o += [S.rect(x2005 + 130, ys + 4, 310, 18, fill=S.PAPER, stroke='none'),
          T(x2005 + 285, ys + 18, 'FISCHER × ÁFRICA · REsp 1.316.149/SP', size=12.5, anchor='middle', weight=600)]
    for yv in range(2005, 2015):
        x = sx(yv)
        o += [S.line(x, ys + 26, x, ys + 33, stroke=S.INK, stroke_width=1),
              T(x, ys + 46, str(yv), size=12.5, anchor='middle', fill=S.INK2)]
    stations = [(x2005, 'start', x2005 - 96, '9ª Vara Cível Central · SP', 'sentença: morais de R$ 500 mil e R$ 100 mil'),
                (x2011, 'end', x2011 - 10, 'TJSP · 3ª Câmara de Direito Privado', 'concorrência desleal; condena em cerca de R$ 20 milhões'),
                (x2014, 'end', x2014 - 14, 'STJ · 03/06/2014', 'voto de Nancy Andrighi prevalece; relator vencido')]
    for x, anc, tx, a, b in stations:
        o += [S.line(x, 374, x, ys, stroke=S.INK, stroke_width=1.3), S.rect(x - 4, 370, 8, 8, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
              T(tx, 352, a, size=12.5, family=S.SANS, weight=650, anchor=anc), T(tx, 367, b, size=12, family=S.SERIF, fill=S.INK2, anchor=anc)]
    o += [S.line(x2014, 340, x2014, 370, stroke=S.CONC, stroke_width=1.8, stroke_dasharray='3 5')]
    return S.svg(w, h, 'Cinco forças incidentes no contrato de Zeca e as decisões que o alcançaram', o).replace(f'viewBox="0 0 {w} {h}"', 'viewBox="0 44 1080 402"', 1)

def build(p:dict)->tuple[str,list[dict]]:
    if p.get('mode')!='rosa':
        q=dict(p)
        x,y,w,h=q.pop('crop',[50,104,1083,340])
        drawing,objects=planta.build(q)
        drawing=re.sub(r'viewBox="[^"]*"',f'viewBox="{x} {y} {w} {h}"',drawing,count=1)
        drawing=re.sub(r'font-size="(1[12](?:\.5)?)"','font-size="13"',drawing)
        return drawing,objects
    desktop=rose();mobile=rose(True)
    answers=''.join(f'<p data-answer="{k}"'+('' if i==0 else ' hidden')+'>'+S.esc(a)+'</p>' for i,(k,l,n,g,a) in enumerate(FORCES))
    return ('<div class="force-rose"><div class="rose-desktop">'+desktop+'</div><div class="rose-mobile">'+mobile+'</div><div class="force-readout">'+answers+'</div></div>',[])
