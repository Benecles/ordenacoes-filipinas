/* Backstage: an Easter egg on the home page's paper. Nothing announces it.
   The drafting grid is pinned to the window on desktop (120 px squares of 5×5 cells of 24 px).
   In the square at column 2, row 3, four cells answer a click with a brief flash. Clicked clockwise
   from the top left, each within 2 s of the last, they mark the corners of a cut: the knife runs
   along the square's left, top and right edges, and the sheet falls away from the reader, hinged
   at its bottom, showing the backstage's surface under it (read live from backstage/bp.css) and the way backstage.
   Desktop and landscape only; reduced motion fades instead of folding. Chairman's idea, 07/10. */
(function () {
  var mq = window.matchMedia('(min-width: 1100px) and (hover: hover) and (pointer: fine) and (orientation: landscape)');
  var MAJOR = 120, CELL = 24, SQ = { x: 120, y: 240 };           // column 2, row 3 of the pinned grid
  var CORNERS = [[1, 1], [2, 1], [2, 2], [1, 2]];                 // TL, TR, BR, BL inside the square
  var TINT = ['var(--dif)', 'var(--conc)', '#e8c547', 'var(--ink)'];
  var WINDOW_MS = 2000, step = 0, last = 0, open = false, layer = null;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var FALL = window.__bsFall || 'drop';   // 'drop': falls through the hole · 'hang': swings toward you and dangles

  var css = document.createElement('style');
  css.textContent =
    '.bs-flash{position:fixed;width:' + CELL + 'px;height:' + CELL + 'px;pointer-events:none;z-index:60;opacity:0;animation:bs-flash .75s ease-out forwards}' +
    '@keyframes bs-flash{0%{opacity:0;transform:scale(.6)}18%{opacity:.9;transform:scale(1)}100%{opacity:0;transform:scale(1.15)}}' +
    '.bs-stage{position:fixed;left:' + SQ.x + 'px;top:' + SQ.y + 'px;width:' + MAJOR + 'px;height:' + MAJOR + 'px;z-index:55;perspective:420px}' +
    '.bs-stage.drop{overflow:hidden}' +
    '.bs-under{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background-size:150% auto;background-position:50% 30%;opacity:0;transition:opacity .2s ease .15s}' +
    '.bs-under::before{content:"";position:absolute;inset:0;box-shadow:inset 0 14px 22px rgba(0,0,0,.6),inset 0 0 28px rgba(0,0,0,.55);pointer-events:none}' +
    '.bs-stage.on .bs-under{opacity:1}' +
    '.bs-under a{position:relative;font:600 12px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;text-decoration:none;padding:8px 10px;border:1.5px solid currentColor}' +
    '.bs-under a:focus-visible{outline:2px solid var(--conc);outline-offset:3px}' +
    '.bs-flap{position:absolute;inset:0;transform-origin:50% 100%;transform-style:preserve-3d;will-change:transform}' +
    '.bs-face{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden}' +
    '.bs-front{background-color:var(--paper);background-image:linear-gradient(var(--grid-major) 1px,transparent 1px),linear-gradient(90deg,var(--grid-major) 1px,transparent 1px),linear-gradient(var(--grid) .5px,transparent .5px),linear-gradient(90deg,var(--grid) .5px,transparent .5px);background-size:120px 120px,120px 120px,24px 24px,24px 24px}' +
    '.bs-back{transform:rotateX(180deg);background-color:var(--paper);filter:brightness(.9);background-image:linear-gradient(90deg,var(--grid) .5px,transparent .5px),linear-gradient(var(--grid) .5px,transparent .5px);background-size:24px 24px;box-shadow:inset 0 0 0 1px var(--grid-major)}' +
    '.bs-stage.drop.on .bs-flap{animation:bs-drop .95s cubic-bezier(.5,0,.85,.35) forwards}' +
    '@keyframes bs-drop{0%{transform:rotateX(0)}100%{transform:rotateX(178deg)}}' +
    '.bs-stage.hang.on .bs-flap{animation:bs-hang 1.5s cubic-bezier(.3,0,.4,1) forwards;filter:drop-shadow(0 6px 6px rgba(0,0,0,.25))}' +
    '@keyframes bs-hang{0%{transform:rotateX(0)}38%{transform:rotateX(-192deg)}54%{transform:rotateX(-171deg)}68%{transform:rotateX(-186deg)}80%{transform:rotateX(-176deg)}90%{transform:rotateX(-182deg)}100%{transform:rotateX(-180deg)}}' +
    '.bs-stage.on .bs-flap{pointer-events:none}' +
    '.bs-cut{position:absolute;inset:-1px;overflow:visible;pointer-events:none}' +
    '.bs-cut path{fill:none;stroke:var(--ink);stroke-width:1.6;stroke-dasharray:360;stroke-dashoffset:360;animation:bs-cut .45s ease-in forwards}' +
    '@keyframes bs-cut{to{stroke-dashoffset:0}}' +
    '@media (prefers-reduced-motion: reduce){.bs-stage.on .bs-flap{animation:none;transition:opacity .3s;opacity:0}.bs-cut path{animation:none;stroke-dashoffset:0}}';
  document.head.appendChild(css);

  // behind the paper: the backstage's own surface, read from backstage/bp.css at load, so the peek always matches backstage
  var T = { mat: '#15386a', ink: '#f3f6fb', 'grid-major': 'rgba(243,246,251,.11)', grid: 'rgba(243,246,251,.045)' };
  try {
    var me = document.currentScript && document.currentScript.src;
    fetch(new URL('../backstage/bp.css', me || location.href)).then(function (r) { return r.ok ? r.text() : ''; }).then(function (t) {
      var root = (t.match(/:root\s*\{([^}]*)\}/) || [])[1] || '';
      Object.keys(T).forEach(function (k) { var m = root.match(new RegExp('--' + k + ':\\s*([^;]+);')); if (m) T[k] = m[1].trim(); });
    }).catch(function () {});
  } catch (e) {}
  function otherSide() {
    var MAT_LINE = T['grid-major'], MAT_FINE = T.grid;
    return { bg: T.mat, ink: T.ink,
      surface: 'background-image:linear-gradient(' + MAT_LINE + ' 1px,transparent 1px),linear-gradient(90deg,' + MAT_LINE + ' 1px,transparent 1px),' +
        'linear-gradient(' + MAT_FINE + ' 1px,transparent 1px),linear-gradient(90deg,' + MAT_FINE + ' 1px,transparent 1px);' +
        'background-size:' + MAJOR + 'px ' + MAJOR + 'px,' + MAJOR + 'px ' + MAJOR + 'px,' + CELL + 'px ' + CELL + 'px,' + CELL + 'px ' + CELL + 'px;background-position:0 0;' +
        'box-shadow:inset 0 0 0 1px rgba(243,246,251,.32)' };    // the square is one major cell: its major lines are its edges
  }

  function flash(i) {
    var d = document.createElement('div');
    d.className = 'bs-flash';
    d.style.left = (SQ.x + CORNERS[i][0] * CELL) + 'px';
    d.style.top = (SQ.y + CORNERS[i][1] * CELL) + 'px';
    d.style.background = TINT[i];
    d.style.boxShadow = '0 0 14px 3px ' + TINT[i];
    document.body.appendChild(d);
    setTimeout(function () { d.remove(); }, 800);
  }

  function reveal() {
    open = true;
    var s = otherSide();
    layer = document.createElement('div');
    layer.className = 'bs-stage ' + FALL;
    layer.innerHTML =
      '<div class="bs-under" style="background-color:' + s.bg + ';' + s.surface + ';color:' + s.ink + '">' +
      '<a href="backstage/" style="color:' + s.ink + ';background:' + s.bg + '">Backstage&nbsp;→</a></div>' +
      '<div class="bs-flap"><div class="bs-face bs-front" style="background-position:-' + SQ.x + 'px -' + SQ.y + 'px"></div><div class="bs-face bs-back"></div></div>' +
      '<svg class="bs-cut" viewBox="0 0 ' + MAJOR + ' ' + MAJOR + '" width="' + (MAJOR + 2) + '" height="' + (MAJOR + 2) + '" aria-hidden="true"><path d="M1 ' + (MAJOR + 1) + ' V1 H' + (MAJOR + 1) + ' V' + (MAJOR + 1) + '"/></svg>';
    document.body.appendChild(layer);
    var cut = layer.querySelector('.bs-cut');
    setTimeout(function () {
      layer.classList.add('on');
      setTimeout(function () { if (cut) cut.style.opacity = '0'; }, reduce.matches ? 50 : 500);
    }, reduce.matches ? 0 : 480);
  }

  function close() {
    if (!layer) return;
    var l = layer; layer = null; open = false;
    var f = l.querySelector('.bs-flap');
    f.style.transform = getComputedStyle(f).transform;      // freeze where the fall left it
    f.style.animation = 'none'; void f.offsetWidth;
    f.style.transition = 'transform .55s cubic-bezier(.2,.7,.3,1)';
    f.style.transform = 'rotateX(0deg)';
    setTimeout(function () { l.classList.remove('on'); }, 380);
    setTimeout(function () { l.remove(); }, 650);
  }

  function onPaper(t) {
    return !t.closest('a,button,input,label,summary,details,nav,header,footer,h1,h2,h3,p,li,svg,figure,.prancha,.patch-bento,.about,.hist-card');
  }

  // the egg exists only where all four cells are open paper (window ≥ ~1,500 px: the course cards sit right of column 2)
  function allClear() {
    return CORNERS.every(function (c) {
      var el = document.elementFromPoint(SQ.x + c[0] * CELL + CELL / 2, SQ.y + c[1] * CELL + CELL / 2);
      return el && (el.classList.contains('bs-flash') || onPaper(el));
    });
  }

  document.addEventListener('click', function (e) {
    if (!mq.matches) return;
    if (open) { if (!layer.contains(e.target)) close(); return; }
    if (!onPaper(e.target) || !allClear()) return;
    var cx = Math.floor((e.clientX - SQ.x) / CELL), cy = Math.floor((e.clientY - SQ.y) / CELL);
    var i = -1;
    for (var k = 0; k < 4; k++) if (CORNERS[k][0] === cx && CORNERS[k][1] === cy) i = k;
    var now = Date.now();
    if (i < 0) { step = 0; return; }
    flash(i);
    if (now - last > WINDOW_MS) step = 0;
    last = now;
    if (i === step) { step++; } else { step = (i === 0) ? 1 : 0; }
    if (step === 4) { step = 0; setTimeout(function () { CORNERS.forEach(function (_, j) { flash(j); }); reveal(); }, 260); }
  });

  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && open) close(); });
})();
