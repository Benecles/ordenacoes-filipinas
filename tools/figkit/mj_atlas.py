"""Metodologia Jurídica · the four atlas plates (aulas 02, 04, 06, 14), redrawn 14/11.

Language: Atlas (LANGUAGES.md 2), in the house of the Latam atlas (work/latam-build/maps.py in the workshop): engraved
water rings, graticule with named parallels, italic sea names, scale bar, flow lines. Each plate crops its own
geography (Europe / the Andes to the River Plate / the Atlantic crossing / the Atlantic to Brazil) so the places the
passage names fill the frame, instead of one shared world map with three dots.

Geometry: Natural Earth 1:50m (public domain), tools/figkit/geo/ne50_atlantic.json {ISO3: [outer rings (lon, lat)]}.
Run:  python3 tools/figkit/mj_atlas.py        (rewrites the first <figure class="plate"> of the four pages)
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'parts'))
from svg import esc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))
GEO = json.load(open(os.path.join(HERE, 'geo', 'ne50_atlantic.json')))
MONO = "var(--mono, 'IBM Plex Mono', ui-monospace, monospace)"
SERIF = "var(--serif, 'Spectral', Georgia, serif)"
HALO = 'paint-order="stroke" stroke="var(--paper)" stroke-width="4.5" stroke-linejoin="round"'
KM_DEG = 111.32


class Frame:
    def __init__(self, W, H, lonc, latc, S):
        self.W, self.H, self.lonc, self.latc, self.S = W, H, lonc, latc, S
        self.kx = math.cos(math.radians(latc))
        self.lon0, self.lon1 = lonc - W / 2 / (self.kx * S), lonc + W / 2 / (self.kx * S)
        self.lat1, self.lat0 = latc + H / 2 / S, latc - H / 2 / S

    def xy(self, lon, lat):
        return (self.W / 2 + (lon - self.lonc) * self.kx * self.S, self.H / 2 - (lat - self.latc) * self.S)

    def land(self, tol=.25):
        out = {}
        for iso, rings in GEO.items():
            parts = []
            for r in rings:
                if not any(self.lon0 - 4 < lo < self.lon1 + 4 and self.lat0 - 4 < la < self.lat1 + 4 for lo, la in r):
                    continue
                pts = [self.xy(lo, la) for lo, la in r]
                h = len(pts) // 2
                pts = dp(pts[:h + 1], tol)[:-1] + dp(pts[h:], tol)
                if area(pts) < 6:
                    continue
                parts.append('M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in pts[:-1]) + 'Z')
            if parts:
                out[iso] = ''.join(parts)
        return out


def dp(pts, tol):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1e-9
    imax, dmax = 0, -1
    for i in range(1, len(pts) - 1):
        x, y = pts[i]
        d = abs(dy * x - dx * y + x2 * y1 - y2 * x1) / L
        if d > dmax:
            imax, dmax = i, d
    return dp(pts[:imax + 1], tol)[:-1] + dp(pts[imax:], tol) if dmax > tol else [pts[0], pts[-1]]


def area(p):
    return abs(sum(p[i][0] * p[i - 1][1] - p[i - 1][0] * p[i][1] for i in range(len(p)))) / 2


# ---------- drawing primitives (house tokens only; coloured text never used: place names are ink) ----------
def text(x, y, s, size=14, fill='var(--ink)', anchor='start', weight=500, italic=False, ls=None, halo=True):
    fam = SERIF if italic else MONO
    a = (f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-family="{esc(fam)}" fill="{fill}" font-weight="{weight}"'
         + (f' text-anchor="{anchor}"' if anchor != 'start' else '')
         + (' font-style="italic"' if italic else '') + (f' letter-spacing="{ls}"' if ls else '')
         + (' ' + HALO if halo else ''))
    return f'<text {a}>{esc(s)}</text>'


def pin(f, lon, lat, tone='focus', r=6.5):
    x, y = f.xy(lon, lat)
    if tone == 'focus':
        o = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3.5}" fill="var(--conc-wash)" stroke="var(--conc)" stroke-width="1.6"/>'
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 2.5}" fill="var(--conc)"/>'
    elif tone == 'ghost':   # drawn, never realised: hollow and dashed
        o = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 2}" fill="var(--paper)" stroke="var(--ink-2)" stroke-width="1.8" stroke-dasharray="3 3"/>'
    else:
        o = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r + 3}" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.8"/>'
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 3}" fill="var(--ink)"/>'
    return o


def flow(f, a, b, bend=.2, tone='var(--ink)', w=2.2, dash=None, head=True, trim=12, label=None, lsize=12.5, ldx=0, ldy=0, lanchor='middle'):
    (x1, y1), (x2, y2) = f.xy(*a), f.xy(*b)
    cx, cy = (x1 + x2) / 2 - (y2 - y1) * bend, (y1 + y2) / 2 + (x2 - x1) * bend

    def toward(px, py, qx, qy, d):   # stop short of the pins so heads do not sit on the rings
        L = math.hypot(qx - px, qy - py) or 1
        return px + (qx - px) / L * d, py + (qy - py) / L * d
    sx, sy = toward(x1, y1, cx, cy, trim)
    ex, ey = toward(x2, y2, cx, cy, trim)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    o = f'<path d="M{sx:.1f} {sy:.1f}Q{cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f}" fill="none" stroke="{tone}" stroke-width="{w}" stroke-linecap="round"{da}/>'
    if head:
        tx, ty = ex - cx, ey - cy
        L = math.hypot(tx, ty) or 1
        ux, uy = tx / L, ty / L
        h1 = (ex - ux * 13 - uy * 6.5, ey - uy * 13 + ux * 6.5)
        h2 = (ex - ux * 13 + uy * 6.5, ey - uy * 13 - ux * 6.5)
        o += (f'<path d="M{h1[0]:.1f} {h1[1]:.1f}L{ex:.1f} {ey:.1f}L{h2[0]:.1f} {h2[1]:.1f}" fill="none" stroke="{tone}" '
              f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
    if label:
        mx, my = .25 * x1 + .5 * cx + .25 * x2, .25 * y1 + .5 * cy + .25 * y2
        o += text(mx + ldx, my + ldy, label, size=lsize, fill='var(--ink-2)', anchor=lanchor)
    return o


def graticule(f, lats, lons):
    o = ''
    for lat in lats:
        _, y = f.xy(0, lat)
        o += (f'<path d="M0 {y:.1f}H{f.W}" fill="none" stroke="var(--grid-major)" stroke-width="{1.1 if lat == 0 else .8}"'
              + ('' if lat == 0 else ' stroke-dasharray="2 5"') + '/>')
    for lon in lons:
        x, _ = f.xy(lon, 0)
        o += f'<path d="M{x:.1f} 0V{f.H}" fill="none" stroke="var(--grid-major)" stroke-width=".7" stroke-dasharray="1 6"/>'
    return o


def grat_labels(f, lats, lons, named):
    o = ''
    for lat in lats:
        _, y = f.xy(0, lat)
        name = named.get(lat) or ('Equador' if lat == 0 else f'{abs(lat):g}°{"N" if lat > 0 else "S"}')
        o += text(f.W - 10, y - 5, name, size=12, fill='var(--muted)', anchor='end', italic=(lat in named or lat == 0))
    for lon in lons:
        x, _ = f.xy(lon, 0)
        o += text(x + 4, 18, f'{abs(lon):g}°{"L" if lon > 0 else "O"}', size=12, fill='var(--muted)')
    return o


def scale_bar(f, km, x, y):
    px = km / KM_DEG * f.S
    o = (f'<path d="M{x} {y}H{x + px:.1f}M{x} {y - 5}V{y + 5}M{x + px / 2:.1f} {y - 3.5}V{y + 3.5}M{x + px:.1f} {y - 5}V{y + 5}" '
         'fill="none" stroke="var(--ink)" stroke-width="1.4"/>')
    o += text(x, y - 10, '0', size=12, fill='var(--ink-2)')
    o += text(x + px, y - 10, f'{km} km', size=12, fill='var(--ink-2)', anchor='end')
    return o


def sea(f, lon, lat, name, size=14):
    x, y = f.xy(lon, lat)
    return text(x, y, name, size=size, fill='var(--muted)', anchor='middle', italic=True, ls='.34em')


def lab(f, lonlat, s, anchor, dx, dy, weight=700, size=15, fill='var(--ink)'):
    x, y = f.xy(*lonlat)
    return text(x + dx, y + dy, s, size=size, fill=fill, anchor=anchor, weight=weight)


def basemap(f, uid, rings_k):
    """defs + engraved water rings + land: the atlas ground, for the plate and for insets."""
    land = f.land()
    rid = {k: f'{uid}-{k}' for k in land}
    defs = ''.join(f'<path id="{rid[k]}" d="{d}"/>' for k, d in land.items())
    o = ''
    for w, col, op in ((15, 'var(--grid-major)', .55), (12, 'var(--paper)', 1), (8.5, 'var(--grid-major)', .55), (6, 'var(--paper)', 1), (3, 'var(--grid-major)', .55)):
        o += (f'<g fill="none" stroke="{col}" stroke-width="{w * rings_k:.1f}" stroke-linejoin="round" opacity="{op}">'
              + ''.join(f'<use href="#{rid[k]}"/>' for k in land) + '</g>')
    o += ''.join(f'<use href="#{rid[k]}" fill="var(--paper-2)" stroke="var(--ink-2)" stroke-width=".6" stroke-linejoin="round"/>' for k in land)
    return defs, o


def inset(f, uid, center, S2, rect, rings_k=.9, pins=None, label=''):
    """Zoomed inset in the atlas manner: locator box on the main map, dashed to a framed enlargement.
    center = (lon, lat), S2 = px per degree of latitude in the inset, rect = (x, y, w, h) in the main frame."""
    x, y, w, h = rect
    f2 = Frame(w, h, center[0], center[1], S2)
    defs, ground = basemap(f2, uid, rings_k)
    (ax, ay), (bx, by) = f.xy(f2.lon0, f2.lat1), f.xy(f2.lon1, f2.lat0)
    o = f'<rect x="{ax:.1f}" y="{ay:.1f}" width="{bx - ax:.1f}" height="{by - ay:.1f}" fill="none" stroke="var(--ink)" stroke-width="1.2"/>'
    o += (f'<path d="M{bx:.1f} {ay:.1f}L{x} {y}M{bx:.1f} {by:.1f}L{x} {y + h}" fill="none" stroke="var(--ink-2)" stroke-width=".9" stroke-dasharray="2 3"/>')
    o += (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>'
          f'<rect width="{w}" height="{h}" fill="var(--paper)"/>{ground}{pins(f2) if pins else ""}</svg>')
    o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="var(--ink)" stroke-width="1.6"/>'
    if label:
        o += text(x + 10, y + h - 10, label, size=12.5, fill='var(--ink-2)', italic=True)
    return o


def build(f, uid, *, aria, rings_k=1.0, grat, named=None, seas=(), body='', scale=None):
    named = named or {}
    defs, ground = basemap(f, uid, rings_k)
    defs += f'<clipPath id="{uid}-clip"><rect width="{f.W}" height="{f.H}"/></clipPath>'
    o = f'<defs>{defs}</defs><rect width="{f.W}" height="{f.H}" fill="var(--paper)"/>'
    o += f'<g clip-path="url(#{uid}-clip)">' + graticule(f, *grat) + ground
    o += grat_labels(f, *grat, named) + ''.join(seas) + body
    if scale:
        o += scale_bar(f, *scale)
    o += '</g>' + f'<rect width="{f.W}" height="{f.H}" fill="none" stroke="var(--ink)" stroke-width="1.4"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f.W} {f.H}" class="plate__svg plate__svg--desktop" '
            f'role="img" aria-label="{esc(aria)}">{o}</svg>')


# ---------- the four plates ----------
COIMBRA, SALAMANCA, TOULOUSE, BOLOGNA = (-8.4103, 40.2033), (-5.6635, 40.9701), (1.4442, 43.6047), (11.3426, 44.4949)
LIMA, BUENOS_AIRES, SAO_PAULO = (-77.0428, -12.0464), (-58.3816, -34.6037), (-46.6333, -23.5505)
OLINDA, RIO = (-34.8553, -8.0089), (-43.1729, -22.9068)
TROPICS = {23.44: 'Trópico de Câncer', -23.44: 'Trópico de Capricórnio'}


def a02():
    f = Frame(1200, 600, 2.0, 42.0, 53.8)
    body = ''
    for dst, bend in ((SALAMANCA, -.35), (TOULOUSE, -.28), (BOLOGNA, -.2)):
        body += flow(f, COIMBRA, dst, bend=bend, tone='var(--conc)', w=2.2, dash='7 5', head=False, trim=11)
    for lonlat, tone in ((SALAMANCA, 'focus'), (TOULOUSE, 'focus'), (BOLOGNA, 'focus'), (COIMBRA, 'hub')):
        body += pin(f, *lonlat, tone=tone)
    body += lab(f, SALAMANCA, 'Salamanca · formação', 'start', 16, 34)
    body += lab(f, TOULOUSE, 'Toulouse · formação', 'middle', 0, 34)
    body += lab(f, BOLOGNA, 'Bolonha · séc. XII · glosadores', 'end', 12, -22)
    body += lab(f, COIMBRA, 'Coimbra', 'end', -20, 8, size=16)
    seas = [sea(f, -10.2, 44.6, 'OCEANO ATLÂNTICO'), sea(f, 6.5, 38.2, 'MAR MEDITERRÂNEO')]
    return build(f, 'mj02', aria='Mapa da Europa ocidental: Coimbra ligada a Salamanca, Toulouse e Bolonha, as universidades da formação portuguesa',
                 rings_k=1.9, grat=([35, 40, 45], [-10, 0, 10]), seas=seas, body=body, scale=(500, 70, 565))


def a04():
    f = Frame(1100, 620, -57.0, -19.0, 13.5)
    body = flow(f, LIMA, BUENOS_AIRES, bend=.18, tone='var(--ink)', w=2.2, dash='7 5', trim=13)
    body += pin(f, *LIMA, tone='focus') + pin(f, *BUENOS_AIRES, tone='hub')
    body += lab(f, LIMA, 'Lima · 1582–1583 · concílio', 'end', -26, 4)
    body += lab(f, LIMA, 'assembleias provinciais', 'end', -26, 24, weight=500, size=13, fill='var(--ink-2)')
    body += lab(f, BUENOS_AIRES, 'Buenos Aires · 1655 · sínodo', 'start', 24, 6)
    body += lab(f, BUENOS_AIRES, 'manda observar os concílios limenhos', 'start', 24, 26, weight=500, size=13, fill='var(--ink-2)')
    seas = [sea(f, -90, -31, 'OCEANO PACÍFICO'), sea(f, -23, -3, 'OCEANO ATLÂNTICO')]
    return build(f, 'mj04', aria='Mapa da América do Sul: o concílio provincial de Lima, 1582–1583, e o sínodo de Buenos Aires, 1655, que manda observar os concílios limenhos',
                 rings_k=1.0, grat=([0, -23.44], [-80, -60]), named={-23.44: 'Trópico de Capricórnio'}, seas=seas, body=body, scale=(1000, 40, 585))


def a06():
    f = Frame(1200, 600, -32.0, 15.0, 9.1)
    body = flow(f, SALAMANCA, LIMA, bend=-.24, tone='var(--ink)', w=2.4, trim=13, label='1610 · 35 anos · ouvidor', ldy=30, ldx=10)
    body += flow(f, LIMA, (-9.9, 39.0), bend=-.3, tone='var(--ink-2)', w=2, dash='7 5', trim=13, label='1626 · volta à Península', ldy=-14, ldx=-24)
    body += pin(f, *SALAMANCA, tone='focus') + pin(f, *LIMA, tone='focus')
    body += lab(f, SALAMANCA, 'Salamanca · Leis, ensino', 'end', 4, -24)
    body += lab(f, LIMA, 'Lima · Audiência', 'end', -22, 6)
    seas = [sea(f, -44, 30, 'OCEANO ATLÂNTICO'), sea(f, -93, -32, 'OCEANO PACÍFICO', size=13)]
    return build(f, 'mj06', aria='Mapa do Atlântico: Solórzano estuda e ensina em Salamanca, vai a Lima como ouvidor em 1610 e volta à Península em 1626',
                 rings_k=.9, grat=([0, 23.44, -23.44], [-80, -60, -40, -20, 0, 20]), named=TROPICS, seas=seas, body=body, scale=(2000, 960, 570))


def a14():
    f = Frame(1000, 640, -22.0, 8.0, 8.2)
    body = flow(f, COIMBRA, RIO, bend=.12, tone='var(--ink-2)', w=2, dash='7 5', trim=12)
    body += flow(f, RIO, OLINDA, bend=-.25, tone='var(--ink)', w=2.4, trim=11)
    body += pin(f, *COIMBRA, tone='focus') + pin(f, *OLINDA, tone='focus') + pin(f, *SAO_PAULO, tone='focus', r=4.5) + pin(f, *RIO, tone='ghost', r=4)
    body += lab(f, COIMBRA, 'Coimbra · Estatutos de 1772', 'end', -22, 5)
    body += lab(f, OLINDA, 'Olinda · 1827 · curso', 'start', 24, 6)

    def pins(g):
        o = flow(g, RIO, SAO_PAULO, bend=.3, tone='var(--ink)', w=2.4, trim=14)
        o += pin(g, *SAO_PAULO, tone='focus') + pin(g, *RIO, tone='ghost', r=5)
        o += lab(g, SAO_PAULO, 'São Paulo · 1827 · curso', 'start', -8, 36)
        o += lab(g, RIO, 'Rio · 1825', 'end', 30, -34)
        o += lab(g, RIO, 'curso não efetivado', 'end', 30, -16, weight=500, size=13, fill='var(--ink-2)')
        return o
    body += inset(f, 'mj14i', (-44.5, -23.4), 36, (500, 468, 330, 150), pins=pins, label='sudeste do Brasil, ampliado')
    seas = [sea(f, -42, 30, 'OCEANO ATLÂNTICO')]
    return build(f, 'mj14', aria='Mapa do Atlântico: de Coimbra aos cursos jurídicos de São Paulo e Olinda, 1827; o curso do Rio, 1825, não se efetivou',
                 rings_k=.9, grat=([0, 23.44, -23.44], [-60, -40, -20, 0, 20]), named=TROPICS, seas=seas, body=body, scale=(2000, 840, 610))


PLATES = {
    'aula-02': (a02, 'A formação portuguesa se conecta a Salamanca, Bolonha e Toulouse.',
                'localiza · o leitor vê onde a formação portuguesa se ligava ao direito comum → Coimbra ligada a Salamanca, Toulouse e Bolonha'),
    'aula-04': (a04, 'Em Lima, as assembleias provinciais de 1582 e 1583 situam o concílio.',
                'localiza · o leitor vê onde o concílio se reuniu e até onde a norma foi observada → de Lima a Buenos Aires'),
    'aula-06': (a06, 'Salamanca — Lima: carreira de Solórzano, 1610.',
                'localiza · o leitor segue Solórzano de Salamanca a Lima e de volta à Península → a carreira cruza o Atlântico'),
    'aula-14': (a14, 'Coimbra é o modelo; os Estatutos de Cachoeira, pensados para o Rio, foram aproveitados em São Paulo e Olinda, em 1827.',
                'localiza · o leitor vê a herança de Coimbra e o desvio do curso do Rio → os cursos de 1827 em São Paulo e Olinda'),
}


def figure(page):
    fn, caption, does = PLATES[page]
    return (f'<figure class="plate" role="group" aria-label="O percurso documentado do ius commune" data-genre="medida" data-does="{esc(does)}">\n'
            '  <div class="plate__sheet">\n'
            '    <div class="plate__title">O percurso documentado do ius commune</div>\n'
            f'    <div class="plate__drawing">\n      <div class="plate__desktop">{fn()}</div>\n    </div>\n'
            f'    <figcaption class="plate__caption">{esc(caption)}</figcaption>\n'
            '  </div>\n</figure>')


def apply(page):
    p = os.path.join(ROOT, 'courses', 'metodologia-juridica', f'{page}.html')
    s = open(p).read()
    i = s.find('<figure class="plate')
    j = s.find('</figure>', i) + len('</figure>')
    assert i > 0 and j > i
    open(p, 'w').write(s[:i] + figure(page) + s[j:])


if __name__ == '__main__':
    for page in PLATES:
        apply(page)
