"""Planta cast for Aula 01: architectural electrical-schematic legal instrument.

No params. Fixed facts: STJ local assigned reading p.4, REsp 1.176.019.
Models the contract as an electrical circuit across three tiers (operação econômica,
vínculo contratual, regime de tutela), with interactive [data-thread] path tracing,
coverage vs. exclusion wash fields, an open circuit-breaker switch on the uncovered
vehicle category, a dashed counterfactual branch (Táxi, expressly not a fourth
litigant), and a docked case-docket spine along the base.
"""
from .planta import S


def build(p):
    o = []
    T = S.text

    def wire(key, label, body):
        o.append(
            f'<g data-thread="{key}" tabindex="0" role="button" aria-label="{label}" aria-pressed="false">'
            + ''.join(body) + '</g>'
        )

    def line(d, col=S.INK, w=1.8, dash=None):
        return S.path(d, fill='none', stroke=col, stroke_width=w, stroke_dasharray=dash)

    def bracket(x1, x2, y, label, col=S.INK2, dy=-7):
        return (
            line(f'M{x1},{y+5} V{y} H{x2} V{y+5}', col, 1.1)
            + T((x1 + x2) / 2, y + dy, label, size=11.5, anchor='middle', fill=col)
        )

    def dot(x, y, fill=S.PAPER, stroke=S.INK, r=5):
        return S.circle(x, y, r, fill=fill, stroke=stroke, stroke_width=1.7)

    def arrow(x, y, direction=1, col=S.INK):
        return line(f'M{x - 7 * direction},{y - 4} L{x},{y} L{x - 7 * direction},{y + 4}', col, 1.6)

    def terminal_block(x, y, w, h, title, sub, accent=S.INK, rows=()):
        parts = [
            S.rect(x, y, w, h, fill=S.PAPER, stroke=accent, stroke_width=1.6),
            S.line(x, y + 32, x + w, y + 32, stroke=S.GRID, stroke_width=1),
            T(x + 12, y + 21, title, size=13.5, family=S.SANS, weight=650, fill=S.INK),
            T(x + 12, y + 48, sub, size=11.5, fill=S.INK2),
        ]
        for idx, (rk, rv) in enumerate(rows):
            ry = y + 68 + idx * 20
            parts.append(S.line(x + 10, ry - 12, x + w - 10, ry - 12, stroke=S.GRID, stroke_width=0.7))
            parts.append(T(x + 12, ry, rk, size=11.5, fill=S.INK2))
            parts.append(T(x + w - 12, ry, rv, size=11.5, anchor='end', fill=S.INK))
        return ''.join(parts)

    # 1. Top multi-tier architectural phase brackets (Processo Aula 01 drafting-table grammar)
    o += [
        bracket(36, 1044, 24, 'OPERAÇÃO ECONÔMICA  ·  CIRCULAÇÃO DE RIQUEZA E DISTRIBUIÇÃO DE RISCOS', S.DIF, -8),
        bracket(36, 510, 52, 'vínculo de consumo (finalismo mitigado · art. 2º CDC)', S.INK2, -6),
        bracket(526, 1044, 52, 'limite da apólice · categoria excluída da cobertura', S.CONC, -6),
        S.line(518, 60, 518, 346, stroke=S.CONC, stroke_width=1, stroke_dasharray='2 4'),
    ]

    # 2. Quiet semantic wash fields (Dictionary: colour.wash with its governing line)
    o += [
        S.rect(254, 82, 540, 92, fill='var(--dif-wash)', opacity='0.48', stroke=S.DIF, stroke_width=1, stroke_dasharray='4 4'),
        T(524, 99, 'COBERTURA CONTRATADA · FROTA E DANOS A TERCEIROS', size=11.5, anchor='middle', fill=S.DIF),
        S.rect(524, 198, 270, 80, fill='var(--conc-wash)', opacity='0.52', stroke=S.CONC, stroke_width=1, stroke_dasharray='4 4'),
        T(659, 214, 'RISCO EXCLUÍDO NA APÓLICE', size=11.5, anchor='middle', fill=S.CONC),
    ]

    # 3. Interactive circuit 1: Seguro (Transportadora <-> Seguradora)
    wire('seguro', 'Rastrear a contratação e a cobertura do seguro', [
        terminal_block(36, 92, 200, 114, 'Transportadora', 'contratante · frota', S.DIF,
                       [('papel', 'consumidora'), ('vínculo', 'apólice vigente')]),
        terminal_block(812, 92, 232, 114, 'Seguradora', 'garante do risco', S.INK,
                       [('dever', 'cobertura prevista'), ('limite', 'cláusula de risco')]),
        line('M236,123 H812', S.DIF, 2.0), arrow(540, 123, 1, S.DIF),
        T(524, 116, 'prêmio · contratação do seguro', size=11.5, anchor='middle', fill=S.DIF),
        line('M812,158 H236', S.INK, 1.8), arrow(500, 158, -1, S.INK),
        T(524, 151, 'garantia da frota e danos a terceiros', size=11.5, anchor='middle', fill=S.INK),
        dot(236, 123, S.DIF, S.DIF, 4.5), dot(812, 123, S.DIF, S.DIF, 4.5),
        dot(236, 158, S.PAPER, S.INK, 4.5), dot(812, 158, S.PAPER, S.INK, 4.5),
    ])

    # 4. Interactive circuit 2: Indenização paga ao terceiro prejudicado
    wire('indenizacao', 'Rastrear o pagamento ao dono do caminhão particular', [
        line('M136,206 V294 H296', S.INK, 1.9), arrow(228, 294, 1, S.INK),
        dot(136, 206, S.INK, S.INK, 4), dot(296, 294, S.PAPER, S.INK, 5),
        T(146, 260, 'indenização paga', size=11.5, fill=S.INK),
        T(146, 278, 'dano reparado', size=11.5, fill=S.INK2),
        terminal_block(296, 260, 214, 68, 'Dono do caminhão', 'prejudicado · caso julgado', S.INK),
    ])

    # 5. Interactive circuit 3: Reembolso negado (chave aberta em laranja)
    wire('reembolso', 'Rastrear por que o reembolso foi negado', [
        line('M812,186 H760 V236 H686', S.CONC, 2.0),
        line('M632,236 H236 V186', S.CONC, 2.0),
        # Open circuit-breaker blade
        line('M632,236 L680,218', S.CONC, 2.2),
        dot(632, 236, S.PAPER, S.CONC, 5), dot(686, 236, S.PAPER, S.CONC, 5),
        dot(812, 186, S.CONC, S.CONC, 4), dot(236, 186, S.CONC, S.CONC, 4),
        T(659, 254, 'chave aberta · sem reembolso', size=11.5, anchor='middle', fill=S.CONC, weight=600),
        T(659, 270, 'categoria fora da cobertura', size=11.5, anchor='middle', fill=S.CONC),
    ])

    # 6. Interactive circuit 4: Hipótese contrafactual (Táxi)
    wire('hipotese', 'Rastrear a hipótese de categoria prevista (táxi)', [
        line('M760,236 V300 H812', S.INK2, 1.5, '4 4'),
        dot(760, 236, S.PAPER, S.INK2, 4), dot(812, 300, S.PAPER, S.INK2, 4.5),
        terminal_block(812, 264, 232, 68, 'Táxi (hipótese)', 'categoria prevista · não é parte', S.INK2),
    ])

    # 7. Docked case-docket spine along the bottom (iconic Processo Aula 01 anchor bar)
    y_spine = 362
    o += [
        S.rect(36, y_spine, 1008, 30, fill=S.PAPER, stroke=S.INK, stroke_width=1.4),
        S.rect(36, y_spine, 210, 30, fill=S.INK, stroke=S.INK, stroke_width=1.4),
        T(141, y_spine + 19, 'STJ · RESP 1.176.019', size=11.5, anchor='middle', fill=S.PAPER, weight=600),
        S.line(500, y_spine, 500, y_spine + 30, stroke=S.INK, stroke_width=1.1),
        S.line(760, y_spine, 760, y_spine + 30, stroke=S.INK, stroke_width=1.1),
        T(373, y_spine + 19, 'art. 2º CDC · consumidora', size=11.5, anchor='middle', fill=S.DIF, weight=600),
        T(630, y_spine + 19, 'art. 421 CC · operação econômica', size=11.5, anchor='middle', fill=S.INK),
        T(902, y_spine + 19, 'pedido improcedente', size=11.5, anchor='middle', fill=S.CONC, weight=600),
    ]

    return S.svg(
        1080, 404,
        'Esquema elétrico-jurídico do seguro no REsp 1.176.019: contratação, cobertura, chave aberta no reembolso e hipótese do táxi',
        o,
    ), []
