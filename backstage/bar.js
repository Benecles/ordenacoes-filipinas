// Backstage bar: one navigation for every backstage page, plus a course scope that travels with you.
// Source: workshop work/backstage/bar.js, copied and wired into every page by weave.py; edit there.
// The course menu shows a course in the current view: Before/after and Archive filter in place (?c=slug);
// every other page goes to the course's twin. Section links carry the scope.
(() => {
  const me = document.currentScript.src;
  const root = me.slice(0, me.lastIndexOf('/') + 1);          // …/backstage/
  const here = location.href.split(/[?#]/)[0].replace(/index\.html$/, '');
  const rel = p => root + p;
  const GROUPS = [
    [['the line', 'line.html'], ['generations', 'generations.html'], ['factory', 'workshop.html'], ['rules', 'rules.html']],
    [['dictionary', 'dictionary.html'], ['figures', 'figures.html'], ['references', 'references.html']],
    [['archive', 'archive.html'], ['before / after', 'pairs.html'], ['blog', 'blog/']],
    [['themes', 'themes/'], ['variations', 'variations/']],
  ];
  const COURSES = [
    ['controle-de-constitucionalidade', 'Controle', 'Controle de Constitucionalidade'],
    ['direito-constitucional-i', 'Constitucional I', 'Direito Constitucional I'],
    ['direito-latino-americano', 'Latam', 'Direito Latino-americano'],
    ['metodologia-juridica', 'Metodologia', 'Metodologia Jurídica'],
    ['processo-civil-i', 'Processo', 'Processo Civil I'],
    ['teoria-geral-dos-contratos', 'Contratos', 'Teoria Geral dos Contratos'],
    ['teoria-do-delito', 'Delito', 'Teoria do Delito'],
  ];
  const GENS = [['everglades', '1 Everglades', '#3fd47e'], ['sequoia', '2 Sequoia', '#9a86ff'], ['yosemite', '3 Yosemite', '#e8a03a'], ['grand-canyon', '4 Grand Canyon', '#25cbd0']];
  const FILTERS = { 'pairs.html': 'pairs', 'archive.html': 'archive' };
  const page = here.slice(root.length);                       // '' | 'pairs.html' | 'processo-civil-i/' …
  const twin = COURSES.find(([s]) => page === s + '/' || page === 'courses/' + s + '/');
  const view = FILTERS[page];
  let scope = twin ? twin[0] : new URLSearchParams(location.search).get('c');
  if (!COURSES.some(([s]) => s === scope)) scope = null;
  const q = s => (s ? '?c=' + s : '');

  const css = `
.bsbar { position: relative; z-index: 50; border-bottom: 1px solid var(--rule);
  font: 500 11px/1.4 var(--mono, "IBM Plex Mono", Menlo, monospace); letter-spacing: .03em; text-transform: uppercase; color: var(--muted); }
.bsbar .in { max-width: 1240px; margin: 0 auto; padding: 14px 30px; display: flex; align-items: center; gap: 0; }
.bsbar a { white-space: nowrap; color: var(--ink-2); text-decoration: none; padding: 4px 0; border-bottom: 1.5px solid transparent; transition: color .15s, border-color .15s; }
.bsbar a:hover { color: var(--ink); }
.bsbar a.on { color: var(--dif); border-bottom-color: var(--dif); }
.bsbar .mark { color: var(--ink); letter-spacing: .16em; margin-right: 18px; display: inline-flex; align-items: center; gap: 9px; }
.bsbar .minib { all: unset; cursor: pointer; margin-right: 10px; display: inline-flex; padding: 3px; border-radius: 2px; transition: transform .15s; } .bsbar .minib:hover { transform: scale(1.12); } .bsbar .minib.open .mini .out { stroke-width: 1.8; }
.bsworks { position: relative; z-index: 49; max-width: 1180px; margin: 0 auto; padding: 4px 30px 18px; border-bottom: 1px solid var(--rule); background: var(--mat); animation: bsunfold .25s cubic-bezier(.2,.8,.2,1); transform-origin: top left; }
@keyframes bsunfold { from { opacity: 0; transform: scaleY(.6); } }
.bsbar .mini { height: 24px; width: auto; overflow: visible; } .bsbar .mini rect { fill: none; stroke: var(--ink-2); stroke-width: .5; } .bsbar .mini .out { stroke: var(--ink); stroke-width: 1; }
.bsbar .mini rect.here { fill: var(--ink); stroke: var(--ink); } .bsbar .mark:hover .mini rect { stroke: var(--ink); }
.bsbar .bsg { display: inline-flex; gap: 9px; padding: 0 9px; border-left: 1px solid var(--rule); }
.bsbar .bsg:first-of-type { border-left: 0; padding-left: 0; }
.bsbar .right { margin-left: auto; padding-left: 10px; display: inline-flex; align-items: center; gap: 11px; white-space: nowrap; }
.bsbar details { position: relative; }
.bsbar summary { list-style: none; cursor: pointer; color: var(--ink-2); padding: 4px 0; border-bottom: 1.5px solid transparent; }
.bsbar summary::-webkit-details-marker { display: none; }
.bsbar summary::after { content: " ▾"; color: var(--muted); }
.bsbar summary:hover { color: var(--ink); }
.bsbar summary.on { color: var(--dif); border-bottom-color: var(--dif); }
.bsbar .menu { position: absolute; right: 0; top: calc(100% + 10px); min-width: 250px; padding: 10px 0; background: var(--mat-2); border: 1px solid var(--rule);
  display: grid; box-shadow: 0 18px 40px -20px rgba(0,0,0,.6); }
.bsbar .menu a { padding: 6px 16px; border: 0; }
.bsbar .menu a:hover { background: rgba(243,246,251,.06); }
.bsbar .menu a.on { color: var(--dif); }
.bsbar .menu hr { border: 0; border-top: 1px solid var(--rule); margin: 8px 0; }
.bsbar .menu .sub { color: var(--dif); }
.bs-hide { display: none !important; }
.bsspine { display: inline-flex; flex-direction: column; width: 7px; height: 18px; background: var(--p); margin-right: 8px; vertical-align: -3px; position: relative; flex: none; }
.bsspine i { display: block; box-shadow: 0 1px 0 var(--mat); } .bsspine u { position: absolute; left: 0; right: 0; bottom: 0; height: 3px; }
.bsbar .lens { display: inline-flex; gap: 3px; align-items: flex-end; height: 24px; }
.bsbar .lens button { all: unset; cursor: pointer; width: 10px; height: 26px; transform: translateY(4px); transition: transform .18s cubic-bezier(.3,1.5,.5,1); }
.bsbar .lens svg { width: 10px; height: 26px; display: block; overflow: visible; }
.bsbar .lens .pb, .bsbar .lens .pt { fill: var(--mat); stroke: var(--ink-2); stroke-width: 1; } .bsbar .lens .pl { fill: var(--c); }
.bsbar .lens button:hover { transform: translateY(0); } .bsbar .lens button.on { transform: translateY(-6px) rotate(-12deg); }
.bsbar .lens button.on .pb, .bsbar .lens button.on .pt { stroke: var(--c); }
.bsbar .lensname { margin-left: 8px; color: var(--ink); cursor: pointer; white-space: nowrap; } .bsbar .lensname:empty { display: none; }
body[data-lens] [data-gens] { transition: opacity .25s; }
.bstip { position: fixed; z-index: 90; pointer-events: none; width: max-content; max-width: 360px; padding: 9px 12px; background: var(--mat-2); border: 1px solid var(--rule);
  box-shadow: 0 16px 34px -18px rgba(0,0,0,.7); font: 400 13px/1.45 var(--mono, monospace); color: var(--ink-2); white-space: pre-line; opacity: 0; transition: opacity .12s; }
.bstip::first-line { color: var(--ink); font-family: var(--body, serif); font-size: 15px; }
.bstip.on { opacity: 1; }

/* objects behave like what they are */
.survey .blade { transform-box: fill-box; transform-origin: 50% 100%; transition: transform .5s cubic-bezier(.3,1.6,.5,1), stroke-width .15s; }
.survey a:hover .blade { transform: rotate(5deg); }
.survey .river { stroke-dasharray: 9 6; animation: bsflow 2.6s linear infinite; cursor: pointer; }   /* justified loop: Grand Canyon is the generation still running */
@keyframes bsflow { to { stroke-dashoffset: -30; } }
.survey .stone { transition: fill .15s, stroke-width .2s; } .survey .stone.lit { fill: var(--gen-yosemite, #ff9ad5); }
.survey .tk.lit { stroke-width: 5; }
.board a { transition: transform .9s cubic-bezier(.5,0,.2,1); }
@media (prefers-reduced-motion: reduce) { .survey .river { animation: none; } .board a, .survey .blade { transition: none; } }
.eye path, .eye circle { transform-box: fill-box; transform-origin: center; transition: transform .07s; } .eye.blink path, .eye.blink circle { transform: scaleY(.08); }
@media print { .bsbar { display: none; } }`;
  document.head.insertAdjacentHTML('beforeend', `<style>${css}</style>`);

  const on = p => (page === p ? ' class="on"' : '');
  const groups = GROUPS.map(items => `<span class="bsg">${items.map(([t, p]) =>
    `<a href="${rel(p)}${FILTERS[p] ? q(scope) : ''}"${on(p)}>${t}</a>`).join('')}</span>`).join('');
  const sc = scope && COURSES.find(([s]) => s === scope);
  const courses = COURSES.map(([s, short]) => {
    const href = view ? `${rel(page)}${q(s)}` : rel('courses/' + s + '/');
    return `<a href="${href}"${s === scope ? ' class="on"' : ''}>${short}</a>`;
  }).join('');
  const sub = sc ? `<hr>${twin ? '' : `<a class="sub" href="${rel('courses/' + sc[0] + '/')}">${sc[1]} · turned over</a>`}${view === 'archive' ? '' : `<a class="sub" href="${rel('archive.html')}?c=${sc[0]}">${sc[1]} · figures</a>`}${view === 'pairs' ? '' : `<a class="sub" href="${rel('pairs.html')}?c=${sc[0]}">${sc[1]} · before / after</a>`}<a class="sub" href="${root}../courses/${sc[0]}/index.html">${sc[1]} · on the site ↗</a>${view ? `<a href="${rel(page)}">all courses</a>` : ''}` : '';
  const bar = document.createElement('nav');
  bar.className = 'bsbar';
  bar.innerHTML = `<div class="in"><a class="mark${page === '' ? ' on' : ''}" href="${rel('')}">Backstage</a>${groups}<span class="right"><span class="lens">${GENS.map(([g, n, c]) => `<button data-g="${g}" style="--c:${c}" data-tip="${n} · pick up its pencil: its work lights up" aria-label="${n}"><svg viewBox="0 0 10 30"><path d="M2 8 V27 H8 V8 Z" class="pb"/><path d="M2 8 L5 1 L8 8" class="pt"/><path d="M4.1 3.6 L5 1 L5.9 3.6 Z" class="pl"/></svg></button>`).join('')}<span class="lensname"></span></span><details><summary${sc ? ' class="on"' : ''}>${sc ? sc[1] : 'courses'}</summary><div class="menu">${courses}${sub}</div></details><a class="foh" href="${root}../index.html" data-tip="the reader's side · this sheet's own front: the folded corner, or ⌘⇧K">front of house</a></span></div>`;
  document.body.prepend(bar);
  const dt = bar.querySelector('details');
  document.addEventListener('click', e => { if (!dt.contains(e.target)) dt.open = false; });

  // the pencil lens: one generation lit, the rest fade (kept in the URL hash as lens=…)
  const setLens = g => { if (g) document.body.dataset.lens = g; else delete document.body.dataset.lens;
    bar.querySelectorAll('.lens button').forEach(b => b.classList.toggle('on', b.dataset.g === g));
    const gn = GENS.find(x => x[0] === g); bar.querySelector('.lensname').textContent = gn ? gn[1] + ' ×' : ''; };
  bar.querySelector('.lensname').addEventListener('click', () => setLens(null));
  // the pencils only where there is something they can light
  if (!document.querySelector('[data-gens], .c.g1, .c.g2, .c.g3, .c.g4')) bar.querySelector('.lens').style.display = 'none';
  // the drafting hatches as SVG patterns, for any drawing on the page (fill: url(#bp-h-<gen>))
  document.body.insertAdjacentHTML('afterbegin', `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
    <pattern id="bp-h-everglades" width="12" height="8" patternUnits="userSpaceOnUse"><rect width="12" height="8" fill="#15386a"/><path d="M0 5 q3 -3 6 0 t6 0" fill="none" stroke="#f3f6fb" stroke-width="1" opacity=".75"/></pattern>
    <pattern id="bp-h-sequoia" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#15386a"/><path d="M3 0 q2 3 0 6" stroke="#f3f6fb" stroke-width="1" opacity=".75"/></pattern>
    <pattern id="bp-h-yosemite" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="#15386a"/><circle cx="2.5" cy="2.5" r=".9" fill="#f3f6fb" opacity=".85"/></pattern>
    <pattern id="bp-h-grand-canyon" width="10" height="5" patternUnits="userSpaceOnUse"><rect width="10" height="5" fill="#15386a"/><path d="M0 2.5 H6" stroke="#f3f6fb" stroke-width="1" opacity=".8"/></pattern>
    <pattern id="bp-h-everglades-lit" width="12" height="8" patternUnits="userSpaceOnUse"><rect width="12" height="8" fill="#15386a"/><path d="M0 5 q3 -3 6 0 t6 0" fill="none" stroke="#3fd47e" stroke-width="1.3"/></pattern>
    <pattern id="bp-h-sequoia-lit" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#15386a"/><path d="M3 0 q2 3 0 6" stroke="#9a86ff" stroke-width="1.3"/></pattern>
    <pattern id="bp-h-yosemite-lit" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="#15386a"/><circle cx="2.5" cy="2.5" r="1.1" fill="#e8a03a"/></pattern>
    <pattern id="bp-h-grand-canyon-lit" width="10" height="5" patternUnits="userSpaceOnUse"><rect width="10" height="5" fill="#15386a"/><path d="M0 2.5 H6" stroke="#25cbd0" stroke-width="1.3"/></pattern>
    </defs></svg>`);
  bar.querySelector('.lens').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
    setLens(document.body.dataset.lens === b.dataset.g ? null : b.dataset.g); });
  // hover cards for anything carrying data-tip
  const tip = document.createElement('div'); tip.className = 'bstip'; document.body.appendChild(tip);
  document.addEventListener('pointerover', e => { const t = e.target.closest('[data-tip]'); if (!t) return; tip.textContent = t.dataset.tip; tip.classList.add('on'); });
  document.addEventListener('pointerout', e => { if (e.target.closest('[data-tip]')) tip.classList.remove('on'); });
  document.addEventListener('pointermove', e => { if (!tip.classList.contains('on')) return;
    const x = Math.min(e.clientX + 16, innerWidth - tip.offsetWidth - 10), y = e.clientY + 18 + tip.offsetHeight > innerHeight ? e.clientY - tip.offsetHeight - 12 : e.clientY + 18;
    tip.style.left = x + 'px'; tip.style.top = y + 'px'; });

  // every card, strip or tile that links to a lesson gets that lesson's spine and joins the lens
  const LED = window.BS_LESSONS;
  if (LED) {
    const spine = d => { const sp = document.createElement('span'); sp.className = 'bsspine'; sp.dataset.g = d.g;
      sp.innerHTML = d.tape.map(([g, n]) => `<i style="background:${LED.pencil[g]};height:${Math.min(2 + n, 6)}px"></i>`).join('') + (d.frm ? `<u style="background:${LED.pencil[d.frm]}"></u>` : '');
      return sp; };
    for (const el of document.querySelectorAll('.strip, article.card, a.tile, a.pair, a.reg-row')) {
      if (el.closest('.bsbar') || el.dataset.gens) continue;
      const a = el.matches('a') ? el : el.querySelector('a[href*="courses/"]'); if (!a) continue;
      const m = a.href.match(/courses\/[^?#]+\.html/); const d = m && LED.lessons[m[0]]; if (!d) continue;
      const gn = el.querySelector('.gn');
      if (gn) {   // an archive tile names the generation that drew the figure: that one wins
        const own = GENS.find(([, n]) => gn.textContent.trim() === n);
        if (own) { el.dataset.gens = own[0]; }
        continue;
      }
      el.dataset.gens = d.gs.join(' '); el.dataset.tip = d.t;
      (el.querySelector('.reg-n, .who, header, .lbl') || el).prepend(spine(d));
    }
  }

  // eyes look at the pointer and blink when clicked (the verb "look", Interaction Dictionary; chairman 15/10: keep, more of that ilk)
  const eyes = [...document.querySelectorAll('svg .eye')].map(g => { const c = g.querySelector('circle'); return c && { g, c, x: +c.getAttribute('cx'), y: +c.getAttribute('cy') }; }).filter(Boolean);
  if (eyes.length) {
    document.addEventListener('pointermove', e => eyes.forEach(o => {
      const m = o.c.ownerSVGElement.getScreenCTM(); if (!m) return;
      const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse()); const dx = p.x - o.x, dy = p.y - o.y, d = Math.hypot(dx, dy) || 1;
      o.c.setAttribute('cx', (o.x + dx / d * Math.min(4.5, d / 40)).toFixed(1)); o.c.setAttribute('cy', (o.y + dy / d * Math.min(2.6, d / 60)).toFixed(1)); }));
    eyes.forEach(o => { o.g.style.cursor = 'pointer'; o.g.addEventListener('click', () => { o.g.classList.add('blink'); setTimeout(() => o.g.classList.remove('blink'), 140); }); });
    const blink = () => { const o = eyes[Math.floor(Math.random() * eyes.length)]; o.g.classList.add('blink'); setTimeout(() => o.g.classList.remove('blink'), 140); setTimeout(blink, 3000 + Math.random() * 5000); };
    setTimeout(blink, 2500);   // justified idle: readers who are awake blink
  }

  // you are here: the planta in miniature beside the mark, the room you stand in filled
  const JOB = (() => { const m = page.match(/^courses\/([^/]+)\//); if (m) return m[1]; const t = COURSES.find(([s]) => page === s + '/'); return t ? t[0] : null; })();
  let ROOM = (() => {
    const map = { 'line.html': 'press', 'workshop.html': 'press', 'rules.html': 'reading', 'dictionary.html': 'reading', 'references.html': 'reading',
      'figures.html': 'gallery', 'pairs.html': 'gallery', 'archive.html': 'plates', 'planta.html': 'desk', '': 'desk' };
    if (map[page] !== undefined) return map[page];
    if (/^generations/.test(page)) return 'founding';
    if (/^(themes|variations)\//.test(page)) return 'studio';
    if (/^(log|blog)\//.test(page)) return 'desk';
    return null;
  })();
  fetch(rel('planta.json')).then(r => r.json()).then(P => {
    if (JOB && P.jobs) ROOM = P.jobs[JOB];      // a course's pages stand where its job stands in the works
    const [ox, oy, ow, oh] = P.outer || [60, 40, 1060, 620], k = 30 / oh;
    const rooms = P.rooms.map(([id, , , x, y, w, h]) =>
      `<rect x="${((x - ox) * k).toFixed(1)}" y="${((y - oy) * k).toFixed(1)}" width="${(w * k).toFixed(1)}" height="${(h * k).toFixed(1)}" class="${id === ROOM ? 'here' : ''}"/>`).join('');
    const btn = document.createElement('button'); btn.className = 'minib'; btn.setAttribute('aria-label', 'the works, unfolded');
    btn.innerHTML = `<svg class="mini" viewBox="-1 -1 ${(ow * k + 2).toFixed(1)} 32" aria-hidden="true"><rect x="0" y="0" width="${(ow * k).toFixed(1)}" height="30" class="out"/>${rooms}</svg>`;
    const mk = bar.querySelector('.mark'); mk.before(btn);
    const here = P.rooms.find(r => r[0] === ROOM); btn.dataset.tip = (here ? 'you are here · ' + here[1] + '\n' : '') + 'click: the works, unfolded';
    // click the mini plan: the whole works unfolds under the bar (the real planta, fetched; its rooms are doors)
    let panel = null;
    btn.addEventListener('click', e => {
      e.stopPropagation();
      if (panel) { panel.remove(); panel = null; btn.classList.remove('open'); return; }
      fetch(rel('planta.html')).then(r => r.text()).then(t => {
        const m = t.match(/<svg viewBox="0 0 1180 \d+" class="planta"[\s\S]*?<\/svg>(?=\s*<\/main>)/), css = t.match(/<style>\s*\.planta[\s\S]*?<\/style>/);
        if (!m) return;
        panel = document.createElement('div'); panel.className = 'bsworks';
        panel.innerHTML = (css ? css[0] : '') + m[0].replace(/href="(?!https?:|#|\.\.\/index)([^"]*)"/g, (q, h) => `href="${rel(h)}"`).replace(/href="\.\.\/index\.html"/g, `href="${root}../index.html"`)
          .replace(/<use href="[^"]*generations\.svg#/g, `<use href="${rel('generations.svg')}#`);
        bar.after(panel); btn.classList.add('open');
        const cur = panel.querySelector(`.room[data-room="${ROOM}"] .floor`); if (cur) cur.style.fill = 'rgba(243,246,251,.16)';
        const job = JOB && panel.querySelector(`a.job[data-job="${JOB}"] .ticket`); if (job) { job.style.strokeWidth = 3; job.style.fill = 'rgba(243,246,251,.22)'; }
      });
    });
    document.addEventListener('click', e => { if (panel && !panel.contains(e.target)) { panel.remove(); panel = null; btn.classList.remove('open'); } });
  }).catch(() => {});

  // ── three easter eggs ─────────────────────────────────────────────────────────────────────────────────────
  // 1 · type "swap" on the front door: every Processo lesson rides the line to your site, then comes back
  let typed = '';
  document.addEventListener('keydown', e => {
    if (e.target.closest('input, textarea')) return;
    typed = (typed + e.key.toLowerCase()).slice(-4);
    const board = document.querySelector('svg.board'); if (typed !== 'swap' || !board) return;
    const stns = board.querySelectorAll('circle.stn'); const end = stns[stns.length - 1];
    const k = board.getBoundingClientRect().width / board.viewBox.baseVal.width;
    board.querySelectorAll('a').forEach((a, i) => {
      const r = a.querySelector('rect'); const dx = (+end.getAttribute('cx') - 14 - +r.getAttribute('x')) * k, dy = (+end.getAttribute('cy') - 20 - +r.getAttribute('y')) * k;
      setTimeout(() => { a.style.transform = `translate(${dx}px, ${dy}px)`; }, i * 60);
      setTimeout(() => { a.style.transform = ''; }, 2600 + i * 40);
    });
  });
  // 2 · click "N stones" under the arch: the arch is laid again, stone by stone, in build order
  document.querySelectorAll('.survey text').forEach(t => {
    if (!/stones$/.test(t.textContent)) return;
    t.style.cursor = 'pointer';
    t.addEventListener('click', () => t.closest('svg').querySelectorAll('.stone').forEach((st, i) => {
      setTimeout(() => st.classList.add('lit'), i * 70); setTimeout(() => st.classList.remove('lit'), 900 + i * 70); }));
  });
  // 3 · click the river: a pulse climbs the canyon wall, touching every older lesson Grand Canyon reached
  document.querySelectorAll('.survey .riverhit').forEach(rv => rv.addEventListener('click', e => {
    e.preventDefault(); e.stopPropagation();
    const ticks = [...rv.closest('svg').querySelectorAll('.tk')].sort((a, b) => +b.getAttribute('y1') - +a.getAttribute('y1'));
    ticks.forEach((t, i) => { setTimeout(() => t.classList.add('lit'), i * 25); setTimeout(() => t.classList.remove('lit'), 500 + i * 25); });
  }));

  // the old crumbs keep their page facts (dates, counts); the bar now carries the way home
  const cr = document.querySelector('.crumbs, .eyebrow');
  if (cr) {
    const a = cr.querySelector('a');
    if (a && /^(← )?(Backstage|Ordenações Filipinas)$/i.test(a.textContent.trim())) {
      const nx = a.nextSibling; a.remove();
      if (nx && nx.nodeType === 3) nx.textContent = nx.textContent.replace(/^\s*·\s*/, '');
      if (!cr.textContent.trim()) cr.remove();
    }
  }

  // filter in place
  if (scope && view === 'pairs') {
    document.querySelectorAll('article.card').forEach(c => {
      const a = c.querySelector('header a');
      if (!a || !a.getAttribute('href').includes('/' + scope + '/')) c.classList.add('bs-hide');
    });
  }
  if (scope && view === 'archive') {
    const name = sc[2];
    document.querySelectorAll('main section').forEach(s => {
      const h = s.querySelector('h2');
      if (h && !h.textContent.trim().startsWith(name)) s.classList.add('bs-hide');
    });
  }
})();
