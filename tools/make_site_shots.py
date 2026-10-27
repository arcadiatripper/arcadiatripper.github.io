#!/usr/bin/env python3
"""Makes the long read's feature pictures (assets/images/flipper/feat_<key>_<lang>.webp) from flipper_snapshot's
site renders (in the flipper repository, under xvfb on Linux):

    ONLY_SITE=1 flipper_snapshot <shots> 2
    python3 tools/make_site_shots.py <shots>
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/images/flipper"

# key: (the render's name, the crop as fractions of the window: left, top, right, bottom)
SHOTS = {
    "hits": ("hits", (0, 0.135, 1, 0.53)),
    "grid": ("grid", (0, 0.135, 1, 0.53)),
    "lazy": ("lazy", (0, 0.135, 1, 0.53)),
    "lit": ("lit", (0, 0.135, 1, 1)),
    "dice": ("dice", (0, 0.08, 1, 0.53)),
    "hand": ("zoomed", (0, 0.135, 1, 0.53)),
    "skip": ("skip", (0, 0.135, 1, 0.6)),
    "trims": ("trims", (0, 0.135, 1, 0.6)),
    "slice": ("edit", (0, 0.135, 1, 0.62)),
}


def main(shots: Path) -> None:
    for key, (name, (l, t, r, b)) in SHOTS.items():
        for lang in ("ko", "en"):
            src = Image.open(shots / f"site_{name}_{lang}.png").convert("RGB")
            w, h = src.size
            crop = src.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
            if crop.width > 1440:
                crop = crop.resize((1440, round(crop.height * 1440 / crop.width)), Image.LANCZOS)
            path = OUT / f"feat_{key}_{lang}.webp"
            crop.save(path, "WEBP", quality=86, method=6)
            print("wrote", path.relative_to(ROOT), crop.size)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
