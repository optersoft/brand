"""The site header: the skip link, the sticky navbar, the theme toggle and the locale
switcher. A port of `@optersoft/astro`'s `Header.astro`, `ThemeToggle.astro` and
`LangSwitcher.astro`, whose ids and classes are `theme.css`'s contract and must not drift.

Both dropdowns are native `<details>` grouped by `name="dx-nav-popover"`, so opening one
closes the other and neither needs a script to open. What the rows *do* is in
`theme.CONTROLS`, one deferred script at the end of the page.

⚠ `collapse` is a **measurement**, not a taste. optersoft.com carries a brand, six links,
three locale pills, a theme toggle and a sign-in button: inline that needs ~900px, and `md`
(768) put the inline row on 130px too early — the label wrapped, the bar grew from 73 to
107px, the wordmark was clipped, and below 768 the overflow pushed the hamburger off-screen.
It passes `lg`. A product site with four links and no switcher fits `md`. One breakpoint
governs three places that MUST agree, which is why it is one argument and a table of literal
class strings: Tailwind generates only the classes it can read in the source.
"""

from frontage import h

from . import icons, labels as labels_module

BREAKPOINTS = {
    "md": {
        "actions": "flex items-center md:order-2",
        "actions_slot": "hidden md:flex md:ml-2",
        "burger": "md:hidden",
        "menu": "hidden items-center justify-between w-full md:!flex md:w-auto md:order-1",
        "list": "flex flex-col md:flex-row md:items-center gap-2 md:gap-7 p-4 md:p-0 mt-4 md:mt-0 text-sm font-medium text-slate-600 dark:text-slate-300",
        "link": "block py-2 md:py-1 hover:text-blue-600 dark:hover:text-blue-400 transition-colors",
        "menu_slot": "md:hidden mt-2 md:mt-0",
    },
    "lg": {
        "actions": "flex items-center lg:order-2",
        "actions_slot": "hidden lg:flex lg:ml-2",
        "burger": "lg:hidden",
        "menu": "hidden items-center justify-between w-full lg:!flex lg:w-auto lg:order-1",
        "list": "flex flex-col lg:flex-row lg:items-center gap-2 lg:gap-7 p-4 lg:p-0 mt-4 lg:mt-0 text-sm font-medium text-slate-600 dark:text-slate-300",
        "link": "block py-2 lg:py-1 hover:text-blue-600 dark:hover:text-blue-400 transition-colors",
        "menu_slot": "lg:hidden mt-2 lg:mt-0",
    },
}

SUMMARY = (
    "list-none inline-flex items-center cursor-pointer select-none text-gray-600 dark:text-gray-300 "
    "hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg text-sm p-2.5"
)
PANEL = (
    "absolute right-0 mt-1 w-36 rounded-lg border border-gray-200 dark:border-gray-700 "
    "bg-white dark:bg-gray-800 shadow-lg py-1 z-30"
)
ROW = (
    "flex w-full items-center gap-2 px-3 py-2 text-sm text-gray-700 dark:text-gray-200 "
    "hover:bg-gray-100 dark:hover:bg-gray-700 no-underline cursor-pointer"
)


def _svg(*children, cls="w-5 h-5", **attrs):
    return h.svg(
        *children,
        cls=cls,
        viewBox="0 0 20 20",
        xmlns="http://www.w3.org/2000/svg",
        **{"aria-hidden": "true"},
        **attrs,
    )


def sun(cls="w-5 h-5"):
    return _svg(h.path(d=icons.SUN, fill_rule="evenodd", clip_rule="evenodd"), cls=cls, fill="currentColor")


def moon(cls="w-5 h-5"):
    return _svg(h.path(d=icons.MOON), cls=cls, fill="currentColor")


def half(cls="w-5 h-5"):
    return _svg(
        h.circle(cx="10", cy="10", r="8", fill="none", stroke="currentColor", stroke_width="1.6"),
        h.path(d="M10 2a8 8 0 010 16z", fill="currentColor"),
        cls=cls,
    )


def theme_toggle(labels, cls="relative ml-2 group"):
    """The three-way theme control: a native `<details>` whose summary glyph is CSS-swapped."""
    return h.details(
        h.summary(
            moon("ic-moon w-5 h-5"),
            half("ic-gray w-5 h-5"),
            sun("ic-sun w-5 h-5"),
            cls=SUMMARY,
            title=labels["theme"],
            **{"aria-label": labels["theme"]},
        ),
        h.div(
            h.button(sun(), h.span(labels["light"]), type="button", cls=f"opt-light {ROW}", data_theme="light"),
            h.button(half(), h.span(labels["gray"]), type="button", cls=f"opt-gray {ROW}", data_theme="gray"),
            h.button(moon(), h.span(labels["dark"]), type="button", cls=f"opt-dark {ROW}", data_theme="dark"),
            id="theme-menu",
            cls=PANEL,
        ),
        id="theme-details",
        name="dx-nav-popover",
        cls=cls,
    )


