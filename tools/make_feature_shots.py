#!/usr/bin/env python3
"""Makes the feature slides' pictures (assets/images/flipper/feature_<key>_<lang>.webp) from flipper_snapshot's
renders. Run flipper_snapshot first (in the flipper repository, under xvfb on Linux):

    flipper_snapshot <shots> 2          the sampler pictures
    flipper_snapshot <shots>/fx 2 fx clean
    (the drum pictures come from the drum screen in the same tool)

    python3 tools/make_feature_shots.py <shots>
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets/images/flipper"

# key: (source per language, crop as fractions of the window: left, top, right, bottom)
FEATURES = {
    "lazy": ({"ko": "lazy_ko.png", "en": "lazy_lit_en.png"}, (0, 0, 1, 1)),
    "melody": ({"ko": "keys_ko.png", "en": "keys_en.png"}, (0, 0.28, 1, 1)),
    "key": ({"ko": "day_ko.png", "en": "day_en.png"}, (0.45, 0, 1, 0.42)),
    "repitch": ({"ko": "day_ko.png", "en": "day_en.png"}, (0.3, 0, 0.8, 0.36)),
    "crisp": ({"ko": "day_ko.png", "en": "day_en.png"}, (0.55, 0, 1, 0.42)),
    "channels": ({"ko": "channels_ko.png", "en": "channels_en.png"}, (0.36, 0.145, 1, 0.56)),
    "midi": ({"ko": "day_ko.png", "en": "day_en.png"}, (0, 0.22, 0.62, 0.66)),
    "drum": ({"ko": "drum/drum_clean_ko.png", "en": "drum/drum_clean_en.png"}, (0, 0, 1, 1)),
    "fx": ({"ko": "fx/fx_clean_slot9_all_ko.png", "en": "fx/fx_clean_slot9_all_en.png"}, (0, 0, 1, 0.5)),
    "scratch": ({"ko": "fx/fx_clean_record45.png", "en": "fx/fx_clean_record45.png"}, (0, 0.45, 0.62, 1)),
    "night": ({"ko": "16_repitch_night_ko.png", "en": "night_en.png"}, (0, 0, 1, 1)),
}


def main(shots: Path) -> None:
    for key, (sources, (l, t, r, b)) in FEATURES.items():
        for lang, name in sources.items():
            src = Image.open(shots / name).convert("RGB")
            w, h = src.size
            crop = src.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
            if crop.width > 1280:
                crop = crop.resize((1280, round(crop.height * 1280 / crop.width)), Image.LANCZOS)
            path = OUT / f"feature_{key}_{lang}.webp"
            crop.save(path, "WEBP", quality=86, method=6)
            print("wrote", path.relative_to(ROOT), crop.size)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
