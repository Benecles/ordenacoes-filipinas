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
    [['the line', ''], ['factory', 'workshop.html'], ['rules', 'rules.html']],
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
  const FILTERS = { 'pairs.html': 'pairs', 'archive.html': 'archive' };
  const page = here.slice(root.length);                       // '' | 'pairs.html' | 'processo-civil-i/' …
  const twin = COURSES.find(([s]) => page === s + '/');
  const view = FILTERS[page];
  let scope = twin ? twin[0] : new URLSearchParams(location.search).get('c');
  if (!COURSES.some(([s]) => s === scope)) scope = null;
  const q = s => (s ? '?c=' + s : '');

  const css = `
.bsbar { position: relative; z-index: 50; border-bottom: 1px solid var(--rule);
  font: 500 11px/1.4 var(--mono, "IBM Plex Mono", Menlo, monospace); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.bsbar .in { max-width: 1240px; margin: 0 auto; padding: 14px 30px; display: flex; align-items: center; gap: 0; }
.bsbar a { white-space: nowrap; color: var(--ink-2); text-decoration: none; padding: 4px 0; border-bottom: 1.5px solid transparent; transition: color .15s, border-color .15s; }
.bsbar a:hover { color: var(--ink); }
.bsbar a.on { color: var(--dif); border-bottom-color: var(--dif); }
.bsbar .mark { color: var(--ink); letter-spacing: .16em; margin-right: 18px; }
.bsbar .bsg { display: inline-flex; gap: 12px; padding: 0 13px; border-left: 1px solid var(--rule); }
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
  bar.innerHTML = `<div class="in"><a class="mark" href="${rel('')}">Backstage</a>${groups}<span class="right"><details><summary${sc ? ' class="on"' : ''}>${sc ? sc[1] : 'courses'}</summary><div class="menu">${courses}${sub}</div></details><a href="${root}../index.html">reader site ↗</a></span></div>`;
  document.body.prepend(bar);
  const dt = bar.querySelector('details');
  document.addEventListener('click', e => { if (!dt.contains(e.target)) dt.open = false; });

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
