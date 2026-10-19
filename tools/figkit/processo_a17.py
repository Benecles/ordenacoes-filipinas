"""Processo Civil I · Aula 17: the native decision form and case panels.

The working HTML form is not an SVG retyping of legal text. Its source is quoted once in the
lesson's .fonte block; this form applies the rule and progressively enhances its default state.
Run `python3 tools/figkit/processo_a17.py` to install the form and call Aula 17's figure injector.
Set FIGKIT_PROBE to write a standalone specimen page for visual inspection.
"""
from pathlib import Path
import os
import sys
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / 'courses' / 'processo-civil-i' / 'aula-17.html'
sys.path.insert(0, os.path.dirname(__file__))
import inject as figure_inject
import processo_a17_panels


def instrument():
    return '''<figure class="a17-instrument" id="art373-instrument" aria-labelledby="a17-form-title" data-does="decidir · classificar o fato e verificar se cabe redistribuição, com fundamento, oportunidade e possibilidade de cumprimento · quando se aplica a regra ordinária?">
  <div class="a17-instrument__head">
    <span class="label">CPC · instrumento de decisão</span>
    <h3 id="a17-form-title">Distribuição do ônus da prova</h3>
  </div>
  <div class="a17-instrument__body">
    <div class="a17-statute">
      <span class="art-head">Pergunta de entrada</span>
      <p>Qual fato precisa ser provado para reconhecer o direito pedido?</p>
      <p>Qual fato, se alegado na defesa, impede, modifica ou extingue esse direito?</p>
      <p>A ficha testa a distribuição ordinária e os limites de uma mudança do encargo.</p>
    </div>
    <form class="a17-controls" id="a17-controls" aria-describedby="a17-result">
      <label for="a17-fato">Qual é o tipo de fato?</label>
      <select name="fato" id="a17-fato">
        <option value="constitutivo" selected>Constitutivo do direito</option>
        <option value="impeditivo">Impeditivo do direito</option>
        <option value="modificativo">Modificativo do direito</option>
        <option value="extintivo">Extintivo do direito</option>
      </select>
      <label for="a17-hipotese">Há hipótese para redistribuir o encargo?</label>
      <select name="hipotese" id="a17-hipotese">
        <option value="nenhuma" selected>Nenhuma · aplica-se o caput</option>
        <option value="lei">Previsão legal</option>
        <option value="dificuldade">Impossibilidade ou excessiva dificuldade do encargo do caput</option>
        <option value="facilidade">Maior facilidade para obter a prova do fato contrário</option>
      </select>
      <fieldset>
        <legend>Salvaguardas do § 1º</legend>
        <label class="check-line"><input type="checkbox" name="fundamentada" value="sim"> Decisão fundamentada</label>
        <label class="check-line"><input type="checkbox" name="oportunidade" value="sim"> Oportunidade para cumprir o encargo</label>
      </fieldset>
      <label for="a17-cumprivel">A parte que receberá o encargo pode cumpri-lo?</label>
      <select name="cumprivel" id="a17-cumprivel">
        <option value="sim" selected>Sim</option>
        <option value="nao">Não · seria impossível ou excessivamente difícil</option>
      </select>
      <div class="a17-result" id="a17-result" data-state="default" role="status" aria-live="polite">
        <span class="a17-result__title">Mantém-se a regra do caput</span>
        <p class="a17-result__text">O ônus ordinário cabe ao autor quanto ao fato constitutivo.</p>
      </div>
    </form>
  </div>
  <figcaption>Instrumento · Classifique o fato e teste os fundamentos, a oportunidade e o limite da redistribuição</figcaption>
</figure>'''


def hero_figure():
    drawing = processo_a17_panels.hero_balance()
    return f'''<figure class="a17-hero-art" id="a17-release42-hero" data-does="prever · quem suporta a dúvida final sobre o fato constitutivo do pedido · qual parte deve suportá-la?" aria-labelledby="a17-hero-title">
<h2 id="a17-hero-title">Quem suporta a dúvida?</h2>
<p class="a17-hero-prompt">Antes de ler a regra, escolha onde colocar a dúvida sobre um fato constitutivo do pedido.</p>
<div class="a17-scale">{drawing}</div>
<p class="a17-hero-outcome" id="a17-hero-outcome" role="status" aria-live="polite" hidden></p>
<figcaption>Escolha um prato para ver o resultado da previsão.</figcaption></figure>'''


