// Backstage bar: one navigation for every backstage page, plus a course scope that travels with you.
// Source: workshop work/backstage/bar.js, copied and wired into every page by weave.py; edit there.
// A course chip shows that course in the current view: Before/after and Archive filter in place (?c=slug);
// every other page goes to the course's twin. Section links carry the scope.
(() => {
  const me = document.currentScript.src;
  const root = me.slice(0, me.lastIndexOf('/') + 1);          // …/backstage/
  const here = location.href.split(/[?#]/)[0].replace(/index\.html$/, '');
  const rel = p => root + p;
  const GROUPS = [
    ['process', [['the line', ''], ['factory', 'workshop.html'], ['generations', 'generations.html'], ['rules', 'rules.html']]],
    ['house', [['dictionary', 'dictionary.html'], ['figures', 'figures.html'], ['references', 'references.html']]],
    ['work', [['archive', 'archive.html'], ['before / after', 'pairs.html'], ['log', 'log/2026-10-15.html']]],
    ['studies', [['themes', 'themes/'], ['variations', 'variations/']]],
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
.bsbar { position: relative; z-index: 50; background: var(--mat, #1d3a2e); border-bottom: 1px solid var(--rule, rgba(229,227,218,.18));
  font: 500 11px/1.4 var(--mono, "IBM Plex Mono", Menlo, monospace); letter-spacing: .05em; text-transform: uppercase; color: var(--muted, #8aa395); }
.bsbar .in { max-width: 1240px; margin: 0 auto; padding: 0 30px; }
.bsbar a { white-space: nowrap; position: static; color: var(--ink-2, #b9c3b4); text-decoration: none; }
.bsbar a:hover { color: var(--ink, #e5e3da); }
.bsbar .r1, .bsbar .r2 { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 18px; padding: 11px 0; }
.bsbar .r2 { border-top: 1px solid var(--grid-major, rgba(229,227,218,.11)); padding: 8px 0 10px; gap: 6px 8px; }
.bsbar .mark { color: var(--ink, #e5e3da); font-weight: 500; letter-spacing: .14em; margin-right: 4px; }
.bsbar .bsg { position: static; white-space: nowrap; display: inline-flex; gap: 11px; align-items: baseline; }
.bsbar .bsg > i { font-style: normal; color: var(--muted, #8aa395); opacity: .7; font-size: 9.5px; }
.bsbar a.on { color: var(--ink, #e5e3da); box-shadow: inset 0 -1.5px 0 var(--dif, #7fb0dd); }
.bsbar .chip { padding: 3px 9px; border: 1px solid var(--rule, rgba(229,227,218,.18)); border-radius: 2px; letter-spacing: .06em; }
.bsbar .chip.on { background: var(--ink, #e5e3da); color: var(--mat, #1d3a2e); border-color: var(--ink, #e5e3da); box-shadow: none; }
.bsbar .home { margin-left: auto; } .bsbar .scope + .home { margin-left: 0; }
.bsbar .scope { margin-left: auto; display: inline-flex; gap: 14px; }
.bsbar .scope a { color: var(--dif, #7fb0dd); }
.bs-hide { display: none !important; }
@media print { .bsbar { display: none; } }`;
  document.head.insertAdjacentHTML('beforeend', `<style>${css}</style>`);

  const on = p => (page === p ? ' class="on"' : '');
  const groups = GROUPS.map(([g, items]) => `<span class="bsg"><i>${g}</i>${items.map(([t, p]) =>
    `<a href="${rel(p)}${FILTERS[p] ? q(scope) : ''}"${on(p)}>${t}</a>`).join('')}</span>`).join('');
  const chips = COURSES.map(([s, short]) => {
    const href = view ? `${rel(page)}${s === scope ? '' : q(s)}` : rel(s + '/');
    return `<a class="chip${s === scope ? ' on' : ''}" href="${href}">${short}</a>`;
  }).join('');
  const sc = scope && COURSES.find(([s]) => s === scope);
  const scopeLinks = sc ? `<span class="scope">${twin ? '' : `<a href="${rel(sc[0] + '/')}">twin</a>`}${view === 'archive' ? '' : `<a href="${rel('archive.html')}?c=${sc[0]}">its figures</a>`}${view === 'pairs' ? '' : `<a href="${rel('pairs.html')}?c=${sc[0]}">its before / after</a>`}<a href="${root}../courses/${sc[0]}/index.html">on the site ↗</a></span>` : '';
  const bar = document.createElement('nav');
  bar.className = 'bsbar';
  bar.innerHTML = `<div class="in"><div class="r1"><a class="mark" href="${rel('')}">Backstage</a>${groups}</div><div class="r2">${chips}${scopeLinks}<a class="home" href="${root}../index.html">reader site ↗</a></div></div>`;
  document.body.prepend(bar);

  // the old crumbs keep their page facts (dates, counts); the bar now carries the way home
  const cr = document.querySelector('.crumbs, .eyebrow');
  if (cr) {
    const a = cr.querySelector('a');
    if (a && /^(Backstage|← Ordenações Filipinas)$/.test(a.textContent.trim())) {
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
