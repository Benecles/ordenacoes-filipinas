"""Processo Civil I · Aula 03: parties and the reported financing record, drawn with figkit."""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import figkit
from figkit import Document, line, svg, t

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "courses" / "processo-civil-i" / "aula-03.html"


def family(markup, name):
    return markup.replace("<svg", f'<svg data-family="{name}"', 1)


def dossier(x, width, title, entries, key, tone="conc"):
    rows = [("title", title, "title")]
    rows.extend(("party", (label, body), ident) for label, body, ident in entries)
    doc = Document(
        f"a03-{key}", x, 65, width, rows, lead=25, indent=104,
        font_size=17, meta_size=13, label_size=11, char_width=8.5,
    )
    marks = doc.highlight([ident for _, _, ident in entries[:1]], tone=tone)
    return doc.paper() + marks + "".join(doc.parts)


def party_seating():
    left = dossier(36, 470, "POLO ATIVO",
                   [("AUTOR", "Gustavo", "gustavo")], "plaintiffs")
    right = dossier(594, 470, "POLO PASSIVO",
                    [("RÉU", "Valter", "valter"),
                     ("RÉU", "Os Galos Primos", "restaurant")], "defendants", tone="dif")
    inner = t(550, 38, "UM PROCESSO · PROVA 1/2015 · Q3", size=15,
              anchor="middle", weight=700, fill="var(--ink-2)")
    inner += line(550, 80, 550, 208, tone="ink", w=1.4, dash="4 4")
    inner += left + right
    inner += line(160, 230, 160, 258, tone="muted", w=1.1, dash="3 4")
    inner += t(550, 280, "MAIQUE · APOIO, SEM DEMANDA", size=15,
               anchor="middle", weight=600, fill="var(--ink-2)")
    picture = svg("20 20 1096 285", inner, cls="fig hero-party",
                  label="Prova 1 de 2015, questão 3: Gustavo ocupa o polo ativo, Valter e Os Galos Primos ocupam o polo passivo, e Maique apoiou sem ajuizar.")
    return '<figure class="a03-figure a03-party">' + family(picture, "figure.seating") + '<figcaption>Gustavo pede tutela contra Valter e a sociedade; o apoio de Maique não o coloca no processo.</figcaption></figure>'


def record_panel(ident, title, entries, tone, label, active=False):
    doc = dossier(34, 532, title, entries, ident, tone=tone)
    cls = "panel fig on" if active else "panel fig"
    return family(svg("20 20 560 222", doc, cls=cls,
                      label=label, ident=ident), "figure.ledger")


def record_panels():
    return "".join([
        record_panel("a03-credit-1", "FINANCIAMENTO IMOBILIÁRIO",
                     [("MUTUÁRIOS", "marido e esposa", "parties")],
                     "conc", "Financiamento imobiliário firmado por marido e esposa.", active=True),
        record_panel("a03-credit-2", "AÇÃO REVISIONAL",
                     [("AUTOR", "marido", "author"),
                      ("AJUIZAMENTO", "marido sozinho", "filing")],
                     "conc", "Ação revisional ajuizada somente pelo marido."),
        record_panel("a03-credit-3", "REsp 1.222.822",
                     [("STJ", "participação ativa necessária", "holding"),
                      ("RESULTADO", "fim sem exame do mérito", "result")],
                     "dif", "STJ: participação ativa tratada como necessária; processo sem exame do mérito."),
    ])


def install():
    page = PAGE.read_text(encoding="utf-8")
    replacements = {
        "<!-- FIGKIT: A03 PARTY -->": party_seating(),
        "<!-- FIGKIT: A03 RECORD -->": record_panels(),
    }
    for marker, markup in replacements.items():
        if page.count(marker) != 1:
            raise SystemExit(f"expected one {marker} in {PAGE}")
        page = page.replace(marker, markup, 1)
    PAGE.write_text(page, encoding="utf-8")
    return PAGE


def specimen_page():
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="../../courses/processo-civil-i/assets/curso.css">
<link rel="stylesheet" href="../../courses/processo-civil-i/assets/aula-03.css"></head><body>
{party_seating()}
<div class="scrolly a03-scrolly"><div class="stage"><figure>{record_panels()}</figure></div></div>
</body></html>"""


if __name__ == "__main__":
    figkit.WARN.clear()
    probe = os.environ.get("FIGKIT_PROBE")
    if probe:
        Path(probe).write_text(specimen_page(), encoding="utf-8")
        print(probe)
    else:
        print(install())
    print("\n".join(figkit.WARN) or "no text warnings")
