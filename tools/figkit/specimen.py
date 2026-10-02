"""Builds specimen/figuras.html: one hand-made reference per figure genre, each a real redo from the QC list.
Run: python3 tools/figkit/specimen.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import figkit, controle_a01, delito_u04, contratos_a01, controle_a27, delito_u05, latam_a02, processo_a01

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

ENTRIES = [
    ('Escala · régua', 'medir', 'Controle · Aula 01 · abertura',
     'O parâmetro vira uma régua graduada; o ato é uma faixa medida contra ela. Passar do limite é ver, não ler.',
     'substitui ctl-a01-s1 (o triângulo)', [controle_a01.hero()], 'controle-de-constitucionalidade'),
    ('Escala · régua', 'medir', 'Controle · Aula 01 · Figs. 1–3',
     'A mesma régua nos três passos da aula; na Fig. 3, a mesma lei medida contra duas réguas (Constituição e Pacto).',
     'substitui ctl-a01-s2, ctl-a01-s3', [controle_a01.fig1(), controle_a01.fig2(), controle_a01.fig3()], 'controle-de-constitucionalidade'),
    ('Plano · dois eixos', 'classificar', 'Delito · Unidade 04 · Fig. 1 (5 passos)',
     'Dolo e culpa dependem de duas perguntas ao mesmo tempo: o que o agente previu e o que fez diante disso. A fronteira do art. 18 corta o plano; o caso do trânsito fica em cima dela.',
     'substitui tdl-u04-s2+4', delito_u04.panels(), 'teoria-do-delito'),
    ('Documento · anatomia + corte de lei', 'ler', 'Contratos · Aula 01 · Fig. 2 (4 passos)',
     'Um contrato de verdade (Ana compra um notebook) lido de três jeitos: proposta e aceitação, bem e preço circulando, e a lei que lhe dá força e limite (arts. 421 e 421-A).',
     'substitui tgc-a01-s6+3', contratos_a01.panels2(), 'teoria-geral-dos-contratos'),
    ('Rota · destino do bem + quadro', 'decidir', 'Contratos · Aula 01 · Fig. 3 (3 passos)',
     'Para onde vai o bem decide entre CDC e Código Civil. As três correntes viram um quadro de dois casos reais do STJ.',
     'substitui tgc-a01-s10+2', contratos_a01.panels3(), 'teoria-geral-dos-contratos'),
    ('Relógio processual', 'contar', 'Controle · Aula 27 · Plenário virtual',
     'Dias reais em colunas, cenários em faixas: a janela de seis dias úteis, a vista que suspende, o destaque que reinicia no presencial (com a janela ainda aberta) e o silêncio que não conta como voto.',
     'substitui p-sessao-a/b/c (ctl-a27)', controle_a27.panels(), 'controle-de-constitucionalidade'),
    ('Caminho de decisão', 'decidir', 'Delito · Unidade 05 · Fig. 1 (3 passos)',
     'Três perguntas num tronco; cada saída é uma consequência jurídica com seu artigo. No último passo, o caso do casaco percorre o caminho inteiro e termina atípico, porque o furto não tem forma culposa.',
     'substitui tdl-u05-s2+2', delito_u05.panels(), 'teoria-do-delito'),
    ('Linha do tempo · e plano', 'ordenar', 'Latam · Aula 02 · Fig. 1 (4 passos)',
     'A tese num plano; a linha argentina liga a validação dos golpes por acordada à destituição de 1947 e à troca da Corte; o painel venezuelano põe regras descumpridas e origem de quase metade na magistratura lado a lado; seguem o circuito de cooptação e as três faixas brasileiras.',
     'substitui dla-a02-s3 (Argentina e Venezuela)', latam_a02.panels(), 'direito-latino-americano'),
    ('Documento · anatomia', 'ler', 'Processo · Aula 01 · petição inicial',
     'A petição como peça real: ler os incisos do art. 319 nos campos onde aparecem e localizar o contrato anexo do art. 320.',
     'substitui pci-a01-s2', [processo_a01.panel()], 'processo-civil-i'),
]


def page():
    out = []
    for genre, verb, where, why, replaces, svgs, course in ENTRIES:
        cells = ''.join(f'<div class="s">{s}</div>' for s in svgs)
        wide = len(svgs) == 1 and 'hero-fork' in svgs[0]
        out.append(f'''<section class="ref"><header><span class="g">{genre}</span><span class="v">verbo · {verb}</span></header>
<h2>{where}</h2><p>{why}</p><p class="r">{replaces}</p><div class="{'wide' if wide else 'grid'}">{cells}</div></section>''')
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Figuras · referências · Ordenações Filipinas</title>
<link rel="stylesheet" href="../courses/controle-de-constitucionalidade/assets/controle.css">
<style>body{{max-width:1180px;margin:0 auto;padding:28px 16px 80px}}
h1{{font:750 34px/1.05 var(--sans);margin:0 0 6px}} .lede{{font:17px/1.5 var(--serif,serif);color:var(--ink-2);max-width:62ch;margin:0 0 30px}}
.ref{{border-top:1.5px solid var(--ink);padding:16px 0 26px}} .ref header{{display:flex;gap:14px;font:600 11px var(--mono);letter-spacing:.1em;text-transform:uppercase}}
.g{{color:var(--conc)}} .v{{color:var(--ink-2)}} .ref h2{{font:700 22px/1.2 var(--sans);margin:8px 0 6px}}
.ref p{{font:16px/1.5 var(--serif,serif);max-width:66ch;margin:0 0 6px}} .ref p.r{{font:11px var(--mono);letter-spacing:.06em;color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px;margin-top:12px}} .wide{{margin-top:12px}}
.s{{border:1.5px solid var(--ink);background:var(--paper);padding:6px}}
.s svg{{display:block;width:100%;height:auto;opacity:1!important;visibility:visible!important;position:static!important;transform:none!important}}</style></head><body>
<h1>Figuras · referências</h1><p class="lede">Uma referência feita à mão por gênero, cada uma refazendo uma figura real do site. É o padrão contra o qual as outras são julgadas.</p>
{''.join(out)}</body></html>'''


if __name__ == '__main__':
    p = os.path.join(ROOT, 'specimen', 'figuras.html')
    open(p, 'w').write(page())
    print(p); print('\n'.join(figkit.WARN) or 'no text warnings')
