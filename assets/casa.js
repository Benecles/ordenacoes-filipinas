/* CASA-1: translation toggle for source blocks (.fonte). Original stays the default; the translation sits under it. */
document.querySelectorAll('.fonte [data-tr]').forEach(function (b) {
  b.addEventListener('click', function () {
    var s = b.closest('.fonte'), t = s.querySelector('.tr'), show = t.hidden;
    t.hidden = !show;
    b.setAttribute('aria-expanded', String(show));
    b.textContent = show ? 'ocultar tradução' : 'ver tradução';
  });
});

/* CASA-2: exam items (.xq). Pick an option: it is marked, the key (data-key on the item, when a key exists) is shown,
   and the grounds open. Open questions open their grounds from "Ver fundamento". */
document.querySelectorAll('.xq').forEach(function (q) {
  var key = q.getAttribute('data-key'), verdict = q.querySelector('.xq-verdict'), show = q.querySelector('.xq-show');
  var opts = [].slice.call(q.querySelectorAll('.xq-opts button[data-opt]'));
  q.classList.add('armed');
  function open(on) { q.classList.toggle('open', on); if (show) { show.setAttribute('aria-expanded', String(on)); show.textContent = on ? 'Ocultar fundamento' : 'Ver fundamento'; } }
  opts.forEach(function (b) {
    b.setAttribute('aria-pressed', 'false');
    b.addEventListener('click', function () {
      var pick = b.getAttribute('data-opt');
      opts.forEach(function (o) {
        var mine = o === b, isKey = !!key && o.getAttribute('data-opt') === key;
        o.setAttribute('aria-pressed', String(mine));
        o.classList.toggle('key', isKey);
        o.classList.toggle('miss', mine && !!key && !isKey);
      });
      q.classList.add('done');
      if (verdict) verdict.textContent = !key ? 'Você marcou ' + pick + '.' : pick === key ? 'Você marcou ' + pick + ': correto.' : 'Você marcou ' + pick + '; a resposta é ' + key + '.';
      open(true);
    });
  });
  if (show) show.addEventListener('click', function () { open(!q.classList.contains('open')); });
  // once open, the reader can put the answer away again and retry (owner 12/11)
  var g = q.querySelector('.xq-ground > div');
  if (g && opts.length) {
    var hide = document.createElement('button');
    hide.type = 'button'; hide.className = 'xq-hide'; hide.textContent = 'Ocultar resposta';
    hide.addEventListener('click', function () {
      open(false); q.classList.remove('done');
      opts.forEach(function (o) { o.setAttribute('aria-pressed', 'false'); o.classList.remove('key', 'miss'); });
      if (verdict) verdict.textContent = '';
      var first = opts[0]; if (first) first.focus({ preventScroll: true });
    });
    g.appendChild(hide);
  }
});

/* CASA-3: universal scrollytelling fallback for any course (24/11). Activates .panel[id] matching
   the .step[data-panel] nearest the reading line; skips blocks already wired by a course's own curso.js. */
document.querySelectorAll('.scrolly').forEach(function (block) {
  var panels = [].slice.call(block.querySelectorAll('.panel[id]'));
  var steps = [].slice.call(block.querySelectorAll('.step[data-panel]'));
  if (!panels.length || !steps.length) return;
  if (block.querySelector('.panel.on') && window.__cursoScrolly) return;
  function activate(id) {
    panels.forEach(function (p) { p.classList.toggle('on', p.id === id); });
    steps.forEach(function (s) { s.classList.toggle('on', s.getAttribute('data-panel') === id); });
  }
  activate(steps[0].getAttribute('data-panel'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) activate(e.target.getAttribute('data-panel'));
      });
    }, { rootMargin: '-30% 0px -50% 0px', threshold: 0 });
    steps.forEach(function (s) { io.observe(s); });
  }
});

/* CASA-4: universal interactive case/regime switcher (.switcher).
   Buttons with [data-pick="key"] activate matching [data-view="key"] panels/explanations inside the same .switcher,
   letting any lesson build live hypothesis testers or regime comparators with zero per-page JS. */
document.querySelectorAll('.switcher').forEach(function (box) {
  var picks = [].slice.call(box.querySelectorAll('[data-pick]'));
  var views = [].slice.call(box.querySelectorAll('[data-view]'));
  if (!picks.length || !views.length) return;
  function select(key) {
    picks.forEach(function (b) {
      var on = b.getAttribute('data-pick') === key;
      b.classList.toggle('on', on);
      b.setAttribute('aria-pressed', String(on));
    });
    views.forEach(function (v) {
      var on = v.getAttribute('data-view') === key;
      v.classList.toggle('on', on);
      v.hidden = !on;
    });
  }
  picks.forEach(function (b) {
    b.addEventListener('click', function () { select(b.getAttribute('data-pick')); });
  });
  var initial = box.querySelector('[data-pick].on') || picks[0];
  select(initial.getAttribute('data-pick'));
});

/* CASA-6 (26/11): every choose-instrument wires itself. A figure holding [data-opt] choices and [data-ans] answers
   shows the answer whose key matches the chosen option, marks the choice pressed, and works by keyboard. No page
   script is needed (Aula 04 shipped four instruments whose page script named the wrong ids). Page scripts that do the
   same are harmless: picking is idempotent. Exam options (.xq-opts) are not figures and are left alone. */
[].forEach.call(document.querySelectorAll('figure'), function (f) {
  var opts = [].slice.call(f.querySelectorAll('[data-opt]')), ans = f.querySelectorAll('[data-ans]');
  if (!opts.length || !ans.length || f.hasAttribute('data-casa6')) return;
  f.setAttribute('data-casa6', '');
  var pick = function (k) {
    [].forEach.call(ans, function (a) { a.setAttribute('display', a.getAttribute('data-ans') === k ? 'inline' : 'none'); });
    opts.forEach(function (o) { o.setAttribute('aria-pressed', o.getAttribute('data-opt') === k ? 'true' : 'false'); });
  };
  opts.forEach(function (o) {
    o.style.cursor = 'pointer';
    if (!o.hasAttribute('tabindex')) o.setAttribute('tabindex', '0');
    if (!o.hasAttribute('role')) o.setAttribute('role', 'button');
    o.addEventListener('click', function () { pick(o.getAttribute('data-opt')); });
    o.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pick(o.getAttribute('data-opt')); } });
  });
});
