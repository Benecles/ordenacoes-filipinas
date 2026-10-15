#!/usr/bin/env python3
"""Fail when an inline <svg> contains an HTML 'breakout' tag (em, b, i, span, p, br, div…).

In HTML parsing, those tags inside foreign content close the <svg>: everything after them renders as loose
text above the drawing (Controle Aula 28, Fig. 2, until 14/10). Use <tspan> for italics or weight inside SVG.
CSS and comments are skipped; <foreignObject> is allowed to hold HTML.
"""
import glob, re, sys

BREAK = r'b|big|blockquote|body|br|center|code|dd|div|dl|dt|em|embed|h[1-6]|head|hr|i|img|li|listing|menu|meta|nobr|ol|p|pre|ruby|s|small|span|strong|strike|sub|sup|table|tt|u|ul|var'
bad = 0
for f in sorted(glob.glob('**/*.html', recursive=True)):
    if 'node_modules' in f:
        continue
    h = open(f, errors='ignore').read()
    h = re.sub(r'(?s)<style\b.*?</style>|<!--.*?-->|<script\b.*?</script>', '', h)
    for m in re.finditer(r'<svg\b', h):
        seg = h[m.start():h.find('</svg>', m.start())]
        seg = re.sub(r'(?s)<foreignObject.*?</foreignObject>', '', seg)
        for b in re.finditer(r'<(%s)\b' % BREAK, seg):
            print(f'FAIL svg-breakout {f}: <{b.group(1)}> inside <svg> (use <tspan>)'); bad += 1
print('svg-breakout:', 'FAIL' if bad else 'PASS')
sys.exit(1 if bad else 0)
