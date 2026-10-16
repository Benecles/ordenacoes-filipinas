"""Generated, source-bound figure panels for the citação document-reading lesson."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "courses/processo-civil-i/aula-06-citacao.html"
SPECIMEN = ROOT / "specimen/figuras.html"
BEGIN = '<!-- figkit:processo-a06-citacao:begin -->'
END = '<!-- figkit:processo-a06-citacao:end -->'


ASSET = {
    "p-ar-record": ("aula-06-citacao-ar.png", 632, 1124, -15, -368, 600, 440),
    "p-ar-signature": ("aula-06-citacao-ar.png", 632, 1124, -15, -610, 600, 300),
    "p-soledade": ("aula-06-citacao-mandado-soledade.jpg", 800, 1102, -116, -670, 600, 450),
    "p-bahia": ("aula-06-citacao-mandado-bahia.jpg", 600, 600, 0, 0, 600, 300),
    "p-edital": ("aula-06-citacao-edital-pelotas.jpg", 600, 552, 0, 0, 600, 552),
}


def svg(ident, label, lines, cls="panel fig figkit"):
    if ident in ASSET:
        filename, image_width, image_height, image_x, image_y, width, height = ASSET[ident]
        href = f"assets/{filename}"
        return (f'<svg data-family="figure.form" id="{ident}" class="{cls}" viewBox="0 0 {width} {height}" '
                f'role="img" aria-label="{label}"><image href="{href}" x="{image_x}" y="{image_y}" width="{image_width}" height="{image_height}" '
                'preserveAspectRatio="none"/></svg>')
    body = [f'<text x="32" y="38" style="font-family:var(--mono);font-size:13px;font-weight:700;letter-spacing:.06em;fill:var(--ink)">{lines[0]}</text>',
            '<path d="M32 54L568 54" style="fill:none;stroke:var(--ink);stroke-width:1.4"/>']
    for i, line in enumerate(lines[1:]):
        y = 104 + i * 72
        tone = "var(--conc)" if i == len(lines[1:]) - 1 else "var(--ink)"
        body.append(f'<path d="M48 {y-18}L48 {y+18}" style="fill:none;stroke:{tone};stroke-width:3"/>')
        body.append(f'<text x="70" y="{y+5}" style="font-family:var(--serif,serif);font-size:19px;fill:var(--ink)">{line}</text>')
    family = "figure.timeline" if ident.startswith("p-nota") else "figure.form"
    return f'<svg data-family="{family}" id="{ident}" class="{cls}" viewBox="0 0 600 250" role="img" aria-label="{label}">{"".join(body)}</svg>'


def step(ident, title, copy, active=False):
    on = " on" if active else ""
    return (f'<div class="step{on}" data-panel="{ident}" data-slides="{title}"><div class="card">'
            f'<span class="label">Registro</span><h3>{title}</h3><p>{' · '.join(copy[1:]) if isinstance(copy, list) else copy}</p></div></div>')


def block(panels, title):
    svgs = "".join(svg(i, a, ls, "panel on fig figkit" if n == 0 else "panel fig figkit") for n, (i, a, ls) in enumerate(panels))
    steps = "".join(step(i, t, c, n == 0) for n, (i, t, c) in enumerate(panels))
    return (f'<div class="scrolly"><div class="stage" aria-hidden="true"><figure>{svgs}'
            f'<figcaption><span>{title}</span><span class="stage-count">1 / {len(panels)}</span></figcaption></figure></div>'
            f'<div class="steps">{steps}</div></div>')


def replace_scrolly(source, index, replacement):
    start = -1
    for _ in range(index):
        start = source.find('<div class="scrolly">', start + 1)
        if start < 0:
            raise ValueError(f"missing scrolly block {index}")
    # The wrapper has a fixed, balanced div tree; find its end by counting div tags.
    import re
    depth = 0
    for match in re.finditer(r'<div\b[^>]*>|</div>', source[start:]):
        depth += 1 if match.group().startswith('<div') else -1
        if depth == 0:
            end = start + match.end()
            return source[:start] + replacement + source[end:]
    raise ValueError(f"unclosed scrolly block {index}")


def build():
    source = PAGE.read_text()
    hero = (f'<svg data-family="figure.form" id="hero-citacao" class="hero-form figkit" viewBox="0 0 600 440" role="img" aria-label="Aviso de recebimento do processo 142/1.14.0003514-0"><image href="assets/aula-06-citacao-ar.png" x="-15" y="-368" width="632" height="1124" preserveAspectRatio="none"/></svg>')
    source = source.replace('<figure class="hero-drawing"', '<figure class="hero-drawing"', 1)
    import re
    source, count = re.subn(r'<figure class="hero-drawing"[^>]*>.*?</figure>', f'<figure class="hero-drawing">{hero}<figcaption class="caption">Três campos do AR: destinatária, resultado e assinatura.</figcaption></figure>', source, count=1, flags=re.S)
    if count != 1:
        raise ValueError("hero source figure not found")
    blocks = [
        block([
            ("p-ar-record", "AR · dados impressos", ["AR · 142/1.14.0003514-0", "Destinatária: Unidasul Distribuidora Alimentícia S.A.", "Resultado postal: POSITIVO"]),
            ("p-ar-signature", "AR · campo de recebedor", ["NOME LEGÍVEL DO RECEBEDOR", "Anotação manuscrita", "Função não indicada"]),
        ], "AR · campos e limite da leitura"),
        block([
            ("p-soledade", "Soledade · 9/6/2011", ["CERTIDÃO · SOLEDADE", "Citação pessoal efetuada", "Contrafé recebida · nota de ciente"]),
            ("p-bahia", "Bahia · 26/4/2016", ["CERTIDÃO · AÇÃO PENAL", "Oficial deixou de intimar", "Porta da casa fechada"]),
        ], "Mandados · dois registros independentes"),
        block([
            ("p-edital", "Pelotas · edital de 2013", ["EDITAL · PELOTAS · 8/10/2013", "Prazo impresso: 30 dias", "Registro histórico"]),
            ("p-edital-current", "CPC atual · faixa do prazo", ["CPC · ART. 257, III", "Prazo judicial: 20 a 60 dias", "Contado da publicação única ou primeira"]),
        ], "Edital histórico e regra atual"),
        block([
            ("p-nota", "Nota · expedição e disponibilização", ["NOTA Nº 1690/2015", "20/05 · expedida", "21/05 · disponibilizada · edição 5561 do DJE"]),
            ("p-nota-publication", "Nota · publicação certificada", ["NOTA Nº 1690/2015", "22/05/2015", "Data considerada publicada"]),
        ], "Nota 1690/2015 · três registros de data"),
    ]
    for n in range(4, 0, -1):
        source = replace_scrolly(source, n, blocks[n - 1])
    PAGE.write_text(source)
    specimen = SPECIMEN.read_text()
    entry = (f'{BEGIN}<section class="ref" id="pci-a06-citacao-form"><header>'
             '<span class="g">Documento · formulário de leitura</span><span class="v">verbo · localizar</span></header>'
             '<h2>Processo · Aula 07 · citação e intimação</h2>'
             '<p>O formulário organiza campos documentais legíveis e preserva o limite do que a assinatura manuscrita permite identificar.</p>'
             '<p class="r">família aprovada · figure.form · tools/figkit/processo_a06_citacao.py</p>'
             f'<div class="grid"><div class="s">{hero}</div></div></section>{END}')
    if BEGIN in specimen and END in specimen:
        a = specimen.index(BEGIN)
        b = specimen.index(END, a) + len(END)
        specimen = specimen[:a] + entry + specimen[b:]
    else:
        anchor = '</body>'
        if specimen.count(anchor) != 1:
            raise ValueError("specimen insertion anchor not found")
        specimen = specimen.replace(anchor, entry + anchor, 1)
    SPECIMEN.write_text(specimen)
    print("generated A06 citação hero and four staged figure blocks")


if __name__ == "__main__":
    build()
