# AOE · PanAm Aquatics half-page advertisement

Standalone ad concepts for Architecture of Excellence™. This folder is self-contained and does
not touch the website. Visual identity and messaging come from the live site
(`gh-pages`, architectureofexcellence.com): the aoe lockup, Manrope, the ivory and charcoal palette,
hairline rules, and the thin-circle motif.

## Concepts

| File | Status | Headline |
|---|---|---|
| `final-editorial.html` | **Final, selected.** Editorial refinement of Concept 2 (portrait + A4) | Performance is visible. Its architecture is not. |
| `concept-1-elevation.html` | Alternate | Performance is visible. Its architecture is not. |
| `concept-2-ripple.html` | Basis for the final (dark: `?theme=dark`) | Performance is visible. Its architecture is not. |
| `concept-3-foundation.html` | Alternate (shared as A4) | The Art and Science of High Performance. |

The final ad lists Organizational Consulting · Speaking & Education · Private Advisory. The earlier
concepts list Speaking & Education · 1:1 Performance & Leadership Coaching · Team & Organizational Consulting.

## Preview

Open `index.html` for the gallery (it has a portrait/horizontal toggle), or open a concept directly:

- `?format=v`: portrait, 148 × 210 mm (default)
- `?format=h`: horizontal half page, 210 × 148 mm
- `?format=a4`: full A4 page, 210 × 297 mm (the portrait layout scaled up; the publisher can resize it)
- `?theme=dark`: dark variant (Concept 2)

## Export to PDF

```sh
npm i -D playwright     # or use a global install
node export.js          # all concepts → export/*.pdf + export/*.png
node export.js concept-1
node export.js final    # final ad → portrait + A4 PDFs
```

PDFs are vector, at exact trim size, with fonts embedded as TrueType. Fonts are static Manrope
weights (SIL OFL, `assets/fonts/OFL.txt`). Static files avoid the Type 3 embedding that variable
fonts produce, which print preflight often rejects.

## Before final print

- **Dimensions**: confirm trim size with PanAm Aquatics. Sizes live in `ad.css` (`--v-w`, `--v-h`)
  and `format.js` (`@page`).
- **Bleed and safe area**: add bleed once specs arrive. The charcoal background must extend past the trim.
- **Colour**: files are RGB. The publication may require CMYK (and a specified rich black), so convert
  in Acrobat or InDesign, or ask the printer to handle conversion.
- **Logo**: `assets/aoe-lockup-*.png` are recoloured from the site's `logo-lockup.png` (1807 px wide,
  about 1,000 ppi at 31 mm). A vector (SVG/EPS/PDF) master would be preferable for final output if one exists.
