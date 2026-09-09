# CLAUDE.md

`optersoft-brand` is the Optersoft chrome as **frontage components**: what every page of an
Optersoft site has around its content. Python, rendered at build time by `frontage site`;
`README.md` is the usage.

## The two things that are not obvious

- **It ships no runtime, and that is a decision, not a limitation.** The theme has to be
  applied before first paint, so `theme.APPLY` is inline in the head; once a page carries
  that, `theme.CONTROLS` (the toggle's clicks and the hamburger) belongs with it rather than
  in an island that would download a runtime on every page. The locale switcher is plain
  links for the same reason — `frontage site` knows every URL. **Do not turn either into an
  island.** `ISLAND.md` §6 in the frontage repo has the reasoning; the plan expected islands
  here and was wrong.
- **`brand.css` has three copies.** Here, `astro/src/styles/brand.css` and
  `dioxus-chrome/assets/brand.css`. They may differ in the four `@font-face` `url()` lines
  and **nothing else** — Astro's are relative (Vite hashes them), Dioxus serves `/fonts/`,
  and this one is `/brand/fonts/`, which is where a site's `STATIC` puts them, because
  Tailwind's CLI does not rewrite a `url()` it reads through an `@import`. They have already
  drifted once (3,834 vs 4,429 bytes). This repository is meant to become the one copy.

## Layout

`optersoft_brand/`: `head.py` (the `<head>`), `shell.py` (the frame), `header.py` (navbar,
theme toggle, locale switcher, skip link), `footer.py`, `page.py` (page header, 404),
`theme.py` (the three-way theme and its two scripts), `links.py` / `labels.py` / `icons.py`
(the company, the words, the glyphs), `static/` (the stylesheets, the fonts, the mark).

## Rules

- **The ids and classes are `theme.css`'s contract**: `#theme-details`, `#theme-menu`,
  `.opt-light/.opt-gray/.opt-dark`, `.ic-sun/.ic-gray/.ic-moon`, `#navbar-menu`,
  `name="dx-nav-popover"`. Renaming one silently breaks the CSS that keys on it.
- **`collapse` is a measurement.** `lg` for a bar with a locale switcher and a sign-in
  button, `md` for a product site with four links — see the note in `header.py`.
- **`gray` is a light-family theme** — dark text on a muted paper. Only true `dark` sets
  `color-scheme: dark`.
- **Favicons are literal paths, never hashed.** Google re-crawls one on its own schedule and
  treats a moved one as new, so a hashed favicon can silently never appear in a result.
- The package is consumed as a **path dependency** (`optersoft-brand = { path = "../brand" }`)
  like every other sibling here, so there is nothing to bump and uncommitted edits ship with
  a deploy — commit the brand alongside the site that needs it.
