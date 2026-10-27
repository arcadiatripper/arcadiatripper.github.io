#!/usr/bin/env python3
"""Makes the long read's feature pictures (assets/images/flipper/feat_<key>_<lang>.webp) from flipper_snapshot's
site renders (in the flipper repository, under xvfb on Linux), as tools/flipper_features.py lists them:

    ONLY_SITE=1 flipper_snapshot <shots> 2
    python3 tools/make_site_shots.py <shots>
"""

import sys
from pathlib import Path

from PIL import Image

from flipper_features import PARTS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/images/flipper"


def main(shots: Path) -> None:
    for part in PARTS:
        for f in part["features"]:
            if f["shot"] is None or f["shot"][0].startswith("@"):
                continue  # the calculator, or a picture the site already has
            name, (l, t, r, b) = f["shot"]
            for lang in ("ko", "en"):
                src = Image.open(shots / f"site_{name}_{lang}.png").convert("RGB")
                w, h = src.size
                crop = src.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
                if crop.width > 1440:
                    crop = crop.resize((1440, round(crop.height * 1440 / crop.width)), Image.LANCZOS)
                path = OUT / f"feat_{f['key']}_{lang}.webp"
                crop.save(path, "WEBP", quality=86, method=6)
                print("wrote", path.relative_to(ROOT), crop.size)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
