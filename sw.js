/* modo avião
   Service worker. With airplane mode on (assets/offline.js) it keeps a copy of every file in
   offline-manifest.json so the site works without a connection. With it off, it keeps a warm copy of what the
   reader has already opened (no extra downloads) and, on a fast connection, of the course they are in; turning
   airplane mode on then copies those instead of fetching them again (16/10). */
const PREFIX = 'ordenacoes-offline-';
const FONT_CACHE = 'ordenacoes-offline-fonts';
const ROOT = self.registration.scope; // …/ordenacoes-filipinas/
const NAV_TIMEOUT = 3500;
const WARM = PREFIX + 'warm';

async function sha10(buf) {
  const d = new Uint8Array(await crypto.subtle.digest('SHA-1', buf));
  return Array.from(d.slice(0, 5), (b) => b.toString(16).padStart(2, '0')).join('');
}
// keep a copy of a response we already have, tagged with its content hash (the manifest's hash)
async function warmPut(url, r) {
  try {
    if (!r || !r.ok || r.type !== 'basic' || (await currentCache())) return;
    const buf = await r.arrayBuffer();
    const h = new Headers(r.headers); h.set('x-sha', await sha10(buf));
    await (await caches.open(WARM)).put(url, new Response(buf, { status: 200, headers: h }));
  } catch (e) {}
}

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));

// Caches are named PREFIX + start time + version; a copy is served only once it carries the DONE marker,
// so a half-written update never answers a request (16/10: the old sort picked a random hash).
const DONE = '__offline_complete__';
const META = '__offline_manifest__';
let active = null, checked = false;
async function completeCaches() {
  const keys = (await caches.keys()).filter((k) => k.startsWith(PREFIX) && k !== FONT_CACHE).sort().reverse();
  const out = [];
  const legacy = [];
  for (const k of keys) {
    const c = await caches.open(k);
    if (/^ordenacoes-offline-[0-9a-f]{12}$/.test(k)) legacy.push([k, c]);  // saved before 16/10: complete by construction
    else if (await c.match(new URL(DONE, ROOT).href)) out.push([k, c]);
  }
  return out.concat(legacy);
}
async function currentCache() {
  if (checked) return active;
  const all = await completeCaches();
  checked = true;
  return (active = all.length ? all[0][1] : null);
}

async function broadcast(msg) {
  for (const c of await self.clients.matchAll({ includeUncontrolled: true })) c.postMessage(msg);
}

async function cacheFonts(cssUrls) {
  const fonts = await caches.open(FONT_CACHE);
  await Promise.all([...cssUrls].map(async (u) => {
    try {
      const r = await fetch(u, { mode: 'cors' });
      if (!r.ok) return;
      const css = await r.clone().text();
      await fonts.put(u, r);
      await Promise.all([...css.matchAll(/url\((https:\/\/fonts\.gstatic\.com\/[^)]+)\)/g)].map(async (m) => {
        if (await fonts.match(m[1])) return;
        try { const f = await fetch(m[1], { mode: 'cors' }); if (f.ok) await fonts.put(m[1], f); } catch (e) {}
      }));
    } catch (e) {}
  }));
}

