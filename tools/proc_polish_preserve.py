#!/usr/bin/env python3
"""Compare required fact sets and .fonte bytes with a Git baseline."""
import argparse, html, json, re, subprocess, unicodedata
from html.parser import HTMLParser
from pathlib import Path

class Visible(HTMLParser):
    def __init__(self): super().__init__(); self.out=[]
    def handle_data(self, data): self.out.append(data)
    def text(self): return unicodedata.normalize('NFC', ' '.join(self.out))

def visible(raw):
    p=Visible(); p.feed(raw.decode('utf-8')); return html.unescape(p.text())

def fonte_blocks(raw):
    # Preserve the exact bytes of each .fonte root element, regardless of whether
    # the page uses <aside>, <div>, or another wrapper element.
    token=re.compile(br'<!--.*?-->|<![^>]*>|</?([A-Za-z][\w:-]*)\b[^>]*>',re.I|re.S)
    void={b'area',b'base',b'br',b'col',b'embed',b'hr',b'img',b'input',b'link',b'meta',b'param',b'source',b'track',b'wbr'}
    stack=[]; blocks=[]
    for m in token.finditer(raw):
        tag=m.group(0)
        if tag.startswith((b'<!--',b'<!')): continue
        name=m.group(1).lower()
        if tag.startswith(b'</'):
            for i in range(len(stack)-1,-1,-1):
                if stack[i][0]==name:
                    entry=stack[i]
                    del stack[i:]
                    if entry[1]: blocks.append((entry[2],m.end(),raw[entry[2]:m.end()]))
                    break
        elif not tag.rstrip().endswith(b'/>') and name not in void:
            cls=re.search(br'\bclass\s*=\s*(["\'])(.*?)\1',tag,re.I|re.S)
            is_fonte=bool(cls and b'fonte' in cls.group(2).split())
            stack.append((name,is_fonte,m.start()))
    return [block for _,__,block in sorted(blocks)]

def fact_sets(raw):
    t=visible(raw)
    articles=set(re.findall(r'\barts?\.?\s*(\d+(?:-[A-Z])?)(?:º|°|o)?',t,re.I))
    dates=set(re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',t))
    dates|=set(re.findall(r'\b\d{1,2}\s+de\s+(?:janeiro|fevereiro|março|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+de\s+\d{4}\b',t,re.I))
    amounts=set(re.findall(r'R\$\s*\d[\d.]*(?:,\d{1,2})?',t,re.I))
    exams=set(re.findall(r'\b(?:Prova|Avaliação|Avaliação|questão)\s*(?:de\s*)?(?:\d{4}(?:/\d+)?|\d+)\b|\b\d{4}/\d+\s+P[12]\b',t,re.I))
    nums=set(re.findall(r'\d+',t))
    # Conservatively retain capitalized two-to-four-word names/entities and standalone proper names.
    names=set(re.findall(r'\b[A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ][a-záàâãéêíóôõúüç]+(?:\s+[A-ZÁÀÂÃÉÊÍÓÔÕÚÜÇ][a-záàâãéêíóôõúüç]+){1,3}\b',t))
    return {'article_numbers':articles,'dates':dates,'amounts':amounts,'party_names':names,'exam_references':exams,'numeric_tokens':nums}

def get_base(site,base,path):
    return subprocess.check_output(['git','show',f'{base}:{path}'],cwd=site)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('site'); ap.add_argument('--base',default='origin/main'); ap.add_argument('--pages',nargs='+',required=True); a=ap.parse_args()
    site=Path(a.site); rows=[]; bad=False
    for rel in a.pages:
        old=get_base(site,a.base,rel); new=(site/rel).read_bytes()
        before=fact_sets(old); after=fact_sets(new)
        diff={k:{'removed':sorted(before[k]-after[k]),'added':sorted(after[k]-before[k])} for k in before if before[k]!=after[k]}
        fb,fa=fonte_blocks(old),fonte_blocks(new)
        row={'page':rel,'fact_set_diff':diff,'fonte_blocks_identical':fb==fa,'fonte_count':len(fb)}
        if fb!=fa: row['fonte_diff']={'before_count':len(fb),'after_count':len(fa)}
        rows.append(row); bad|=bool(diff or fb!=fa)
    print(json.dumps(rows,ensure_ascii=False,indent=2))
    return 1 if bad else 0
if __name__=='__main__': raise SystemExit(main())
