"""Build the page-specific party seating figure and IDPJ timing folios for Aula 05."""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import figkit as f

ROOT = HERE.parents[1]
PAGE = ROOT / "courses/processo-civil-i/aula-05.html"


def hero_figure():
    inner = []
    inner.append('<ellipse class="table" cx="542" cy="205" rx="250" ry="82"/>')
    inner.append('<path class="table-rule" d="M314 205H770"/>')
    inner.append(f.t(542, 195, "COBRANÇA", size=12, fill="var(--ink-2)", anchor="middle", weight=700, caps=True))
    inner.append(f'<text x="542" y="230" text-anchor="middle" class="table-label" style="font-size:25px;fill:var(--ink)">R$ 100.000</text>')

    # Round seat marks place the parties around the same debt, rather than connecting them as a flowchart.
    seats = [
        (155, 205, "seat", "seat-name", "seat-note",
         [(85, 201, "Adamastor", "end"), (85, 225, "credor · autor", "end")]),
        (905, 111, "seat", "seat-name", "seat-note",
         [(948, 107, "Francisco", "start"), (948, 131, "fiador · réu", "start")]),
        (905, 205, "seat", "seat-name", "seat-note",
         [(948, 201, "Raimundo", "start"), (948, 225, "afiançado · devedor", "start")]),
        (905, 299, "seat", "seat-name", "seat-note",
         [(948, 295, "Florinda", "start"), (948, 319, "cofiadora", "start")]),
    ]
    for cx, cy, klass, name_cls, note_cls, labels in seats:
        inner.append(f'<circle class="{klass}" cx="{cx}" cy="{cy}" r="24"/>')
        inner.append(f'<circle class="table-rule" cx="{cx}" cy="{cy}" r="10"/>')
        for x, y, label, anchor in labels:
            c = name_cls if y in (201, 107, 201, 295) else note_cls
            size = 17 if c == name_cls else 14
            inner.append(f.t(x, y, label, size=size, fill="var(--ink)" if c == name_cls else "var(--ink-2)", anchor=anchor, weight=700 if c == name_cls else 500, ls="0", cls=c))
    inner.append(f.line(80, 373, 1000, 373, tone="ink", w=1.2))
    inner.append(f.t(540, 402, "CONTESTAÇÃO DE FRANCISCO · PEDIDO DE CHAMAMENTO", size=13, anchor="middle", fill="var(--ink-2)", weight=650, caps=True))
    graphic = f.svg("-80 0 1220 430", "".join(inner), cls="a05-hero-graphic fig", label="A cobrança de Adamastor reúne o credor e três pessoas ligadas à dívida. Francisco, fiador réu, ocupa o assento marcado; o pedido na contestação chama Raimundo, afiançado, e Florinda, cofiadora.", ident="pci-a05-f1")
    graphic = graphic.replace('<svg id="pci-a05-f1"', '<svg id="pci-a05-f1" data-family="figure.seating"', 1)
    return (f'<figure class="a05-hero-figure">{graphic}'
            '<figcaption>Adamastor cobra Francisco, fiador; a contestação pede a entrada do afiançado Raimundo e da cofiadora Florinda.</figcaption>'
            '<span class="src" hidden data-src="Exame 2018/2, Avaliação 1, questão 2, versão v1, PDF p. 1; CPC, art. 130."></span>'
            '</figure>')