class A17HeroMatcher(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pan_buttons = 0
        self.outcome = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'button' and 'a17-pan' in attrs.get('class', '').split():
            self.pan_buttons += 1
        if 'a17-hero-outcome' in attrs.get('class', '').split() and attrs.get('role') == 'status':
            self.outcome = True


def match_built_page():
    matcher = A17HeroMatcher()
    matcher.feed(PAGE.read_text(encoding='utf-8'))
    if matcher.pan_buttons != 2 or not matcher.outcome:
        raise SystemExit(f'A17 hero matcher: expected two .a17-pan buttons and an outcome status line; found {matcher.pan_buttons} buttons, status={matcher.outcome}')


def timeline_scrolly():
    panels = (processo_a17_panels.decision_timeline(),
              processo_a17_panels.decision_timeline(publication=True))
    return f'''<div class="scrolly a17-timeline-scrolly" aria-label="Linha do tempo do REsp 70.170/SP">
  <div class="stage"><figure>{panels[0]}{panels[1]}<figcaption>Fig. 1 · O julgamento e a publicação do precedente ocorreram com intervalo de 55 dias.</figcaption></figure></div>
  <div class="steps">
    <section class="step on" data-panel="pci-a17-precedent-time"><h3>Julgamento · 18 abr. 2000</h3><p>A 4ª Turma julgou o REsp 70.170/SP, sobre cotas condominiais periódicas.</p></section>
    <section class="step" data-panel="pci-a17-precedent-time-2"><h3>Publicação · 12 jun. 2000</h3><p>O intervalo medido entre julgamento e publicação é de 55 dias; o acórdão aplicou o art. 943 do CC/1916.</p></section>
  </div>
</div>'''


def specimen_section():
    return f'''<section class="ref native-ref"><header><span class="g">Instrumento · formulário de decisão</span><span class="v">verbo · decidir</span></header>
<h2>Processo · Aula 17 · art. 373</h2><p>O leitor seleciona o tipo de fato e testa as hipóteses e salvaguardas legais para a redistribuição.</p><p class="r">primeira ocorrência · Aula 17</p>
{instrument()}</section>'''


def specimen_page():
    css = (ROOT / 'courses' / 'processo-civil-i' / 'assets' / 'aula-17.css').as_uri()
    js = (ROOT / 'courses' / 'processo-civil-i' / 'assets' / 'aula-17.js').as_uri()
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Figkit · Processo Civil Aula 17</title><link rel="stylesheet" href="{css}">
<style>body{{max-width:1180px;margin:0 auto;padding:24px 16px 80px;background:var(--paper);color:var(--ink)}}h1{{font:750 30px/1.1 var(--sans)}}.native-ref{{border-top:1.5px solid var(--ink);padding:16px 0 26px}}.native-ref header{{display:flex;gap:14px;font:600 11px var(--mono);letter-spacing:.1em;text-transform:uppercase}}.native-ref .g{{color:var(--conc)}}.native-ref .v{{color:var(--ink-2)}}.native-ref h2{{font:700 22px/1.2 var(--sans);margin:8px 0 6px}}.native-ref p{{font:16px/1.5 var(--serif,serif);max-width:66ch;margin:0 0 6px}}.native-ref p.r{{font:11px var(--mono);letter-spacing:.06em;color:var(--muted)}}</style></head><body>
<h1>Figuras · referências</h1><p>Instrumento nativo de decisão construído a partir do art. 373.</p>{specimen_section()}
<script src="{js}"></script></body></html>'''


def install():
    source = PAGE.read_text(encoding='utf-8')
    for marker, generated, description in (
        ('<!-- A17 HERO FIGURE -->', hero_figure(), 'hero'),
        ('<!-- A17 TIMELINE FIGURE -->', timeline_scrolly(), 'timeline'),
    ):
        if source.count(marker) == 1:
            source = source.replace(marker, generated, 1)
        elif description == 'hero' and source.count('<figure class="a17-hero-art"') == 1:
            # the marker was used up by an earlier hero: replace the whole figure, so the wrapper (pan buttons,
            # outcome line, caption) follows the generator, not only the drawing inside it
            start = source.find('<figure class="a17-hero-art"')
            end = source.find('</figure>', source.find('</svg>', start)) + len('</figure>')
            source = source[:start] + generated + source[end:]
        elif source.count(marker) == 0 and (
            ('pci-a17-hero' in source if description == 'hero' else 'pci-a17-precedent-time' in source)
        ):
            continue
        else:
            raise SystemExit(f'expected one A17 {description} marker or its generated output')
    start = source.find('<figure class="a17-instrument"')
    end_at = source.find('</figure>', start)
    if start < 0 or end_at < 0 or source.find('<figure class="a17-instrument"', start + 1) >= 0:
        raise SystemExit(f'expected exactly one generated art. 373 form in {PAGE}')
    end = end_at + len('</figure>')
    PAGE.write_text(source[:start] + instrument() + source[end:], encoding='utf-8')
    source = PAGE.read_text(encoding='utf-8')
    first_id = 'id="pci-a17-precedent-time"'
    second_id = 'id="pci-a17-precedent-time-2"'
    if first_id not in source and source.count(second_id) == 2:
        source = source.replace(second_id, first_id, 1)
        PAGE.write_text(source, encoding='utf-8')
    figure_inject.inject('courses/processo-civil-i/aula-17.html', {
        'pci-a17-hero': processo_a17_panels.hero_balance(),
        'pci-a17-precedent-time': processo_a17_panels.decision_timeline(),
        'pci-a17-precedent-time-2': processo_a17_panels.decision_timeline(publication=True),
        'pci-a17-presumption': processo_a17_panels.presumption_panel(),
    })
    match_built_page()
    return PAGE


if __name__ == '__main__':
    probe = os.environ.get('FIGKIT_PROBE')
    if probe:
        Path(probe).write_text(specimen_page(), encoding='utf-8')
        print(probe)
    else:
        print(install())
    print('no text warnings')
