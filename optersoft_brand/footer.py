"""The footer: the company.

Every Optersoft site ends with the same block — "Optersoft, S.L.", the social row, two
columns of links into optersoft.com, the copyright line and the registry ids — which is what
makes hive, make, frontage and optersoft.com read as one company at the bottom of the page
even when the top of it is the product's own.
"""

from frontage import h

from . import links as links_module
from .head import LOGO

LINK = "text-slate-600 hover:text-blue-600 transition-colors dark:text-slate-400 dark:hover:text-blue-400"


def footer(
    name="Optersoft, S.L.",
    tagline="Software consultancy and training",
    office="Registered office: Barcelona, Spain",
    rights="All rights reserved",
    legal="ES B64542335 · D-U-N-S 770940638",
    logo=LOGO,
    home=None,
    columns=None,
    socials=True,
    years=None,
    width="max-w-6xl",
    end=None,
):
    columns = links_module.OPTERSOFT_COLUMNS if columns is None else columns
    home = f"{links_module.OPTERSOFT}/" if home is None else home
    if years is None:
        import datetime

        years = str(datetime.date.today().year)
    return h.footer(
        h.div(
            h.div(
                h.div(
                    h.a(
                        h.img(src=logo, alt="Optersoft", width="28", height="28", cls="h-7 w-7 rounded-lg"),
                        h.p(name, cls="text-lg font-extrabold tracking-tight text-slate-900 dark:text-white"),
                        href=home,
                        cls="flex items-center gap-2.5",
                    ),
                    h.p(tagline, cls="mt-2 text-slate-500 dark:text-slate-400") if tagline else None,
                    h.p(office, cls="mt-1 text-slate-500 dark:text-slate-400") if office else None,
                    _socials() if socials else None,
                    cls="lg:col-span-2",
                ),
                *[_column(i, item) for i, item in enumerate(columns)],
                cls="grid gap-10 sm:grid-cols-2 lg:grid-cols-4",
            ),
            h.div(
                h.p(f"© {years} {name} {rights}"),
                h.div(
                    h.p(legal, cls="font-mono font-light") if legal else None,
                    end,
                    cls="flex items-center gap-4",
                ),
                cls=(
                    "mt-10 flex flex-col gap-1 border-t border-slate-200 pt-6 text-sm text-slate-500 "
                    "sm:flex-row sm:items-center sm:justify-between dark:border-slate-800 dark:text-slate-400"
                ),
            ),
            cls=f"container mx-auto px-5 sm:px-6 py-12 {width}",
        ),
        cls="border-t border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950",
    )


def _socials():
    return h.ul(
        *[
            h.li(
                h.a(
                    h.svg(
                        h.path(d=icon),
                        cls="h-5 w-5",
                        fill="currentColor",
                        viewBox="0 0 24 24",
                        **{"aria-hidden": "true"},
                    ),
                    href=href,
                    target="_blank",
                    rel="noopener noreferrer",
                    cls=(
                        "inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 "
                        "text-slate-500 hover:border-blue-200 hover:text-blue-600 transition-colors "
                        "dark:border-slate-700 dark:text-slate-400 dark:hover:border-blue-500/40 "
                        "dark:hover:text-blue-400"
                    ),
                    **{"aria-label": f"Optersoft on {label}"},
                )
            )
            for label, href, icon in links_module.SOCIALS
        ],
        cls="mt-4 flex items-center gap-2",
    )


def _column(index, item):
    return h.nav(
        h.p(
            item["heading"],
            id=f"footer-col-{index}",
            cls="text-xs font-semibold uppercase tracking-widest text-slate-400 dark:text-slate-500",
        ),
        h.ul(
            *[h.li(h.a(one["label"], href=one["href"], cls=LINK)) for one in item["links"]],
            cls="mt-4 flex flex-col gap-2.5",
        ),
        **{"aria-labelledby": f"footer-col-{index}"},
    )