async function download(force) {
  const res = await fetch(new URL('offline-manifest.json', ROOT), { cache: 'no-store' });
  const man = await res.json();
  const done0 = await completeCaches();
  const prev = done0.length ? done0[0] : null;
  if (!force && prev && prev[0].endsWith('-' + man.version)) {
    await broadcast({ type: 'offline-done', version: man.version, files: man.files.length, fresh: false, bytes: man.bytes }); return;
  }
  // resume: a download of this same version that stopped halfway (lost signal, closed tab) is picked up, not restarted
  const partial = (await caches.keys()).filter((k) => k.startsWith(PREFIX) && k.endsWith('-' + man.version) && k !== FONT_CACHE).sort().pop();
  const name = (!force && partial) || (PREFIX + Date.now() + '-' + man.version);
  const cache = await caches.open(name);
  const have = new Set((await cache.keys()).map((r) => r.url));
  // what the previous copy holds, by content hash: unchanged files are copied across, never fetched again
  let old = {}, oldCache = null;
  if (prev && !force) {
    oldCache = prev[1];
    const m = await oldCache.match(new URL(META, ROOT).href);
    if (m) old = (await m.json()).hash || {};
  }
  const hash = man.hash || {};
  const warm = (await caches.has(WARM)) ? await caches.open(WARM) : null;
  const total = man.files.length, reader = man.reader || total;
  const fontCss = new Set();
  const fontsOf = (t) => { for (const m of String(t || '').matchAll(/https:\/\/fonts\.googleapis\.com\/css2\?[^"')\s]+/g)) fontCss.add(m[0].replace(/&amp;/g, '&')); };
  let done = 0, failed = 0, copied = 0, next = 0, readySent = false;
  async function one(path) {
    const url = new URL(path, ROOT).href;
    const page = /\.html$|\/$/.test(path);
    if (have.has(url)) { copied++; if (page && fontCss.size < 3) { const c = await cache.match(url); if (c) fontsOf(await c.text()); } return; }
    if (warm && hash[path]) {
      const w = await warm.match(url);
      if (w && w.headers.get('x-sha') === hash[path]) { await cache.put(url, w); copied++; return; }
    }
    if (oldCache && hash[path] && old[path] === hash[path]) {
      const hit = await oldCache.match(url);
      if (hit) { await cache.put(url, hit); copied++; return; }
    }
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const r = await fetch(url, { cache: attempt ? 'reload' : 'no-cache' });
        if (!r.ok) throw new Error(r.status);
        if (page) fontsOf(await r.clone().text());
        await cache.put(url, r); return;
      } catch (e) { if (attempt === 2) failed++; else await new Promise((ok) => setTimeout(ok, 300 * (attempt + 1))); }
    }
  }
  const readerSet = new Set(man.files.slice(0, reader));
  let readerLeft = readerSet.size;
  function tick(path) {
    done++;
    if (readerSet.has(path) && --readerLeft === 0 && !readySent) { readySent = true; broadcast({ type: 'offline-ready', done, total }); }
    if (done % 10 === 0 || done === total) broadcast({ type: 'offline-progress', done, total });
  }
  // can this file be had without the network (resumed copy, warm copy, unchanged in the old copy)?
  async function local(path) {
    const url = new URL(path, ROOT).href;
    if (have.has(url)) return true;
    if (warm && hash[path]) { const w = await warm.match(url); if (w && w.headers.get('x-sha') === hash[path]) return true; }
    return !!(oldCache && hash[path] && old[path] === hash[path] && (await oldCache.match(url)));
  }
  const TYPES = { html: 'text/html; charset=utf-8', css: 'text/css', js: 'text/javascript', json: 'application/json', svg: 'image/svg+xml',
    jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp', gif: 'image/gif', ico: 'image/x-icon', woff2: 'font/woff2', woff: 'font/woff' };
  const typeOf = (p) => TYPES[(p.endsWith('/') ? 'html' : p.split('.').pop().toLowerCase())] || 'application/octet-stream';
  async function pack(k) {
    const need = [];
    for (const f of k.files) if (!(await local(f))) need.push(f);
    if (need.length <= 2) { for (const f of k.files) { await one(f); tick(f); } return; }  // a pack for 1-2 files isn't worth it
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const r = await fetch(new URL(k.u, ROOT).href);
        if (!r.ok) throw new Error(r.status);
        const put = async (f, body) => { await cache.put(new URL(f, ROOT).href, new Response(body, { headers: { 'Content-Type': typeOf(f) } })); };
        if (k.kind === 'text') {
          const all = await r.json();
          for (const f of k.files) { if (/\.html$|\/$/.test(f) && fontCss.size < 3) fontsOf(all[f]); await put(f, all[f]); tick(f); }
        } else {
          const buf = await r.arrayBuffer();
          for (const [f, off, len] of k.index) { await put(f, buf.slice(off, off + len)); tick(f); }
        }
        return;
      } catch (e) { if (attempt === 2) { for (const f of k.files) { await one(f); tick(f); } return; } await new Promise((ok) => setTimeout(ok, 400 * (attempt + 1))); }
    }
  }
  if (man.packs) {
    // packs (built at deploy): ~100 requests instead of ~1,300; 6 in flight, reader packs first
    let pi = 0;
    await Promise.all(Array.from({ length: 6 }, async () => { while (pi < man.packs.length) await pack(man.packs[pi++]); }));
  } else {
    // single files: reader pages first in the manifest; 16 in flight (HTTP/2 multiplexes them on one connection)
    await Promise.all(Array.from({ length: 16 }, async () => { while (next < total) { const f = man.files[next++]; await one(f); tick(f); } }));
  }
  await cacheFonts(fontCss);
  await cache.put(new URL(META, ROOT).href, new Response(JSON.stringify({ version: man.version, hash })));
  await cache.put(new URL(DONE, ROOT).href, new Response('1'));
  active = cache; checked = true;
  for (const k of await caches.keys()) if (k.startsWith(PREFIX) && k !== name && k !== FONT_CACHE) await caches.delete(k);
  await broadcast({ type: 'offline-done', version: man.version, files: total, failed, copied, fresh: true, bytes: man.bytes });
}

async function wipe() {
  active = null; checked = true;
  for (const k of await caches.keys()) if (k.startsWith(PREFIX)) await caches.delete(k);
  await broadcast({ type: 'offline-wiped' });
}

self.addEventListener('message', (e) => {
  const t = e.data && e.data.type;
  if (t === 'offline-download') e.waitUntil(download(!!e.data.force).catch((err) => broadcast({ type: 'offline-error', message: String(err) })));
  if (t === 'offline-check') e.waitUntil(download(false).catch(() => {}));
  if (t === 'offline-wipe') e.waitUntil(wipe());
  if (t === 'warm-course' && e.data.prefix) e.waitUntil(warmCourse(e.data.prefix).catch(() => {}));
});

function timeout(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), ms)); }

