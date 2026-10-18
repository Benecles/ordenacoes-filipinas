/* modo avião: a discreet corner button that saves the whole site
   on this device (via sw.js) so it can be read without a connection. */
(function () {
  if (!('serviceWorker' in navigator) || !('caches' in window)) return;
  var KEY = 'ordenacoes-offline';
  var root = new URL('..', document.currentScript.src).href; // site root
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { v ? localStorage.setItem(KEY, v) : localStorage.removeItem(KEY); } catch (e) {} }

  var css = document.createElement('style');
  css.textContent =
    '.cu-plane{position:fixed;left:10px;bottom:10px;z-index:80;width:30px;height:30px;border-radius:50%;border:1px solid currentColor;' +
    'background:var(--paper,#f2eee3);color:var(--ink-2,#4a4f55);opacity:.28;cursor:pointer;display:grid;place-items:center;padding:0;transition:opacity .2s}' +
    '.cu-plane:hover,.cu-plane:focus-visible,.cu-plane[aria-expanded="true"]{opacity:1}' +
    '.cu-plane.on{opacity:.9;color:#e8820c}' +
    '.cu-plane svg{width:16px;height:16px}' +
    // while saving, the circle around the plane is the progress bar; it closes into the orange ring of airplane mode
    '.cu-plane svg.cu-ring{position:absolute;inset:-1px;width:30px;height:30px;transform:rotate(-90deg);pointer-events:none;opacity:0;transition:opacity .4s}' +
    '.cu-ring circle{fill:none;stroke:#e8820c;stroke-width:1.6;stroke-dasharray:100;stroke-dashoffset:100;transition:stroke-dashoffset .35s}' +
    '.cu-plane.busy{opacity:1;border-color:var(--grid,#d8d2c0)}.cu-plane.busy svg.cu-ring{opacity:1}' +
    '.cu-pop{position:fixed;left:10px;bottom:48px;z-index:81;width:min(300px,calc(100vw - 20px));background:var(--paper,#f2eee3);color:var(--ink,#1d2530);' +
    'border:1.5px solid var(--ink,#1d2530);box-shadow:4px 4px 0 var(--grid-major,#c9c1aa);padding:14px 14px 12px;font:14px/1.45 Georgia,serif}' +
    '.cu-pop[hidden]{display:none}' +
    '.cu-pop b.t{display:block;font:700 15px Helvetica,Arial,sans-serif;margin-bottom:4px}' +
    '.cu-pop p{margin:0 0 10px}' +
    '.cu-pop .row{display:flex;gap:8px;flex-wrap:wrap}' +
    '.cu-pop button{font:600 13px Helvetica,Arial,sans-serif;padding:7px 10px;border:1.5px solid var(--ink,#1d2530);background:var(--paper,#f2eee3);color:var(--ink,#1d2530);cursor:pointer}' +
    '.cu-pop button.go{background:var(--ink,#1d2530);color:var(--paper,#f2eee3)}' +
    '.cu-pop .idle{margin:0 0 10px;min-height:2.9em;transition:opacity .45s}.cu-pop .idle.fade{opacity:0}' +
    '.cu-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}' +
    '@media (prefers-reduced-motion:reduce){.cu-pop .idle,.cu-ring circle{transition:none}}' +
    '.cu-pop small{display:block;color:var(--muted,#7a7566);font:11px/1.4 Menlo,monospace;margin-top:6px}' +
    '@media print{.cu-plane,.cu-pop{display:none!important}}';
  document.head.appendChild(css);

  var btn = document.createElement('button');
  btn.className = 'cu-plane'; btn.type = 'button';
  btn.setAttribute('aria-label', 'Modo avião: ler o site sem internet');
  btn.setAttribute('aria-expanded', 'false');
  btn.title = 'Modo avião';
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5z"/></svg>' +
    '<svg class="cu-ring" viewBox="0 0 30 30" aria-hidden="true"><circle cx="15" cy="15" r="14.5" pathLength="100"/></svg>';
  var pop = document.createElement('div');
  pop.className = 'cu-pop'; pop.hidden = true; pop.setAttribute('role', 'dialog'); pop.setAttribute('aria-label', 'Modo avião');
  document.body.appendChild(btn); document.body.appendChild(pop);

  // while saving, calm lines rotate instead of a file count; the bar still measures
  var IDLE = [
    'Pode continuar lendo enquanto isso.',
    'Guardando as aulas, uma por uma.',
    'Os desenhos vão junto com o texto.',
    'Dobrando as páginas com cuidado.',
    'Tudo fica neste aparelho, e só nele.',
    'Depois, é só abrir, com ou sem sinal.'
  ];
  var idleTimer = null, idleAt = 0;
  function stopIdle() { if (idleTimer) { clearInterval(idleTimer); idleTimer = null; } }
  function startIdle() {
    stopIdle();
    idleTimer = setInterval(function () {
      var el = pop.querySelector('.idle');
      if (!el) { stopIdle(); return; }
      el.classList.add('fade');
      setTimeout(function () { idleAt = (idleAt + 1) % IDLE.length; el.textContent = IDLE[idleAt]; el.classList.remove('fade'); }, 450);
    }, 4200);
  }
  var sizeMb = 0, ready = false, busy = false, last = ['off', {}], ringOff = null;
  var arc = btn.querySelector('.cu-ring circle');
  function ring(pct) {
    if (ringOff) { clearTimeout(ringOff); ringOff = null; }
    btn.classList.add('busy');
    arc.style.strokeDashoffset = String(100 - pct);
    btn.setAttribute('aria-label', 'Modo avião: guardando o site, ' + pct + '%');
  }
  function ringDone() {
    ring(100);
    // the full ring hands over to the orange circle of airplane mode
    ringOff = setTimeout(function () { btn.classList.remove('busy'); arc.style.strokeDashoffset = '100'; btn.setAttribute('aria-label', 'Modo avião: ler o site sem internet'); }, 700);
  }
  function loadSize() {
    if (sizeMb) return;
    fetch(root + 'offline-size.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (d) {
      sizeMb = d.mb; var el = pop.querySelector('[data-mb]'); if (el) el.textContent = 'cerca de ' + sizeMb + ' MB';
      if (d.facts && d.facts.length) { IDLE = d.facts.slice(); for (var i = IDLE.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), x = IDLE[i]; IDLE[i] = IDLE[j]; IDLE[j] = x; } }
    }).catch(function () {});
  }
  function view(state, extra) {
    extra = extra || {};
    btn.classList.toggle('on', get() === 'on');
    last = [state, extra];
    stopIdle();
    loadSize();
    if (state === 'off') pop.innerHTML = '<b class="t">Modo avião</b><p>Guarda o site inteiro neste aparelho (<span data-mb>cerca de ' + (sizeMb ? sizeMb + ' MB' : '… MB') + '</span>) para você ler sem internet: no avião, no ônibus, onde não tiver sinal. Os links continuam funcionando.</p><div class="row"><button class="go" data-a="on">Ativar</button><button data-a="close">Agora não</button></div>';
    if (state === 'busy') {
      idleAt = 0;
      pop.innerHTML = '<b class="t">Guardando o site…</b><p class="idle" aria-hidden="true">' + IDLE[0] + '</p><span class="cu-sr" role="status">Guardando o site neste aparelho.</span>';
      startIdle();
    }
    if (state === 'on') pop.innerHTML = '<span class="cu-sr" role="status">' + (extra.note ? 'Pronto. ' + extra.note : 'Modo avião ativo.') + '</span><b class="t">Modo avião ativo</b><p>O site está guardado neste navegador e abre mesmo sem internet. Com conexão, as páginas continuam se atualizando.</p><div class="row"><button data-a="refresh">Atualizar cópia</button><button data-a="off">Desativar</button><button data-a="close">Fechar</button></div>' + (extra.note ? '<small>' + extra.note + '</small>' : '')
    // while the backstage is still saving in the background, the facts keep turning under the note
    if (state === 'on' && extra.still) { pop.insertAdjacentHTML('beforeend', '<p class="idle" aria-hidden="true">' + IDLE[idleAt % IDLE.length] + '</p>'); startIdle(); }
    if (state === 'error') pop.innerHTML = '<span class="cu-sr" role="alert">Não deu para guardar o site.</span><b class="t">Não deu para guardar</b><p>Precisa de conexão para baixar a cópia. Tente de novo com internet.</p><div class="row"><button class="go" data-a="on">Tentar de novo</button><button data-a="close">Fechar</button></div>';
  }
  function open(v) { if (!v) stopIdle(); pop.hidden = !v; btn.setAttribute('aria-expanded', String(!!v)); }

  function withWorker(cb, quiet) {
    navigator.serviceWorker.register(root + 'sw.js', { scope: root }).then(function () {
      return navigator.serviceWorker.ready;
    }).then(function (reg) { cb(reg.active); }).catch(function () { if (!quiet) { view('error'); open(true); } });
  }
  navigator.serviceWorker.addEventListener('message', function (e) {
    var d = e.data || {};
    if (d.type === 'offline-progress') {
      // a page opened mid-download learns about it here
      if (!busy) { busy = true; if (!ready) last = ['busy', {}]; }
      ring(Math.round(100 * d.done / d.total));
    }
    if (d.type === 'offline-ready') { ready = true; set('on'); view('on', { note: 'Já dá para ler sem internet; o bastidor termina de baixar.', still: true }); }
    if (d.type === 'offline-done') { busy = ready = false; if (btn.classList.contains('busy')) ringDone(); set('on'); view('on', { note: d.files + ' arquivos guardados' + (d.failed ? ', ' + d.failed + ' falharam' : '') + (d.copied ? ' (' + d.copied + (d.copied === 1 ? ' já estava guardado)' : ' já estavam guardados)') : '') + '.' }); }
    if (d.type === 'offline-error') { busy = false; btn.classList.remove('busy'); view('error'); }
  });

  pop.addEventListener('click', function (e) {
    var a = e.target.getAttribute && e.target.getAttribute('data-a');
    if (!a) return;
    if (a === 'close') open(false);
    if (a === 'on' || a === 'refresh') {
      if (!navigator.onLine) { view('error'); return; }
      busy = true; view('busy', {}); ring(0);
      withWorker(function (w) { w.postMessage({ type: 'offline-download', force: a === 'refresh' }); });
    }
    if (a === 'off') {
      set(null);
      navigator.serviceWorker.getRegistrations().then(function (rs) {
        rs.forEach(function (r) { if (r.active) r.active.postMessage({ type: 'offline-wipe' }); r.unregister(); });
      });
      caches.keys().then(function (ks) { ks.forEach(function (k) { if (k.indexOf('ordenacoes-offline-') === 0) caches.delete(k); }); });
      view('off'); open(false);
    }
  });
  btn.addEventListener('click', function () {
    if (pop.hidden) { if (busy) view(last[0], last[1]); else view(get() === 'on' ? 'on' : 'off'); open(true); } else open(false);
  });
  // a press anywhere else folds the window away (the ring keeps showing the progress); pointerdown in the capture
  // phase, so a button that re-renders the window is still inside it when we look
  document.addEventListener('pointerdown', function (e) {
    if (!pop.hidden && !pop.contains(e.target) && !btn.contains(e.target)) open(false);
  }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') open(false); });

  if (get() === 'on') {
    btn.classList.add('on');
    // quietly refresh the saved copy when the site has changed: after the page has loaded (so Safari's bar isn't
    // held open by the 170 KB manifest on a weak signal, 18/10) and at most every 30 minutes
    var CHECKED = 'ordenacoes-offline-checked';
    var since = 0; try { since = Date.now() - Number(localStorage.getItem(CHECKED) || 0); } catch (e) {}
    if (navigator.onLine && since > 30 * 60 * 1000) {
      var check = function () {
        try { localStorage.setItem(CHECKED, String(Date.now())); } catch (e) {}
        withWorker(function (w) { w.postMessage({ type: 'offline-check' }); }, true);
      };
      var later = function () { setTimeout(function () { (window.requestIdleCallback || setTimeout)(check, { timeout: 5000 }); }, 2000); };
      if (document.readyState === 'complete') later(); else window.addEventListener('load', later, { once: true });
    }
  } else if (navigator.onLine) {
    // airplane mode off: the worker keeps a warm copy of what you read; on a fast connection with data saver off it
    // also warms the rest of this course once the page is idle, so turning airplane mode on has less left to fetch
    var c = navigator.connection || {};
    var m = location.pathname.match(/\/(courses\/[^\/]+\/)/);
    withWorker(function (w) {
      if (!m || c.saveData || (c.effectiveType && c.effectiveType !== '4g')) return;
      var go = function () { w.postMessage({ type: 'warm-course', prefix: m[1] }); };
      setTimeout(function () { (window.requestIdleCallback || setTimeout)(go, { timeout: 4000 }); }, 3000);
    }, true);
  }
})();
