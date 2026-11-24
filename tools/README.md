# profile art

The SVGs in `assets/` are generated. Edit `build.py`, then run from the repo root:

```sh
python3 -m venv .venv && .venv/bin/pip install uharfbuzz fonttools
cd tools && ../.venv/bin/python build.py
```

All text is converted to outlines (Instrument Serif, Space Grotesk, Geist Mono, Bai Jamjuree), because GitHub serves README SVGs as plain images with no web fonts and no JavaScript. Animations are CSS keyframes plus SMIL, and they switch off under `prefers-reduced-motion`. Font paths in `textpath.py` point at local font files; change `G` if yours live elsewhere.
