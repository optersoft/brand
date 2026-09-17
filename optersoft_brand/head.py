"""What every page of an Optersoft site puts in its `<head>`.

`frontage.head`'s `Title` and `Meta` render nothing and write into the page's head, so this
is a view a layout drops in — the port of `Layout.astro`'s head, minus the parts a frontage
site template already owns (`charset`, the viewport, `<html>` itself).
"""

import re
from pathlib import Path

from frontage import h
from frontage.head import Meta, Tag, Title

from . import theme

#: The Optersoft mark, at the paths `STATIC` puts it under. ⚠ **Literal, never hashed**:
#: Google re-crawls a favicon on its own slow schedule and treats a moved one as new, so a
#: content-hashed favicon can silently never appear in a search result.
ICONS = [
    ("/brand/assets/favicon.ico", "icon", None, "any"),
    ("/brand/assets/favicon-32x32.png", "icon", "image/png", "32x32"),
    ("/brand/assets/favicon-16x16.png", "icon", "image/png", "16x16"),
    ("/brand/assets/apple-touch-icon.png", "apple-touch-icon", None, "180x180"),
]

LOGO = "/brand/assets/optersoft.png"

#: The mark as the **letter** it is: the *o* of "optersoft", read from `optersoft-o.svg` so the
#: header can inline it (`header.wordmark`) as the uppercase O — the glyph scaled to the height of the *f*, on
#: the baseline — with `pter` and `soft` as live text after it. `viewBox` is the glyph's advance ×
#: its height; `height` and `shift` are the em fractions `icons.py` wrote into the file, which
#: make an inline <svg> sit exactly where the glyph would.
_LETTER_SVG = (Path(__file__).parent / "static" / "assets" / "optersoft-o.svg").read_text()
LETTER = {
    "viewBox": re.search(r'viewBox="([^"]+)"', _LETTER_SVG).group(1),
    "d": re.search(r' d="([^"]+)"', _LETTER_SVG).group(1),
    "fill": re.search(r'fill="(#[0-9a-f]{6})"', _LETTER_SVG).group(1),
    "height": re.search(r'data-em-height="([^"]+)"', _LETTER_SVG).group(1) + "em",
    "shift": re.search(r'data-em-shift="([^"]+)"', _LETTER_SVG).group(1) + "em",
}

#: The chrome's CSS is a **Tailwind source**, not a stylesheet a page links: it opens with
#: `@custom-variant` and `@source`, which a browser cannot use. A site imports it in its own
#: `tailwind.css`, after `@import "tailwindcss"`, and `frontage site --tailwind` compiles the
#: result — one stylesheet, the site's, with the brand in it.
STYLESHEET = "/brand/styles/chrome.css"


def head(
    title,
    description,
    canonical=None,
    noindex=False,
    site="Optersoft",
    locale=None,
    image=None,
    icons=ICONS,
    manifest=None,
):
    """The head every page needs: the title, the description, the social cards, the icons and
    the pre-paint theme script.

    A crawler, a search result and the preview card a chat app shows for your link read this
    HTML and never run the page, which is the whole reason it is written at build time.

    Every one of these renders nothing where it stands: `Title` and `Meta` write what a page
    says about itself, and `Tag` — the links, the icons, the pre-paint script — puts a whole
    element in the `<head>`. A layout that returned a bare `h.link` put a `<link>` in the
    *body*, which is where a browser will happily leave it and no crawler will look.
    """
    tags = [
        Title(title),
        Meta(description, name="description"),
        Meta("noindex, follow" if noindex else "index, follow", name="robots"),
        Meta(title, property="og:title"),
        Meta(description, property="og:description"),
        Meta("website", property="og:type"),
        Meta(site, property="og:site_name"),
        Meta("summary_large_image" if image else "summary", name="twitter:card"),
        Meta(title, name="twitter:title"),
        Meta(description, name="twitter:description"),
        # One meta, no `media` query: the script below rewrites its content to the active
        # theme's bar colour, and a media-gated pair would leave the wrong one live.
        Meta(theme.BAR["light"], name="theme-color"),
    ]
    if canonical:
        tags += [Tag(h.link(rel="canonical", href=canonical)), Meta(canonical, property="og:url")]
    if locale:
        tags.append(Meta(locale, property="og:locale"))
    if image:
        tags += [Meta(image, property="og:image"), Meta(image, name="twitter:image")]
    for href, rel, kind, sizes in icons or ():
        tags.append(Tag(h.link(rel=rel, href=href, type=kind, sizes=sizes)))
    if manifest:
        tags.append(Tag(h.link(rel="manifest", href=manifest)))
    # Inline, and first: it is what stops a flash of the wrong colour scheme, and nothing
    # that has to be fetched can do that.
    tags.append(Tag(h.script(theme.APPLY)))
    return tags
