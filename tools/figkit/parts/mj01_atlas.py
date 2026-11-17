"""Draft atlas plates for Hespanha ch. 14; geography from the course atlas."""
import re

from tools.figkit import mj_atlas as atlas


SANS = "var(--sans, 'Archivo', system-ui, sans-serif)"
WASH = {'ITA': ('var(--conc-wash)', 'var(--conc)'), 'FRA': ('var(--dif-wash)', 'var(--dif)'), 'DEU': ('var(--dif-wash)', 'var(--dif)')}


def _plate(*args, washes=(), **kwargs):
    # Lesson plates use the same atlas at every width, without desktop-only front classes, and the front's type:
    # place names in the sans, graticule labels in italic serif, land washed where the passage puts the law.
    svg = atlas.build(*args, **kwargs).replace('plate__svg plate__svg--desktop', 'mj01-atlas')
    def retype(m):
        t = m.group(0)
        if 'font-weight="700"' in t:
            return t.replace(atlas.esc(atlas.MONO), atlas.esc(SANS))
        if 'fill="var(--muted)"' in t and 'font-style' not in t:
            return t.replace(atlas.esc(atlas.MONO), atlas.esc(atlas.SERIF)).replace('<text ', '<text font-style="italic" ')
        return t
    svg = re.sub(r'<text [^>]*>', retype, svg)
    for iso in washes:
        fill, stroke = WASH[iso]
        svg = re.sub(r'(<use href="#[\w-]+-%s") fill="var\(--paper-2\)" stroke="var\(--ink-2\)"' % iso, r'\1 fill="%s" stroke="%s"' % (fill, stroke), svg)
    return svg


def build(params):
    mode = params['mode']
    if mode == 'cidades':
        f = atlas.Frame(1080, 550, 11.6, 43.6, 105)
        body = atlas.pin(f, 11.3426, 44.4949, tone='ink')
        body += atlas.lab(f, (11.3426, 44.4949), 'Bolonha', 'start', 20, -12)
        body += atlas.lab(f, (11.3426, 44.4949), 'Irnério · primeira metade do séc. XII', 'start', 20, 10, size=12, weight=400)
        body += atlas.lab(f, (11.3426, 44.4949), 'Acúrsio · 1230–1240', 'start', 20, 29, size=12, weight=400)
        body += atlas.pin(f, 12.3888, 43.1107, tone='ink')
        body += atlas.lab(f, (12.3888, 43.1107), 'Perugia', 'start', 20, 0)
        body += atlas.lab(f, (12.3888, 43.1107), 'Bártolo · 1314–1357', 'start', 20, 22, size=12, weight=400)
        return _plate(f, 'mj01-cidades', aria='Bolonha e Perugia na península italiana', grat=([42,44,46],[8,12,16]), body=body + ''.join(atlas.sea(f, *a, size=15) for a in ((9.0, 42.9, 'MAR TIRRENO'),)), scale=(55,500,100), washes=('ITA',)), []
    if mode == 'difusao':
        f = atlas.Frame(1080, 620, 12, 49, 30)
        italy, france, germany = (11.34,44.49),(2.2,47),(10.5,51.8)
        body = atlas.flow(f, italy, france, bend=-.18, tone='var(--ink-2)', dash='4 5')
        body += atlas.flow(f, italy, germany, bend=.16, tone='var(--ink-2)', dash='4 5')
        for place, label, sub, dx, dy in [
            (italy,'Itália','Recepção · desde o séc. XIII',18,20),
            (france,'França','Glosadores ultramontani',-18,-15),
            (germany,'Alemanha','Recepção · sécs. XV–XVI',18,-15),
        ]:
            body += atlas.lab(f, place, label, 'end' if dx<0 else 'start', dx,dy,size=16)
            body += atlas.lab(f, place, sub, 'end' if dx<0 else 'start', dx,dy+21,size=12,weight=400)
        body += atlas.text(32,575,'Direito subsidiário: na falta de direito local',size=14,italic=True)
        return _plate(f,'mj01-difusao',aria='Da Itália à Europa: ensino dos glosadores em França e recepção tardia na Alemanha',grat=([40,50],[0,10,20,30]),body=body + ''.join(atlas.sea(f, *a[:3], size=a[3]) for a in ((-9.6, 49.2, 'OCEANO ATLÂNTICO', 12), (4.5, 40.5, 'MEDITERRÂNEO', 13))),scale=(760,800,590), washes=('ITA','FRA','DEU')), []
    raise ValueError(mode)
