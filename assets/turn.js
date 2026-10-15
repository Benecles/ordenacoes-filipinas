// The turn: every sheet has a back. The dog-eared corner (bottom right) or ⌘⇧K turns the page over.
// Reader → backstage: the page slides down off the desk and the blueprint under it stays. Backstage → reader: the
// page slides back in from above. Loaded in <head> on every page (offline_build.py) so the arriving page can join.
// Cross-document view transitions where the browser has them (Safari 18.2+, Chrome 126+); elsewhere the leaving page
// plays its half alone. The transition is opted into only for a turn, so ordinary links never animate.
(function () {
  var KEY = 'ordenacoes-turn';
  var me = (document.currentScript && document.currentScript.src) || '';
  var base = me.replace(/assets\/turn\.js.*$/, '');
  if (!base) return;
  var root = document.documentElement;
  var here = location.href.split(/[?#]/)[0];
  var path = here.indexOf(base) === 0 ? here.slice(base.length) : '';
  var back = /^backstage\//.test(path);
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var crossDoc = 'PageRevealEvent' in window;
  var BP = '#15386a';
  var turning = false;

  // the sheet's other side: courses/<c>/<page> ↔ backstage/courses/<c>/<page>; the home ↔ the backstage's front door
  function other() {
    var p = path.replace(/index\.html$/, '');
    if (back) {
      var m = p.slice(10).match(/^(?:courses\/)?((?:controle|direito|metodologia|processo|teoria)[^/]*\/.*)$/);
      return base + (m ? 'courses/' + m[1] : '');
    }
    var c = p.match(/^courses\/([^/]+\/)([^/]*)$/) || p.match(/^courses\/([^/]+\/)/);   // deeper sheets: the course's back
    return base + (c ? 'backstage/courses/' + c[1] + (c[2] || '') : 'backstage/');
  }

  // the two halves of the motion, written only for the turn in progress
  var VT = {
    down: '@view-transition{navigation:auto}' +
      '::view-transition-group(root){animation:none}' +
      '::view-transition-old(root){z-index:2;transform-origin:50% 0;animation:turn-off .74s cubic-bezier(.55,0,.8,.3) both;' +
        'box-shadow:0 0 0 1px rgba(0,0,0,.12),0 -14px 34px rgba(0,0,0,.3)}' +
      '::view-transition-new(root){z-index:1;animation:turn-lights .74s ease-out both}' +
      '@keyframes turn-off{to{transform:translateY(104vh) rotate(1.1deg)}}' +
      '@keyframes turn-lights{from{filter:brightness(.72)}}',
    up: '@view-transition{navigation:auto}' +
      '::view-transition-group(root){animation:none}' +
      '::view-transition-old(root){z-index:1;animation:turn-dim .78s ease-in both}' +
      '::view-transition-new(root){z-index:2;transform-origin:50% 100%;animation:turn-on .78s cubic-bezier(.2,.9,.25,1.04) both;' +
        'box-shadow:0 0 0 1px rgba(0,0,0,.12),0 16px 34px rgba(0,0,0,.32)}' +
      '@keyframes turn-on{from{transform:translateY(-104vh) rotate(-.9deg)}}' +
      '@keyframes turn-dim{to{filter:brightness(.72)}}'
  };
  function style(id, css) {
    var s = document.getElementById(id) || document.createElement('style');
    s.id = id; s.textContent = css; (document.head || root).appendChild(s); return s;
  }

  // arriving: if this page was turned to, take part in the transition, then drop the opt-in again
  var dir = null;
  try { dir = sessionStorage.getItem(KEY); sessionStorage.removeItem(KEY); } catch (e) {}
  if (dir === 'down' || dir === 'up') {
    if (crossDoc) {
      var s = style('turn-vt', VT[dir]);
      addEventListener('pagereveal', function (e) {
        var t = e.viewTransition; if (!t) { s.remove(); return; }
        t.finished.then(function () { s.remove(); }, function () { s.remove(); });
      }, { once: true });
    } else if (dir === 'up' && !reduce) {   // no cross-document transitions: the page still comes in from above
      style('turn-in', 'html.turn-in{background:' + BP + '!important}html.turn-in body{transform:translateY(-104vh)}');
      root.classList.add('turn-in');
      addEventListener('DOMContentLoaded', function () {
        requestAnimationFrame(function () { requestAnimationFrame(function () {
          document.body.style.transition = 'transform .78s cubic-bezier(.2,.9,.25,1.04)';
          root.classList.remove('turn-in');
          setTimeout(function () { document.body.style.transition = ''; }, 900);
        }); });
      });
    }
  }
  // leaving for an ordinary link with an opt-in still present: no animation
  addEventListener('pageswap', function (e) { if (e.viewTransition && !turning) e.viewTransition.skipTransition(); });

  function turn() {
    if (turning) return; turning = true;
    var to = other(), d = back ? 'up' : 'down';
    if (reduce) { location.href = to; return; }
    try { sessionStorage.setItem(KEY, d); } catch (e) {}
    if (crossDoc) { style('turn-vt', VT[d]); location.href = to; return; }
    if (d === 'down') {   // no cross-document transitions: this page slides off alone, then the back loads
      style('turn-out', 'html.turn-out{background:' + BP + '!important;overflow:hidden}' +
        'html.turn-out body{background:var(--paper,#f2eee3);transition:transform .7s cubic-bezier(.55,0,.8,.3);' +
        'transform:translateY(104vh) rotate(1.1deg);transform-origin:50% 0;box-shadow:0 -14px 34px rgba(0,0,0,.3)}');
      root.classList.add('turn-out');
      setTimeout(function () { location.href = to; }, 680);
    } else {
      location.href = to;
    }
  }
  addEventListener('pageshow', function (e) {   // back-forward cache: come back as an untouched sheet
    if (!e.persisted) return; turning = false; root.classList.remove('turn-out');
    var s = document.getElementById('turn-vt'); if (s) s.remove();
  });

  // ⌘⇧K (free in Safari; chairman 15/10). ⌃⌘B, the first key for this, still works.
  addEventListener('keydown', function (e) {
    var k = e.code === 'KeyK' && e.metaKey && e.shiftKey && !e.ctrlKey && !e.altKey;
    var b = e.code === 'KeyB' && e.metaKey && e.ctrlKey && !e.shiftKey && !e.altKey;
    if (!k && !b) return;
    if (b && window.__bsEgg) return;   // the home page plays its fold on ⌃⌘B and goes itself
    if (e.target.closest && e.target.closest('input, textarea, [contenteditable]')) return;
    e.preventDefault(); turn();
  });

  // the corner: dog-eared, showing a sliver of the other side. The blueprint is the house's inspect element (chairman
// 15/10): on the reader it is always there but never announced — invisible, unlabelled, out of the tab order, it
// curls only when the pointer reaches the very corner. Backstage it stays in view, labelled.
  function corner() {
    if (document.querySelector('.turn-corner')) return;
    style('turn-css',
      '.turn-corner{position:fixed;right:0;bottom:0;z-index:84;width:34px;height:34px;display:block;cursor:pointer;' +
        'transition:width .32s cubic-bezier(.3,1.5,.5,1),height .32s cubic-bezier(.3,1.5,.5,1);-webkit-tap-highlight-color:transparent}' +
      '.turn-corner:hover,.turn-corner:focus-visible{width:62px;height:62px;outline:none}' +
      '.turn-corner.quiet{width:22px;height:22px;opacity:0;transition:opacity .25s,width .32s cubic-bezier(.3,1.5,.5,1),height .32s cubic-bezier(.3,1.5,.5,1)}' +
      '.turn-corner.quiet:hover{width:46px;height:46px;opacity:1}' +
      '.turn-corner:active{width:72px;height:72px}' +
      '.turn-corner svg{display:block;width:100%;height:100%;overflow:visible}' +
      '.turn-corner .under{fill:#0b1f3d}' +
      '.turn-corner .flap{filter:drop-shadow(-1.5px -1.5px 2px rgba(0,0,0,.28))}' +
      '.turn-corner .crease{stroke:rgba(255,255,255,.35);stroke-width:1;vector-effect:non-scaling-stroke}' +
      '.turn-corner .ln{stroke-width:1;vector-effect:non-scaling-stroke}' +
      '@media print{.turn-corner{display:none}}');
    var a = document.createElement('a');
    a.className = back ? 'turn-corner' : 'turn-corner quiet'; a.href = other();
    if (back) { a.setAttribute('aria-label', 'Front of house · ⌘⇧K'); a.title = 'Front of house · ⌘⇧K'; }
    else { a.tabIndex = -1; a.setAttribute('aria-hidden', 'true'); }
    // the flap is the sheet's own corner folded back: on the reader its back is the blueprint (white drafting
    // lines); backstage its back is the reader's paper (ruled text lines)
    var flap = back
      ? '<path class="flap" d="M100 0 L0 100 L0 0 Z" fill="#f2eee3"/>' +
        '<g class="ln" stroke="#1d2530" opacity=".45"><path d="M12 22 H70"/><path d="M12 36 H56"/><path d="M12 50 H42"/><path d="M12 64 H28"/></g>'
      : '<path class="flap" d="M100 0 L0 100 L0 0 Z" fill="' + BP + '"/>' +
        '<g class="ln" stroke="#f3f6fb" opacity=".5"><path d="M18 0 V82"/><path d="M0 30 H70"/><path d="M40 0 V60" stroke-dasharray="3 3"/><circle cx="18" cy="30" r="6" fill="none"/></g>';
    a.innerHTML = '<svg viewBox="0 0 100 100" aria-hidden="true"><path class="under" d="M100 0 L100 100 L0 100 Z"/>' + flap +
      '<path class="crease" d="M100 0 L0 100"/></svg>';
    a.addEventListener('click', function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;   // new tab etc. stay ordinary links
      e.preventDefault(); turn();
    });
    document.body.appendChild(a);
  }
  if (document.body) corner(); else addEventListener('DOMContentLoaded', corner);
  // any link marked data-turn (the back's "↺ the front") plays the same turn
  addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-turn]');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
    e.preventDefault(); turn();
  });
})();
