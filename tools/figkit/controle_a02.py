"""Controle Aula 02 · document anatomy for the CF/88 amendment procedure."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Document, svg, t


ART_60_2 = (
    "A proposta será discutida e votada em cada Casa do Congresso Nacional, em dois turnos, "
    "considerando-se aprovada se obtiver, em ambos, três quintos dos votos dos respectivos membros."
)
ART_65 = (
    "O projeto de lei aprovado por uma Casa será revisto pela outra, em um só turno de discussão "
    "e votação, e enviado à sanção ou promulgação, se a Casa revisora o aprovar, ou arquivado, "
    "se o rejeitar."
)


def panel():
    """Two real constitutional passages the reader reads and compares."""
    x, w, y, gap = 16, 528, 44, 14
    common = dict(lead=28, indent=0, font_size=17, meta_size=16, char_width=8.854)
    amendment = Document(
        'a02-art-60', x, y, w,
        [('title', 'CF/88 · Art. 60, § 2º', 'title'), ('clause', ART_60_2, 'passage')],
        **common,
    )
    bill_y = y + amendment.h + gap
    bill = Document(
        'a02-art-65', x, bill_y, w,
        [('title', 'CF/88 · Art. 65, caput', 'title'), ('clause', ART_65, 'passage')],
        **common,
    )
    height = bill_y + bill.h + 16
    inner = t(x, 27, 'COMPARE OS TURNOS E O QUÓRUM', size=16, caps=True,
              weight=700, fill='var(--ink-2)')
    inner += amendment.paper() + ''.join(amendment.parts)
    inner += bill.paper() + ''.join(bill.parts)
    return svg(
        f'0 0 560 {height:g}', inner, cls='panel fig on', ident='p-art-compare',
        label='Trechos da Constituição Federal: art. 60, parágrafo 2º, e art. 65',
    )


if __name__ == '__main__':
    print(panel())
