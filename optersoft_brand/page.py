"""The page-top block and the branded 404 — `PageHeader.astro` and `NotFound.astro`."""

from frontage import h


def backdrop(glow=False):
    """The faint grid + glow behind a page header or hero."""
    return [
        h.div(
            cls=(
                "pointer-events-none absolute inset-0 opacity-[0.06] "
                "[background-image:linear-gradient(to_right,#1e293b_1px,transparent_1px),"
                "linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] [background-size:44px_44px] "
                "dark:opacity-[0.08] dark:[background-image:linear-gradient(to_right,#64748b_1px,transparent_1px),"
                "linear-gradient(to_bottom,#64748b_1px,transparent_1px)]"
            ),
            **{"aria-hidden": "true"},
        ),
        h.div(
            cls=(
                "pointer-events-none absolute -top-24 left-1/2 -translate-x-1/2 h-72 w-[42rem] max-w-full "
                "rounded-full bg-gradient-to-r from-blue-400/30 to-indigo-400/30 blur-3xl"
            ),
            **{"aria-hidden": "true"},
        )
        if glow
        else None,
    ]


def page_header(heading, label=None, intro=None, glow=False, width="max-w-6xl", children=None):
    """The eyebrow + h1 + intro block that opens a page, one component across the sites so
    their page tops cannot drift apart."""
    return h.section(
        backdrop(glow),
        h.div(
            h.p(label, cls="text-sm font-semibold uppercase tracking-widest text-blue-600 dark:text-blue-400")
            if label
            else None,
            h.h1(
                heading,
                cls=(
                    "text-4xl sm:text-5xl font-extrabold tracking-tight text-balance text-slate-900 dark:text-white"
                    + (" mt-3" if label else "")
                ),
            ),
            h.p(intro, cls="mt-5 max-w-2xl text-lg text-slate-600 leading-relaxed dark:text-slate-300")
            if intro
            else None,
            children,
            cls=f"container relative mx-auto px-5 sm:px-6 py-16 sm:py-20 {width}",
        ),
        cls="relative overflow-hidden bg-white border-b border-slate-200 dark:bg-slate-950 dark:border-slate-800",
    )


def not_found(heading, body, home, other=None, code="404"):
    """The branded 404 body, rendered inside a site's own shell so it keeps its chrome."""
    return h.div(
        h.p(code, cls="font-mono text-sm font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400"),
        h.h1(heading, cls="mt-4 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl dark:text-white"),
        h.p(body, cls="mt-5 max-w-xl text-lg leading-relaxed text-slate-600 dark:text-slate-300"),
        h.div(
            h.a(
                home["label"],
                href=home["href"],
                cls=(
                    "inline-flex items-center justify-center rounded-xl bg-blue-600 px-6 py-3 text-base "
                    "font-semibold text-white transition-colors hover:bg-blue-500"
                ),
            ),
            h.a(
                other["label"],
                href=other["href"],
                cls=(
                    "inline-flex items-center justify-center rounded-xl border border-slate-300 px-6 py-3 "
                    "text-base font-semibold text-slate-900 transition-colors hover:bg-slate-100 "
                    "dark:border-slate-700 dark:text-white dark:hover:bg-slate-800"
                ),
            )
            if other
            else None,
            cls="mt-10 flex flex-col gap-3 sm:flex-row",
        ),
        cls="flex min-h-[60vh] flex-col items-center justify-center px-5 py-20 text-center sm:px-6",
    )
