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
});
