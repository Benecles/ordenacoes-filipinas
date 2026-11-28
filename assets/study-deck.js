/* Ordenações Filipinas — Study Deck: Global Legal Search (Cmd+K / Ctrl+K), Reading Progress Hairline,
   and Live Chapter Outline (Sumário, Cmd+J). Pure vanilla JS, zero dependencies, 100% offline-capable,
   strictly using house tokens (surface.paper, surface.night, colour.ink, colour.blue, colour.orange). */
(function () {
  if (window.__ofStudyDeck) return;
  if (/\/backstage(\/|$)/.test(location.pathname)) return;
  window.__ofStudyDeck = true;

  var scriptSrc = (document.currentScript && document.currentScript.src) || '';
  var rootUrl = './';
  try { rootUrl = new URL('../', scriptSrc).href; } catch (_) {}

  var curCourse = (location.pathname.match(/\/courses\/([^/]+)\//) || [])[1] || '';
  var isMac = /Mac|iPhone|iPad|iPod/i.test(navigator.platform || navigator.userAgent || '');
  var modKey = isMac ? '⌘' : 'Ctrl+';

  function fold(s) {
    return String(s || '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
  }

  // 1. Scoped drafting-table CSS (strictly house tokens, light + night native)
  var style = document.createElement('style');
  style.textContent = [
    '.of-prog{position:fixed;top:0;left:0;height:2.5px;width:0;background:var(--dif,#2b5597);z-index:95;pointer-events:none;transition:width .08s linear}',
    '.of-dock{position:fixed;right:14px;bottom:56px;z-index:81;display:flex;flex-direction:column;align-items:flex-end;gap:7px}',
    '.of-btn{display:inline-flex;align-items:center;gap:7px;border:1.5px solid var(--ink,#1d2530);background:var(--paper,#f2eee3);color:var(--ink,#1d2530);box-shadow:3px 3px 0 var(--grid-major,#c9c1aa);padding:7px 11px;font:500 11px/1.2 var(--mono,monospace);letter-spacing:.07em;text-transform:uppercase;cursor:pointer;transition:transform .12s ease,border-color .12s ease}',
    '.of-btn:hover,.of-btn:focus-visible{border-color:var(--dif,#2b5597);color:var(--dif,#2b5597);transform:translate(-1px,-1px);outline:none}',
    '.of-btn kbd{font:600 10px/1 var(--mono,monospace);padding:2px 5px;border:1px solid var(--rule,#c9c1aa);color:var(--ink-2,#4d5662)}',
    '.of-backdrop{position:fixed;inset:0;z-index:120;background:rgba(12,15,22,.46);display:grid;place-items:start center;padding:min(10vh,84px) 16px 24px}',
    '.of-backdrop[hidden],.of-toc[hidden]{display:none}',
    '.of-modal{width:min(680px,100%);max-height:min(76dvh,640px);display:flex;flex-direction:column;background:var(--paper,#f2eee3);color:var(--ink,#1d2530);border:1.5px solid var(--ink,#1d2530);box-shadow:7px 7px 0 var(--grid-major,#c9c1aa);overflow:hidden}',
    '.of-head{display:flex;align-items:center;gap:10px;padding:12px 16px;border-bottom:1.5px solid var(--ink,#1d2530);background:var(--paper-2,var(--paper,#f2eee3))}',
    '.of-head input{flex:1;min-width:0;border:0;background:transparent;color:var(--ink,#1d2530);font:400 18px/1.3 var(--serif,Georgia,serif);outline:none}',
    '.of-head input::placeholder{color:var(--ink-2,#5c6570);font-style:italic}',
    '.of-head button{border:1px solid var(--ink-2,#5c6570);background:transparent;color:var(--ink-2,#5c6570);font:500 10px/1 var(--mono,monospace);letter-spacing:.08em;text-transform:uppercase;padding:5px 8px;cursor:pointer}',
    '.of-tabs{display:flex;flex-wrap:wrap;gap:6px;padding:9px 16px;border-bottom:1px solid var(--rule,#c9c1aa)}',
    '.of-tab{border:1px solid var(--rule,#c9c1aa);background:transparent;color:var(--ink-2,#5c6570);padding:4px 9px;font:500 10.5px/1.3 var(--mono,monospace);letter-spacing:.06em;text-transform:uppercase;cursor:pointer}',
    '.of-tab[aria-pressed="true"]{border-color:var(--dif,#2b5597);background:var(--dif-wash,rgba(43,85,151,.12));color:var(--dif,#2b5597);font-weight:600}',
    '.of-results{list-style:none;margin:0;padding:0;overflow:auto;flex:1}',
    '.of-results li{border-bottom:1px dotted var(--rule,#c9c1aa)}',
    '.of-results a{display:grid;grid-template-columns:76px minmax(0,1fr);gap:12px;padding:11px 16px;text-decoration:none;color:inherit;align-items:baseline}',
    '.of-results a:hover,.of-results a.of-sel{background:var(--dif-wash,rgba(43,85,151,.1));outline:none}',
    '.of-kind{font:600 10px/1.3 var(--mono,monospace);letter-spacing:.07em;text-transform:uppercase;color:var(--dif,#2b5597)}',
    '.of-kind.k-a{color:var(--conc,#b4432a)}.of-kind.k-t{color:var(--dif,#2b5597)}.of-kind.k-c{color:var(--ink,#1d2530)}',
    '.of-title{display:block;font:650 15px/1.3 var(--sans,system-ui,sans-serif);color:var(--ink,#1d2530)}',
    '.of-desc{display:block;margin-top:2px;font:400 13.5px/1.45 var(--serif,Georgia,serif);color:var(--ink-2,#5c6570)}',
    '.of-meta{display:block;margin-top:3px;font:500 10px/1.2 var(--mono,monospace);letter-spacing:.05em;text-transform:uppercase;color:var(--muted,#777)}',
    '.of-foot{display:flex;justify-content:space-between;gap:12px;padding:8px 16px;border-top:1px solid var(--rule,#c9c1aa);font:500 10px/1.4 var(--mono,monospace);letter-spacing:.05em;color:var(--ink-2,#5c6570)}',
    '.of-empty{padding:24px 18px;font:400 15px/1.55 var(--serif,Georgia,serif);color:var(--ink-2,#5c6570)}',
    '.of-toc{position:fixed;right:0;top:0;height:100dvh;width:min(340px,92vw);z-index:115;background:var(--paper,#f2eee3);color:var(--ink,#1d2530);border-left:1.5px solid var(--ink,#1d2530);box-shadow:-4px 0 0 var(--grid-major,#c9c1aa);display:flex;flex-direction:column;padding:20px 18px 24px;box-sizing:border-box}',
    '.of-toc header{display:flex;justify-content:space-between;align-items:baseline;padding-bottom:12px;border-bottom:1.5px solid var(--ink,#1d2530);margin-bottom:10px}',
    '.of-toc h2{margin:0;font:750 20px/1.15 var(--sans,system-ui,sans-serif)}',
    '.of-toc header button{border:1px solid var(--ink-2,#5c6570);background:transparent;color:inherit;font:500 10px/1 var(--mono,monospace);text-transform:uppercase;letter-spacing:.07em;padding:5px 8px;cursor:pointer}',
    '.of-toc ol{list-style:none;margin:0;padding:0;overflow:auto;flex:1}',
    '.of-toc li{border-bottom:1px dotted var(--rule,#c9c1aa)}',
    '.of-toc li a{display:grid;grid-template-columns:26px 1fr;gap:8px;padding:10px 4px;text-decoration:none;color:var(--ink,#1d2530);font:500 14px/1.4 var(--sans,system-ui,sans-serif)}',
    '.of-toc li a .n{font:600 11px/1.6 var(--mono,monospace);color:var(--ink-2,#5c6570)}',
    '.of-toc li a.on,.of-toc li a:hover{color:var(--dif,#2b5597)}',
    '.of-toc li a.on .n{color:var(--dif,#2b5597)}',
    '.of-toc-links{display:flex;flex-wrap:wrap;gap:12px;padding-top:12px;margin-top:10px;border-top:1px solid var(--rule,#c9c1aa);font:600 11px/1.4 var(--mono,monospace);text-transform:uppercase;letter-spacing:.06em}',
    '.of-toc-links a{text-decoration:none;color:var(--conc,#b4432a)}.of-toc-links a:hover{text-decoration:underline}',
    '@media(max-width:600px) and (orientation:portrait){.of-dock{right:10px;bottom:54px}.of-btn{padding:6px 9px;font-size:10px}.of-btn kbd{display:none}.of-results a{grid-template-columns:1fr;gap:3px}}',
    '@media(prefers-reduced-motion:reduce){.of-prog,.of-btn{transition:none!important}}',
    '@media print{.of-prog,.of-dock,.of-backdrop,.of-toc{display:none!important}}'
  ].join('\n');
  document.head.appendChild(style);

  // 2. Floating dock
  var dock = document.createElement('div');
  dock.className = 'of-dock';
  var searchBtn = document.createElement('button');
  searchBtn.type = 'button';
  searchBtn.className = 'of-btn';
  searchBtn.setAttribute('aria-label', 'Buscar em todo o site');
  searchBtn.innerHTML = '<span>Buscar</span><kbd>' + modKey + 'K</kbd>';
  dock.appendChild(searchBtn);

  // 3. Reading progress + Chapter outline (Sumário) on lesson pages
  var chapters = [].slice.call(document.querySelectorAll('section.chapter[id], main section[id]')).filter(function (ch) {
    return ch.id !== 'bibliografia' && ch.id !== 'exercicio' && ch.querySelector('h2');
  });
  var tocDrawer = null, tocBtn = null, tocLinks = [];
  if (chapters.length >= 2) {
    var prog = document.createElement('div');
    prog.className = 'of-prog';
    prog.setAttribute('aria-hidden', 'true');
    document.body.appendChild(prog);

    var raf = false;
    function updateProg() {
      raf = false;
      var h = document.documentElement.scrollHeight - window.innerHeight;
      var pct = h > 0 ? Math.max(0, Math.min(100, (window.scrollY / h) * 100)) : 0;
      prog.style.width = pct.toFixed(1) + '%';
    }
    window.addEventListener('scroll', function () { if (!raf) { raf = true; requestAnimationFrame(updateProg); } }, { passive: true });
    updateProg();

    tocBtn = document.createElement('button');
    tocBtn.type = 'button';
    tocBtn.className = 'of-btn';
    tocBtn.setAttribute('aria-label', 'Abrir sumário da aula');
    tocBtn.setAttribute('aria-expanded', 'false');
    tocBtn.innerHTML = '<span>Sumário</span><kbd>' + modKey + 'J</kbd>';
    dock.insertBefore(tocBtn, searchBtn);

    tocDrawer = document.createElement('aside');
    tocDrawer.className = 'of-toc';
    tocDrawer.hidden = true;
    tocDrawer.setAttribute('aria-label', 'Sumário desta aula');
    var tocHtml = '<header><h2>Sumário</h2><button type="button" aria-label="Fechar sumário">Fechar</button></header><ol>';
    chapters.forEach(function (ch, idx) {
      var h2 = ch.querySelector('h2');
      var label = h2 ? h2.textContent.trim() : ch.id;
      var num = String(idx + 1).padStart(2, '0');
      tocHtml += '<li><a href="#' + ch.id + '" data-ch="' + ch.id + '"><span class="n">' + num + '</span><span>' + label.replace(/</g, '&lt;') + '</span></a></li>';
    });
    tocHtml += '</ol><div class="of-toc-links">';
    var ex = document.querySelector('#exercicio, .exam-section');
    if (ex && ex.id) tocHtml += '<a href="#' + ex.id + '">Exercícios →</a>';
    tocHtml += '<a href="' + rootUrl + 'caderno.html">Meu caderno →</a></div>';
    tocDrawer.innerHTML = tocHtml;
    document.body.appendChild(tocDrawer);

    tocLinks = [].slice.call(tocDrawer.querySelectorAll('a[data-ch]'));
    function setToc(open) {
      tocDrawer.hidden = !open;
      tocBtn.setAttribute('aria-expanded', String(open));
      if (open) tocDrawer.querySelector('button').focus();
    }
    tocBtn.addEventListener('click', function () { setToc(tocDrawer.hidden); });
    tocDrawer.querySelector('button').addEventListener('click', function () { setToc(false); tocBtn.focus(); });
    tocDrawer.addEventListener('click', function (e) { if (e.target.closest('a')) setToc(false); });

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            tocLinks.forEach(function (a) { a.classList.toggle('on', a.getAttribute('data-ch') === en.target.id); });
          }
        });
      }, { rootMargin: '-18% 0px -70% 0px' });
      chapters.forEach(function (ch) { io.observe(ch); });
    }
  }
  document.body.appendChild(dock);

  // 4. Global Cmd+K Legal Search Modal
  var backdrop = document.createElement('div');
  backdrop.className = 'of-backdrop';
  backdrop.hidden = true;
  backdrop.innerHTML = [
    '<div class="of-modal" role="dialog" aria-modal="true" aria-label="Busca global Ordenações Filipinas">',
    '  <div class="of-head"><input type="search" autocomplete="off" spellcheck="false" placeholder="Buscar aula, capítulo, conceito ou artigo (ex: evicção, art. 476, Zeca)…"><button type="button" data-close>Esc</button></div>',
    '  <div class="of-tabs" role="group" aria-label="Filtrar resultados">',
    '    <button type="button" class="of-tab" data-k="all" aria-pressed="true">Tudo</button>',
    '    <button type="button" class="of-tab" data-k="l" aria-pressed="false">Aulas</button>',
    '    <button type="button" class="of-tab" data-k="h" aria-pressed="false">Capítulos</button>',
    '    <button type="button" class="of-tab" data-k="t" aria-pressed="false">Conceitos</button>',
    '    <button type="button" class="of-tab" data-k="a" aria-pressed="false">Artigos & Casos</button>',
    '  </div>',
    '  <ul class="of-results" role="listbox"></ul>',
    '  <div class="of-foot"><span class="of-count">Carregando índice…</span><span>↑↓ navegar · Enter abrir</span></div>',
    '</div>'
  ].join('');
  document.body.appendChild(backdrop);

  var input = backdrop.querySelector('input');
  var listEl = backdrop.querySelector('.of-results');
  var countEl = backdrop.querySelector('.of-count');
  var tabs = [].slice.call(backdrop.querySelectorAll('.of-tab'));
  var indexData = null, courseMap = {}, filterK = 'all', selIdx = 0, visibleItems = [];
  var KIND_LABEL = { c: 'Curso', l: 'Aula', h: 'Capítulo', t: 'Conceito', a: 'Artigo/Caso' };

  function loadIndex() {
    if (indexData) return Promise.resolve(indexData);
    return fetch(rootUrl + 'assets/search-index.json').then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    }).then(function (d) {
      d.courses.forEach(function (c) { courseMap[c.s] = c.n; });
      d.items.forEach(function (it) {
        it._t = fold(it.t);
        it._d = fold(it.d);
        it._c = fold(courseMap[it.c] || it.c);
      });
      indexData = d;
      return d;
    });
  }

  function renderResults() {
    if (!indexData) return;
    var q = fold(input.value).trim();
    var terms = q ? q.split(/\s+/).filter(Boolean) : [];
    var scored = [];
    for (var i = 0; i < indexData.items.length; i++) {
      var it = indexData.items[i];
      if (filterK !== 'all' && it.k !== filterK) continue;
      var sc = 0;
      if (!terms.length) {
        if (curCourse && it.c === curCourse && (it.k === 'l' || it.k === 'c')) sc = 50;
        else if (!curCourse && it.k === 'c') sc = 40;
        else continue;
      } else {
        var ok = true;
        for (var j = 0; j < terms.length; j++) {
          var w = terms[j];
          if (it._t.indexOf(w) !== -1) sc += (it._t.indexOf(w) === 0 ? 30 : 18);
          else if (it._d.indexOf(w) !== -1) sc += 8;
          else if (it._c.indexOf(w) !== -1) sc += 4;
          else { ok = false; break; }
        }
        if (!ok) continue;
        if (curCourse && it.c === curCourse) sc += 12;
        if (it.k === 'l') sc += 6;
        else if (it.k === 't') sc += 5;
      }
      scored.push([sc, it]);
    }
    scored.sort(function (a, b) { return b[0] - a[0]; });
    visibleItems = scored.slice(0, 30).map(function (x) { return x[1]; });
    selIdx = 0;

    listEl.replaceChildren();
    if (!visibleItems.length) {
      var empty = document.createElement('li');
      empty.className = 'of-empty';
      empty.textContent = q ? 'Nenhum resultado para “' + input.value.trim() + '”.' : 'Digite um termo jurídico, número de artigo (ex: art. 476) ou nome de aula.';
      listEl.appendChild(empty);
      countEl.textContent = '0 resultados';
      return;
    }
    visibleItems.forEach(function (it, idx) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = rootUrl + it.u;
      if (idx === 0) a.className = 'of-sel';
      var kind = document.createElement('span');
      kind.className = 'of-kind k-' + it.k;
      kind.textContent = KIND_LABEL[it.k] || '';
      var body = document.createElement('span');
      var tt = document.createElement('span'); tt.className = 'of-title'; tt.textContent = it.t;
      body.appendChild(tt);
      if (it.d) { var dd = document.createElement('span'); dd.className = 'of-desc'; dd.textContent = it.d; body.appendChild(dd); }
      var mm = document.createElement('span'); mm.className = 'of-meta'; mm.textContent = courseMap[it.c] || it.c;
      body.appendChild(mm);
      a.append(kind, body);
      a.addEventListener('click', function () { closeSearch(); });
      li.appendChild(a);
      listEl.appendChild(li);
    });
    countEl.textContent = scored.length + (scored.length === 1 ? ' resultado' : ' resultados') + (scored.length > 30 ? ' (mostrando 30)' : '');
  }

  function updateSel() {
    var links = listEl.querySelectorAll('a');
    links.forEach(function (a, i) {
      a.classList.toggle('of-sel', i === selIdx);
      if (i === selIdx) a.scrollIntoView({ block: 'nearest' });
    });
  }

  function openSearch() {
    if (tocDrawer && !tocDrawer.hidden) { tocDrawer.hidden = true; tocBtn.setAttribute('aria-expanded', 'false'); }
    backdrop.hidden = false;
    input.focus();
    input.select();
    loadIndex().then(renderResults).catch(function () {
      countEl.textContent = 'Índice indisponível neste modo';
    });
  }

  function closeSearch() {
    backdrop.hidden = true;
  }

  searchBtn.addEventListener('click', openSearch);
  backdrop.querySelector('[data-close]').addEventListener('click', closeSearch);
  backdrop.addEventListener('click', function (e) { if (e.target === backdrop) closeSearch(); });
  input.addEventListener('input', renderResults);
  tabs.forEach(function (tb) {
    tb.addEventListener('click', function () {
      filterK = tb.getAttribute('data-k');
      tabs.forEach(function (x) { x.setAttribute('aria-pressed', String(x === tb)); });
      renderResults();
      input.focus();
    });
  });

  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (backdrop.hidden) openSearch(); else closeSearch();
      return;
    }
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'j' && tocDrawer) {
      e.preventDefault();
      var open = tocDrawer.hidden;
      tocDrawer.hidden = !open;
      tocBtn.setAttribute('aria-expanded', String(open));
      return;
    }
    if (!backdrop.hidden) {
      if (e.key === 'Escape') { e.preventDefault(); closeSearch(); }
      else if (e.key === 'ArrowDown' && visibleItems.length) { e.preventDefault(); selIdx = (selIdx + 1) % visibleItems.length; updateSel(); }
      else if (e.key === 'ArrowUp' && visibleItems.length) { e.preventDefault(); selIdx = (selIdx - 1 + visibleItems.length) % visibleItems.length; updateSel(); }
      else if (e.key === 'Enter' && visibleItems[selIdx]) {
        e.preventDefault();
        location.href = rootUrl + visibleItems[selIdx].u;
        closeSearch();
      }
    } else if (e.key === 'Escape' && tocDrawer && !tocDrawer.hidden) {
      tocDrawer.hidden = true;
      tocBtn.setAttribute('aria-expanded', 'false');
    }
  });
})();
