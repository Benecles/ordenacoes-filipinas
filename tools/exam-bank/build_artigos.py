#!/usr/bin/env python3
"""Generate the Processo Civil I CPC provision index from its structured data."""
from __future__ import annotations
import argparse, html, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DEFAULT = Path(__file__).with_name('processo_artigos.json')
OUTPUT_DEFAULT = ROOT / 'courses/processo-civil-i/artigos.html'

def esc(value: object) -> str:
    return html.escape(str(value), quote=True)

def render(data: dict) -> str:
    items = []
    for item in data['provisions']:
        items.append(
            '<li><h3>' + esc(item['provision']) + '</h3>'
            '<p>' + esc(item['summary']) + '</p>'
            '<a href="' + esc(item['home_href']) + '">Ver o artigo na aula</a></li>'
        )
    return '''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Artigos do curso · Processo Civil I</title><meta name="description" content="Índice dos dispositivos do CPC trabalhados nas aulas de Processo Civil I."><link rel="stylesheet" href="assets/curso.css?v=32067c15c6"><link rel="stylesheet" href="../../assets/casa.css"><style>.article-index{max-width:920px;margin:36px auto;padding:0 clamp(16px,4vw,48px)}.article-index>p{max-width:68ch;font:400 18px/1.6 var(--serif)}.article-index ol{list-style:none;padding:0;margin:28px 0}.article-index li{padding:18px 0;border-top:1px solid var(--grid-major)}.article-index h3{margin:0 0 5px;font:600 18px/1.35 var(--serif)}.article-index li p{margin:0 0 7px;max-width:68ch;color:var(--ink-2)}.article-index a{font:500 13px/1.5 var(--mono);color:var(--conc)}.endnav{max-width:920px;margin:36px auto;padding:0 clamp(16px,4vw,48px)}</style></head><body class="casa" data-int="proposto"><nav class="topbar"><a href="index.html">← Processo Civil I-a</a><span>Consulta · CPC</span><button class="theme-toggle" type="button" aria-pressed="false" title="Alternar modo noite">Modo noite</button></nav><header class="hero"><div class="kicker label"><span>Processo Civil I-a</span><span>DIR02002</span><span>Consulta</span></div><h1><span class="split">Artigos do</span><span class="split">curso</span></h1><p class="deck">Localize a regra processual na aula em que ela ganha aplicação.</p><div class="titleblock label" role="list"><div role="listitem">Dispositivos<b>''' + str(len(items)) + '''</b></div><div role="listitem">Uso<b>artigos do CPC</b></div><div role="listitem">Destino<b>aula de referência</b></div></div></header><main class="article-index"><p>O índice reúne os dispositivos trabalhados no curso. Cada entrada aponta para uma aula, que apresenta o texto legal e sua aplicação.</p><ol>''' + ''.join(items) + '''</ol></main><nav class="endnav" aria-label="Navegação"><a href="index.html">← Voltar ao curso</a></nav><script src="assets/curso.js?v=7928ccf795"></script><script src="../../assets/casa.js" defer></script><script src="../../assets/offline.js" defer></script><script src="../../assets/highlight.js" defer></script><script src="../../assets/highlight-panel.js" defer></script></body></html>'''

def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = content.encode('utf-8')
    if path.exists() and path.read_bytes() == encoded:
        return False
    path.write_bytes(encoded)
    return True

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=DATA_DEFAULT)
    parser.add_argument('--output', type=Path, default=OUTPUT_DEFAULT)
    args = parser.parse_args()
    data = json.loads(args.data.read_text(encoding='utf-8'))
    write_if_changed(args.output, render(data))

if __name__ == '__main__':
    main()
