"""Aula 09 planta: time and risk as categorical relations, never a value series.

Sources: CC 157, 317, 478–480, 421-A III; CDC 6 V; Venosa 68–76;
Caio Mário 145, 148. The contract-life line is sequence only, not duration.
"""
from . import svg as S


def build(p):
    t = S.text
    out = [
        t(24, 28, 'CAUSAS AO LONGO DO CONTRATO', size=12),
        t(24, 53, 'Sequência dos fatos · sem escala de preço, tempo ou risco', size=14, family=S.SERIF, fill=S.INK2),
        S.line(142, 77, 954, 77, stroke=S.INK, stroke_width=1.2),
        S.path('M946,72 L954,77 L946,82', fill='none', stroke=S.INK, stroke_width=1.2),
    ]
    for x, label in [(150, 'celebração'), (560, 'eventual mudança'), (925, 'execução')]:
        out += [S.line(x, 68, x, 88, stroke=S.MUTED, stroke_width=1),
                t(x, 65, label, size=12, anchor='middle', fill=S.INK2)]

    # The three tracks distinguish when imbalance is present and whether it
    # belongs to ordinary risk; relative offsets are symbols, not measured gaps.
    tracks = [
        ('lesao', 'Lesão', 'desproporção já na assinatura', 'CC 157', 130),
        ('ordinario', 'Álea normal', 'oscilações incluídas no negócio', 'CC 421-A, III', 229),
        ('posterior', 'Fato posterior', 'excesso fora do risco assumido', 'CC 317 / 478 · CDC 6º, V', 328),
    ]
    for key, title, summary, rule, y in tracks:
        out.append(f'<g data-thread="{key}" data-fio="{key}" tabindex="0" role="link" aria-label="{S.esc(title + ": " + summary)}">')
        out += [S.path(f'M142,{y} L954,{y}', fill='none', stroke=S.INK, stroke_width=14, opacity='0', pointer_events='stroke'),
                t(24, y - 9, title, size=16, family=S.SERIF, weight='600'),
                t(24, y + 14, rule, size=11, fill=S.INK2)]
        if key == 'lesao':
            out += [S.line(150, y - 8, 925, y - 8, stroke=S.INK2, stroke_width=1.8),
                    S.line(150, y + 8, 925, y + 8, stroke=S.INK2, stroke_width=1.8),
                    S.line(150, y - 8, 150, y + 8, stroke=S.CONC, stroke_width=2.3),
                    t(925, y - 16, 'origem', size=11, anchor='end', fill=S.CONC)]
        elif key == 'ordinario':
            out += [S.rect(150, y - 14, 775, 28, fill=S.GRID, opacity='.6'),
                    S.path(f'M150,{y} C230,{y-11} 300,{y+11} 385,{y} S540,{y-11} 625,{y} S780,{y+11} 925,{y}',
                           fill='none', stroke=S.INK2, stroke_width=2),
                    t(925, y - 20, 'faixa qualitativa', size=11, anchor='end', fill=S.INK2)]
        else:
            out += [S.rect(150, y - 14, 775, 28, fill=S.GRID, opacity='.6'),
                    S.path(f'M150,{y} L555,{y} C600,{y} 605,{y-28} 655,{y-28} L925,{y-28}',
                           fill='none', stroke=S.CONC, stroke_width=2.4),
                    S.line(560, y - 21, 560, y + 20, stroke=S.MUTED, stroke_width=1, stroke_dasharray='2 4'),
                    t(925, y - 41, 'mudança posterior', size=11, anchor='end', fill=S.CONC)]
        out += [S.circle(150, y, 5, fill=S.PAPER, stroke=S.INK, stroke_width=1.5),
                S.rect(919, y - (8 if key == 'posterior' else 5), 10, 10, fill=S.PAPER,
                       stroke=S.CONC if key == 'posterior' else S.INK, stroke_width=1.5),
                t(150, y + 31, summary, size=12, family=S.SERIF, fill=S.INK2)]
        out.append('</g>')

    return S.svg(1000, 400, 'Três causas situadas na sequência contratual: lesão originária, álea normal e alteração posterior', out), []
