(function () {
  var key = 'ordenacoes-theme';
  var root = document.documentElement;

  try {
    if (localStorage.getItem(key) === 'dark') root.dataset.theme = 'dark';
  } catch (_) {}

  document.addEventListener('DOMContentLoaded', function () {
    var button = document.querySelector('.theme-toggle');
    if (!button) return;

    function sync() {
      button.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
    }

    sync();
    button.addEventListener('click', function () {
      var dark = root.dataset.theme !== 'dark';
      if (dark) root.dataset.theme = 'dark';
      else delete root.dataset.theme;
      try {
        localStorage.setItem(key, dark ? 'dark' : 'light');
      } catch (_) {}
      sync();
    });
  });
})();
