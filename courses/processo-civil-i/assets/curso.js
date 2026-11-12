// Scrollytelling: each .step names the figure panel it needs (data-panel).
// Without JS the first panel of each stage stays visible and the text reads normally.
(function () {
  if (!('IntersectionObserver' in window)) return;
  document.querySelectorAll('.scrolly').forEach(function (block) {
    var panels = block.querySelectorAll('.panel');
    var caption = block.querySelector('.stage-count');
    var steps = Array.prototype.slice.call(block.querySelectorAll('.step'));
    function show(step) {
      steps.forEach(function (s) { s.classList.toggle('on', s === step); });
      var id = step.getAttribute('data-panel');
      panels.forEach(function (p) {
        var on = p.id === id;
        if (on && !p.classList.contains('on')) {
          // restart draw-on strokes each time a panel comes back
          p.querySelectorAll('.grow,.pop,.fade,.pulse').forEach(function (g) { g.style.animation = 'none'; g.getBoundingClientRect(); g.style.animation = ''; });
        }
        p.classList.toggle('on', on);
      });
      if (caption) caption.textContent = step.getAttribute('data-slides') || '';
      var counter = block.querySelector('.stage-step');
      if (counter) counter.textContent = (steps.indexOf(step) + 1) + ' / ' + steps.length;
    }
    // A drawing that stays in place beside its passage (not a pinned .stage) changes state when a paragraph enters the
    // lower third, so the drawing is still on screen when it changes (owner 12/11: states arrived almost off screen).
    var fig = block.querySelector('figure, .stage');
    var inPlace = fig && getComputedStyle(fig).position !== 'sticky';
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) show(e.target); });
    }, { rootMargin: inPlace ? '-62% 0px -30% 0px' : '-45% 0px -45% 0px' });
    steps.forEach(function (s) { io.observe(s); });
  });
})();

// Reading progress hairline + remember the last lesson opened (per-viewer convenience only).
(function () {
  var m = location.pathname.match(/aula-(\d\d)\.html$/);
  if (!m) return;
  var bar = document.createElement('div');
  bar.className = 'read-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  function upd() {
    var h = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, scrollY / h) : 0) + ')';
  }
  addEventListener('scroll', upd, { passive: true });
  addEventListener('resize', upd);
  upd();
  try {
    var t = document.title.split(' · ')[0];
    if (!localStorage.getItem('ordenacoes-no-resume')) localStorage.setItem('ordenacoes-dla-last', JSON.stringify({ n: m[1], t: t }));
  } catch (e) {}
})();

// Printing: light theme, every answer open, and each step printed next to its own figure.
(function () {
  var saved = null, opened = [], clones = [];
  addEventListener('beforeprint', function () {
    var r = document.documentElement;
    saved = r.dataset.theme || null; delete r.dataset.theme;
    document.querySelectorAll('details:not([open])').forEach(function (d) { d.open = true; opened.push(d); });
    document.querySelectorAll('.scrolly .step').forEach(function (s) {
      var p = document.getElementById(s.getAttribute('data-panel'));
      var card = s.querySelector('.card');
      if (!p || !card) return;
      var c = p.cloneNode(true);
      c.removeAttribute('id'); c.classList.remove('panel', 'on'); c.classList.add('print-fig');
      c.querySelectorAll('[id]').forEach(function (n) { n.id = n.id + '-print'; });
      c.querySelectorAll('[marker-end]').forEach(function (n) { n.setAttribute('marker-end', n.getAttribute('marker-end').replace(/\)$/, '-print)')); });
      card.insertBefore(c, card.firstChild); clones.push(c);
    });
  });
  addEventListener('afterprint', function () {
    if (saved) document.documentElement.dataset.theme = saved;
    opened.forEach(function (d) { d.open = false; }); opened = [];
    clones.forEach(function (c) { c.remove(); }); clones = [];
  });
})();

