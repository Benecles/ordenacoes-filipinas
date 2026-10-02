"""Controle Aula 04 · ficha para classificar o parâmetro no caso RE 466.343."""
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, Field, WARN, line, svg, t


def panel():
    field = Field('a04-c14', x0=130, x1=397, y0=110, y1=300)
    field.region(110, 200, 'muted', .38)
    field.region(200, 300, 'muted', .18)
    field.axes(
        [(200, ('Constituição', 'norma formal')),
         (340, ('Tratado DH', 'status do tratado'))],
        [(130, ('Constitucional', 'CF / rito § 3º')),
         (270, ('Supralegal', 'tratado de DH'))],
        xtitle='Norma invocada', ytitle='Status')
    field.o.append(line(130, 200, 397, 200, tone='ink', w=1, dash='4 4'))
    field.point(200, 130, 'CF', active=True, tone='ink', dx=10, dy=2,
                sub='parâmetro CF')
    field.point(340, 160, '§ 3º', active=True, tone='ink', dx=-10, dy=-4,
                anchor='end', sub='equivale a emenda')
    field.point(340, 270, 'C14', active=True, tone='conc', dx=-10, dy=-4,
                anchor='end', sub='convencionalidade')

    doc = Document(
        'a04-c14-record', x=20, y=394, w=380,
        lines=[
            ('title', 'C14 · RE 466.343', 'case'),
            ('clause', ('Objeto', 'prisão civil do depositário infiel'), 'object'),
            ('clause', ('Norma / status', 'direito humano · supralegal'), 'standard'),
            ('clause', ('Comparação', 'controle difuso de convencionalidade'), 'control'),
            ('clause', ('Limite', 'o trecho não informa o resultado'), 'limit'),
            ('sign', ('Outro objeto / norma', 'Status / comparação'), 'transfer'),
        ], lead=17, indent=122)

    inner = t(20, 30, 'FICHA · QUAL PADRÃO É INVOCADO?', size=12, weight=700, caps=True)
    inner += t(20, 50, 'O tipo de exame acompanha o estatuto da norma citada.', size=11)
    inner += line(20, 66, 400, 66, tone='muted', w=1)
    inner += ''.join(field.o)
    inner += doc.paper() + ''.join(doc.parts)
    return svg('4 10 412 600', inner, cls='panel fig on', ident='p-caso-c14',
               label='Ficha de classificação: Constituição e tratado de direitos humanos por estatuto, com RE 466.343 marcado como tratado supralegal e campo para novo caso')


def specimen_page():
    css = (Path(__file__).resolve().parents[2] /
           'courses' / 'controle-de-constitucionalidade' / 'assets' / 'controle.css').as_uri()
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Figkit · Controle Aula 04</title>
<link rel="stylesheet" href="{css}">
<style>body{{max-width:760px;margin:0 auto;padding:24px 16px}}figure{{margin:0;background:var(--paper);border:1.5px solid var(--ink);box-shadow:6px 6px 0 var(--grid-major)}}figure svg{{display:block;width:100%;height:auto;opacity:1!important;visibility:visible!important;position:static!important}}figcaption{{padding:8px 12px;border-top:1px solid var(--ink);font:10.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}}</style></head><body>
<figure>{panel()}<figcaption>Fig. 1 · Ficha de classificação do parâmetro</figcaption></figure></body></html>'''


if __name__ == '__main__':
    WARN.clear()
    probe = os.environ.get('FIGKIT_PROBE')
    if probe:
        Path(probe).write_text(specimen_page(), encoding='utf-8')
        print(probe)
    print('\n'.join(WARN) or 'no text warnings')