def lang_switcher(langs, label):
    """The locale switcher, twice: a `<details>` below `sm`, a pill strip from `sm` up.

    Three pills are 111px and the theme toggle is 40px; on a 320px bar that difference is the
    whole brand wordmark. Every row carries `hreflang`, and the current locale is a link to
    itself with `aria-current` rather than a dead span — self-referencing alternates are what
    make a locale set coherent to a crawler.
    """
    face = next((item["label"] for item in langs if item.get("current")), langs[0]["label"] if langs else "")
    rows = [
        h.a(
            item["name"],
            href=item["href"],
            hreflang=item["code"],
            cls=(
                "flex w-full items-center px-3 py-2 text-sm no-underline font-semibold text-blue-600 "
                "dark:text-blue-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                if item.get("current")
                else "flex w-full items-center px-3 py-2 text-sm no-underline text-gray-700 dark:text-gray-200 "
                "hover:bg-gray-100 dark:hover:bg-gray-700"
            ),
            **({"aria-current": "true"} if item.get("current") else {}),
        )
        for item in langs
    ]
    pills = [
        h.a(
            item["label"],
            href=item["href"],
            hreflang=item["code"],
            cls=(
                "px-2.5 py-1 rounded-md transition-colors bg-gray-900 text-white dark:bg-white dark:text-gray-900"
                if item.get("current")
                else "px-2.5 py-1 rounded-md transition-colors text-gray-500 hover:text-gray-900 "
                "dark:text-gray-400 dark:hover:text-white"
            ),
            **({"aria-current": "true"} if item.get("current") else {}),
        )
        for item in langs
    ]
    return [
        h.details(
            h.summary(
                h.span(face, cls="inline-flex h-5 w-5 items-center justify-center text-xs font-semibold"),
                cls=SUMMARY,
                title=label,
                **{"aria-label": label},
            ),
            h.div(*rows, cls=PANEL),
            name="dx-nav-popover",
            cls="relative shrink-0 sm:hidden",
        ),
        h.div(
            *pills,
            cls=(
                "hidden sm:flex shrink-0 items-center rounded-lg border border-gray-200 p-0.5 text-xs "
                "font-semibold dark:border-gray-600"
            ),
            role="group",
            **{"aria-label": label},
        ),
    ]


def skip_link(label):
    """WCAG 2.4.1 Bypass Blocks, level A: the first focusable node in the document.

    `sr-only focus:not-sr-only`, never `hidden` — a `display: none` element is not focusable.
    """
    return h.a(
        label,
        href="#main",
        cls=(
            "sr-only focus:not-sr-only focus:absolute focus:z-50 focus:top-2 focus:left-2 focus:rounded-lg "
            "focus:bg-white dark:focus:bg-gray-800 focus:px-4 focus:py-2 focus:text-gray-900 dark:focus:text-white "
            "focus:shadow-lg focus:outline-2 focus:outline-offset-2 focus:outline-indigo-600"
        ),
    )


def letter(letter, cls=""):
    """The mark inline as the letter it is: an <svg> sized to the o's height on the baseline, so
    `"pter"` follows it as the rest of the word. `margin-right` repeats the name's
    `tracking-tight`, which letter-spacing puts after every character but not after an element."""
    return h.svg(
        h.path(d=letter["d"], fill=letter["fill"], fill_rule="evenodd"),
        viewBox=letter["viewBox"],
        xmlns="http://www.w3.org/2000/svg",
        cls=f"inline-block w-auto {cls}".strip(),
        style=f"height:{letter['height']};vertical-align:{letter['shift']};margin-right:-.025em",
        **{"aria-hidden": "true"},
    )


def initial(text, cls=""):
    """The lockup's capital, set live: the font's own uppercase O in the brand blue — the same
    glyph `optersoft-wordmark.svg` draws, kerning with the `pter` that follows as one word.
    `#2563eb` is Tailwind's `blue-600`, in both themes: the blue is the brand's, not the
    surface's."""
    return h.span(text, cls=f"text-blue-600 {cls}".strip())


