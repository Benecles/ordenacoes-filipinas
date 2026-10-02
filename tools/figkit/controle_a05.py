"""Controle Aula 05 figure: classify treaties by subject and approval route."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from figkit import Ruler, svg, t, line, TONE, WARN


def fig1():
    ruler = Ruler(
        'f501', 40, 160, 520,
        stops=['Infraconstitucional', 'Supralegal', ('Equivalente', 'à emenda')],
        title='Posição do tratado no direito interno',
        minor=5,
    )
    art = ruler.body()
    # The first category sits at the scale origin, so a labeled projection is clearer than a zero-length strip.
    first = ruler.pos(0)
    art += t(first, 260, 'OUTROS TEMAS', size=10.5, weight=700)
    art += line(first, 276, first, ruler.y + ruler.h, tone='muted', w=1.2, dash='3 3')
    art += ruler.strip(356, 1, ('DIREITOS HUMANOS', 'sem rito do § 3º'), tone='dif', reading=False)
    art += ruler.strip(430, 2, ('DIREITOS HUMANOS', 'rito do § 3º'), tone='conc', reading=False)
    art += t(40, 464, 'CINZA · OUTROS TEMAS', size=10, fill=TONE['muted'], weight=600)
    art += t(225, 464, 'AZUL · DH SEM § 3º', size=10, fill=TONE['dif'], weight=600)
    art += t(394, 464, 'TERRACOTA · DH RITO § 3º', size=10, fill=TONE['conc'], weight=600)
    return svg(
        '24 144 552 336', art,
        cls='panel fig on', ident='p-a05-ruler',
        label='Tratados sobre outros temas ficam no nível infraconstitucional; tratados de direitos humanos sem o rito do parágrafo terceiro são supralegais; aprovados por esse rito, equivalem a emenda constitucional.',
    )


if __name__ == '__main__':
    if WARN:
        print('\n'.join(WARN), file=sys.stderr)
        raise SystemExit(1)
    print(fig1())
