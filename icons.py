# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow>=10", "fonttools>=4.50", "brotli>=1.1", "uharfbuzz>=0.40"]
# ///
"""The Optersoft mark — the *o* of the wordmark — and everything the chrome ships of it.

    uv run icons.py            # writes optersoft_brand/static/assets/
    uv run icons.py DIR ...    # the same files into other directories (../astro/src/assets, …)

**The mark is the first letter of the name.** It is the *o* of "optersoft" with the wordmark's
two weights in one glyph: heavy on the left, where `opter` is set ExtraBold, and light on
the right, where `soft` is set Light — the outer contour of Hanken Grotesk's ExtraBold *o*
minus a counter pushed off-centre, so the left stem is the ExtraBold stem and the right
stem is the Light stem, to the unit (measured 2026-09-17: 137 and 62 per 1000 em, on an
*o* 501 wide and 513 tall, with the 35-unit bearings of the glyph). Set in the word it
replaces the first *o* as an **uppercase O** — the same glyph scaled up to the height of the *f* on the baseline, so it stands out ("para destacar", 2026-09-17);
alone, it is the icon. One shape, no joins, and it prints in one colour.

Everything below is derived from that geometry and the tracked `hanken-grotesk.woff2`
(HarfBuzz shapes the letters, fontTools draws them), never edited by hand:

| file | what | used by |
|---|---|---|
| `optersoft.svg` | the mark alone, blue, in a 64-unit square | the source icon |
| `optersoft-o.svg` | the mark as the **uppercase O**: the glyph scaled to the height of the *f*, viewBox = its advance × height, with the em fractions an inline `<svg>` needs as `data-` attributes | `head.LETTER` → `header.wordmark`, inline |
| `optersoft-mono.svg` | the mark alone in `currentColor` | print, one-colour |
| `optersoft-wordmark.svg` | **the lockup**: the font's own uppercase `O` (blue) + `pter` + `soft` as paths, no font needed; letters in `currentColor` | decks, print, anywhere the header is not |
| `optersoft.png` 192 | the mark alone, blue, transparent | `LOGO`: the footer, the PDFs |
| `favicon-16x16.png`, `favicon-32x32.png`, `favicon.ico` | the mark alone | `ICONS` |
| `apple-touch-icon.png` 180 (edge to edge), `optersoft-512.png` | the blue mark on a white **square** | iOS and avatar hosts mask their own |

    uv run icons.py --site DIR  # a site's own `public/`: the favicons at the LITERAL names a
                               # page links them by, plus the two `android-chrome-*` sizes
                               # the web manifest and the schema.org `logo` name
    uv run icons.py --render mark:96 out.png     # one file, for an app that asks for its own
    uv run icons.py --render tile:512 logo.png   # size: `mark` is the bare mark, `tile` the
    uv run icons.py --render ico:16,32,48 f.ico  # square white-on-blue, `ico` a multi-size icon
    uv run icons.py --render wordmark:320x132 l.png   # the LOCKUP in a box of that size, centred
    uv run icons.py --render letter:120x120 l.png     # the LOGO alone, blue on white, edge to
                                               # edge (`@blue` on either spec: white on the
                                               # brand tile instead)
    uv run icons.py --rust PATH.rs               # the mark as a generated Rust module, for the
                                                 # Dioxus chrome to inline (no asset to fetch)

Needs `rsvg-convert` (librsvg) on PATH for the rasters.
"""

from __future__ import annotations

import io
import re
import subprocess
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from PIL import Image

HERE = Path(__file__).parent
STATIC = HERE / "optersoft_brand" / "static"
ASSETS = STATIC / "assets"
FONT = STATIC / "fonts" / "hanken-grotesk.woff2"

BLUE, WHITE = "#2563eb", "#ffffff"
INK = "#0f172a"  # slate-900, the colour the header sets the name in

# ---- the letter, in font units (1000 per em), y up as in the font -----------------------------
ADVANCE = 571  # the ExtraBold o's advance width
BEARING = 35  # its left side bearing
O_W, O_H = 501, 513  # the o's outer width and height (x-height 493 + 10 of overshoot each side)
OVERSHOOT = 10
STEM_HEAVY, STEM_LIGHT = 137, 62  # ExtraBold and Light side stems
STEM_TOP = 100  # the ring's thickness at top and bottom (ExtraBold 120, Light 55)
HEAVY, LIGHT = 800, 300  # the wordmark's weights
TRACKING = -25  # `tracking-tight`, -0.025 em, as the header sets the name


