"""Delito Unidade 01 · seção 3.1 (Fato, norma e juízo), one case file."""
import os, sys
from math import ceil
sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, svg

# Each entry follows the worked example and table in unidade-01.html, section 3.1.
RECORD = [
    ('title', 'Ficha · fato, norma e juízo', 'head'),
    ('party', ('FATO', 'A pessoa abriu a porta e deixou o bebê sozinho por horas.'), 'fact'),
    ('clause', ('NORMA', 'A omissão pode exigir dever jurídico e possibilidade concreta de agir.'), 'rule'),
    ('clause', ('JUÍZO', 'Há hipótese de omissão relevante.'), 'judgment'),
    ('clause', ('FALTAM', 'dever · capacidade · resultado demonstrado'), 'pending'),
]


def panel():
    d = Document('u01-s7', 16, 20, 568, RECORD, lead=21, indent=96)
    o = d.paper() + d.highlight(['pending'], 'mix') + ''.join(d.parts)
    o += d.stamp('EM ABERTO', 500, 50, tone='mix', angle=0)
    view = f'0 0 600 {ceil(d.y + d.h + 16)}'
    return svg(view, o, cls='fig', ident='tdl-u01-s7',
               label='Ficha de caso: fato, norma, juízo e pontos pendentes')


def panels():
    return [panel()]
