#!/usr/bin/env python3
"""Generate the Processo Civil I P1 workbench and spaced-repetition cards from exam-bank.json."""
from __future__ import annotations
import argparse, html, json, re, hashlib
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BANK_DEFAULT = Path('/Users/benecles/Developer/ordenacoes-filipinas-workshop/work/pipeline/processo-civil-i/exam-bank.json')
CPC_INDEX_DEFAULT = Path('/Users/benecles/Developer/ordenacoes-filipinas-workshop/work/pipeline/processo-civil-i/chapters/cpc-lei-13105-capture-2026-09-28/index.json')
OFFICIAL_KEY_DEFAULT = Path(__file__).with_name('processo-official-keys.json')
TOPICS = [
    {'id':'semana-01','label':'Semana 01','title':'Apresentação, fase de conhecimento e petição inicial','lessons':['aula-01.html'],'article':'Art. 321','frame':'Apresente o defeito, indique a oportunidade de correção e conclua com a consequência processual.'},
    {'id':'semanas-03-04','label':'Semanas 03–04','title':'Improcedência liminar, audiência, partes e litisconsórcio','lessons':['aula-02.html','aula-03.html'],'article':'Art. 332','frame':'Identifique a hipótese legal e os fatos que a acionam; conclua pela consequência prevista.'},
    {'id':'semanas-05-06','label':'Semanas 05–06','title':'Intervenção de terceiros','lessons':['aula-04.html','aula-05.html','aula-05-casos.html','aula-12.html'],'article':'Art. 125','frame':'Nomeie a modalidade de intervenção, seus pressupostos e o efeito que produz no processo.'},
    {'id':'semana-07','label':'Semana 07','title':'Comunicação, atos, cooperação e prazos','lessons':['aula-06-citacao.html','aula-06.html','aula-07.html','aula-07-preclusao.html'],'article':'Art. 219','frame':'Localize o ato e o marco de contagem, aplique o prazo legal e indique a data ou consequência pedida.'},
    {'id':'semana-08','label':'Semana 08','title':'Resposta do réu','lessons':['aula-08.html','aula-08-revelia.html'],'article':'Art. 336','frame':'Indique a resposta cabível, o momento e o efeito da alegação ou omissão descrita.'},
    {'id':'semana-09','label':'Semana 09','title':'Nulidades, estabilização, saneamento e julgamento','lessons':['aula-09.html','aula-13.html'],'article':'Art. 276','frame':'Aponte a forma violada, o prejuízo ou a finalidade do ato e conclua sobre seu aproveitamento ou invalidação.'},
]
FRAMES = {
 'objective':'Marque a alternativa e aponte a condição do dispositivo que decide a questão.',
 'case':'Responda à consequência pedida, indique o fato que aciona a regra e aplique cada requisito ao enunciado.',
 'discursive':'Organize a resposta em conclusão, regra aplicável, confronto com os fatos e consequência.',
 'VF':'Classifique cada afirmação e corrija a que contrariar o dispositivo.',
 'V/F':'Classifique cada afirmação e corrija a que contrariar o dispositivo.',
 'true_false':'Classifique cada afirmação e corrija a que contrariar o dispositivo.',
}

def esc(s): return html.escape(str(s or ''), quote=True)
def label_exam(a):
    year = str(a.get('year') or 'Prova')
    qn = str(a.get('question_number') or '')
    prof = ' · Prof. Sérgio Mattos' if year == '2025/2' else ''
    exam = f'Prova {year}{prof}'
    if qn: exam += f' · questão {qn}'
    return exam

def p1_appearance(a):
    lesson = a.get('lesson_id')
    # This one record is still pending the chair's ruling, although it remains in questions[].
    if a.get('year') == '2025/2' and a.get('question_number') == 5: return False
    return any(lesson in t['lessons'] for t in TOPICS)

def get_question_record(record):
    appearances = [a for a in record.get('appearances',[]) if p1_appearance(a)]
    if not appearances: return None
    # A consolidated record is rendered once; all P1 exam appearances are listed as provenance.
    lead = appearances[0]
    topic = next((t for t in TOPICS if lead.get('lesson_id') in t['lessons']), TOPICS[-1])
    q = dict(lead)
    q['appearances'] = appearances
    q['id'] = record.get('id') or hashlib.sha256(lead.get('verbatim_text','').encode()).hexdigest()[:16]
    q['topic_id'] = topic['id']
    q['topic_title'] = lead.get('topic') or topic['title']
    q['exam_labels'] = list(dict.fromkeys(label_exam(a) for a in appearances))
    q['source_years'] = list(dict.fromkeys(str(a.get('year') or '') for a in appearances))
    return q