def _glyph_top(char: str, wght: int) -> float:
    """How far above the baseline `char` reaches at `wght`, in font units — read from the font."""
    from fontTools.pens.boundsPen import BoundsPen

    inst = instantiateVariableFont(TTFont(FONT), {"wght": wght})
    gs = inst.getGlyphSet()
    pen = BoundsPen(gs)
    gs[inst.getBestCmap()[ord(char)]].draw(pen)
    return pen.bounds[3]


#: In the word the mark is an **uppercase O**: the same glyph scaled from the x-height up to the
#: height of the *f* in `soft`, on the baseline, overshooting that line above and below the way a
#: round capital does — the owner's decision of 2026-09-17 ("para destacar, at the same height
#: as the f"). Uniform scale, so the stems grow with it and the shape stays the icon's.
F_HEIGHT = _glyph_top("f", LIGHT)
LETTER_SCALE = (F_HEIGHT + 2 * OVERSHOOT) / O_H

RX, RY = O_W / 2, O_H / 2
rx, ry = RX - (STEM_HEAVY + STEM_LIGHT) / 2, RY - STEM_TOP
DX = (STEM_HEAVY - STEM_LIGHT) / 2  # the counter's shift to the right


def ring(cx: float, cy: float, s: float = 1.0) -> str:
    """The mark as a path (evenodd), centred at (cx, cy) in y-down coordinates, scaled by s."""
    a, b, c, d = RX * s, RY * s, rx * s, ry * s
    return (
        f"M{cx - a:.2f} {cy:.2f} a{a:.2f} {b:.2f} 0 1 0 {2 * a:.2f} 0 a{a:.2f} {b:.2f} 0 1 0 {-2 * a:.2f} 0 Z "
        f"M{cx + DX * s - c:.2f} {cy:.2f} a{c:.2f} {d:.2f} 0 1 0 {2 * c:.2f} 0 a{c:.2f} {d:.2f} 0 1 0 {-2 * c:.2f} 0 Z"
    )


# The letter: viewBox is the scaled glyph box — advance wide, o-height tall, the baseline
# OVERSHOOT from the bottom — and the file carries the two em fractions an inline <svg> needs to
# sit exactly where the glyph would: `data-em-height` for `height`, `data-em-shift` for
# `vertical-align`. `head.LETTER` reads them, so no consumer hard-codes the size.
K = LETTER_SCALE
LETTER_VIEWBOX = f"0 0 {ADVANCE * K:.0f} {O_H * K:.0f}"
LETTER_PATH = ring(BEARING * K + RX * K, RY * K, K)
LETTER_HEIGHT_EM = O_H * K / 1000
LETTER_SHIFT_EM = -OVERSHOOT * K / 1000


def letter_svg(fill: str = BLUE) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{LETTER_VIEWBOX}" role="img" aria-label="O" '
        f'data-em-height="{LETTER_HEIGHT_EM:.3f}" data-em-shift="{LETTER_SHIFT_EM:.3f}">\n'
        f'  <path d="{LETTER_PATH}" fill="{fill}" fill-rule="evenodd"/>\n</svg>\n'
    )


MARGIN_TILE = 11.0  # the mark inside a colour block: it needs a field around it
MARGIN_WHITE = 6.0  # the mark on white: nothing to hold it off the edge but the eye
MARGIN_APPLE = 0.0  # `apple-touch-icon`: Apple asks for artwork edge to edge — the system adds
                    # the corner radius and, on a widget or a notification, its own padding, so
                    # any margin of ours is padding on top of padding and only shrinks the mark


def icon_svg(fill: str = BLUE, *, ground: str | None = None, rounded: bool = True, margin: float = 4.0) -> str:
    """The mark alone in a 64-unit square, `margin` units clear of the edge.

    `ground` fills the square behind it. The masked icons need one — iOS and the avatar hosts
    composite a transparent PNG onto black — and since 2026-09-18 it is WHITE with the mark in
    the brand blue, so those tiles read as the same blue *O* as every other file here; `BLUE`
    with a white mark is the inverse, for a slot with a light chrome of its own.

    ⚠ `margin` is optical, not a safe area: the mark is a **ring**, so its farthest point from
    the centre is half its height — a circular avatar crop and iOS's rounded corners both cut
    only the square's corners, which the mark never reaches, at ANY margin. So a white-ground
    icon takes `MARGIN_WHITE`, `apple-touch-icon` takes `MARGIN_APPLE` (none — Apple adds its
    own); only a mark inside a colour block needs `MARGIN_TILE`, where the inset is what keeps
    it from reading as a blue square rather than a mark.
    """
    s = (64 - 2 * margin) / O_H
    rect = f'  <rect width="64" height="64" rx="{16 if rounded else 0}" fill="{ground}"/>\n' if ground else ""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Optersoft">\n'
        + rect
        + f'  <path d="{ring(32, 32, s)}" fill="{fill}" fill-rule="evenodd"/>\n</svg>\n'
    )


