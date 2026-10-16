/* caderno: chapter bookmarks kept in this browser. */
(function () {
  'use strict';
  // ── the way back: a ribbon hanging from the top of the page, with the count, whenever anything is saved ──
  function savedCount() {
    var n = 0;
    try {
      var bm = JSON.parse(localStorage.getItem('ordenacoes-bm') || '[]'); if (Array.isArray(bm)) n += bm.length;
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (k && k.indexOf('ordenacoes-hl:') === 0) { var h = JSON.parse(localStorage.getItem(k) || '[]'); if (Array.isArray(h)) n += h.length; }
      }
    } catch (e) { return 0; }
    return Math.min(n, 999);
  }
  var tabCss = document.createElement('style');
  tabCss.textContent =
    '.cu-cad-tab{position:fixed;top:0;right:44px;z-index:30;display:flex;flex-direction:column;align-items:center;text-decoration:none;color:var(--paper);transform:translateY(-6px);transition:transform .25s cubic-bezier(.3,1.5,.5,1)}' +
    '.cu-cad-tab svg{display:block;width:30px;height:62px;filter:drop-shadow(0 2px 2px rgba(0,0,0,.22))}' +
    '.cu-cad-tab .rib{fill:var(--ink)}.cu-cad-tab .n{fill:var(--paper);font:600 11px/1 "IBM Plex Mono",monospace;text-anchor:middle}' +
    '.cu-cad-tab .lbl{position:absolute;right:-6px;top:68px;white-space:nowrap;font:500 11px/1 "IBM Plex Mono",monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--ink);background:var(--paper);padding:5px 8px;opacity:0;transform:translateY(-4px);transition:opacity .2s,transform .2s;pointer-events:none;box-shadow:0 4px 10px -4px rgba(0,0,0,.35)}' +
    '.cu-cad-tab:hover,.cu-cad-tab:focus-visible{transform:translateY(2px);outline:none}.cu-cad-tab:hover .lbl,.cu-cad-tab:focus-visible .lbl{opacity:1;transform:none}' +
    '.cu-cad-tab:focus-visible svg{outline:2px solid var(--dif);outline-offset:2px}' +
    '.cu-cad-tab.bump{animation:cu-cad-bump .5s cubic-bezier(.3,1.6,.5,1)}@keyframes cu-cad-bump{0%{transform:translateY(-6px)}40%{transform:translateY(6px)}100%{transform:translateY(-6px)}}' +
    '@media(prefers-reduced-motion:reduce){.cu-cad-tab,.cu-cad-tab .lbl{transition:none}.cu-cad-tab.bump{animation:none}}@media print{.cu-cad-tab{display:none}}';
  document.head.appendChild(tabCss);
  var tab = null;
  function renderTab(bump) {
    if (/\/caderno\.html$/i.test(location.pathname)) return;
    var n = savedCount();
    if (!n) { if (tab) { tab.remove(); tab = null; } return; }
    if (!tab) {
      tab = document.createElement('a'); tab.className = 'cu-cad-tab'; tab.href = '/caderno.html';
      tab.innerHTML = '<svg viewBox="0 0 30 62" aria-hidden="true"><path class="rib" d="M2 0h26v62l-13-10-13 10z"/><text class="n" x="15" y="36"></text></svg><span class="lbl">Meu caderno</span>';
      document.body.appendChild(tab);
    }
    tab.querySelector('.n').textContent = n;
    tab.setAttribute('aria-label', 'Meu caderno: ' + n + (n === 1 ? ' item guardado' : ' itens guardados'));
    if (bump) { tab.classList.remove('bump'); void tab.offsetWidth; tab.classList.add('bump'); }
  }
  window.cuCadernoTab = renderTab;
  window.addEventListener('storage', function () { renderTab(false); });
  if (document.body) renderTab(false); else document.addEventListener('DOMContentLoaded', function () { renderTab(false); });

  var path = normalizePath(location.pathname);
  if (!path || /\/index\.html$/i.test(location.pathname) || !/^\/courses\//.test(path)) return;
  if (!/\.html$/i.test(path) || !/^\/courses\/[a-z0-9-]+\/(?:aula-[a-z0-9][a-z0-9-]*|unidade-[a-z0-9][a-z0-9-]*|suplemento-[a-z0-9][a-z0-9-]*|revisao(?:-[a-z0-9][a-z0-9-]*)?)\.html$/i.test(path)) return;

  var KEY = 'ordenacoes-bm';
  var BLOCK = 'p,li,td,th,blockquote,figcaption,dd,dt,h2,h3,h4';
  var SKIP = 'nav,button,select,input,textarea,summary,svg,script,style,label,[contenteditable],.topbar,.label,.kicker,.titleblock,.endnav,.course-nav,.stage,.deck-wrap,.deck-tools,.art-tools,.art-key,.heading-anchor,.chapter-nav,.chapter-pagination,.skip-link,.site-return,.num,.tag,.cu-pop,.cu-hlbar';
  var pageHeadings = Array.prototype.slice.call(document.querySelectorAll('h2'));
  if (!pageHeadings.length) return;

  function normalizePath(value) {
    if (typeof value !== 'string' || value.length > 300) return '';
    var p = value.split(/[?#]/)[0].replace(/\\/g, '/');
    if (p.charAt(0) !== '/') p = '/' + p;
    p = p.replace(/\/index\.html$/i, '/');
    return p;
  }
  function safeText(value, max) {
    return String(value || '').replace(/\s+/g, ' ').trim().slice(0, max);
  }
  function safeMark(item) {
    return !!item && typeof item === 'object' && normalizePath(item.path) === path &&
      /^\/courses\/[a-z0-9-]+\/[a-z0-9][a-z0-9._-]*\.html$/i.test(item.path) &&
      typeof item.chapterId === 'string' && item.chapterId.length > 0 && item.chapterId.length <= 120 &&
      typeof item.chapterTitle === 'string' && item.chapterTitle.length <= 240 &&
      typeof item.course === 'string' && item.course.length <= 160 &&
      typeof item.lessonTitle === 'string' && item.lessonTitle.length <= 240 &&
      typeof item.created === 'string' && item.created.length <= 40;
  }
  function readMarks() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw || raw.length > 200000) return [];
      var parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return [];
      return parsed.filter(safeMark).map(function (m) {
        return { path: m.path, course: m.course, lessonTitle: m.lessonTitle, chapterId: m.chapterId,
          chapterTitle: m.chapterTitle, created: m.created };
      });
    } catch (e) { return []; }
  }
  var marks = readMarks();
  // the <title> ends with the course name; the h1's innerText keeps the space where a split span breaks the line
  var titleParts = String(document.title || '').split(' · ');
  var course = safeText(titleParts.length > 1 ? titleParts[titleParts.length - 1] : '', 160);
  // the page <title> holds the lesson's name whole; the hero h1 is split into lines with no space between them (16/10)
  var lessonTitle = safeText(document.title.split(' · ')[0], 240) || safeText(document.querySelector('h1') && String(document.querySelector('h1').textContent).replace(/\s+/g, ' '), 240);

  var css = document.createElement('style');
  css.textContent =
    '.cu-bm-toggle{display:inline-grid;place-items:center;vertical-align:middle;width:40px;height:44px;margin-left:.4em;padding:0;border:0;background:transparent;color:var(--ink-2);cursor:pointer;touch-action:manipulation}' +
    '.cu-bm-toggle svg{display:block;width:20px;height:30px;overflow:visible;transition:transform .22s cubic-bezier(.3,1.6,.5,1)}' +
    '.cu-bm-toggle .cu-bm-paper{fill:var(--paper);stroke:currentColor;stroke-width:1.6;stroke-linejoin:round;transition:fill .15s}' +
    '.cu-bm-toggle .cu-bm-fold{display:none}' +
    '.cu-bm-toggle:hover{color:var(--ink)}.cu-bm-toggle:hover svg{transform:translateY(2px)}' +
    '.cu-bm-toggle[aria-pressed="true"]{color:var(--ink)}.cu-bm-toggle[aria-pressed="true"] .cu-bm-paper{fill:var(--ink)}.cu-bm-toggle[aria-pressed="true"] svg{transform:translateY(6px)}' +
    '.cu-bm-toggle:focus-visible{outline:2px solid var(--dif);outline-offset:2px}' +
    '.chapter h2,.reading-sheet h2{position:relative}' +
    '.cu-bm-margin{position:fixed;z-index:8;top:112px;left:8px;display:none;pointer-events:none;color:var(--ink)}' +
    '.cu-bm-margin svg{display:block;width:22px;height:27px;filter:drop-shadow(1px 1px 0 var(--paper))}' +
    '.cu-bm-margin .cu-bm-paper{fill:var(--ink);stroke:var(--ink);stroke-width:1.6;stroke-linejoin:round}' +
    '.cu-bm-margin .cu-bm-fold{display:none}' +
    '.cu-bm-margin.is-visible{display:block}' +
    '@media(max-width:600px) and (orientation:portrait){.cu-bm-toggle{width:36px;height:36px;margin-left:.25em}.cu-bm-margin{display:none!important}}' +
    '@media(prefers-reduced-motion:reduce){.cu-bm-toggle,.cu-bm-margin{scroll-behavior:auto;animation:none!important;transition:none!important}}' +
    '@media print{.cu-bm-toggle,.cu-bm-margin{display:none!important}}';
  document.head.appendChild(css);

  function ribbonSvg() {
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', '0 0 20 26'); svg.setAttribute('aria-hidden', 'true');
    var paper = document.createElementNS(svg.namespaceURI, 'path');
    paper.setAttribute('class', 'cu-bm-paper'); paper.setAttribute('d', 'M3.5 1h13v23.5l-6.5-5-6.5 5z');
    var fold = document.createElementNS(svg.namespaceURI, 'path');
    fold.setAttribute('class', 'cu-bm-fold'); fold.setAttribute('d', 'M4.8 3.3h10.4v17.7L10 17.6l-5.2 3.4z');
    svg.appendChild(paper); svg.appendChild(fold); return svg;
  }
  function slug(text) {
    var value = safeText(text, 180).toLocaleLowerCase('pt-BR');
    try { value = value.normalize('NFD').replace(/[\u0300-\u036f]/g, ''); } catch (e) {}
    return value.replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 72) || 'capitulo';
  }
  var used = Object.create(null);
  Array.prototype.forEach.call(document.querySelectorAll('[id]'), function (el) { used[el.id] = true; });
  pageHeadings.forEach(function (h) {
    if (!h.id) {
      var base = slug(h.textContent), id = base, n = 2;
      while (used[id] || document.getElementById(id)) id = base + '-' + n++;
      h.id = id; used[id] = true;
    }
  });


  var noteEl = null, noteTimer = 0;
  var noteCss = document.createElement('style');
  noteCss.textContent = '.cu-bm-note{position:fixed;left:50%;bottom:28px;z-index:40;transform:translate(-50%,16px);opacity:0;display:flex;gap:14px;align-items:center;background:var(--ink);color:var(--paper);font:500 12px/1 "IBM Plex Mono",monospace;letter-spacing:.06em;padding:12px 16px;box-shadow:0 10px 24px -10px rgba(0,0,0,.5);transition:opacity .2s,transform .25s cubic-bezier(.3,1.4,.5,1)}' +
    '.cu-bm-note.on{opacity:1;transform:translate(-50%,0)}.cu-bm-note a{color:var(--paper);text-underline-offset:3px}' +
    '@media(prefers-reduced-motion:reduce){.cu-bm-note{transition:none}}@media print{.cu-bm-note{display:none}}';
  document.head.appendChild(noteCss);
  function note(text, withLink) {
    if (!noteEl) { noteEl = document.createElement('div'); noteEl.className = 'cu-bm-note'; noteEl.setAttribute('role', 'status'); document.body.appendChild(noteEl); }
    noteEl.innerHTML = '';
    var s = document.createElement('span'); s.textContent = text; noteEl.appendChild(s);
    if (withLink) { var l = document.createElement('a'); l.href = '/caderno.html'; l.textContent = 'Ver no caderno →'; noteEl.appendChild(l); }
    noteEl.classList.add('on'); clearTimeout(noteTimer);
    noteTimer = setTimeout(function () { noteEl.classList.remove('on'); }, 3200);
  }
  function isMarked(id) { return marks.some(function (m) { return m.path === path && m.chapterId === id; }); }
  function syncButton(button, heading) {
    var active = isMarked(heading.id);
    button.setAttribute('aria-pressed', String(active));
    button.setAttribute('aria-label', active ? 'Desmarcar capítulo: ' + safeText(heading.textContent, 180) : 'Marcar capítulo: ' + safeText(heading.textContent, 180));
    button.title = active ? 'Desmarcar capítulo' : 'Marcar capítulo';
  }
  function persist(next) {
    try {
      if (next.length) localStorage.setItem(KEY, JSON.stringify(next));
      else localStorage.removeItem(KEY);
      return true;
    } catch (e) { return false; }
  }
  var sections = [];
  pageHeadings.forEach(function (heading) {
    var chapterTitle = safeText(heading.textContent, 240);
    var button = document.createElement('button');
    button.type = 'button'; button.className = 'cu-bm-toggle'; button.setAttribute('data-bookmark-toggle', ''); button.appendChild(ribbonSvg());
    syncButton(button, heading); heading.appendChild(button);
    var section = heading.closest('section') || heading.parentElement;
    sections.push({ heading: heading, section: section, button: button });
    button.addEventListener('click', function () {
      var found = isMarked(heading.id), next = marks.filter(function (m) { return !(m.path === path && m.chapterId === heading.id); });
      if (!found) {
        next.push({ path: path, course: course || path.split('/')[2], lessonTitle: lessonTitle,
          chapterId: heading.id, chapterTitle: chapterTitle, created: new Date().toISOString() });
      }
      if (!persist(next)) return;
      marks = next; syncButton(button, heading); updateMargin();
      note(!found ? 'Capítulo guardado' : 'Capítulo tirado do caderno', !found);
      if (window.cuCadernoTab) window.cuCadernoTab(!found);
    });
  });

  var margin = document.createElement('span');
  margin.className = 'cu-bm-margin'; margin.setAttribute('aria-hidden', 'true'); margin.appendChild(ribbonSvg());
  document.body.appendChild(margin);
  function updateMargin() {
    var candidates = sections.filter(function (item) {
      if (!isMarked(item.heading.id)) return false;
      var rect = item.section.getBoundingClientRect();
      return rect.top < window.innerHeight * .58 && rect.bottom > 80;
    }).sort(function (a, b) { return b.heading.getBoundingClientRect().top - a.heading.getBoundingClientRect().top; });
    if (!candidates.length || window.innerWidth <= 600) { margin.classList.remove('is-visible'); return; }
    var rect = candidates[0].heading.getBoundingClientRect();
    margin.style.left = Math.max(8, rect.left - 46) + 'px';
    margin.classList.add('is-visible');
  }
  window.addEventListener('scroll', updateMargin, { passive: true });
  window.addEventListener('resize', updateMargin);
  updateMargin();

  function deepLinkHighlight() {
    var match = /^#hl=(.+)$/.exec(location.hash || '');
    if (!match) return;
    var id; try { id = decodeURIComponent(match[1]); } catch (e) { return; }
    if (!id || id.length > 160) return;
    var highlightKey = 'ordenacoes-hl:' + path;
    var highlight = null;
    try {
      var raw = localStorage.getItem(highlightKey);
      if (!raw || raw.length > 2000000) return;
      var list = JSON.parse(raw);
      if (!Array.isArray(list)) return;
      highlight = list.find(function (h) { return h && h.id === id && Number.isFinite(h.s) && Number.isFinite(h.e) && typeof h.q === 'string' && h.q.length <= 10000; });
    } catch (e) { return; }
    if (!highlight) return;

    var attempts = 0;
    function locate() {
      attempts++;
      var existing = document.querySelectorAll('mark.cu-hl[data-h]');
      var painted = Array.prototype.filter.call(existing, function (el) { return el.getAttribute('data-h') === id; });
      if (painted.length) {
        painted.forEach(function (el) { el.classList.add('cu-hl-return'); });
        var target = painted[0]; target.scrollIntoView({ block: 'center', behavior: reducedMotion() ? 'auto' : 'smooth' });
        window.setTimeout(function () { painted.forEach(function (el) { el.classList.remove('cu-hl-return'); }); }, 1500);
        return;
      }
      var idx = textIndex();
      var start = Math.max(0, Math.floor(highlight.s));
      if (idx.text.slice(start, start + highlight.q.length) !== highlight.q) {
        var found = idx.text.indexOf(highlight.q); if (found < 0) { if (attempts < 30) window.setTimeout(locate, 100); return; }
        start = found;
      }
      var point = offsetPoint(idx.nodes, start);
      if (point) {
        var range = document.createRange(); range.setStart(point.node, point.offset); range.collapse(true);
        var rect = range.getBoundingClientRect();
        if (rect.height || rect.top || rect.left) {
          window.scrollTo({ top: window.pageYOffset + rect.top - Math.min(180, window.innerHeight * .28), behavior: reducedMotion() ? 'auto' : 'smooth' });
          var parent = point.node.parentElement;
          if (parent) { parent.classList.add('cu-hl-return'); window.setTimeout(function () { parent.classList.remove('cu-hl-return'); }, 1500); }
          return;
        }
      }
      if (attempts < 30) window.setTimeout(locate, 100);
    }
    function textIndex() {
      var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: function (node) {
        return node.nodeValue && node.parentElement && node.parentElement.closest(BLOCK) && !node.parentElement.closest(SKIP) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }});
      var nodes = [], parts = [], pos = 0, node;
      while ((node = walker.nextNode())) { nodes.push({ node: node, start: pos }); parts.push(node.nodeValue); pos += node.nodeValue.length; }
      return { nodes: nodes, text: parts.join('') };
    }
    function offsetPoint(nodes, offset) {
      for (var i = 0; i < nodes.length; i++) {
        var len = nodes[i].node.nodeValue.length;
        if (offset <= nodes[i].start + len) return { node: nodes[i].node, offset: Math.max(0, offset - nodes[i].start) };
      }
      return null;
    }
    function reducedMotion() { return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', locate, { once: true }); else locate();
  }
  var returnStyle = document.createElement('style');
  returnStyle.textContent = '.cu-hl-return{outline:2px solid var(--conc)!important;outline-offset:3px!important;transition:outline-color .2s}@media(prefers-reduced-motion:reduce){.cu-hl-return{transition:none}}';
  document.head.appendChild(returnStyle);
  deepLinkHighlight();
})();
