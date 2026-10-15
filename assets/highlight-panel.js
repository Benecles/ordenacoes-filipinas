/* painel de marcações: lists this page's highlights and jumps to each. Shown only once a page has a mark. */
(function () {
  var path = location.pathname.replace(/index\.html$/, ''), key = 'ordenacoes-hl:' + path;
  var css = document.createElement('style');
  css.textContent = '.cu-hl-open{position:fixed;right:58px;bottom:12px;z-index:82;border:1.5px solid var(--ink,#1d2530);background:var(--paper,#f2eee3);color:var(--ink,#1d2530);box-shadow:3px 3px 0 var(--grid-major,#c9c1aa);padding:8px 11px;font:11px/1.2 var(--mono,monospace);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.cu-hl-open[hidden],.cu-hl-panel[hidden]{display:none}.cu-hl-panel{position:fixed;z-index:83;right:0;top:0;height:100dvh;width:min(360px,92vw);overflow:auto;background:var(--paper,#f2eee3);color:var(--ink,#1d2530);border-left:1.5px solid var(--ink,#1d2530);box-shadow:-3px 0 0 var(--grid-major,#c9c1aa);padding:22px 18px 32px;font:15px/1.45 var(--sans,Arial,sans-serif)}.cu-hl-panel h2{font:750 24px/1.1 var(--sans,Arial,sans-serif);letter-spacing:-.01em;margin:0}.cu-hl-panel header{display:flex;align-items:start;justify-content:space-between;border-bottom:1.5px solid var(--ink,#1d2530);padding-bottom:13px;margin-bottom:10px}.cu-hl-panel button{font:inherit;color:inherit;background:transparent;border:1px solid currentColor;cursor:pointer;padding:5px 8px}.cu-hl-list{list-style:none;margin:0;padding:0}.cu-hl-list li{border-bottom:1px dotted var(--ink-2,#777);padding:11px 0}.cu-hl-list a{display:grid;grid-template-columns:12px 1fr;gap:9px;text-decoration:none}.cu-hl-list a:hover{text-decoration:underline;text-underline-offset:3px}.cu-hl-swatch{width:10px;height:1em;background:var(--sw,#f4d35e);margin-top:3px}.cu-hl-empty{color:var(--ink-2,#666);padding:12px 0}.cu-hl-all{display:block;margin-top:18px;padding-top:12px;border-top:1px solid var(--ink-2,#777);color:var(--conc,#9b4e35);font:11px/1.4 var(--mono,monospace);letter-spacing:.07em;text-transform:uppercase;text-decoration:none}.cu-hl-all:hover{text-decoration:underline;text-underline-offset:3px}.cu-hl-panel-open{overflow:hidden}@media print{.cu-hl-open,.cu-hl-panel{display:none!important}}';
  document.head.appendChild(css);
  var open = document.createElement('button'); open.className = 'cu-hl-open'; open.type = 'button'; open.innerHTML = 'Marcações <span aria-live="polite"></span>';
  open.setAttribute('aria-expanded', 'false'); open.setAttribute('aria-controls', 'cu-hl-panel');
  var panel = document.createElement('aside'); panel.className = 'cu-hl-panel'; panel.id = 'cu-hl-panel'; panel.hidden = true; panel.setAttribute('aria-label', 'Marcações desta página');
  panel.innerHTML = '<header><h2>Marcações</h2><button type="button" aria-label="Fechar painel">Fechar</button></header><p class="cu-hl-empty" hidden>Nenhuma marcação nesta página.</p><ol class="cu-hl-list"></ol><a class="cu-hl-all">Ver tudo no caderno →</a>';
  try { panel.querySelector('.cu-hl-all').href = new URL('../caderno.html', document.currentScript.src).href; } catch (_) {}
  document.body.append(open, panel);
  var list = panel.querySelector('ol'), count = open.querySelector('span'), empty = panel.querySelector('.cu-hl-empty');
  function data() { try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (_) { return []; } }
  function render(items) {
    list.replaceChildren(); count.textContent = items.length ? '(' + items.length + ')' : '';
    open.hidden = !items.length; if (!items.length && !panel.hidden) toggle(false);
    empty.hidden = !!items.length; list.hidden = !items.length;
    items.slice().sort(function (a,b) { return a.s-b.s; }).forEach(function (h, i) {
      var li = document.createElement('li'), a = document.createElement('a'), sw = document.createElement('i'), tx = document.createElement('span');
      a.href = '#'; sw.className = 'cu-hl-swatch'; sw.style.setProperty('--sw', ({1:'#f4d35e',2:'#bcd98a',3:'#a9c7ea',4:'#f0b2a4',5:'#d3bde8'})[h.c] || '#f4d35e');
      tx.textContent = (i + 1) + '. ' + String(h.q || '').replace(/\s+/g, ' ').trim(); a.append(sw, tx);
      a.addEventListener('click', function (e) { e.preventDefault(); var mark = document.querySelector('mark.cu-hl[data-h="' + CSS.escape(h.id) + '"]'); if (mark) { panel.hidden = true; open.setAttribute('aria-expanded','false'); mark.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'}); mark.click(); } });
      li.appendChild(a); list.appendChild(li);
    });
  }
  function toggle(show) { panel.hidden = !show; open.setAttribute('aria-expanded', String(show)); document.documentElement.classList.toggle('cu-hl-panel-open', show); if (show) panel.querySelector('button').focus(); else open.focus(); }
  open.addEventListener('click', function () { toggle(panel.hidden); }); panel.querySelector('button').addEventListener('click', function () { toggle(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) toggle(false); });
  document.addEventListener('ordenacoes:highlights-change', function (e) { render(e.detail.highlights || data()); });
  render(data());
})();
