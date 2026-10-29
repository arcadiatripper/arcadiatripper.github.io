#!/usr/bin/env python3
"""Writes the tripper home page (/ko/ and /en/) from tools/tripper_home/.

    python3 tools/build_home.py

page.html is the page itself (one file for both languages; words swap by data-en). glyphs.json (the dot
logo), shot.txt (the flipper screenshot the dots build) and cat.json (the voxel cat) go into it here.
On the site the address decides the language (/ko/, /en/); the ko / en keys go to the other address.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

import topbar

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "tripper_home"
SITE = "https://arcadiatripper.com"
E = html.escape

GTAG = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-EK4GXNHFLS"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-EK4GXNHFLS');
</script>"""

WORDS = {
    "ko": ("tripper", "tripper의 프로젝트를 하나씩 모아 두는 곳. 001 flipper, 모두를 위한 무료 오픈소스 샘플러 플러그인."),
    "en": ("tripper", "tripper's projects, one by one. 001 flipper, a free, open-source sampler plug-in."),
}


def head(lang: str) -> str:
    title, description = WORDS[lang]
    return f"""<!doctype html>
<!-- Written by tools/build_home.py from tools/tripper_home/page.html: change it there, not here. -->
<html lang="{lang}">
<head>
{GTAG}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="{E(description)}">
<meta name="theme-color" content="#e6eef8">
<link rel="canonical" href="{SITE}/{lang}/">
<link rel="alternate" hreflang="ko" href="{SITE}/ko/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}/{lang}/">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:site_name" content="arcadiatripper">
<meta property="og:image" content="{SITE}/assets/images/og-tripper.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/images/favicon.ico" sizes="any">
<link rel="icon" href="/assets/images/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
"""


def main() -> None:
    page = (SRC / "page.html").read_text(encoding="utf-8")
    data = ("const GLY=" + json.dumps(json.loads((SRC / "glyphs.json").read_text(encoding="utf-8")))
            + ';const SHOT="' + (SRC / "shot.txt").read_text(encoding="utf-8").strip()
            + '";const CAT=' + (SRC / "cat.json").read_text(encoding="utf-8").strip() + ";")
    assert page.count("const GLY=GLYPHS;") == 1
    body = page.replace("const GLY=GLYPHS;", data)
    # page.html starts with its own <title>; the head above goes before it
    for lang in ("ko", "en"):
        page_body = body.replace("<!--TOPBAR-->", topbar.bar(lang, "blue", "/ko/", "/en/", fixed=True), 1)
        page_body = page_body.replace("</main>", "</main>", 1)
        text = head(lang) + topbar.STYLE + "\n" + page_body.replace("<style>", "</head>\n<body>\n<style>", 1)
        text = text.replace("</body>", topbar.SCRIPT + "\n</body>", 1) if "</body>" in text else text + topbar.SCRIPT
        if "</body>" not in text:
            text += "\n</body>\n</html>\n"
        path = ROOT / lang / "index.html"
        path.write_text(text, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
