"""Paper objects for interpretation, fixed to Aula 07's assigned reading.

assinatura: REsp 1.013.976, p. 1 (schematic, not a facsimile).
rebanho: Venosa pp. 63–64; silhouettes do not enumerate the herd.
quotas: REsp 15.339, escritura's 49%; 100 marks express percentage,
not a count of companies or beneficiaries.
lacuna: Venosa p. 65, three analytical states, not a chronology.
"""
from . import svg as S


def label(x, y, words, tone=S.INK, size=18):
    return S.text(x, y, words, size=size, family=S.SERIF, fill=tone)


def assinatura():
    o = [S.rect(86, 20, 470, 305, fill=S.PAPER2, stroke=S.INK, stroke_width=1.2),
         S.text(112, 51, 'MÚTUO · ESQUEMA DA ASSINATURA', size=14)]
    for y, end in [(78, 520), (94, 492), (110, 520), (126, 465)]:
        o.append(S.line(112, y, end, y, stroke=S.GRID, stroke_width=1))
    o += [label(112, 164, 'Sociedade devedora'),
          label(112, 204, 'Sócio: coobrigado', S.DIF),
          S.line(112, 217, 520, 217, stroke=S.DIF, stroke_width=1.4),
          S.path('M132,263 Q156,231 144,262 Q171,246 180,261 Q192,271 213,250 M184,268 L244,255',
                 fill='none', stroke=S.INK, stroke_width=1.5),
          S.line(112, 280, 350, 280, stroke=S.INK, stroke_width=1),
          label(112, 306, 'assinatura no contrato', size=16),
          label(86, 365, 'O nome “avalista” não cria título de crédito.', S.CONC)]
    return S.svg(650, 390, 'Assinatura no mútuo: a obrigação decorre do conteúdo da avença', o)


def sheep(x, y, small=False, conceived=False):
    k = .56 if small else 1
    # An unborn lamb is enclosed by the mother's body: membership without visibility.
    o = [f'<g transform="translate({x} {y}) scale({k})">',
         S.path('M0,0 C-12,-15 1,-31 14,-28 C22,-42 42,-39 49,-29 C67,-35 79,-20 72,-8 C86,4 70,17 56,12 C36,22 12,16 0,0 Z',
                fill=S.PAPER2, stroke=S.INK, stroke_width=1.5),
         S.path('M66,-17 Q96,-29 96,-7 L83,1 L72,-1 M14,13 V34 M51,15 V34',
                fill='none', stroke=S.INK, stroke_width=1.5)]
    if conceived:
        o += [S.path('M24,-9 Q35,-21 47,-9 Q54,4 40,6 L28,3 Z', fill='none', stroke=S.DIF, stroke_width=1.4, stroke_dasharray='3 3')]
    o.append('</g>')
    return o


def rebanho():
    o = [S.path('M58,104 Q278,24 575,105 L575,284 Q297,341 58,280 Z',
                fill='none', stroke=S.INK, stroke_width=1.4),
         label(58, 34, 'Venda do rebanho'), label(70, 354, 'As crias concebidas acompanham o conjunto.', S.DIF)]
    for x, y, pregnant in [(125, 151, True), (310, 143, False), (200, 244, True), (420, 228, False)]:
        o += sheep(x, y, conceived=pregnant)
    o += [S.line(169, 146, 191, 72, stroke=S.DIF, stroke_width=1),
          label(203, 77, 'cria ainda não nascida', size=17)]
    return S.svg(650, 385, 'O rebanho inclui as crias concebidas, mesmo desconhecidas', o)


def quotas():
    o = [label(32, 31, 'Cada participação nas empresas'),
         S.text(32, 60, '100 marcas = a totalidade; não o número de ações', size=12)]
    for i in range(100):
        x, y = 48 + (i % 10) * 25, 93 + (i // 10) * 25
        o.append(S.circle(x, y, 6, fill=S.INK if i < 49 else S.PAPER,
                          stroke=S.INK, stroke_width=1))
    o += [label(330, 115, '49% atribuídos'), label(330, 142, 'aos beneficiários'),
          label(330, 207, 'Restante conservado'), label(330, 234, 'pelo instituidor'),
          S.line(330, 269, 603, 269, stroke=S.DIF, stroke_width=1.3),
          label(330, 300, 'Fim: continuidade', S.DIF),
          label(330, 326, 'da organização', S.DIF)]
    return S.svg(650, 355, 'A divisão das participações servia à continuidade da organização', o)


def lacuna(state):
    o = [S.path('M42,35 H378 V284 H42 Z', fill=S.PAPER2, stroke=S.INK, stroke_width=1.2),
         S.text(62, 63, 'CONTEÚDO CONTRATUAL', size=14)]
    for y, end in [(89, 350), (105, 326), (121, 350), (216, 350), (232, 308), (248, 350)]:
        o.append(S.line(62, y, end, y, stroke=S.GRID, stroke_width=1))
    if state == 1:
        o += [label(62, 157, 'correção monetária', size=18),
              label(62, 190, 'índice extinto', S.CONC),
              S.line(60, 182, 204, 182, stroke=S.CONC, stroke_width=1.5)]
        bottom = ['A previsão perdeu', 'seu índice.']
    elif state == 2:
        # A fitted insertion occupies precisely the gap within the original sheet.
        o += [S.path('M58,142 H172 V152 H192 V142 H358 V198 H192 V188 H172 V198 H58 Z',
                     fill=S.PAPER, stroke=S.DIF, stroke_width=1.4),
              label(72, 177, 'índice próximo', S.DIF)]
        bottom = ['Reconstrução da', 'declaração incompleta.']
    else:
        # Legal consequences extend beyond the sheet: external sources, rather
        # than a replacement inserted into an existing contractual provision.
        o += [S.path('M54,142 H130 M152,142 H238 M260,142 H350', fill='none', stroke=S.GRID, stroke_width=1),
              S.path('M28,78 H17 V300 H395 V78 H386', fill='none', stroke=S.DIF, stroke_width=1.6),
              label(62, 180, 'ponto não previsto', S.CONC)]
        bottom = ['Efeitos integrados:', 'lei, usos, equidade.']
    for i, line in enumerate(bottom):
        o.append(label(42, 338 + i * 26, line, S.DIF if state > 1 else S.INK))
    return S.svg(420, 390, 'Lacuna contratual: ' + ' '.join(bottom), o)


def build(p):
    mode = p['mode']
    if mode == 'lacuna':
        return lacuna(int(p['state'])), []
    return {'assinatura': assinatura, 'rebanho': rebanho, 'quotas': quotas}[mode](), []