class TextExtractor(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]
    def handle_data(self,data): self.parts.append(data)

def statute_text(index_path, article_id):
    index=json.loads(index_path.read_text())
    chapter=next(c for c in index['chapters'] if c['id']==article_id)
    source=(index_path.parent / index['capture_path']).resolve()
    number=re.search(r'\d+',article_id).group(0)
    target=f'art{number}'
    class ArticleExtractor(HTMLParser):
        def __init__(self): super().__init__(); self.active=False; self.parts=[]
        def handle_starttag(self,tag,attrs):
            if tag!='a': return
            name=dict(attrs).get('name','')
            if name==target: self.active=True
            elif self.active and re.fullmatch(r'art\d+',name): self.active=False
        def handle_data(self,data):
            if self.active: self.parts.append(data)
    parser=ArticleExtractor()
    parser.feed(source.read_text(encoding=index.get('capture_encoding','utf-8'),errors='replace'))
    if not parser.parts: raise ValueError(f'Cannot find {article_id} in official CPC capture')
    text=' '.join(' '.join(parser.parts).split())
    section=re.search(r'\s+(?:Se[cç][aã]o|Subse[cç][aã]o|Cap[ií]tulo|T[ií]tulo)\s+[IVXLCDM]+\b',text,re.I)
    if section: text=text[:section.start()]
    text=re.sub(r'\b(arts?)\s+\.',r'\1.',text)
    return re.sub(r'\s+([,.;:])',r'\1',text).strip()

def answer_details(q, official_keys=None):
    aps=q['appearances']; official=[]; verified=[]; basis=[]
    for a in aps:
        val=a.get('official_answer')
        if val and val not in official: official.append(str(val))
        val=a.get('verified_answer')
        if val and val not in verified: verified.append(str(val))
        for c in a.get('citations',[]) or []:
            loc=c.get('locator')
            # Exam-bank locators are editorial provenance, not part of the
            # reader-facing legal basis. Keep them in the source data and
            # render only legal/doctrinal citations on the public page.
            if loc and not re.search(r'\b(?:PDF\s+p|original gabarito|compendium|compêndio|arquivo[- ]fonte)\b', str(loc), re.I) and loc not in basis:
                basis.append(str(loc))
    key_record=(official_keys or {}).get(q.get('id'))
    if key_record:
        val=key_record.get('official_answer')
        if val and val not in official: official.append(val)
        loc=key_record.get('source_locator')
        if loc and not re.search(r'\b(?:PDF\s+p|original gabarito|compendium|compêndio|arquivo[- ]fonte)\b', str(loc), re.I) and loc not in basis:
            basis.append(loc)
    if q.get('id')=='exam-2018-2-p1-v1-q8' and 'Sim. Exame de mérito. Coisa julgada.' in official:
        official=[x for x in official if x!='Exame de mérito. Coisa julgada.']
    if q.get('id')=='exam-2018-2-p1-v1-q10':
        verified=[x for x in verified if not x.startswith('Pedido subsidiário é formulado para ser examinado apenas se o pedido principal não for acolhido')]
    if q.get('id')=='exam-2018-2-p1-v1-q9':
        verified=[re.sub(r'\s*O gabarito não fornece exemplo concreto para validação\.?$', '', x) for x in verified]
    key='; '.join(official) if official else 'Não indicado.'
    ans='; '.join(verified) if verified else 'Resposta verificada não registrada.'
    if key_record and key_record.get('status_note'):
        ans += ' ' + key_record['status_note']
    return key,ans,('; '.join(basis) if basis else 'Base normativa não discriminada.')

def render_question(q, official_keys=None):
    question=esc(q.get('verbatim_text',''))
    exams='; '.join(q['exam_labels'])
    key,ans,basis=answer_details(q,official_keys)
    return f'''<section class="bank-question" id="{esc(q['id'])}"><h4>{esc(exams)}</h4><p class="pergunta">{question}</p><details><summary>Gabarito comentado</summary><p><span class="answer-label">Gabarito oficial:</span> {esc(key)}</p><p><span class="answer-label">Resposta verificada:</span> {esc(ans)}</p><p><span class="answer-label">Base:</span> {esc(basis)}</p></details></section>'''

