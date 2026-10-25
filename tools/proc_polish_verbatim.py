#!/usr/bin/env python3
"""Check exam card question/case quotations against Processo's exam bank."""
import argparse, html, json, re, unicodedata
from html.parser import HTMLParser
from pathlib import Path

class Text(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.hidden_summary=0
    def handle_starttag(self, tag, attrs):
        if tag=='span' and dict(attrs).get('class','')=='bet-case-label': self.hidden_summary+=1
        if tag in ('p','div','br','li'): self.parts.append(' ')
    def handle_endtag(self, tag):
        if tag=='span' and self.hidden_summary: self.hidden_summary-=1
        if tag in ('p','div','br','li'): self.parts.append(' ')
    def handle_data(self, data):
        if not self.hidden_summary: self.parts.append(data)
    def result(self): return norm(' '.join(self.parts))

def norm(s):
    s=unicodedata.normalize('NFC',html.unescape(s))
    return re.sub(r'\s+',' ',s).strip().casefold()
def text(s):
    p=Text(); p.feed(s); return p.result()
def classes(attrs): return dict(attrs).get('class','').split()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('site'); ap.add_argument('--bank',required=True); a=ap.parse_args()
    bank=json.loads(Path(a.bank).read_text())
    records=[]
    for q in bank.get('questions',[]):
        for appearance in q.get('appearances',[]):
            records.append(appearance)
    errors=0; checked=0
    for page in sorted(Path(a.site,'courses/processo-civil-i').glob('aula-*.html')):
        src=page.read_text(encoding='utf-8')
        for block in re.findall(r'<div class="bet">(.*?)<div class="bet-opts">',src,re.S):
            km=re.search(r'class="bet-k">(.*?)</span>',block,re.S)
            label=text(km.group(1)) if km else ''
            q=re.search(r'class="bet-q">(.*?)</p>',block,re.S)
            qtext=text(q.group(1)) if q else ''
            context=label+' '+qtext
            if not re.search(r'(?:prova\s+(?:19|20)\d{2}|avalia[çc][ãa]o[^.]{0,40}(?:19|20)\d{2}|quest[ãa]o\s*\d+\s+da\s+prova\s+(?:de\s+)?(?:19|20)\d{2}|(?:19|20)\d{2}/\d+\s+P[12])',context,re.I): continue
            qm=re.search(r'quest[ãa]o\s*(\d+)',context,re.I)
            if not qm: print(f'FAIL {page.name}: exam card has no question number'); errors+=1; continue
            qn=qm.group(1); year=re.search(r'(?:19|20)\d{2}',context).group(0)
            candidates=[r for r in records if str(r.get('question_number'))==qn and year in str(r.get('year'))]
            case=re.search(r'<details\b[^>]*class="[^"]*bet-case[^"]*"[^>]*>(.*?)</details>',block,re.S)
            case_inner=case.group(1) if case else ''
            case_text=text(case_inner if 'bet-case-text' in case_inner else re.sub(r'<summary\b[^>]*>.*?</summary>', ' ', case_inner, flags=re.S)) if case else ''
            exact=[r for r in candidates if (qtext and qtext in norm(r.get('verbatim_text',''))) or (case_text and case_text in norm(r.get('verbatim_text','')))]
            if exact: candidates=exact
            if not candidates:
                print(f'FAIL {page.name}: no bank record for {year} question {qn}'); errors+=1; continue
            record=candidates[0]; source=norm(record.get('verbatim_text','')); checked+=1
            if not qtext or qtext not in source:
                print(f'FAIL {page.name}: exam question is not an exact bank substring'); errors+=1
            # Only a labeled exam case is compared to the bank. Own legal contexts use another label.
            if case:
                sm=re.search(r'<summary\b[^>]*>(.*?)</summary>',case.group(1),re.S)
                case_label=text(sm.group(1)) if sm else ''
                if 'prova' in case_label or 'avaliação' in case_label or 'avaliacao' in case_label:
                    if not case_text or case_text not in source:
                        print(f'FAIL {page.name}: exam case is not an exact bank substring'); errors+=1
    print(f'{checked} exam cards checked; {errors} mismatch(es)')
    return 1 if errors else 0
if __name__=='__main__': raise SystemExit(main())
