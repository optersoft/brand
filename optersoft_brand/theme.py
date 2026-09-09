"""The fleet's three-way colour theme — light / gray / dark — and the one script a page of
this chrome carries.

`dioxus_chrome::THEME_APPLY_SCRIPT` and `@optersoft/astro`'s `theme.ts` are the same two
pieces, so an Astro site, a Dioxus app and a frontage site read the same `localStorage` key,
set the same classes on `<html>` and paint the same bar colour. A reader who picks "Gray" on
optersoft.com expects academy and the product sites to follow.

⚠ `gray` is a **light-family** theme — dark text on a muted paper — so only true `dark` sets
`color-scheme: dark`.

**Why this is JavaScript and not an island.** The first half of it has to run *before first
paint*, or the page flashes the wrong colour scheme: there is no moment at which a runtime,
however small, could do that job. Once the page carries those twelve lines, the toggle's
three click handlers belong in them too — an island there would download a quarter of a
megabyte on every page of a content site to set a class and a `localStorage` key. So the
chrome is **zero runtime**, and the pages that use it ship no `<script src>` at all.
"""

THEMES = ("light", "gray", "dark")

#: The `localStorage` key the preference is kept under. optersoft.com's cookie notice names
#: it verbatim — renaming it is a copy change there too.
KEY = "color-theme"

#: The mobile browser chrome's colour per theme (`<meta name="theme-color">`).
BAR = {"light": "#ffffff", "gray": "#d9dde3", "dark": "#020617"}

#: Applied before first paint, and again on `DOMContentLoaded` in case anything stomped on
#: the class. Verbatim from `dioxus_chrome::THEME_APPLY_SCRIPT`.
APPLY = """
(function () {
  const BAR = { light: '#ffffff', gray: '#d9dde3', dark: '#020617' };
  const apply = () => {
    const t = localStorage.getItem('color-theme')
      || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const el = document.documentElement;
    el.classList.toggle('dark', t === 'dark');
    el.classList.toggle('gray', t === 'gray');
    el.style.colorScheme = t === 'dark' ? 'dark' : 'light';
    let m = document.querySelector('meta[name="theme-color"]');
    if (!m) { m = document.createElement('meta'); m.name = 'theme-color'; document.head.appendChild(m); }
    m.content = BAR[t] || BAR.light;
  };
  apply();
  document.addEventListener('DOMContentLoaded', apply);
})();
""".strip()

#: What the toggle's rows do, and the hamburger. Deferred: neither is needed before paint.
CONTROLS = """
(function () {
  const BAR = { light: '#ffffff', gray: '#d9dde3', dark: '#020617' };
  for (const row of document.querySelectorAll('#theme-menu button[data-theme]')) {
    row.addEventListener('click', () => {
      const t = row.dataset.theme || 'light';
      const el = document.documentElement;
      el.classList.toggle('dark', t === 'dark');
      el.classList.toggle('gray', t === 'gray');
      el.style.colorScheme = t === 'dark' ? 'dark' : 'light';
      localStorage.setItem('color-theme', t);
      let m = document.querySelector('meta[name="theme-color"]');
      if (!m) { m = document.createElement('meta'); m.name = 'theme-color'; document.head.appendChild(m); }
      m.content = BAR[t] || BAR.light;
      const d = document.getElementById('theme-details');
      if (d) d.open = false;
    });
  }
  const button = document.querySelector('button[aria-controls="navbar-menu"]');
  const menu = document.getElementById('navbar-menu');
  if (button && menu) {
    button.addEventListener('click', () => {
      const open = menu.classList.toggle('hidden') === false;
      button.setAttribute('aria-expanded', String(open));
    });
  }
})();
""".strip()
