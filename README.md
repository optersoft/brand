# optersoft-brand

The Optersoft chrome for [frontage](https://frontage.optersoft.com) sites: the layout, the header with the three-way theme toggle and the locale switcher, the footer with the company, the brand stylesheet and the fonts.

**It ships no runtime.** Every page of a site on this chrome is HTML and stops there — see [Why there is no island](#why-there-is-no-island).

```py
# site.py
import optersoft_brand
STATIC = [(optersoft_brand.static, "brand")]

# tailwind.css
# @import "tailwindcss";
# @import "../brand/optersoft_brand/static/styles/chrome.css";

# layouts/site.py
import optersoft_brand as brand

BRAND = {"href": "/", "name": "opter", "suffix": "soft", "logo": brand.LOGO}
LINKS = [brand.link("/", "Home"), brand.link("/about/", "About")]


def layout(children, title, description, **rest):
    return [brand.head(title, description, **rest), brand.shell(children, brand=BRAND, links=LINKS)]
```

Then `frontage site . --out public --tailwind`.

## What is in it

| | |
|---|---|
| `head(title, description, …)` | the `<head>` every page needs: the description, the social cards, the icons, and the pre-paint theme script |
| `shell(children, brand=…, links=…, langs=…)` | the frame: skip link, sticky header, `<main id="main">`, footer, and the deferred controls script |
| `header(...)`, `footer(...)` | the two halves, for a page that wants one without the other |
| `page_header(heading, label=…, intro=…)` | the eyebrow + h1 + intro block that opens a page |
| `not_found(heading, body, home=…)` | the branded 404 body, rendered inside your own shell |
| `theme_toggle`, `lang_switcher`, `skip_link` | the header's parts |
| `link`, `column`, `lang`, `OPTERSOFT_COLUMNS`, `SOCIALS` | the company, as links |
| `static` | the directory a site copies with `STATIC`: `styles/`, `fonts/`, `assets/` |

## Why there is no island

The theme has to be applied **before first paint** or the page flashes the wrong colour scheme, and nothing that has to be fetched can do that — not a 265 KB runtime, not a 2 KB one. So the chrome carries twelve inline lines in the head. Once a page carries those, the toggle's three click handlers belong with them: an island there would download a runtime on every page of a content site to set a class and a `localStorage` key.

The same reasoning made the locale switcher plain links: the build knows every URL, so there is nothing left to compute in a browser.

Two `<script>` elements with no `src`, and that is the whole of it.

## The brand, and the three copies of it

`static/styles/brand.css` — the typeface and the palette — also exists in [`optersoft/astro`](https://github.com/optersoft/astro) for the Astro sites and in `dioxus-chrome` for the Dioxus apps. The three differ in **four lines**, the `@font-face` URLs, because each build resolves them differently; everything else must stay equal, or a reader who picks "Gray" on optersoft.com meets a different grey on the next site.

This repository is meant to become the one copy and retire the other two. Until it is, a brand change is three commits.

## License

Apache-2.0. The Optersoft name, wordmark and logo are trademarks and are not licensed with the code.