# ---- the lockup ---------------------------------------------------------------------------------
def _ttf_bytes() -> bytes:
    f = TTFont(FONT)
    f.flavor = None
    b = io.BytesIO()
    f.save(b)
    return b.getvalue()


def _glyphs(text: str, wght: int, x0: float) -> tuple[str, float]:
    """Outlines of `text` at `wght` as one path (y down, baseline y = 0), starting at x0; returns (path, x after)."""
    data = _ttf_bytes()
    face = hb.Face(data)
    font = hb.Font(face)
    font.set_variations({"wght": wght})
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    inst = instantiateVariableFont(TTFont(io.BytesIO(data)), {"wght": wght})
    gs = inst.getGlyphSet()
    order = inst.getGlyphOrder()
    parts, x = [], x0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        gs[order[info.codepoint]].draw(TransformPen(pen, (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset)))
        parts.append(pen.getCommands())
        x += pos.x_advance + TRACKING
    return " ".join(parts), x


#: The lockup spells the name with the font's own **uppercase O** at the `pter` weight, not with
#: the constructed mark: on a deck or a printed page the word is read as a word, and a real
#: capital sets it the way the type designer drew it. The mark stays the icon (`optersoft.svg`,
#: `optersoft-o.svg`) and stays the header's inline letter; only this file uses the glyph.
O_TOP = _glyph_top("O", HEAVY)


def wordmark_parts(mark_fill: str = BLUE, letters: str = "currentColor", soft_opacity: float = 0.45) -> tuple[str, str]:
    """The lockup as `(viewBox, body)` — the `O`, `pter` and `soft`, no outer `<svg>`."""
    cap, x = _glyphs("O", HEAVY, 0)
    pter, x = _glyphs("pter", HEAVY, x)
    soft, x_end = _glyphs("soft", LIGHT, x)
    width = x_end - TRACKING + BEARING  # end at the last glyph's advance plus a matching bearing
    ascent, descent = O_TOP + OVERSHOOT, 230  # the O's top and the p's descender (204 below the baseline)
    body = (
        f'  <path d="{cap}" fill="{mark_fill}"/>\n'
        f'  <path d="{pter}" fill="{letters}"/>\n'
        f'  <path d="{soft}" fill="{letters}" fill-opacity="{soft_opacity}"/>\n'
    )
    return f"0 {-ascent} {width:.0f} {ascent + descent}", body


def wordmark_svg(mark_fill: str = BLUE, letters: str = "currentColor", soft_opacity: float = 0.45) -> str:
    view_box, body = wordmark_parts(mark_fill, letters, soft_opacity)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" role="img" aria-label="Optersoft">\n'
        f"{body}</svg>\n"
    )


def _box(view_box: str, body: str, w: int, h: int, *, ground: str | None = None, pad: float = 0.12) -> str:
    """`body` centred in a `w`×`h` box, `pad` of the short side clear on every edge.

    For the consoles outside the fleet that ask for a logo at a fixed pixel size — Google
    Workspace's Admin custom logo, a Marketplace banner, an OAuth consent screen. A nested
    `<svg>` does the fitting, so nothing is ever distorted, whatever the slot's aspect.
    """
    m = min(w, h) * pad
    rect = f'  <rect width="{w}" height="{h}" fill="{ground}"/>\n' if ground else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        'role="img" aria-label="Optersoft">\n' + rect
        + f'  <svg x="{m:.1f}" y="{m:.1f}" width="{w - 2 * m:.1f}" height="{h - 2 * m:.1f}" '
        f'viewBox="{view_box}" preserveAspectRatio="xMidYMid meet">\n{body}  </svg>\n</svg>\n'
    )


def wordmark_box(w: int, h: int, *, on_blue: bool = False, pad: float = 0.12) -> str:
    """The whole lockup in a box. `on_blue` is white on the brand tile; otherwise it is the
    header's colouring — blue mark, slate-900 `opter`, the same at 45% for `soft`."""
    view_box, body = wordmark_parts(WHITE if on_blue else BLUE, WHITE if on_blue else INK)
    return _box(view_box, body, w, h, ground=BLUE if on_blue else None, pad=pad)


