#!/usr/bin/env python3
"""Puts the flipper guide (샘플러 안내서) and manual (사용 설명서) on the site.

The two pages are written elsewhere, each by its own builder (tutorial/build.py, manual/build_man.py in the
project files), as one self-contained page per language. This script takes those built pages and:
  - wraps them in a full document (head, analytics, icons, canonical and language links),
  - links the header: the logo goes to the flipper page, plus the other document and the other language,
  - points links between the two documents at their site addresses,
  - serves the guide's listening examples from /assets/audio/guide/ (copied from the guide's audio folder).

Usage: python3 tools/build_docs.py [source folder]
The source folder holds tutorial.html, tutorial_en.html, manual.html, manual_en.html and audio/
(default /mnt/project-files/flipper/site-docs). Writes ko|en/flipper/guide/ and ko|en/flipper/manual/.
"""
import re
import shutil
import sys
from pathlib import Path

import topbar

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/flipper/site-docs")
SITE = "https://arcadiatripper.com"

DOCS = {
    "guide": {"ko": "tutorial.html", "en": "tutorial_en.html"},
    "manual": {"ko": "manual.html", "en": "manual_en.html"},
}
NAME = {
    "guide": {"ko": "샘플러가 뭘까?", "en": "what is a sampler?"},
    "manual": {"ko": "flipper 사용설명서", "en": "flipper manual"},
}
DESCRIPTION = {
    "guide": {"ko": "샘플러가 소리를 자르고, 피치를 바꾸고, 옛 기계의 질감을 내는 원리를 듣고 보며 익히는 안내서.",
              "en": "How a sampler cuts sound, changes pitch and gets the grain of old machines, explained with sounds and pictures."},
    "manual": {"ko": "flipper의 기능을 화면 순서대로 설명하는 사용 설명서.",
               "en": "The flipper manual: every feature, screen by screen."},
}
# where the pages lived before the site, so links between them still land
OLD = {
    "https://claude.ai/artifact/KrL6fbpcTcVtwT3u5RxFZq": ("guide", "ko"),
    "https://claude.ai/artifact/3VZryjUPep46U2PS98Q4LP": ("guide", "en"),
    "https://claude.ai/artifact/NDiTZmwrLjqqCAtxpj1Z2e": ("manual", "ko"),
    "https://claude.ai/artifact/AJQiXt8bgroersME8Mextp": ("manual", "en"),
}
AUDIO = "/assets/audio/guide/"

HEAD = """<!doctype html>
<!-- Written by tools/build_docs.py from the {kind} builder's page: change the words there, not here. -->
<html lang="{lang}">
  <head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EK4GXNHFLS"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', 'G-EK4GXNHFLS');
    </script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    {title}
    <meta name="description" content="{description}">
    <link rel="canonical" href="{site}{here}">
    <link rel="alternate" hreflang="ko" href="{site}{ko}">
    <link rel="alternate" hreflang="en" href="{site}{en}">
    <link rel="icon" href="/assets/images/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" href="/assets/images/favicon-32.png" sizes="32x32">
    <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
    <style>
:root{{box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}
html{{scroll-padding-top:env(safe-area-inset-top,0px)}}
body{{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}}
img{{max-width:100%}}
[hidden]:not([hidden=until-found i]){{display:none!important}}
    </style>
{style}
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap">
    <style>
.h1sub{{margin:.3em 0 1.4em;text-align:center;font-size:clamp(17px,2.2vw,22px);font-weight:700;color:var(--soft)}}
    </style>
{tbstyle}
    <style>
a.bar__logo{{color:inherit;text-decoration:none}}
.bar__logo svg{{height:24px}}
.bar .lang{{white-space:nowrap}}
.doclink+.lang{{margin-left:0}}
.foot__in{{align-items:center}}
.foot__tr{{display:block;flex:none;margin-left:auto;color:var(--ink);line-height:0}}
.foot__tr .tb-logo-svg{{height:22px;width:auto}}
@media (max-width:560px){{.foot__in{{flex-direction:column;align-items:flex-start;gap:14px}}.foot__tr{{margin-left:0}}}}
@media (max-width:480px){{.bar__tag{{display:none}}.bar__in{{gap:8px}}.bar .lang{{padding:6px 8px}}}}
    </style>
  </head>
  <body>
"""