def folio(initial):
    base = [
        '<rect class="paper" x="70" y="76" width="460" height="450"/>',
        '<path class="rule" d="M70 132H530"/>',
    ]
    if initial:
        base += [
            f.t(104, 112, "PETIÇÃO INICIAL", size=13, weight=700, fill="var(--ink-2)", caps=True),
            f.t(104, 181, "Pedido de desconsideração", size=20, fill="var(--ink)", weight=700, ls="0"),
            f.t(104, 220, "Acompanha a demanda desde o início", size=15, fill="var(--ink-2)", ls="0"),
            '<path class="page-mark" d="M104 255H464M104 280H426M104 305H448"/>',
            '<rect class="stamp-outline" x="116" y="354" width="314" height="60" transform="rotate(-3 273 384)"/>',
            f.t(273, 391, "SEM INCIDENTE SEPARADO", size=14, anchor="middle", fill="var(--dif)", weight=700, caps=True),
            f.t(104, 462, "Citação na própria demanda", size=16, fill="var(--ink-2)", ls="0"),
            f.t(104, 493, "sem suspensão por instauração", size=15, fill="var(--ink-2)", ls="0"),
        ]
        label = "Pedido na petição inicial. Sem incidente separado e sem suspensão pela instauração."
        ident = "a05-pedido-inicial"
    else:
        base += [
            f.t(104, 112, "PROCESSO EM CURSO", size=13, weight=700, fill="var(--ink-2)", caps=True),
            f.t(104, 181, "Cobrança já iniciada", size=20, fill="var(--ink)", weight=700, ls="0"),
            f.t(104, 220, "Pedido superveniente", size=17, fill="var(--ink-2)", ls="0"),
            '<path class="page-mark" d="M104 255H286M104 280H262"/>',
            '<rect class="stamp-limit" x="104" y="326" width="188" height="58" transform="rotate(-3 198 355)"/>',
            f.t(198, 363, "SUSPENSO", size=15, anchor="middle", fill="var(--conc)", weight=700, caps=True),
            '<rect class="paper" x="320" y="220" width="182" height="252"/>',
            '<path class="rule" d="M320 273H502"/>',
            f.t(411, 256, "INCIDENTE", size=13, anchor="middle", fill="var(--ink-2)", weight=700, caps=True),
            f.t(411, 320, "IDPJ", size=22, anchor="middle", fill="var(--ink)", weight=700, caps=True),
            '<circle class="stamp-on" cx="411" cy="383" r="43"/>',
            f.t(411, 388, "15 DIAS", size=14, anchor="middle", fill="var(--conc)", weight=700, caps=True),
            f.t(104, 445, "Alvo citado", size=12, fill="var(--ink-2)", ls="0"),
            f.t(104, 467, "responde e requer provas", size=12, fill="var(--ink-2)", ls="0"),
            f.t(104, 489, "Prazo: 15 dias da citação", size=12, fill="var(--ink-2)", ls="0"),
        ]
        label = "Pedido superveniente. Incidente instaurado e processo suspenso. A pessoa visada é citada para responder e requerer provas em quinze dias contados da citação."
        ident = "a05-pedido-superveniente"
    panel = "panel on a05-document" if initial else "panel a05-document"
    graphic = f.svg("0 0 600 600", "".join(base), cls=panel, label=label, ident=ident)
    return graphic.replace(f'<svg id="{ident}"', f'<svg id="{ident}" data-family="figure.form"', 1)


def timing_figure():
    first, second = folio(True), folio(False)
    return f'''<div class="scrolly a05-s2">
  <div class="stage">
    <figure aria-label="Duas entradas temporais para o mesmo pedido de desconsideração">
      {first}
      {second}
      <figcaption><span class="stage-step">1 / 2</span><span>Mesmo pedido · fase diferente</span></figcaption>
    </figure>
  </div>
  <div class="steps">
    <section class="step on" data-panel="a05-pedido-inicial" data-slides="Petição inicial">
      <div class="card">
        <h3>Pedido na petição inicial</h3>
        <p>O pedido já integra a demanda; não se abre incidente separado. A pessoa cujo patrimônio se busca alcançar é citada no processo inicial.</p>
        <span class="src" hidden data-src="CPC, art. 134, § 2º; Didier, Curso de Direito Processual Civil, v. 1, cap. 13, § 6.4."></span>
      </div>
    </section>
    <section class="step" data-panel="a05-pedido-superveniente" data-slides="Processo em curso">
      <div class="card">
        <h3>Pedido durante o processo</h3>
        <p>O pedido superveniente abre o incidente e suspende o processo. A pessoa visada é citada e tem 15 dias para se manifestar e pedir provas.</p>
        <span class="src" hidden data-src="CPC, arts. 134, § 3º, e 135; Didier, Curso de Direito Processual Civil, v. 1, cap. 13, § 6.4."></span>
      </div>
    </section>
  </div>
</div>'''


def replace_between(page, start_marker, end_marker, replacement):
    a = page.find(start_marker)
    b = page.find(end_marker, a + len(start_marker))
    if a < 0 or b < 0:
        raise SystemExit(f"Missing markers: {start_marker}")
    return page[:a] + start_marker + "\n" + replacement + "\n" + end_marker + page[b + len(end_marker):]


def main():
    page = PAGE.read_text(encoding="utf-8")
    page = replace_between(page, "<!-- FIGKIT A05 F1 START -->", "<!-- FIGKIT A05 F1 END -->", hero_figure())
    page = replace_between(page, "<!-- FIGKIT A05 F2 START -->", "<!-- FIGKIT A05 F2 END -->", timing_figure())
    PAGE.write_text(page, encoding="utf-8")
    print(f"Generated F1 and F2 in {PAGE}")


if __name__ == "__main__":
    main()
