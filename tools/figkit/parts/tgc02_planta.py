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

    # Desktop architectural force-vector drafting-table instrument
    w, h = 1080, 396
    o = []
    T = S.text

    def bracket(x1, x2, y, label, col=S.INK2, dy=-7):
        return (
            S.path(f'M{x1},{y+5} V{y} H{x2} V{y+5}', fill='none', stroke=col, stroke_width=1.1)
            + T((x1 + x2) / 2, y + dy, label, size=12.5, anchor='middle', fill=col)
        )

    y0 = 196
    zx, nx, ax = 300, 780, 1010
    def grp(key, label, note, parts):
        return (f'<g data-thread="{key}" data-fio="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">'
                + ''.join(parts) + '</g>')
    def hollow(x, y, col=S.INK, r=8):
        return S.circle(x, y, r, fill=S.PAPER, stroke=col, stroke_width=2.2)
    # wider boundary first (função social), then the parties' boundary (relatividade), so every ring is traceable
    o += [grp('social', 'Função social', 'respeitar o vínculo alheio', [
              S.rect(40, 92, 1000, 212, fill='none', stroke=S.INK2, stroke_width=1.4, stroke_dasharray='2 6'),
              S.rect(33, 85, 14, 14, fill=S.PAPER, stroke=S.INK2, stroke_width=1.6),
              T(40, 328, 'Função social', size=13, family=S.SANS, weight=650),
              T(144, 328, 'o vínculo respeita o meio que ele afeta', size=12.5, family=S.SERIF, fill=S.INK2)]),
          grp('relatividade', 'Relatividade', 'a prestação cabe às partes', [
              S.rect(196, 138, 700, 134, fill='none', stroke=S.INK, stroke_width=1.8, stroke_dasharray='8 5'),
              T(884, 130, 'Relatividade', size=13, family=S.SANS, weight=650, anchor='end'),
              T(884, 160, 'a prestação cabe só às partes', size=12.5, family=S.SERIF, fill=S.INK2, anchor='end')]),
          grp('liberdade', 'Liberdade contratual', 'escolher e autovincular-se', [
              S.line(zx, y0 - 8, zx, 112, stroke=S.DIF, stroke_width=1.8), S.path(f'M{zx},112 H{zx - 12} L{zx - 6},118 L{zx - 12},124 H{zx}', fill=S.PAPER, stroke=S.DIF, stroke_width=1.8),
              T(zx + 12, 108, 'Liberdade contratual', size=13, family=S.SANS, weight=650, fill=S.DIF),
              T(zx + 12, 124, 'escolher e autovincular-se', size=12.5, family=S.SERIF, fill=S.INK2)]),
          grp('forca', 'Força obrigatória', 'exigir o compromisso', [
              S.rect(530, y0 - 18, 12, 36, fill=S.INK, stroke=S.INK, stroke_width=1.2),
              T(536, y0 + 42, 'Força obrigatória', size=13, family=S.SANS, weight=650, anchor='middle'),
              T(536, y0 + 58, 'exigir o compromisso', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle')]),
          grp('conduta', 'Boa-fé objetiva', 'agir com lealdade', [
              S.line(ax - 10, y0, nx + 70, y0, stroke=S.CONC, stroke_width=2, stroke_dasharray='3 5'),
              S.path(f'M{nx + 70},{y0 - 12} V{y0 + 12} M{nx + 70},{y0 - 12} L{nx + 56},{y0 - 6} L{nx + 66},{y0} L{nx + 56},{y0 + 6} L{nx + 70},{y0 + 12}', fill='none', stroke=S.CONC, stroke_width=2),
              T(ax, y0 - 20, 'África', size=13, family=S.SANS, anchor='middle', weight=650),
              T(ax + 24, y0 + 78, 'Boa-fé objetiva', size=13, family=S.SANS, weight=650, anchor='end', fill=S.CONC),
              T(ax + 24, y0 + 94, 'respeitar o contrato alheio', size=12.5, family=S.SERIF, fill=S.INK2, anchor='end')]),
          hollow(ax, y0, S.CONC)]
    # the contract thread: Zeca to Nova Schin; the core carries the trace hook
    o += [S.line(zx, y0, nx, y0, stroke=S.INK, stroke_width=2.6, data_lk='liberdade forca relatividade social conduta'),
          hollow(zx, y0), hollow(nx, y0),
          T(zx, y0 + 28, 'Zeca', size=13, family=S.SANS, anchor='middle', weight=650), T(nx, y0 + 28, 'Nova Schin', size=13, family=S.SANS, anchor='middle', weight=650),
          T(660, y0 - 14, 'exclusividade contratada', size=12.5, family=S.SERIF, fill=S.INK2, anchor='middle')]
    # case spine along the base
    ys = 350
    o += [S.rect(36, ys, 1008, 30, fill=S.PAPER, stroke=S.INK, stroke_width=1.4), S.rect(36, ys, 224, 30, fill=S.INK, stroke=S.INK, stroke_width=1.4),
          T(148, ys + 19, 'TJSP · ZECA PAGODINHO', size=12.5, anchor='middle', fill=S.PAPER, weight=600),
          S.line(520, ys, 520, ys + 30, stroke=S.INK, stroke_width=1.1), S.line(780, ys, 780, ys + 30, stroke=S.INK, stroke_width=1.1),
          T(390, ys + 19, 'autonomia · exigível', size=12.5, anchor='middle', weight=600),
          T(650, ys + 19, 'relatividade · entre as partes', size=12.5, anchor='middle'),
          T(912, ys + 19, 'interferência gera reparação', size=12.5, anchor='middle', weight=600)]

    return S.svg(w, h, 'Cinco forças incidentes no mesmo contrato de exclusividade', o).replace(f'viewBox="0 0 {w} {h}"', 'viewBox="0 72 1080 318"', 1)

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
