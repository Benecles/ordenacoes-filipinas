#!/usr/bin/env python3
"""Render validated lesson JSON as a static page using the CASA house theme."""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVG_TAGS = {'svg', 'title', 'desc', 'g', 'path', 'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'text', 'tspan'}
SVG_ATTRS = {'viewBox', 'width', 'height', 'x', 'y', 'x1', 'x2', 'y1', 'y2', 'cx', 'cy', 'r', 'rx', 'ry', 'd', 'points', 'fill', 'fill-rule', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'stroke-dasharray', 'opacity', 'transform', 'font-size', 'font-family', 'font-weight', 'text-anchor', 'dominant-baseline', 'role', 'aria-label', 'aria-hidden', 'hidden', 'id', 'data-object', 'data-object-state', 'data-state'}
CSS_CLASS_RE = re.compile(r'\.([_a-zA-Z][\w-]*)')


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def need(obj, index, typ, key, kind=str):
    value = obj.get(key)
    if not isinstance(value, kind) or (kind is str and not value.strip()):
        raise ValueError(f'block {index} ({typ}): required {key!r} must be a non-empty {kind.__name__}')
    return value


def strings(obj, index, typ, key, *, optional=False):
    values = obj.get(key)
    if optional and values is None:
        return []
    if not isinstance(values, list) or any(not isinstance(x, str) or not x.strip() for x in values):
        raise ValueError(f'block {index} ({typ}): {key} must be an array of non-empty strings')
    return values


def inline_text(value: str) -> str:
    """Escape plain text; permit a small emphasis, held/limit, and defined-term grammar."""
    token = re.compile(r'\[\[(held|limit)\|([^\[\]]+)\]\]|\[\[term\|([^|\[\]]+)\|([^\[\]]+)\]\]|\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`')
    out, pos = [], 0
    for m in token.finditer(value):
        out.append(esc(value[pos:m.start()]))
        if m.group(1) is not None:
            out.append(f'<span class="{m.group(1)}">{esc(m.group(2))}</span>')
        elif m.group(3) is not None:
            out.append(f'<span class="term" data-def="{esc(m.group(4))}">{esc(m.group(3))}</span>')
        else:
            groups = m.groups()[4:]
            tag = 'strong' if groups[0] is not None else ('em' if groups[1] is not None else 'code')
            out.append(f'<{tag}>{esc(next(x for x in groups if x is not None))}</{tag}>')
        pos = m.end()
    out.append(esc(value[pos:]))
    return ''.join(out)


def safe_href(value: str, where: str) -> str:
    if not isinstance(value, str) or not value.strip() or re.match(r'\s*(?:[a-z]+:|//)', value, re.I) or any(ord(c) < 32 for c in value):
        raise ValueError(f'{where}: href must be a non-empty local URL')
    return value


def validate_svg(svg: str, objects: list, index: int) -> str:
    if not isinstance(svg, str) or not svg.strip():
        raise ValueError(f'block {index} (figure): svg must be a non-empty inline SVG')
    try:
        root = ET.fromstring(svg)
    except ET.ParseError as e:
        raise ValueError(f'block {index} (figure): invalid SVG XML: {e}') from e
    if root.tag.split('}')[-1] != 'svg':
        raise ValueError(f'block {index} (figure): root element must be svg')
    ids = set()
    for el in root.iter():
        tag = el.tag.split('}')[-1]
        if tag not in SVG_TAGS:
            raise ValueError(f'block {index} (figure): SVG element <{tag}> is not allowed')
        for raw, val in el.attrib.items():
            name = raw.split('}')[-1]
            if name not in SVG_ATTRS or name.lower().startswith('on') or 'url(' in val.lower() or re.search(r'(?:javascript:|data:)', val, re.I):
                raise ValueError(f'block {index} (figure): SVG attribute {name!r} is not allowed')
            if name == 'id':
                if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', val) or val in ids:
                    raise ValueError(f'block {index} (figure): invalid or duplicate SVG id {val!r}')
                ids.add(val)
        if el.text and re.search(r'<|>', el.text):
            # ElementTree has already decoded entities; text remains text when serialized.
            pass
    title = next((e for e in root if e.tag.split('}')[-1] == 'title'), None)
    if title is None or not (title.text or '').strip():
        raise ValueError(f'block {index} (figure): SVG requires a descriptive <title>')
    svg_objects = {e.attrib['data-object'] for e in root.iter() if 'data-object' in e.attrib}
    declared = {o['id'] for o in objects}
    if svg_objects != declared:
        raise ValueError(f'block {index} (figure): SVG data-object ids must match declared objects')
    state_groups = {}
    for el in root.iter():
        if 'data-object-state' in el.attrib or 'data-state' in el.attrib:
            if el.tag.split('}')[-1] != 'g' or 'data-object-state' not in el.attrib or el.attrib.get('data-state') != 'active':
                raise ValueError(f'block {index} (figure): SVG state variants must be <g data-object-state="id" data-state="active">')
            object_id = el.attrib['data-object-state']
            if object_id not in declared or object_id in state_groups:
                raise ValueError(f'block {index} (figure): each declared object needs exactly one active state group')
            state_groups[object_id] = el
    if state_groups.keys() != declared:
        raise ValueError(f'block {index} (figure): add one active SVG state group for each declared object')
    return svg


def render_case(b, i):
    title = esc(need(b, i, b['type'], 'title'))
    context = b.get('context', b.get('text'))
    if not isinstance(context, str) or not context.strip():
        raise ValueError(f'block {i} ({b["type"]}): required context (or legacy text) must be non-empty')
    body = [f'<p>{inline_text(context)}</p>']
    for key, label in [('question', 'Questão'), ('decision', 'Decisão'), ('reasoning', 'Fundamentação')]:
        if b.get(key) is not None:
            body.append(f'<p><span class="ui-label">{label}:</span> {inline_text(need(b, i, b["type"], key))}</p>')
    return f'<details class="bet-case"><summary><span class="bet-case-label">Caso</span> {title}</summary><div class="bet-case-text">{"".join(body)}</div></details>'


def render_exam_item(item, i):
    if not isinstance(item, dict):
        raise ValueError(f'block {i} (exam-item): each item must be an object')
    q = inline_text(need(item, i, 'exam-item', 'question'))
    options = strings(item, i, 'exam-item', 'options')
    answer = inline_text(need(item, i, 'exam-item', 'answer'))
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    choices = ''.join(f'<li><span class="choice-label">{letters[j] if j < len(letters) else j + 1}.</span> {inline_text(option)}</li>' for j, option in enumerate(options))
    explanation = item.get('explanation')
    answer_html = f'<p class="answer"><span class="ui-label">Resposta:</span> {answer}</p>'
    if explanation:
        answer_html += f'<p>{inline_text(need(item, i, "exam-item", "explanation"))}</p>'
    return f'<li class="exam-question"><p class="question">{q}</p><ol class="choices">{choices}</ol><details class="answer-reveal"><summary>Ver resposta</summary>{answer_html}</details></li>'


def render_block(b, i, output_dir):
    if not isinstance(b, dict) or not isinstance(b.get('type'), str):
        raise ValueError(f'block {i} (unknown): expected an object with a string type')
    t = b['type']
    if t == 'heading':
        level = b.get('level', 2)
        if level not in (2, 3, 4):
            raise ValueError(f'block {i} (heading): level must be 2, 3, or 4')
        text = inline_text(need(b, i, t, 'text'))
        return f'<h{level}>{text}</h{level}>'
    if t == 'prose':
        paragraphs = b.get('paragraphs')
        if paragraphs is None:
            paragraphs = [need(b, i, t, 'text')]
        if not isinstance(paragraphs, list) or not paragraphs or any(not isinstance(x, str) or not x.strip() for x in paragraphs):
            raise ValueError(f'block {i} (prose): paragraphs must be a non-empty array of strings')
        return '<section class="corpo">' + ''.join(f'<p>{inline_text(p)}</p>' for p in paragraphs) + '</section>'
    if t == 'source':
        label = esc(need(b, i, t, 'label'))
        kind = b.get('kind', 'doctrine')
        if kind not in ('doctrine', 'statute', 'decision'):
            raise ValueError(f'block {i} (source): kind must be doctrine, statute, or decision')
        paragraphs = b.get('paragraphs', [b.get('text')])
        if not isinstance(paragraphs, list) or not paragraphs or any(not isinstance(x, str) or not x.strip() for x in paragraphs):
            raise ValueError(f'block {i} (source): paragraphs must be a non-empty array of strings')
        source_class = {'doctrine': 'fonte', 'statute': 'fonte lim', 'decision': 'fonte dec'}[kind]
        return f'<aside class="{source_class}"><header><span class="loc">{label}</span></header><blockquote lang="pt-BR">{"".join(f"<p>{esc(x)}</p>" for x in paragraphs)}</blockquote></aside>'
    if t == 'case-card':
        return render_case(b, i)
    if t == 'figure':
        caption = inline_text(need(b, i, t, 'caption'))
        if 'svg' in b:
            objects = b.get('objects', [])
            if not isinstance(objects, list):
                raise ValueError(f'block {i} (figure): objects must be an array')
            normalized = []
            for o in objects:
                if not isinstance(o, dict) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', str(o.get('id', ''))):
                    raise ValueError(f'block {i} (figure): each object requires a simple id')
                normalized.append({'id': o['id'], 'label': need(o, i, t, 'label'), 'description': need(o, i, t, 'description')})
            if len({o['id'] for o in normalized}) != len(normalized):
                raise ValueError(f'block {i} (figure): object ids must be unique')
            art = validate_svg(b['svg'], normalized, i)
            controls = ''
            if normalized:
                controls = (f'<div class="visually-hidden"><p class="object-description" id="figure-description-{i}" aria-live="polite" aria-atomic="true"></p>'
                            + ''.join(f'<span data-object-label="{esc(o["id"])}">{esc(o["label"])}</span><span data-description-for="{esc(o["id"])}">{esc(o["description"])}</span>' for o in normalized)
                            + '</div>')
            return f'<figure class="art interactive-figure"><div class="figure-viewport" tabindex="0" role="region" aria-label="Figura interativa; deslize horizontalmente para ler todos os elementos">{art}</div>{controls}<figcaption>{caption}</figcaption></figure>'
        src = need(b, i, t, 'src')
        p = Path(src)
        if p.is_absolute() or '..' in p.parts or p.suffix.lower() != '.svg':
            raise ValueError(f'block {i} (figure): src must be a repo-relative SVG path without \'..\'')
        alt = esc(b.get('alt', b['caption']))
        return f'<figure class="art"><img src="{esc(Path(os.path.relpath(ROOT / src, output_dir)).as_posix())}" alt="{alt}"><figcaption>{caption}</figcaption></figure>'
    if t == 'step-through':
        title = inline_text(need(b, i, t, 'title'))
        steps = strings(b, i, t, 'steps')
        if not steps:
            raise ValueError(f'block {i} (step-through): steps must not be empty')
        return f'<section class="scrolly"><h2>{title}</h2><ol class="steps">' + ''.join(f'<li class="stage"><div class="panel on">{inline_text(x)}</div></li>' for x in steps) + '</ol></section>'
    if t == 'self-check':
        q = inline_text(need(b, i, t, 'question'))
        answer = inline_text(need(b, i, t, 'answer'))
        return f'<details class="bet-case self-check"><summary>{q}</summary><div class="bet-case-text"><p>{answer}</p></div></details>'
    if t == 'exam-item':
        return '<ol class="exam-list">' + render_exam_item(b, i) + '</ol>'
    if t == 'exam-case':
        title = esc(need(b, i, t, 'title'))
        context = inline_text(need(b, i, t, 'context'))
        items = b.get('items')
        if not isinstance(items, list) or not items:
            raise ValueError(f'block {i} (exam-case): items must be a non-empty array')
        return f'<section class="exam-case"><h2>{title}</h2><div class="exam-context"><p>{context}</p></div><ol class="exam-list">' + ''.join(render_exam_item(item, i) for item in items) + '</ol></section>'
    raise ValueError(f'block {i} ({t}): unsupported block type')


def defined_classes(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    return set(CSS_CLASS_RE.findall(css))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--check-classes', action='store_true')
    a = ap.parse_args()
    source, out = Path(a.input), Path(a.output)
    try:
        data = json.loads(source.read_text(encoding='utf-8'))
        if not isinstance(data, dict) or not isinstance(data.get('blocks'), list):
            raise ValueError('lesson: expected object with blocks array')
        title = need(data, 0, 'lesson', 'title')
        course = need(data, 0, 'lesson', 'course')
        if not re.fullmatch(r'[a-zA-Z0-9_-]+', course):
            raise ValueError('lesson: course must be a simple identifier')
        nav = data.get('navigation', {})
        if not isinstance(nav, dict):
            raise ValueError('lesson: navigation must be an object')
        home_href = safe_href(nav.get('home', '../../index.html'), 'navigation.home')
        home_label = esc(nav.get('home_label', 'Início'))
        previous = nav.get('previous')
        following = nav.get('next')
        def nav_link(item, label):
            if item is None:
                return ''
            if not isinstance(item, dict):
                raise ValueError(f'navigation.{label}: expected href and title')
            href = esc(safe_href(item.get('href'), f'navigation.{label}'))
            name = esc(need(item, 0, f'navigation.{label}', 'title'))
            return f'<a href="{href}"><span>{label}</span><b>{name}</b></a>'
        course_label = esc(course.replace('-', ' ').replace('_', ' ').title())
        body = '\n'.join(render_block(b, i, out.parent.resolve()) for i, b in enumerate(data['blocks'], 1))
        css_hrefs = [os.path.relpath(ROOT / 'assets/casa.css', out.parent.resolve()), os.path.relpath(ROOT / 'assets/lesson.css', out.parent.resolve())]
        js_hrefs = [os.path.relpath(ROOT / 'assets/casa.js', out.parent.resolve()), os.path.relpath(ROOT / 'assets/lesson.js', out.parent.resolve()), os.path.relpath(ROOT / 'assets/offline.js', out.parent.resolve()), os.path.relpath(ROOT / 'assets/highlight.js', out.parent.resolve()), os.path.relpath(ROOT / 'assets/highlight-panel.js', out.parent.resolve())]
        turn_href = Path(os.path.relpath(ROOT / 'assets/turn.js', out.parent.resolve())).as_posix()
        doc = ('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
               f'<script src="{esc(turn_href)}"></script><title>{esc(title)} · Ordenações Filipinas</title><link rel="stylesheet" href="{esc(Path(css_hrefs[0]).as_posix())}"><link rel="stylesheet" href="{esc(Path(css_hrefs[1]).as_posix())}"></head>'
               '<body><a class="skip-link" href="#conteudo">Pular para o conteúdo</a><nav class="topbar" aria-label="Navegação principal">'
               f'<a class="brand" href="{esc(home_href)}">Ordenações Filipinas</a><span class="course-name">{course_label}</span></nav>'
               '<main class="lesson-main" id="conteudo"><header class="hero"><p class="hero-meta">' + course_label + '</p><h1>' + esc(title) + '</h1>'
               + (f'<p class="deck">{esc(data["deck"])}</p>' if isinstance(data.get('deck'), str) and data['deck'].strip() else '')
               + '</header><article class="lesson-content">' + body + '</article><nav class="lesson-nav" aria-label="Aulas vizinhas">'
               + nav_link(previous, 'Anterior') + nav_link(following, 'Próxima') + '</nav></main><footer class="site-footer"><a href="' + esc(home_href) + '">' + home_label + '</a></footer>'
               + ''.join(f'<script src="{esc(Path(h).as_posix())}" defer></script>' for h in js_hrefs) + '</body></html>')
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(doc, encoding='utf-8')
        if a.check_classes:
            if re.search(r'<style\b', doc, re.I) or re.search(r'\sstyle\s*=', doc, re.I):
                raise ValueError('output: page-local CSS is forbidden')
            classes = re.findall(r'\bclass="([^"]*)"', doc)
            used = {c for group in classes for c in group.split()}
            hrefs = re.findall(r'<link\b[^>]*\brel="stylesheet"[^>]*\bhref="([^"]+)"', doc, re.I)
            defined = set()
            for href in hrefs:
                csspath = (out.parent / href).resolve()
                if not csspath.is_file():
                    raise ValueError(f'output: linked stylesheet not found: {href}')
                defined |= defined_classes(csspath.read_text(encoding='utf-8'))
            missing = sorted(used - defined)
            if missing:
                raise ValueError('output: undefined CSS classes: ' + ', '.join(missing))
        print(f'Rendered {out} ({len(data["blocks"])} blocks)')
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(str(e), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
