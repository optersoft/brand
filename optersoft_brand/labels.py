"""The chrome's own words — the accessible names of its controls.

English by default; a localised site passes its translations to `Header` or `Shell`. A port
of `@optersoft/astro`'s `labels.ts`, kept word for word so the three chromes say the same
thing.
"""

SKIP = "skip"
MENU = "menu"
THEME = "theme"
LIGHT = "light"
GRAY = "gray"
DARK = "dark"
LANGUAGE = "language"

#: The defaults. `gray` is a LIGHT-family theme — a muted paper, not a second dark.
LABELS = {
    SKIP: "Skip to content",
    MENU: "Open menu",
    THEME: "Toggle theme",
    LIGHT: "Light",
    GRAY: "Gray",
    DARK: "Dark",
    LANGUAGE: "Language",
}


def labels(overrides=None):
    """The defaults with a site's own words over them."""
    found = dict(LABELS)
    found.update(overrides or {})
    return found
