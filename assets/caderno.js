/* Caderno local: imported values remain text and links are rebuilt from validated paths. */
(function () {
  'use strict';
  var KEY_BM = 'ordenacoes-bm', PREFIX_HL = 'ordenacoes-hl:', MAX_FILE = 2 * 1024 * 1024, MAX_ITEMS = 1500;
  var root = document.getElementById('caderno-app');
  if (!root) return;
  var list = root.querySelector('.entries'), empty = root.querySelector('.empty'), status = root.querySelector('[role="status"]');
  var memoryBookmarks = [], unavailable = false;

  function normalizePath(value) {
    if (typeof value !== 'string' || value.length > 240 || !value.startsWith('/') || value.indexOf('\\') >= 0) return null;
    var url;
    try { url = new URL(value, location.origin); } catch (_) { return null; }
    if (url.origin !== location.origin || url.search || url.hash || url.username || url.password) return null;
    var path = url.pathname.replace(/\/index\.html$/i, '/');
    if (!/^\/courses\/[a-z0-9-]+\/(?:aula-[a-z0-9][a-z0-9-]*|unidade-[a-z0-9][a-z0-9-]*|suplemento-[a-z0-9][a-z0-9-]*|revisao(?:-[a-z0-9][a-z0-9-]*)?)\.html$/i.test(path)) return null;
    return path;
  }
  function plainObject(v) { return !!v && typeof v === 'object' && !Array.isArray(v) && (Object.getPrototypeOf(v) === Object.prototype || Object.getPrototypeOf(v) === null); }
  function validBookmark(v) {
    if (!plainObject(v)) return null;
    var path = normalizePath(v.path), id = v.chapterId;
    if (!path || typeof id !== 'string' || !/^[\w-]{1,120}$/.test(id)) return null;
    if (typeof v.course !== 'string' || v.course.length > 120 || typeof v.lessonTitle !== 'string' || v.lessonTitle.length > 180 || typeof v.chapterTitle !== 'string' || v.chapterTitle.length > 240) return null;
    if (typeof v.created !== 'string' || v.created.length > 40) return null;
    return { path: path, course: v.course, lessonTitle: v.lessonTitle, chapterId: id, chapterTitle: v.chapterTitle, created: v.created };
  }
  function validHighlight(v) {
    if (!plainObject(v) || typeof v.id !== 'string' || !/^[\w-]{1,120}$/.test(v.id)) return null;
    if (!Number.isSafeInteger(v.s) || !Number.isSafeInteger(v.e) || v.s < 0 || v.e <= v.s || v.e - v.s > 12000) return null;
    // highlight.js stores the colour as a string ("1"–"5"); until 16/10 this check wanted a number and dropped every mark
    var c = typeof v.c === 'string' && /^[1-5]$/.test(v.c) ? +v.c : v.c;
    if (typeof v.q !== 'string' || !v.q.trim() || v.q.length > 12000 || !Number.isInteger(c) || c < 1 || c > 5) return null;
    return { id: v.id, s: v.s, e: v.e, q: v.q, c: c };
  }
  function readBookmarks() {
    try {
      var raw = localStorage.getItem(KEY_BM), parsed = raw ? JSON.parse(raw) : [];
      if (!Array.isArray(parsed) || parsed.length > MAX_ITEMS) return [];
      return parsed.map(validBookmark).filter(Boolean);
    } catch (_) { unavailable = true; return []; }
  }
  function readHighlights() {
    var result = Object.create(null), keys = [];
    try {
      for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && k.indexOf(PREFIX_HL) === 0) keys.push(k); }
      keys.forEach(function (key) {
        var path = normalizePath(key.slice(PREFIX_HL.length));
        if (!path) return;
        var data = JSON.parse(localStorage.getItem(key) || '[]');
        if (!Array.isArray(data)) return;
        result[path] = data.slice(0, MAX_ITEMS).map(validHighlight).filter(Boolean);
      });
    } catch (_) { unavailable = true; }
    return result;
  }
  function say(message) { status.textContent = message; }
  function slugTitle(slug) {
    return slug.replace(/\.html$/i, '').replace(/-/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
  }
  function pageLabel(path, bookmark) {
    if (bookmark && bookmark.lessonTitle) return bookmark.lessonTitle;
    return slugTitle(path.split('/').pop());
  }
  function courseLabel(path, bookmark) {
    return bookmark && bookmark.course ? bookmark.course : slugTitle(path.split('/')[2]);
  }
  function safeLink(path, hash) {
    var a = document.createElement('a');
    a.href = path + hash;
    return a;
  }
  function makeEntry(type, path, mark) {
    var li = document.createElement('li'), main = document.createElement('div'), kind = document.createElement('span'), a, del = document.createElement('button');
    li.className = 'entry'; li.setAttribute('data-entry', ''); li.dataset.type = type; li.dataset.path = path;
    main.className = 'entry-main'; kind.className = 'entry-kind'; kind.textContent = type === 'bookmark' ? 'Capítulo guardado' : 'Trecho marcado'; main.appendChild(kind);
    if (type === 'bookmark') {
      li.dataset.chapterId = mark.chapterId;
      a = safeLink(path, '#' + encodeURIComponent(mark.chapterId));
      a.textContent = mark.chapterTitle || mark.chapterId;
    } else {
      li.dataset.highlightId = mark.id;
      a = safeLink(path, '#hl=' + encodeURIComponent(mark.id));
      a.textContent = 'Abrir trecho marcado';
      var quote = document.createElement('blockquote'); quote.textContent = mark.q; main.appendChild(quote);
    }
    main.insertBefore(a, main.children[1] || null);
    del.type = 'button'; del.className = 'delete'; del.setAttribute('data-delete', ''); del.textContent = 'Apagar';
    del.setAttribute('aria-label', 'Apagar ' + (type === 'bookmark' ? 'capítulo guardado' : 'trecho marcado'));
    li.append(main, del); return li;
  }
  function render() {
    memoryBookmarks = readBookmarks();
    var highlights = readHighlights(), groups = Object.create(null), count = 0;
    memoryBookmarks.forEach(function (b) {
      var key = b.path;
      if (!groups[key]) groups[key] = { path: key, course: courseLabel(key, b), lesson: pageLabel(key, b), bookmarks: [], highlights: [] };
      groups[key].bookmarks.push(b);
    });
    Object.keys(highlights).forEach(function (path) {
      (highlights[path] || []).forEach(function (h) {
        if (!groups[path]) groups[path] = { path: path, course: courseLabel(path), lesson: pageLabel(path), bookmarks: [], highlights: [] };
        groups[path].highlights.push(h);
      });
    });
    list.replaceChildren();
    var byCourse = Object.create(null);
    Object.keys(groups).sort().forEach(function (path) {
      var g = groups[path], c = byCourse[g.course] || (byCourse[g.course] = []); c.push(g);
    });
    Object.keys(byCourse).sort().forEach(function (course) {
      var section = document.createElement('section'), h2 = document.createElement('h2');
      section.className = 'course-group'; h2.textContent = course; section.appendChild(h2);
      byCourse[course].sort(function (a,b) { return a.path.localeCompare(b.path); }).forEach(function (g) {
        var block = document.createElement('section'), h3 = document.createElement('h3'), ol = document.createElement('ol');
        block.className = 'lesson-group'; h3.textContent = g.lesson; ol.className = 'entry-list';
        g.bookmarks.forEach(function (b) { ol.appendChild(makeEntry('bookmark', g.path, b)); count++; });
        g.highlights.slice().sort(function (a,b) { return a.s - b.s; }).forEach(function (h) { ol.appendChild(makeEntry('highlight', g.path, h)); count++; });
        block.append(h3, ol); section.appendChild(block);
      });
      list.appendChild(section);
    });
    empty.hidden = count > 0;
    if (count) list.hidden = false;
    else list.hidden = true;
  }
  function getData() { return { version: 1, bookmarks: readBookmarks(), highlights: readHighlights() }; }
  function canStore() { try { var s = localStorage; var k = '__ordenacoes_test__'; s.setItem(k, '1'); s.removeItem(k); return true; } catch (_) { unavailable = true; return false; } }
  function saveBookmarks(items) { try { localStorage.setItem(KEY_BM, JSON.stringify(items)); return true; } catch (_) { unavailable = true; return false; } }
  function identityHighlight(h) { return h.id + '\u0000' + h.q; }
  function exportJSON() {
    unavailable = false;
    var data = getData();
    if (unavailable) { say('Não foi possível ler as marcações guardadas neste navegador.'); return false; }
    var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }), url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = 'meu-caderno-ordenacoes-filipinas.json'; a.click(); setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    say('Arquivo JSON preparado para download.'); return data;
  }
  function validateImport(raw) {
    if (!plainObject(raw) || raw.version !== 1 || !Array.isArray(raw.bookmarks) || !plainObject(raw.highlights)) throw new Error('Formato inválido: use um arquivo JSON v1 do caderno.');
    if (raw.bookmarks.length > MAX_ITEMS) throw new Error('O arquivo tem marcações demais.');
    var bookmarks = raw.bookmarks.map(validBookmark);
    if (bookmarks.some(function (b) { return !b; })) throw new Error('Há um capítulo ou caminho inválido no arquivo.');
    var total = 0, highlights = Object.create(null);
    Object.keys(raw.highlights).forEach(function (rawPath) {
      var path = normalizePath(rawPath), arr = raw.highlights[rawPath];
      if (!path || !Array.isArray(arr) || arr.length > MAX_ITEMS) throw new Error('Há um caminho ou lista de trechos inválida no arquivo.');
      total += arr.length; if (total > MAX_ITEMS) throw new Error('O arquivo tem marcações demais.');
      var items = arr.map(validHighlight);
      if (items.some(function (h) { return !h; })) throw new Error('Há um trecho inválido no arquivo.');
      highlights[path] = (highlights[path] || []).concat(items);
    });
    return { bookmarks: bookmarks, highlights: highlights };
  }
  function mergeImport(data) {
    if (!canStore()) throw new Error('Este navegador não permite guardar marcações. Nada foi importado.');
    var existingB = readBookmarks(), existingH = readHighlights();
    if (unavailable) throw new Error('Não foi possível ler as marcações guardadas. Nada foi importado.');
    var bmKeys = Object.create(null), added = 0;
    existingB.forEach(function (b) { bmKeys[b.path + '\u0000' + b.chapterId] = true; });
    data.bookmarks.forEach(function (b) { var k = b.path + '\u0000' + b.chapterId; if (!bmKeys[k]) { existingB.push(b); bmKeys[k] = true; added++; } });
    var nextH = Object.create(null);
    Object.keys(existingH).forEach(function (p) { nextH[p] = existingH[p].slice(); });
    Object.keys(data.highlights).forEach(function (path) {
      var arr = nextH[path] || (nextH[path] = []), seen = Object.create(null);
      arr.forEach(function (h) { seen[identityHighlight(h)] = true; });
      data.highlights[path].forEach(function (h) { var k = identityHighlight(h); if (!seen[k]) { arr.push(h); seen[k] = true; added++; } });
    });
    try {
      if (existingB.length || data.bookmarks.length) localStorage.setItem(KEY_BM, JSON.stringify(existingB));
      Object.keys(data.highlights).forEach(function (path) { localStorage.setItem(PREFIX_HL + path, JSON.stringify(nextH[path])); });
    } catch (_) { unavailable = true; throw new Error('O navegador não conseguiu guardar tudo. A importação pode estar incompleta.'); }
    return added;
  }
  root.addEventListener('click', function (event) {
    var button = event.target.closest('[data-delete]'); if (!button) return;
    var entry = button.closest('[data-entry]'), type = entry.dataset.type, path = normalizePath(entry.dataset.path);
    if (!path) return;
    try {
      if (type === 'bookmark') {
        var current = readBookmarks().filter(function (b) { return !(b.path === path && b.chapterId === entry.dataset.chapterId); });
        if (!saveBookmarks(current)) { say('Não foi possível apagar neste navegador.'); return; }
      } else {
        var key = PREFIX_HL + path, rows = JSON.parse(localStorage.getItem(key) || '[]'), id = entry.dataset.highlightId;
        if (!Array.isArray(rows)) throw new Error();
        var remaining = rows.filter(function (h) { return !(h && h.id === id); });
        if (remaining.length) localStorage.setItem(key, JSON.stringify(remaining)); else localStorage.removeItem(key);
      }
      say('Marcaçāo apagada.'); render();
    } catch (_) { unavailable = true; say('Não foi possível apagar neste navegador.'); }
  });
  root.querySelector('[data-export]').addEventListener('click', exportJSON);
  root.querySelector('[data-import]').addEventListener('change', function (event) {
    var file = event.target.files && event.target.files[0]; event.target.value = ''; if (!file) return;
    if (file.size > MAX_FILE) { say('Arquivo maior que o limite de 2 MB.'); return; }
    var reader = new FileReader();
    reader.onerror = function () { say('Não foi possível ler o arquivo.'); };
    reader.onload = function () {
      try {
        var raw = JSON.parse(String(reader.result)), clean = validateImport(raw), added = mergeImport(clean);
        render(); say(added ? added + ' marcação(ões) adicionada(s); conflitos mantidos como estavam.' : 'O arquivo não acrescentou marcações novas.');
      } catch (error) { say(error && error.message ? error.message : 'Arquivo inválido.'); }
    };
    reader.readAsText(file);
  });
  var theme = document.querySelector('.theme-toggle');
  if (theme) {
    function syncTheme() { var dark = document.documentElement.dataset.theme === 'dark'; theme.setAttribute('aria-pressed', String(dark)); }
    syncTheme(); theme.addEventListener('click', function () { var dark = document.documentElement.dataset.theme !== 'dark'; if (dark) document.documentElement.dataset.theme = 'dark'; else delete document.documentElement.dataset.theme; try { localStorage.setItem('ordenacoes-theme', dark ? 'dark' : 'light'); } catch (_) {} syncTheme(); });
  }
  window.OrdenacoesCaderno = { exportData: exportJSON, importData: function (raw) { try { var added = mergeImport(validateImport(raw)); render(); say(added ? added + ' marcação(ões) adicionada(s); conflitos mantidos como estavam.' : 'O arquivo não acrescentou marcações novas.'); return added; } catch (e) { say(e.message || 'Arquivo inválido.'); return false; } }, normalizePath: normalizePath };
  render();
})();