def render_review(page, questions, index_path, official_keys=None):
    source=page.read_text()
    # Keep the current course identity, hero, styling, and course route; replace the page's review content.
    source=source.replace('<div role="listitem">Cobertura<b>Semanas 1–9</b></div><div role="listitem">Organização<b>ordem do programa</b></div><div role="listitem">Respostas<b>gabarito comentado</b></div>', '<div role="listitem">Cobertura<span class="title-value">Semanas 1–9</span></div><div role="listitem">Organização<span class="title-value">ordem do programa</span></div><div role="listitem">Respostas<span class="title-value">gabarito comentado</span></div>')
    if '.titleblock .title-value' not in source: source=source.replace('</style>', '.topic-block .answer-label{display:inline-block;margin-right:5px;font:500 10px/1.5 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--conc)}.topic-block .frame .answer-label{display:block;margin:0 0 5px}.titleblock .title-value{display:block;font-weight:600}\n</style>', 1)
    # Offsets are taken after the edits above: computing them first shifted the splice into the hero (gate 09/10).
    start=source.index('<nav class="revisao-nav"', source.index('</header>'))
    nav_end=source.index('</nav>',start)+len('</nav>')
    intro_start=source.index('<div class="revisao-intro">',nav_end)
    intro_end=source.index('</div>',intro_start)+len('</div>')
    nav='''<nav class="revisao-nav" aria-label="Tópicos da revisão">'''+''.join(f'<a href="#{t["id"]}">{esc(t["label"])}</a>' for t in TOPICS)+'''</nav>'''
    intro='''<div class="revisao-intro"><p>Em cada questão, identifique o ato processual, localize a regra e confronte seus requisitos com os fatos narrados. Nas objetivas, teste cada alternativa pela condição legal que decide o caso; nas dissertativas, conclua antes de justificar.</p></div>'''
    blocks=[]
    for t in TOPICS:
        group=[q for q in questions if q['topic_id']==t['id']]
        statute=statute_text(index_path,t['article'])
        frames=list(dict.fromkeys(FRAMES.get(str(q.get('kind')),FRAMES['case']) for q in group))
        blocks.append(f'''<article class="topic-block" id="{t['id']}"><div class="topic-label">{esc(t['label'])}</div><h3>{esc(t['title'])}</h3><div class="fonte dec"><div class="src">Código de Processo Civil · {esc(t['article'])}</div><blockquote><p>{esc(statute)}</p></blockquote></div>{''.join(render_question(q,official_keys) for q in group)}<div class="frame"><span class="answer-label">Roteiro de resposta</span>{''.join(f'<p>{esc(f)}</p>' for f in frames)}</div></article>''')
    body='''<section class="chapter" aria-labelledby="banco-p1"><span class="num conc" aria-hidden="true">01</span><h2 id="banco-p1">Banco de questões da P1</h2><p class="lede">Semanas 1–9 · questões agrupadas pela ordem do programa</p></section>'''+''.join(blocks)
    # Existing intro goes before topic blocks. Page's existing footer scripts and route remain.
    insert=nav+'\n'+intro+'\n'+body
    # Replace from old nav through immediately before the original bottom scripts.
    scripts=source.index('<script src="../../assets/casa.js"',intro_end)
    return source[:start]+insert+'\n'+source[scripts:]