def wordmark(brand):
    """The brand cluster. Three shapes, newest first:

    - `{"initial": "O", "name": "pter", "suffix": "soft"}` — **the lockup** (2026-09-18): the
      name as text, its capital in the brand blue, `soft` light. No image and no `aria-label`:
      the text spells the name, and it is the same picture as `optersoft-wordmark.svg`.
    - `{"letter": LETTER, "name": "pter", "suffix": "soft"}` — the constructed mark inlined
      as the first letter (`label` is what assistive tech reads; default "Optersoft").
    - `{"logo": URL, "name": "opter", "suffix": "soft"}` — an image before the name."""
    if brand.get("initial"):
        return h.a(
            h.span(
                initial(brand["initial"]),
                brand["name"],
                h.span(brand["suffix"], cls="font-light text-slate-400 dark:text-slate-500") if brand.get("suffix") else None,
            ),
            href=brand["href"],
            cls="flex items-center text-lg font-extrabold tracking-tight text-slate-900 dark:text-white",
        )
    if brand.get("letter"):
        return h.a(
            h.span(
                letter(brand["letter"]),
                brand["name"],
                h.span(brand["suffix"], cls="font-light text-slate-400 dark:text-slate-500") if brand.get("suffix") else None,
            ),
            href=brand["href"],
            cls="flex items-center text-lg font-extrabold tracking-tight text-slate-900 dark:text-white",
            **{"aria-label": brand.get("label", "Optersoft")},
        )
    return h.a(
        h.img(src=brand["logo"], alt=brand.get("alt", ""), width="32", height="32", cls="h-8 w-8 rounded-lg")
        if brand.get("logo")
        else None,
        h.span(
            brand["name"],
            h.span(brand["suffix"], cls="font-light text-slate-400 dark:text-slate-500") if brand.get("suffix") else None,
        ),
        href=brand["href"],
        cls="flex items-center gap-2.5 text-lg font-extrabold tracking-tight text-slate-900 dark:text-white",
    )


def header(brand, links=(), langs=None, labels=None, collapse="md", width="max-w-6xl", actions=None, menu=None):
    """The header every Optersoft site renders, with its own brand and links filled in."""
    words = labels_module.labels(labels)
    bp = BREAKPOINTS[collapse]
    return [
        skip_link(words["skip"]),
        h.nav(
            # ⚠ `flex-wrap` is LOAD-BEARING: `#navbar-menu` is `w-full` by design, and when
            # the hamburger opens the menu has to fall to a second row *under* the bar. In a
            # nowrap row it cannot — it squeezes the brand into nothing and opens off-screen.
            h.div(
                # `min-w-0` so the brand is what shrinks last, not first.
                h.div(brand if not isinstance(brand, dict) else wordmark(brand), cls="flex min-w-0 items-center gap-3"),
                h.div(
                    lang_switcher(langs, words["language"]) if langs else None,
                    theme_toggle(words),
                    h.div(actions, cls=bp["actions_slot"]) if actions is not None else None,
                    h.button(
                        h.span(
                            h.svg(
                                h.path(
                                    stroke="currentColor",
                                    stroke_linecap="round",
                                    stroke_linejoin="round",
                                    stroke_width="2",
                                    d=icons.BURGER,
                                ),
                                cls="w-5 h-5",
                                xmlns="http://www.w3.org/2000/svg",
                                fill="none",
                                viewBox="0 0 17 14",
                                **{"aria-hidden": "true"},
                            )
                        ),
                        type="button",
                        cls=(
                            f"{bp['burger']} inline-flex shrink-0 items-center justify-center text-gray-600 "
                            "dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none "
                            "focus:ring-2 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5 "
                            "ml-2 cursor-pointer"
                        ),
                        **{"aria-label": words["menu"], "aria-controls": "navbar-menu", "aria-expanded": "false"},
                    ),
                    cls=bp["actions"],
                ),
                h.div(
                    h.ul(
                        *[
                            h.li(
                                # `py-2` on a phone, not `py-1`: this is the only way to reach
                                # these pages on a small screen, and a 21px-tall tap target
                                # misses WCAG 2.2 SC 2.5.8's 24×24 floor.
                                h.a(
                                    item["label"],
                                    href=item["href"],
                                    cls=bp["link"],
                                    **({"aria-current": "page"} if item.get("current") else {}),
                                )
                            )
                            for item in links
                        ],
                        h.li(menu, cls=bp["menu_slot"]) if menu is not None else None,
                        cls=bp["list"],
                    ),
                    id="navbar-menu",
                    cls=bp["menu"],
                ),
                cls=f"container mx-auto flex flex-wrap items-center justify-between gap-4 px-5 sm:px-6 py-4 {width}",
            ),
            cls=(
                "sticky top-0 z-30 w-full border-b border-slate-200/70 bg-white/85 backdrop-blur "
                "dark:border-slate-800/70 dark:bg-slate-950/85"
            ),
        ),
    ]
