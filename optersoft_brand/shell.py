"""The frame every page shares: the header, a growing `<main>`, the footer, and the one
deferred script the controls need.

The port of `dioxus_chrome`'s `Shell` and `@optersoft/astro`'s `Shell.astro`. `main` carries
the id the skip link points at, which is the whole of WCAG 2.4.1 once the link exists.
"""

from frontage import h

from . import theme
from .footer import footer as footer_component
from .header import header as header_component


def shell(children, brand, links=(), langs=None, labels=None, collapse="md", width="max-w-6xl", **rest):
    """The whole page body. `rest` goes to the footer — `columns=`, `years=`, `end=`."""
    return h.div(
        header_component(brand, links=links, langs=langs, labels=labels, collapse=collapse, width=width),
        h.main(children, id="main", cls="flex-grow"),
        footer_component(width=width, **rest),
        # At the end of the body, so nothing waits for it: the theme was applied before
        # paint by `head()`, and these are the clicks.
        h.script(theme.CONTROLS),
        cls="flex flex-col min-h-full",
    )
