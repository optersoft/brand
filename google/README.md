# `google/` — the Optersoft logo where Google asks for one

Generated, never edited by hand. Every file is **the logo** — the constructed mark, the *o* of
the name carrying the wordmark's two weights — in the brand blue `#2563eb` on an **opaque
white** ground, filled edge to edge. The wordmark is not used here: below ~200 px wide the
lockup stops reading, and every slot Google offers is either square or nearly so.

Two rules, both deliberate:

- **The logo, not the font's capital O.** The real `O` belongs to the lockup
  (`optersoft-wordmark.svg`), where it is a letter in a word. Wherever the shape stands alone —
  a console slot, an icon, a favicon — it is the mark.
- **The ground is white and opaque**, not transparent (2026-09-18). Google composites a logo
  onto a white card in one place and onto its own dark chrome in another, and a transparent PNG
  loses on the second. `alt-white-on-blue-120.png` is the answer for a slot that wants the
  inverse.

| file | slot |
|---|---|
| `oauth-consent-logo-120.png` | Cloud Console → Branding → app logo (120×120) |
| `marketplace-icon-128.png`, `marketplace-icon-32.png` | Workspace Marketplace SDK application icons |
| `admin-custom-logo-320x132.png` | Admin console → Account → Personalization → custom logo (the Gmail header) |
| `marketplace-banner-220x140.png` | Marketplace card banner |
| `optersoft-o-512.png`, `optersoft-o.svg` | the mark itself, for whatever asks next — the same shape as `static/assets/optersoft-o.svg`, but boxed and on white rather than sized for the header's inline `<svg>` |
| `alt-white-on-blue-120.png` | the inverse, for a slot that composites onto its own dark chrome |

To regenerate, from the repo root:

```sh
uv run icons.py --render letter:120x120      google/oauth-consent-logo-120.png
uv run icons.py --render letter:128x128      google/marketplace-icon-128.png
uv run icons.py --render letter:32x32        google/marketplace-icon-32.png
uv run icons.py --render letter:320x132      google/admin-custom-logo-320x132.png
uv run icons.py --render letter:220x140      google/marketplace-banner-220x140.png
uv run icons.py --render letter:512x512      google/optersoft-o-512.png
uv run icons.py --render letter:512x512      google/optersoft-o.svg
uv run icons.py --render letter:120x120@blue google/alt-white-on-blue-120.png
```

⚠ **Uploading is manual, in both consoles**, and a logo change on the OAuth consent screen
can send the app back through verification. Nothing here is served — these are files to hand
to a web form, not assets the chrome ships.
