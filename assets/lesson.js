/* SVG object controls and paired visible state groups for shared lesson figures. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.interactive-figure').forEach(function (figure) {
    var svg = figure.querySelector('svg');
    var description = figure.querySelector('.object-description');
    if (!svg) return;
    var targets = Array.from(svg.querySelectorAll('[data-object]'));
    var states = Array.from(svg.querySelectorAll('[data-object-state][data-state="active"]'));
    var descriptions = {};
    var labels = {};
    figure.querySelectorAll('[data-object-label]').forEach(function (item) { labels[item.dataset.objectLabel] = item.textContent; });
    figure.querySelectorAll('[data-description-for]').forEach(function (item) { descriptions[item.dataset.descriptionFor] = item.textContent; });
    targets.forEach(function (target) {
      var id = target.dataset.object;
      target.setAttribute('role', 'button');
      target.setAttribute('tabindex', '0');
      target.setAttribute('aria-label', labels[id] || id);
      target.setAttribute('aria-pressed', 'false');
      if (description) target.setAttribute('aria-describedby', description.id);
    });
    function select(id) {
      svg.setAttribute('data-active-object', id);
      targets.forEach(function (target) {
        var active = target.dataset.object === id;
        target.setAttribute('aria-pressed', String(active));
        target.classList.toggle('is-active', active);
      });
      states.forEach(function (group) {
        if (group.dataset.objectState === id) group.removeAttribute('hidden');
        else group.setAttribute('hidden', 'hidden');
      });
      if (description) {
        description.textContent = descriptions[id] || labels[id] || id;
      }
    }
    targets.forEach(function (target) {
      target.addEventListener('click', function () { select(target.dataset.object); });
      target.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          select(target.dataset.object);
        }
      });
    });
    states.forEach(function (group) { group.setAttribute('hidden', 'hidden'); });
  });
});
