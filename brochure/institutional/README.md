# AOE Institutional Framework brochure

- `AOE_Institutional_Framework_dark.pdf` / `AOE_Institutional_Framework_light.pdf`: print-ready A4, 14 pages, with the fonts embedded.
- `diagrams/`: each diagram as a standalone vector SVG, in a dark and a light version, for Illustrator, Figma, Affinity or slides.
- Editable source: the copy and diagram geometry are in `build.py`, and the styling is in `institutional.css`.

Rebuild:

    python3 build.py      # writes institutional.html
    node render.js        # writes both PDFs, diagrams/*.svg and previews/

Open `institutional.html` in a browser to preview it. Add `#light` to the URL to see the ivory version.