async function fromCache(req) {
  const cache = await currentCache();
  if (!cache) return null;
  let hit = await cache.match(req, { ignoreSearch: true });
  if (!hit && req.mode === 'navigate') {
    const u = new URL(req.url);
    if (u.pathname.endsWith('/')) hit = await cache.match(u.origin + u.pathname + 'index.html', { ignoreSearch: true });
    if (!hit) hit = await cache.match(new URL('index.html', ROOT).href);
  }
  return hit || null;
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    e.respondWith((async () => {
      const fonts = await caches.open(FONT_CACHE);
      const hit = await fonts.match(req.url);
      if (hit) return hit;
      const r = await fetch(req);
      if (r.ok && (await currentCache())) fonts.put(req.url, r.clone());
      return r;
    })());
    return;
  }
  if (!req.url.startsWith(ROOT) || url.pathname.endsWith('/sw.js') || url.pathname.endsWith('offline-manifest.json')) return;
  if (req.mode === 'navigate') {
    // Airplane mode on: the saved copy answers first, the network only for a page it doesn't hold (18/10: a
    // spotty connection made every click wait on the network). Updates still arrive: offline.js asks for an
    // offline-check on every page load, which fetches only what changed. Airplane mode off: just the network,
    // and a warm copy of what came back.
    e.respondWith((async () => {
      const saved = await currentCache();
      if (saved) {
        const u = new URL(req.url);
        const hit = (await saved.match(req, { ignoreSearch: true })) ||
          (u.pathname.endsWith('/') && (await saved.match(u.origin + u.pathname + 'index.html', { ignoreSearch: true })));
        if (hit) return hit;
      }
      try {
        const r = await (saved ? Promise.race([fetch(req), timeout(NAV_TIMEOUT)]) : fetch(req));
        if (!saved) e.waitUntil(warmPut(req.url, r.clone()));
        return r;
      }
      catch (err) { return (await fromCache(req)) || (await caches.match(req.url, { cacheName: WARM })) || new Response('<h1>Sem conexão</h1><p>Esta página ainda não foi guardada no modo avião.</p>', { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }); }
    })());
    return;
  }
  e.respondWith((async () => {
    const hit = await fromCache(req);
    if (hit) return hit;
    try { const r = await fetch(req); e.waitUntil(warmPut(req.url, r.clone())); return r; }
    catch (err) { const w = await caches.match(req.url, { cacheName: WARM, ignoreSearch: true }); if (w) return w; throw err; }
  })());
});

// warm the course the reader is in, two requests at a time, skipping what is already warm (offline.js asks only on
// a fast connection with data saver off, after the page is idle)
async function warmCourse(prefix) {
  if (await currentCache()) return;
  const man = await (await fetch(new URL('offline-manifest.json', ROOT))).json();
  const warm = await caches.open(WARM);
  const todo = man.files.filter((f) => f.startsWith(prefix) && !f.endsWith('/'));
  let i = 0;
  async function worker() {
    while (i < todo.length) {
      const f = todo[i++], url = new URL(f, ROOT).href;
      const w = await warm.match(url);
      if (w && w.headers.get('x-sha') === man.hash[f]) continue;
      try { await warmPut(url, await fetch(url)); } catch (e) {}
    }
  }
  await Promise.all([worker(), worker()]);
}
