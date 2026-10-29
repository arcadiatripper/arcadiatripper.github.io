"""The top bar's own fonts, cut to the letters the bar uses and put in the page itself.

The bar used to load JetBrains Mono and IBM Plex Sans KR from Google Fonts, so for a moment the menu showed in the
system font before switching (레네 2026-10-29). Now every build collects the characters in the bar (both languages)
and cuts the fonts in tools/fonts/ (OFL, licences next to them) down to those, as woff2 inside the page: nothing to
fetch, so nothing switches. A new menu word is picked up by the next build on its own.
"""
import base64
import io
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = Path(__file__).resolve().parent / "fonts"
ASCII = "".join(chr(i) for i in range(32, 127))


def _cut(font: TTFont, text: str) -> str:
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = [0, 1, 2]
    s = subset.Subsetter(opts)
    s.populate(text=text)
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


@lru_cache(maxsize=None)
def css(text: str) -> str:
    """@font-face rules for "tb mono" (Latin) and "tb kr" (Hangul), weights 400 and 700, holding only `text`."""
    latin = "".join(sorted(set(ASCII + "".join(c for c in text if ord(c) < 0x1100))))
    hangul = "".join(sorted(set(c for c in text if ord(c) >= 0x1100))) + "?"
    rules = []
    for w in (400, 700):
        mono = instancer.instantiateVariableFont(TTFont(FONTS / "JetBrainsMono[wght].ttf"), {"wght": w})
        rules.append(("tb mono", w, _cut(mono, latin)))
        kr = TTFont(FONTS / f"IBMPlexSansKR-{'Regular' if w == 400 else 'Bold'}.ttf")
        rules.append(("tb kr", w, _cut(kr, hangul)))
    return "<style>\n" + "\n".join(
        f'@font-face{{font-family:"{fam}";font-weight:{w};font-display:block;src:url(data:font/woff2;base64,{b}) format("woff2")}}'
        for fam, w, b in rules) + "\n</style>\n"