def letter_box(w: int, h: int, *, on_blue: bool = False, pad: float | None = None) -> str:
    """The **logo** alone in a box — the constructed mark, blue on white.

    This is what an outside console gets when it asks for *a logo* rather than a lockup, and it
    is the mark, not the font's capital: the real `O` is the lockup's business, because there it
    is a letter in a word. Anywhere the shape stands alone it is the logo.

    The viewBox is the mark's ink box rather than `LETTER_VIEWBOX` (which carries the glyph's
    side bearings), so the fit reaches the edge instead of padding it. The ground is opaque
    white — a console composites a logo onto a white card in one place and onto its own dark
    chrome in another, and a transparent PNG loses on the second. `on_blue` is the inverse and
    keeps a field around the mark, the way any mark inside a colour block does.
    """
    view_box = f"{BEARING * K:.0f} 0 {O_W * K:.0f} {O_H * K:.0f}"
    body = f'  <path d="{LETTER_PATH}" fill="{WHITE if on_blue else BLUE}" fill-rule="evenodd"/>\n'
    if pad is None:
        pad = 0.12 if on_blue else 0.0
    return _box(view_box, body, w, h, ground=BLUE if on_blue else WHITE, pad=pad)


# ---- rasters ------------------------------------------------------------------------------------
def raster_wh(source: str, w: int, h: int) -> Image.Image:
    out = subprocess.run(
        ["rsvg-convert", "-w", str(w), "-h", str(h)], input=source.encode(), capture_output=True, check=True
    ).stdout
    return Image.open(io.BytesIO(out)).convert("RGBA")


def raster(source: str, px: int) -> Image.Image:
    return raster_wh(source, px, px)


def png(im: Image.Image) -> bytes:
    b = io.BytesIO()
    im.save(b, "PNG", optimize=True)
    return b.getvalue()