// Figure elements with data-go="<panel id>" take the reader to the step that shows that panel.
(function () {
  function go(el) {
    var step = document.querySelector('.step[data-panel="' + el.getAttribute('data-go') + '"]');
    if (step) step.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('[data-go]');
    if (el) go(el);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var el = e.target.closest && e.target.closest('[data-go]');
    if (el) { e.preventDefault(); go(el); }
  });
})();

// Text ↔ figure links: everything sharing a data-lk key lights up together (hover, or tap on touch screens).
(function () {
  var groups = {};
  document.querySelectorAll('[data-lk]').forEach(function (el) {
    var k = el.getAttribute('data-lk');
    (groups[k] = groups[k] || []).push(el);
  });
  if (!Object.keys(groups).length) return;
  var pinned = null;
  function set(k, on) { (groups[k] || []).forEach(function (el) { el.classList.toggle('on', on); }); }
  document.addEventListener('mouseover', function (e) {
    var el = e.target.closest && e.target.closest('[data-lk]');
    if (el && !pinned) set(el.getAttribute('data-lk'), true);
  });
  document.addEventListener('mouseout', function (e) {
    var el = e.target.closest && e.target.closest('[data-lk]');
    if (el && !pinned) set(el.getAttribute('data-lk'), false);
  });
  document.addEventListener('click', function (e) {
    var el = e.target.closest && e.target.closest('.lk[data-lk]');
    if (pinned) { set(pinned, false); if (el && el.getAttribute('data-lk') === pinned) { pinned = null; return; } pinned = null; }
    if (el && matchMedia('(hover: none)').matches) { pinned = el.getAttribute('data-lk'); set(pinned, true); }
  });
})();

// "Place your bets": answers stay hidden until the reader picks an option; then the court's side is marked.
(function () {
  document.querySelectorAll('.bet').forEach(function (bet) {
    bet.classList.add('js-waiting');
    bet.querySelectorAll('button[data-opt]').forEach(function (b) {
      b.addEventListener('click', function () {
        bet.querySelectorAll('button[data-opt]').forEach(function (o) {
          o.setAttribute('aria-pressed', String(o === b));
          if (o.hasAttribute('data-court')) o.classList.add('court');
        });
        bet.classList.remove('js-waiting');
      });
    });
  });
})();

// Phone: tap a pinned figure to tuck it up for more reading room; tap again to bring it back. One setting for the page.
(function () {
  var mq = matchMedia('(max-width:860px) and (orientation:portrait)');
  var stages = document.querySelectorAll('.scrolly .stage');
  function mark() {
    stages.forEach(function (st) {
      var f = st.querySelector('figure');
      var ok = mq.matches && getComputedStyle(st).position === 'sticky';
      st.classList.toggle('tuckable', ok);
      if (!f) return;
      if (ok) { f.setAttribute('tabindex', '0'); f.setAttribute('role', 'button'); f.setAttribute('aria-expanded', String(!document.body.classList.contains('figs-tucked'))); }
      else { f.removeAttribute('tabindex'); f.removeAttribute('role'); f.removeAttribute('aria-expanded'); }
    });
  }
  function toggle() {
    var on = document.body.classList.toggle('figs-tucked');
    stages.forEach(function (s) { var f = s.querySelector('figure'); if (f && s.classList.contains('tuckable')) f.setAttribute('aria-expanded', String(!on)); });
  }
  stages.forEach(function (st) {
    var f = st.querySelector('figure');
    if (!f) return;
    f.addEventListener('click', function (e) {
      if (!st.classList.contains('tuckable') || e.target.closest('a,button,input,select,summary')) return;
      toggle();
    });
    f.addEventListener('keydown', function (e) {
      if ((e.key === 'Enter' || e.key === ' ') && st.classList.contains('tuckable') && e.target === f) { e.preventDefault(); toggle(); }
    });
  });
  mark();
  (mq.addEventListener ? mq.addEventListener('change', mark) : mq.addListener(mark));
})();
