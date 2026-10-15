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
    [['the line', ''], ['generations', 'generations.html'], ['factory', 'workshop.html'], ['rules', 'rules.html']],
    [['dictionary', 'dictionary.html'], ['figures', 'figures.html'], ['references', 'references.html']],
    [['archive', 'archive.html'], ['before / after', 'pairs.html'], ['log', 'log/2026-10-15.html']],
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
  const GENS = [['everglades', '1 Everglades', '#8fd694'], ['shenandoah', '2 Shenandoah', '#b4b0ff'], ['arches', '3 Arches', '#ff9ad5'], ['grand-canyon', '4 Grand Canyon', '#4fd8c4']];
  const FILTERS = { 'pairs.html': 'pairs', 'archive.html': 'archive' };
  const page = here.slice(root.length);                       // '' | 'pairs.html' | 'processo-civil-i/' …
  const twin = COURSES.find(([s]) => page === s + '/');
  const view = FILTERS[page];
  let scope = twin ? twin[0] : new URLSearchParams(location.search).get('c');
  if (!COURSES.some(([s]) => s === scope)) scope = null;
  const q = s => (s ? '?c=' + s : '');

  const css = `
.bsbar { position: relative; z-index: 50; border-bottom: 1px solid var(--rule);
  font: 500 11px/1.4 var(--mono, "IBM Plex Mono", Menlo, monospace); letter-spacing: .04em; text-transform: uppercase; color: var(--muted); }
.bsbar .in { max-width: 1240px; margin: 0 auto; padding: 14px 30px; display: flex; align-items: center; gap: 0; }
.bsbar a { white-space: nowrap; color: var(--ink-2); text-decoration: none; padding: 4px 0; border-bottom: 1.5px solid transparent; transition: color .15s, border-color .15s; }
.bsbar a:hover { color: var(--ink); }
.bsbar a.on { color: var(--dif); border-bottom-color: var(--dif); }
.bsbar .mark { color: var(--ink); letter-spacing: .16em; margin-right: 18px; }
.bsbar .bsg { display: inline-flex; gap: 11px; padding: 0 11px; border-left: 1px solid var(--rule); }
.bsbar .bsg:first-of-type { border-left: 0; padding-left: 0; }
.bsbar .right { margin-left: auto; display: inline-flex; align-items: center; gap: 16px; white-space: nowrap; }
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
.bsbar .lens { display: inline-flex; gap: 5px; align-items: flex-end; padding-right: 4px; }
.bsbar .lens button { all: unset; cursor: pointer; width: 9px; height: 16px; background: var(--c); opacity: .85; transition: height .15s, opacity .15s; }
.bsbar .lens button:hover { opacity: 1; height: 20px; }
.bsbar .lens button.on { height: 22px; opacity: 1; box-shadow: 0 2px 0 var(--ink); }
body[data-lens] [data-gens] { transition: opacity .25s; }
body[data-lens="everglades"] [data-gens]:not([data-gens~="everglades"]),
body[data-lens="shenandoah"] [data-gens]:not([data-gens~="shenandoah"]),
body[data-lens="arches"] [data-gens]:not([data-gens~="arches"]),
body[data-lens="grand-canyon"] [data-gens]:not([data-gens~="grand-canyon"]),
body[data-lens="everglades"] .c:not(.g1), body[data-lens="shenandoah"] .c:not(.g2), body[data-lens="arches"] .c:not(.g3), body[data-lens="grand-canyon"] .c:not(.g4) { opacity: .12; }
.bstip { position: fixed; z-index: 90; pointer-events: none; width: max-content; max-width: 360px; padding: 9px 12px; background: var(--mat-2); border: 1px solid var(--rule);
  box-shadow: 0 16px 34px -18px rgba(0,0,0,.7); font: 400 13px/1.45 var(--mono, monospace); color: var(--ink-2); white-space: pre-line; opacity: 0; transition: opacity .12s; }
.bstip::first-line { color: var(--ink); font-family: var(--body, serif); font-size: 15px; }
.bstip.on { opacity: 1; }
@media print { .bsbar { display: none; } }`;
  document.head.insertAdjacentHTML('beforeend', `<style>${css}</style>`);

  const on = p => (page === p ? ' class="on"' : '');
  const groups = GROUPS.map(items => `<span class="bsg">${items.map(([t, p]) =>
    `<a href="${rel(p)}${FILTERS[p] ? q(scope) : ''}"${on(p)}>${t}</a>`).join('')}</span>`).join('');
  const sc = scope && COURSES.find(([s]) => s === scope);
  const courses = COURSES.map(([s, short]) => {
    const href = view ? `${rel(page)}${q(s)}` : rel(s + '/');
    return `<a href="${href}"${s === scope ? ' class="on"' : ''}>${short}</a>`;
  }).join('');
  const sub = sc ? `<hr>${twin ? '' : `<a class="sub" href="${rel(sc[0] + '/')}">${sc[1]} · twin</a>`}${view === 'archive' ? '' : `<a class="sub" href="${rel('archive.html')}?c=${sc[0]}">${sc[1]} · figures</a>`}${view === 'pairs' ? '' : `<a class="sub" href="${rel('pairs.html')}?c=${sc[0]}">${sc[1]} · before / after</a>`}<a class="sub" href="${root}../courses/${sc[0]}/index.html">${sc[1]} · on the site ↗</a>${view ? `<a href="${rel(page)}">all courses</a>` : ''}` : '';
  const bar = document.createElement('nav');
  bar.className = 'bsbar';
  bar.innerHTML = `<div class="in"><a class="mark" href="${rel('')}">Backstage</a>${groups}<span class="right"><span class="lens">${GENS.map(([g, n, c]) => `<button data-g="${g}" style="--c:${c}" title="${n}" aria-label="${n}"></button>`).join('')}</span><details><summary${sc ? ' class="on"' : ''}>${sc ? sc[1] : 'courses'}</summary><div class="menu">${courses}${sub}</div></details><a href="${root}../index.html">site ↗</a></span></div>`;
  document.body.prepend(bar);
  const dt = bar.querySelector('details');
  document.addEventListener('click', e => { if (!dt.contains(e.target)) dt.open = false; });

  // the pencil lens: one generation lit, the rest fade (kept in the URL hash as lens=…)
  const setLens = g => { if (g) document.body.dataset.lens = g; else delete document.body.dataset.lens;
    bar.querySelectorAll('.lens button').forEach(b => b.classList.toggle('on', b.dataset.g === g)); };
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
    const spine = d => { const sp = document.createElement('span'); sp.className = 'bsspine'; sp.style.setProperty('--p', LED.pencil[d.g]);
      sp.innerHTML = d.tape.map(([g, n]) => `<i style="background:${LED.pencil[g]};height:${Math.min(2 + n, 6)}px"></i>`).join('') + (d.frm ? `<u style="background:${LED.pencil[d.frm]}"></u>` : '');
      return sp; };
    for (const el of document.querySelectorAll('.strip, article.card, a.tile, a.pair')) {
      if (el.closest('.bsbar') || el.dataset.gens) continue;
      const a = el.matches('a') ? el : el.querySelector('a[href*="courses/"]'); if (!a) continue;
      const m = a.href.match(/courses\/[^?#]+\.html/); const d = m && LED.lessons[m[0]]; if (!d) continue;
      const gn = el.querySelector('.gn');
      if (gn) {   // an archive tile names the generation that drew the figure: that one wins
        const own = GENS.find(([, n]) => gn.textContent.trim() === n);
        if (own) { el.dataset.gens = own[0]; gn.style.color = own[2]; }
        continue;
      }
      el.dataset.gens = d.gs.join(' '); el.dataset.tip = d.t;
      (el.querySelector('.who, header, .lbl') || el).prepend(spine(d));
    }
  }

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