def write(assets: Path) -> list[Path]:
    assets.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []

    def put(name: str, data: bytes | str):
        p = assets / name
        p.write_bytes(data.encode() if isinstance(data, str) else data)
        made.append(p)

    bare = icon_svg(BLUE)
    put("optersoft.svg", bare)
    put("optersoft-o.svg", letter_svg())
    put("optersoft-mono.svg", icon_svg("currentColor"))
    put("optersoft-wordmark.svg", wordmark_svg())
    put("optersoft.png", png(raster(bare, 192)))
    put("favicon-16x16.png", png(raster(icon_svg(BLUE, margin=1), 16)))
    put("favicon-32x32.png", png(raster(icon_svg(BLUE, margin=2), 32)))
    # Pillow writes each ICO size by resampling the base frame unless `append_images` holds an
    # exact match — so the base is the 48 and the 16 and 32 are rendered on their own.
    ico = io.BytesIO()
    f48, f16, f32 = (
        raster(icon_svg(BLUE, margin=3), 48),
        raster(icon_svg(BLUE, margin=1), 16),
        raster(icon_svg(BLUE, margin=2), 32),
    )
    f48.save(ico, "ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[f16, f32])
    put("favicon.ico", ico.getvalue())
    put("apple-touch-icon.png", png(raster(icon_svg(BLUE, ground=WHITE, rounded=False, margin=MARGIN_APPLE), 180)))
    # `optersoft-512` keeps a margin: the avatar hosts crop it to a CIRCLE, and a ring drawn to
    # the edge is tangent to the inscribed one — it would look shaved where the icon does not.
    put("optersoft-512.png", png(raster(icon_svg(BLUE, ground=WHITE, rounded=False, margin=MARGIN_WHITE), 512)))
    return made


def write_site(public: Path) -> list[Path]:
    """A site's own `public/`: the same mark, at the literal paths that site's pages link.

    ⚠ Literal, never hashed — the note on `head.ICONS` says why. The two `android-chrome-*`
    sizes are what `site.webmanifest` lists and what the schema.org `Organization.logo` points
    at, so they stay the square white-on-blue tile, not the bare mark: a launcher and a search
    result both put the icon on their own background. `apple-touch-icon.png` does not — since
    2026-09-18 it is the blue mark on white, like the one in `assets/`, so the two files of that
    name are the same picture.
    """
    public.mkdir(parents=True, exist_ok=True)
    made: list[Path] = []

    def put(name: str, data: bytes):
        p = public / name
        p.write_bytes(data)
        made.append(p)

    put("favicon-16x16.png", png(raster(icon_svg(BLUE, margin=1), 16)))
    put("favicon-32x32.png", png(raster(icon_svg(BLUE, margin=2), 32)))
    ico = io.BytesIO()
    f48, f16, f32 = (
        raster(icon_svg(BLUE, margin=3), 48),
        raster(icon_svg(BLUE, margin=1), 16),
        raster(icon_svg(BLUE, margin=2), 32),
    )
    f48.save(ico, "ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[f16, f32])
    put("favicon.ico", ico.getvalue())
    put("apple-touch-icon.png", png(raster(icon_svg(BLUE, ground=WHITE, rounded=False, margin=MARGIN_APPLE), 180)))
    tile = icon_svg(WHITE, ground=BLUE, rounded=False, margin=MARGIN_TILE)
    put("android-chrome-192x192.png", png(raster(tile, 192)))
    put("android-chrome-512x512.png", png(raster(tile, 512)))
    return made


RUST = '''//! The Optersoft mark, as data. **Generated — do not edit.**
//!
//! Written by `icons.py --rust` in the `brand` checkout, which holds the geometry: the mark is
//! the *o* of "optersoft" carrying the wordmark's two weights, and in a word it is the
//! uppercase O, scaled to the height of the `f`. Regenerate it there; never retype a path.

/// The mark's outline, as an SVG `d` attribute, in the [`VIEW_BOX`] coordinate system.
pub const PATH: &str = "{d}";

/// The letter's box: its advance width by its height, the baseline {overshoot:.0f} units up from the bottom.
pub const VIEW_BOX: &str = "{view_box}";

/// The brand blue the mark is drawn in.
pub const FILL: &str = "{fill}";

/// Inline style that puts the mark where the glyph would sit: the height and the baseline shift
/// are em fractions of the surrounding text, and the negative margin repeats `tracking-tight`,
/// which letter-spacing applies after a character but not after an element.
pub const STYLE: &str = "height:{height:.3f}em;vertical-align:{shift:.3f}em;margin-right:-.025em";
'''


def write_rust(path: Path) -> list[Path]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        RUST.format(d=LETTER_PATH, view_box=LETTER_VIEWBOX, fill=BLUE, overshoot=OVERSHOOT * K,
                    height=LETTER_HEIGHT_EM, shift=LETTER_SHIFT_EM)
    )
    return [path]


def render(spec: str, out: Path) -> list[Path]:
    """One file from a spec: `mark:<px>`, `tile:<px>` or `ico:<px>,<px>,…`."""
    kind, _, rest = spec.partition(":")
    out.parent.mkdir(parents=True, exist_ok=True)
    if kind == "ico":
        sizes = sorted(int(v) for v in rest.split(","))
        frames = [raster(icon_svg(BLUE, margin=max(1, round(s / 16))), s) for s in sizes]
        buf = io.BytesIO()
        frames[-1].save(buf, "ICO", sizes=[(s, s) for s in sizes], append_images=frames[:-1])
        out.write_bytes(buf.getvalue())
    elif kind in ("wordmark", "letter"):
        # `<kind>:<W>x<H>` or `<kind>:<W>x<H>@blue` — the lockup, or the uppercase O alone.
        size, _, ground = rest.partition("@")
        w, _, hh = size.partition("x")
        w, hh = int(w), int(hh or w)
        maker = wordmark_box if kind == "wordmark" else letter_box
        source = maker(w, hh, on_blue=ground == "blue")
        out.write_bytes(source.encode() if out.suffix == ".svg" else png(raster_wh(source, w, hh)))
    elif kind in ("mark", "tile"):
        px = int(rest)
        source = icon_svg(BLUE, margin=max(1, round(px / 16))) if kind == "mark" else icon_svg(WHITE, ground=BLUE, rounded=False, margin=MARGIN_TILE)
        out.write_bytes(png(raster(source, px)) if out.suffix != ".svg" else source.encode())
    else:
        raise SystemExit(f"unknown render spec {spec!r}: use mark:<px>, tile:<px>, wordmark|letter:<W>x<H>[@blue] or ico:<px>,…")
    return [out]


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--render":
        for p in render(args[1], Path(args[2])):
            print(p)
        raise SystemExit
    if args and args[0] == "--rust":
        for p in write_rust(Path(args[1])):
            print(p)
        raise SystemExit
    if args and args[0] == "--site":
        targets, writer = [Path(a) for a in args[1:]], write_site
    else:
        targets, writer = [Path(a) for a in args] or [ASSETS], write
    for t in targets:
        for p in writer(t):
            print(p)
