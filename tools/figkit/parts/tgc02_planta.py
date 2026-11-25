"""Aula 02 force rose, cast through the planta part.

mode: 'rosa' (default). Five traceable rays relate Zeca's existing exclusivity
contract to freedom, binding force, relativity, social function and objective
good faith. A range control extends only the selected drawn ray; it assigns no
numerical weight to a principle. No arbitrary facts or legal rankings.
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
  'A África não devia a prestação artística prometida pelo cantor, porque não era parte daquele contrato.'),
 ('social','Função social','respeitar o vínculo alheio',138,
  'O contrato integra a vida social: a interferência ilícita de quem conhece o vínculo pode gerar responsabilidade.'),
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
            length = 32
            o.append(f'<g data-thread="{key}" data-fio="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">')
            o.append(S.line(cx, cy, x, y, stroke=S.INK, stroke_width=1.7))
            o.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({angle})"><g class="ray-extension">')
            o.append(S.line(0, 0, length, 0, stroke=S.CONC if key == 'social' else S.DIF if key in ('liberdade', 'conduta') else S.INK, stroke_width=2))
            o.append(S.circle(length, 0, 4, fill=S.PAPER, stroke=S.INK, stroke_width=1.5))
            o.append('</g></g>')
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
    w, h = 1080, 404
    o = []
    T = S.text

    def bracket(x1, x2, y, label, col=S.INK2, dy=-7):
        return (
            S.path(f'M{x1},{y+5} V{y} H{x2} V{y+5}', fill='none', stroke=col, stroke_width=1.1)
            + T((x1 + x2) / 2, y + dy, label, size=12.5, anchor='middle', fill=col)
        )

    def card(x, y, cw, ch, title, note, tag, accent=S.INK):
        return ''.join([
            S.rect(x, y, cw, ch, fill=S.PAPER, stroke=accent, stroke_width=1.6),
            S.line(x, y + 30, x + cw, y + 30, stroke=S.GRID, stroke_width=0.9),
            T(x + 14, y + 20, title, size=13.5, family=S.SANS, weight=650, fill=S.INK),
            T(x + 14, y + 48, note, size=12.5, family=S.SERIF, fill=S.INK2),
            T(x + 14, y + 68, tag, size=12.5, fill=accent),
        ])

    # 1. Top multi-tier phase brackets
    o += [
        bracket(36, 1044, 24, 'CINCO FORÇAS SOBRE A OPERAÇÃO CONTRATUAL  ·  CASO ZECA PAGODINHO', S.DIF, -8),
        bracket(36, 526, 52, 'autonomia e exigibilidade · força interna do vínculo', S.DIF, -6),
        bracket(554, 1044, 52, 'limites externos · relatividade, função social e boa-fé', S.CONC, -6),
        S.line(540, 60, 540, 344, stroke=S.GRID, stroke_width=1, stroke_dasharray='3 4'),
    ]

    # 2. Quiet semantic wash fields
    o += [
        S.rect(36, 72, 304, 214, fill='var(--dif-wash)', opacity='0.44', stroke=S.DIF, stroke_width=1, stroke_dasharray='4 4'),
        S.rect(740, 72, 304, 214, fill='var(--conc-wash)', opacity='0.46', stroke=S.CONC, stroke_width=1, stroke_dasharray='4 4'),
    ]

    # 3. Interactive force vectors + terminal blocks (preserving data-thread, data-fio, .ray-extension)
    layout = {
        'liberdade':    (48,  84, 280, 82, 'art. 421 CC · autonomia',        S.DIF,  424, 152, 328, 125, 196),
        'forca':        (48, 190, 280, 82, 'pacta sunt servanda',            S.INK,  424, 196, 328, 231, 160),
        'relatividade': (752, 84, 280, 82, 'eficácia inter partes',          S.INK,  656, 152, 752, 125, -16),
        'social':       (752,190, 280, 82, 'art. 421 CC · tutela externa',   S.CONC, 656, 196, 752, 231,  20),
        'conduta':      (364,264, 352, 68, 'art. 422 CC · lealdade objetiva',S.DIF,  540, 224, 540, 264,  90),
    }

    for key, label, note, _angle, _answer in FORCES:
        bx, by, bw, bh, tag, accent, sx, sy, ex, ey, rot = layout[key]
        mx, my = (sx + ex) / 2, (sy + ey) / 2
        o.append(f'<g data-thread="{key}" data-fio="{key}" role="button" tabindex="0" aria-pressed="false" aria-label="{S.esc(label)}">')
        o.append(S.line(sx, sy, ex, ey, stroke=accent, stroke_width=1.9))
        o.append(f'<g transform="translate({mx:.1f},{my:.1f}) rotate({rot})"><g class="ray-extension">')
        o.append(S.line(0, 0, 26, 0, stroke=accent, stroke_width=2.2))
        o.append(S.circle(26, 0, 4, fill=S.PAPER, stroke=accent, stroke_width=1.6))
        o.append('</g></g>')
        o.append(S.circle(sx, sy, 4.5, fill=accent, stroke=accent, stroke_width=1.4))
        o.append(S.circle(ex, ey, 4.5, fill=S.PAPER, stroke=accent, stroke_width=1.6))
        if key == 'conduta':
            o.append(''.join([
                S.rect(bx, by, bw, bh, fill=S.PAPER, stroke=accent, stroke_width=1.6),
                S.line(bx, by + 30, bx + bw, by + 30, stroke=S.GRID, stroke_width=0.9),
                T(bx + 14, by + 20, label, size=13.5, family=S.SANS, weight=650, fill=S.INK),
                T(bx + bw - 14, by + 20, 'art. 422 CC', size=12.5, anchor='end', fill=accent),
                T(bx + 14, by + 50, note + ' · respeito ao contrato alheio', size=12.5, family=S.SERIF, fill=S.INK2),
            ]))
        else:
            o.append(card(bx, by, bw, bh, label, note, tag, accent))
        o.append('</g>')

    # 4. Center anchored contract core
    cx, cy, cw, ch = 424, 126, 232, 98
    o += [
        S.rect(cx + 5, cy + 5, cw, ch, fill='var(--grid-major)', stroke='none'),
        S.rect(cx, cy, cw, ch, fill=S.PAPER, stroke=S.INK, stroke_width=1.8, data_lk='liberdade forca relatividade social conduta'),
        S.rect(cx, cy, cw, 28, fill=S.INK, stroke=S.INK, stroke_width=1.4),
        T(cx + cw / 2, cy + 18, 'VÍNCULO VIGENTE', size=12.5, anchor='middle', fill=S.PAPER, weight=600),
        T(cx + cw / 2, cy + 52, 'Zeca · Nova Schin', size=14.5, family=S.SANS, anchor='middle', weight=700, fill=S.INK),
        S.line(cx + 16, cy + 64, cx + cw - 16, cy + 64, stroke=S.GRID, stroke_width=1),
        T(cx + cw / 2, cy + 84, 'exclusividade contratada', size=12.5, family=S.SERIF, anchor='middle', fill=S.INK2),
    ]

    # 5. Docked case-docket spine along the base
    y_spine = 356
    o += [
        S.rect(36, y_spine, 1008, 30, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
        S.rect(36, y_spine, 224, 30, fill=S.INK, stroke=S.INK, stroke_width=1.4),
        T(148, y_spine + 19, 'TJSP · ZECA PAGODINHO', size=12.5, anchor='middle', fill=S.PAPER, weight=600),
        S.line(520, y_spine, 520, y_spine + 30, stroke=S.INK, stroke_width=1.1),
        S.line(780, y_spine, 780, y_spine + 30, stroke=S.INK, stroke_width=1.1),
        T(390, y_spine + 19, 'autonomia · compromisso exigível', size=12.5, anchor='middle', fill=S.DIF, weight=600),
        T(650, y_spine + 19, 'relatividade · prestação das partes', size=12.5, anchor='middle', fill=S.INK),
        T(912, y_spine + 19, 'art. 421 · terceiro responde', size=12.5, anchor='middle', fill=S.CONC, weight=600),
    ]

    return S.svg(w, h, 'Cinco forças incidentes no mesmo contrato de exclusividade', o)

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
    return ('<div class="force-rose"><div class="rose-desktop">'+desktop+'</div><div class="rose-mobile">'+mobile+'</div><div class="force-readout">'+answers+'</div><label class="trace-length">Extensão gráfica do raio <input type="range" min="0.7" max="1.3" step="0.05" value="1" aria-label="Extensão gráfica do raio selecionado"></label></div>',[])
