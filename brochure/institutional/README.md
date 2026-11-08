# AOE institutional documents

There are three coordinated documents, all built from the same source. They share the same pages, copy and diagrams.

| Document | File | Pages |
|---|---|---|
| A: Comprehensive Institutional Framework & Methodology | `AOE_Institutional_Framework_dark.pdf` | 18 |
| B: Institutional Competency Framework | `AOE_Competency_Framework_dark.pdf` | 12 |
| C: Institutional Implementation Methodology | `AOE_Implementation_Methodology_dark.pdf` | 8 |

- `diagrams/`: each diagram as a standalone vector SVG (dark).
- Editable source:
  - `build.py` holds the copy, the diagram geometry and which pages appear in each document (`DOCS`).
  - `institutional.css` holds the styling.

To edit the copy, change it once in `build.py`. Every document that uses that page updates when you rebuild.

Rebuild:

    python3 build.py      # writes institutional.html, competency-framework.html, implementation-methodology.html
    node render.js        # writes the three dark PDFs, diagrams/*.svg and previews/

Open any of the `.html` files in a browser to preview it. Add `#light` to the URL to see the ivory version.