def render_cards(path, questions, official_keys=None):
    source=path.read_text()
    cards=[]
    for q in questions:
        key,ans,basis=answer_details(q,official_keys)
        lesson=q.get('lesson_id','aula-01.html')
        m=re.search(r'aula-(\d+)',lesson); aula=(m.group(1) if m else '01')
        title=q.get('topic') or q['topic_title']
        exams=q['exam_labels']
        r=f"Gabarito oficial: {key} Resposta verificada: {ans} Base: {basis}"
        cards.append({'id':q['id'],'a':aula,'t':title,'topic':title,'week':q['topic_id'],'exam':exams,'q':q.get('verbatim_text',''),'r':r,'href':lesson})
    all_json=json.dumps(cards,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    source=re.sub(r'(<script>\s*\(function\(\)\{\s*[\'\"]use strict[\'\"];var ALL=).*?(,KEY=)',lambda m:m.group(1)+all_json+m.group(2),source,count=1,flags=re.S)
    # Add source-generated controls and filtering metadata.
    source=source.replace('<span>90 perguntas das aulas</span>','<span>'+str(len(questions))+' questões da P1</span>')
    if '../../assets/casa.css' not in source:
        source=source.replace('<link rel="stylesheet" href="assets/curso.css?v=32067c15c6">','<link rel="stylesheet" href="../../assets/casa.css">\n<link rel="stylesheet" href="assets/curso.css?v=32067c15c6">')
    source=source.replace('<select id="aula" aria-label="Filtrar por aula"><option value="">Todas as aulas</option></select>', '<select id="aula" aria-label="Filtrar por aula"><option value="">Todas as aulas</option></select><select id="exam" aria-label="Filtrar por prova"><option value="">Todas as provas</option></select><select id="topic" aria-label="Filtrar por tópico"><option value="">Todos os tópicos</option></select>')
    # The replacement above contains its own match target. Collapse any pairs
    # left by earlier runs so this generator is idempotent on existing output.
    filter_pair='<select id="exam" aria-label="Filtrar por prova"><option value="">Todas as provas</option></select><select id="topic" aria-label="Filtrar por tópico"><option value="">Todos os tópicos</option></select>'
    source=re.sub(r'(?:'+re.escape(filter_pair)+r')+', filter_pair, source)
    source=source.replace("var sel=$('aula'),seen={};ALL.forEach(function(c){if(!seen[c.a]){seen[c.a]=true;var o=document.createElement('option');o.value=c.a;o.textContent='Aula '+c.a+' · '+c.t;sel.appendChild(o)}});", "var sel=$('aula'),seen={},examSel=$('exam'),topicSel=$('topic'),examFilter='',topicFilter='';ALL.forEach(function(c){if(!seen[c.a]){seen[c.a]=true;var o=document.createElement('option');o.value=c.a;o.textContent='Aula '+c.a+' · '+c.t;sel.appendChild(o)}});var seenExam={},seenTopic={};ALL.forEach(function(c){(c.exam||[]).forEach(function(e){if(!seenExam[e]){seenExam[e]=true;var o=document.createElement('option');o.value=e;o.textContent=e;examSel.appendChild(o)}});if(!seenTopic[c.topic]){seenTopic[c.topic]=true;var t=document.createElement('option');t.value=c.topic;t.textContent=c.t;topicSel.appendChild(t)}});")
    source=source.replace("var aula='',queue=[]", "var aula='',queue=[]")
    source=source.replace("function pool(){return ALL.filter(function(c){return !aula||c.a===aula})}", "function pool(){return ALL.filter(function(c){return (!aula||c.a===aula)&&(!examFilter||(c.exam||[]).indexOf(examFilter)>=0)&&(!topicFilter||c.topic===topicFilter)})}")
    source=source.replace("document.createTextNode(' · '+cur.t)", "document.createTextNode(' · '+cur.t+' · '+(cur.exam||[]).join('; '))")
    source=source.replace("sel.onchange=function(){aula=sel.value;build()};", "sel.onchange=function(){aula=sel.value;build()};examSel.onchange=function(){examFilter=examSel.value;build()};topicSel.onchange=function(){topicFilter=topicSel.value;build()};")
    handler_pair="examSel.onchange=function(){examFilter=examSel.value;build()};topicSel.onchange=function(){topicFilter=topicSel.value;build()};"
    source=re.sub(r'(?:'+re.escape(handler_pair)+r')+', handler_pair, source)
    # Add the shared behavior script while keeping the existing theme control.
    if '../../assets/casa.js' not in source:
        source=source.replace('<script src="../../assets/offline.js" defer></script>', '<script src="../../assets/casa.js" defer></script>\n<script src="../../assets/offline.js" defer></script>')
    path.write_text(source)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--bank',type=Path,default=BANK_DEFAULT); ap.add_argument('--cpc-index',type=Path,default=CPC_INDEX_DEFAULT); ap.add_argument('--official-keys',type=Path,default=OFFICIAL_KEY_DEFAULT); ap.add_argument('--site',type=Path,default=ROOT); args=ap.parse_args()
    bank=json.loads(args.bank.read_text())
    official_keys=json.loads(args.official_keys.read_text()).get('answers',{}) if args.official_keys.is_file() else {}
    records=[q for row in bank['questions'] if (q:=get_question_record(row))]
    if len(records)!=55:
        raise SystemExit(f'Expected 55 verified P1 bank records after excluding candidate-stage items; got {len(records)}. No output written.')
    review=args.site/'courses/processo-civil-i/revisao-p1.html'; cards=args.site/'courses/processo-civil-i/cartoes.html'
    review.write_text(render_review(review,records,args.cpc_index,official_keys))
    render_cards(cards,records,official_keys)
    print(f'Generated {len(records)} P1 records; source exclusions preserved: {len(bank.get("excluded",[]))}; outputs: {review}, {cards}')
if __name__=='__main__': main()
