"""The company, as links: where every site sends a reader who wants Optersoft rather than the
product in front of them.

The footer's default columns and social row come from here, so a product site carries the
same doors as optersoft.com without naming a single URL of its own. A port of
`@optersoft/astro`'s `links.ts`.
"""

#: The canonical origin of the company site. Never derived from a request.
OPTERSOFT = "https://optersoft.com"


def link(href, label, current=False):
    """One navigation link. `current` marks the page the reader is on."""
    return {"href": href, "label": label, "current": current}


def column(heading, links):
    return {"heading": heading, "links": list(links)}


def lang(code, label, name, href, current=False):
    """One locale of the switcher.

    `name` is the language's name **in that language**, never translated into the page's
    locale — a reader who wants Catalan is looking for the word "Català".
    """
    return {"code": code, "label": label, "name": name, "href": href, "current": current}


#: The company's pages, English paths. optersoft.com passes its own localised columns;
#: every other site gets these.
OPTERSOFT_COLUMNS = [
    column(
        "Optersoft",
        [
            link(f"{OPTERSOFT}/services", "Services"),
            link(f"{OPTERSOFT}/technology", "Technology"),
            link(f"{OPTERSOFT}/academy", "Academy"),
            link(f"{OPTERSOFT}/apps", "Apps"),
            link(f"{OPTERSOFT}/about", "About"),
            link(f"{OPTERSOFT}/contact", "Contact"),
        ],
    ),
    column(
        "Legal",
        [
            link(f"{OPTERSOFT}/legal", "Legal notice"),
            link(f"{OPTERSOFT}/privacy", "Privacy policy"),
            link(f"{OPTERSOFT}/cookies", "Cookies"),
        ],
    ),
]

#: Official social profiles: name, URL, the icon's SVG path (24×24 viewBox). optersoft.com
#: mirrors these in its Organization `sameAs` JSON-LD.
SOCIALS = [
    (
        "LinkedIn",
        "https://www.linkedin.com/company/optersoft",
        "M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.42v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 110-4.14 2.07 2.07 0 010 4.14zM7.12 20.45H3.55V9h3.57v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.22.79 24 1.77 24h20.45c.98 0 1.78-.78 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z",
    ),
    (
        "GitHub",
        "https://github.com/optersoft",
        "M12 .5C5.37.5 0 5.78 0 12.29c0 5.2 3.44 9.61 8.21 11.16.6.11.82-.25.82-.56 0-.28-.01-1.02-.02-2-3.34.72-4.04-1.61-4.04-1.61-.55-1.39-1.34-1.76-1.34-1.76-1.09-.75.08-.73.08-.73 1.21.08 1.84 1.25 1.84 1.25 1.07 1.84 2.81 1.31 3.5 1 .11-.78.42-1.31.76-1.61-2.67-.3-5.47-1.34-5.47-5.96 0-1.32.47-2.39 1.24-3.23-.12-.31-.54-1.53.12-3.19 0 0 1.01-.33 3.3 1.23a11.5 11.5 0 016.01 0c2.29-1.56 3.3-1.23 3.3-1.23.66 1.66.24 2.88.12 3.19.77.84 1.24 1.91 1.24 3.23 0 4.63-2.81 5.65-5.49 5.95.43.37.82 1.1.82 2.22 0 1.61-.01 2.9-.01 3.29 0 .32.22.69.83.57A12.02 12.02 0 0024 12.29C24 5.78 18.63.5 12 .5z",
    ),
    (
        "GitLab",
        "https://gitlab.com/optersoft",
        "M23.955 13.587l-1.342-4.135-2.664-8.189a.455.455 0 00-.867 0L16.418 9.45H7.582L4.919 1.263a.455.455 0 00-.868 0L1.386 9.452.044 13.587a.924.924 0 00.331 1.023L12 23.054l11.625-8.444a.92.92 0 00.33-1.023",
    ),
]