def url(kind: str, lang: str) -> str:
    return f"/{lang}/flipper/{kind}/"


def page(kind: str, lang: str) -> str:
    src = (SRC / DOCS[kind][lang]).read_text()
    # day / night follows the device; a press of the key holds only for this visit
    src = src.replace("localStorage", "sessionStorage")
    head, sep, body = src.partition('<header class="bar">')
    if not sep:
        raise SystemExit(f"{DOCS[kind][lang]}: no header bar")
    title = f"<title>{NAME[kind][lang]}</title>"
    style = "\n".join(re.findall(r"<style>.*?</style>", head, re.S))

    bar, _, rest = body.partition("</header>")
    dn = re.search(r'<button type="button" class="dn".*?</button>', bar, re.S).group(0)
    # the shared top bar (tools/topbar.py) in flipper's butter, with the page's own day / night key
    header = topbar.bar(lang, "butter", url(kind, "ko"), url(kind, "en"), extra=dn, night="dark")
    rest = rest.replace("</body></html>", "")
    # the guide's title (2026-10-29): the short question on top, what it teaches under it
    if kind == "guide":
        sub = {"ko": "샘플러가 소리를 다루는 법", "en": "How a sampler handles sound"}[lang]  # not a second question (레네 10-29)
        rest = re.sub(r"<h1>[^<]*</h1>", f'<h1>{NAME[kind][lang][0].upper() + NAME[kind][lang][1:] if lang == "en" else NAME[kind][lang]}</h1>'
                      f'<p class="h1sub">{sub}</p>', rest, count=1)
    for old, (k, l) in OLD.items():
        rest = rest.replace(old, url(k, l))
    rest = rest.replace("'audio/", f"'{AUDIO}")
    # the footer signs with the same dot logo as the top bar and the tripper page (2026-10-29), not the old bold word
    # (logo only, no "© tripper" beside it: 레네 10-29)
    foot = f'<a class="foot__tr" href="/{lang}/" aria-label="tripper">{topbar.LOGO}</a>'
    if "<strong>© tripper</strong>" not in rest:
        raise SystemExit(f"{DOCS[kind][lang]}: no footer signature")
    rest = rest.replace("<strong>© tripper</strong>", foot)
    # links to the other document open in the same tab now
    rest = re.sub(r'(href="/(?:ko|en)/flipper/(?:guide|manual)/") target="_blank" rel="noopener"', r"\1", rest)

    return HEAD.format(
        kind=kind, lang=lang, title=title, description=DESCRIPTION[kind][lang], site=SITE,
        here=url(kind, lang), ko=url(kind, "ko"), en=url(kind, "en"), style=style,
        tbstyle=topbar.STYLE,
    ) + header + rest + "\n" + topbar.SCRIPT + "\n  </body>\n</html>\n"


def main() -> None:
    used = set()
    for kind in DOCS:
        for lang in ("ko", "en"):
            html = page(kind, lang)
            used |= set(re.findall(re.escape(AUDIO) + r"([A-Za-z0-9_.-]+\.wav)", html))
            out = ROOT / lang / "flipper" / kind / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html)
            print(f"wrote {out.relative_to(ROOT)} ({len(html) // 1024} KB)")
    audio = ROOT / AUDIO.strip("/")
    audio.mkdir(parents=True, exist_ok=True)
    for old in audio.glob("*.wav"):
        if old.name not in used:
            old.unlink()
    for name in sorted(used):
        shutil.copy2(SRC / "audio" / name, audio / name)
    print(f"copied {len(used)} sounds to {AUDIO}")


if __name__ == "__main__":
    main()
