"""The Optersoft chrome, for a frontage site.

Everything around the content that makes a page look like it belongs to the company: the
layout, the header with the three-way theme toggle and the locale switcher, the footer with
the company, the brand stylesheet and the fonts. A site imports the components and copies
the assets:

    # site.py
    import optersoft_brand
    STATIC = [(optersoft_brand.static, "brand")]

    # layouts/site.py
    from optersoft_brand import head, shell

    def layout(children, title, description, **rest):
        return [head(title, description, **rest), shell(children, brand=BRAND, links=LINKS)]

**This ships no runtime.** The theme has to be applied before first paint or the page flashes
the wrong colour scheme, and nothing that has to be fetched can do that — so the chrome
carries two small inline scripts (`theme.APPLY` and `theme.CONTROLS`) and no island. Every
page of a site on this chrome is HTML and stops there.

The brand itself — `brand.css`, `theme.css`, the fonts, the mark — is the same file the
Dioxus apps and the Astro sites use. When it changes there, change it here in the same
commit; `optersoft/brand` is meant to become the one copy, and `astro/` and `dioxus-chrome`
are the two it is meant to replace.
"""

from pathlib import Path

from .footer import footer
from .head import ICONS, LETTER, LOGO, STYLESHEET, head
from .header import header, lang_switcher, skip_link, theme_toggle
from .labels import LABELS, labels
from .links import OPTERSOFT, OPTERSOFT_COLUMNS, SOCIALS, column, lang, link
from .page import backdrop, not_found, page_header
from .shell import shell
from .theme import BAR, CONTROLS, KEY, THEMES

#: The directory a site copies into its output — the stylesheets, the fonts and the mark.
#: `STATIC = [(optersoft_brand.static, "brand")]` puts it at `/brand/`, which is where
#: `head()` and `brand.css` look for it.
static = Path(__file__).resolve().parent / "static"

__all__ = [
    "BAR",
    "CONTROLS",
    "ICONS",
    "KEY",
    "LABELS",
    "LETTER",
    "LOGO",
    "OPTERSOFT",
    "OPTERSOFT_COLUMNS",
    "SOCIALS",
    "STYLESHEET",
    "THEMES",
    "backdrop",
    "column",
    "footer",
    "head",
    "header",
    "labels",
    "lang",
    "lang_switcher",
    "link",
    "not_found",
    "page_header",
    "shell",
    "skip_link",
    "static",
    "theme_toggle",
]
