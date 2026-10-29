"""The one top bar every page wears (tripper home, flipper, its guide and manual, artist).

Same place, size, words and behaviour everywhere; only the colour changes with the page (2026-10-29: "the logo
stays, the bar's colour changes per plug-in"): blue glass on the tripper home and the artist page, butter glass
on flipper's pages, a green or silver one for the next plug-in.

    bar(lang, tint, ko_href, en_href, extra="", fixed=False)  -> the <header> html
    STYLE, SCRIPT                                               -> inline <style> / <script>, once per page

Desktop: plugins ▾, articles ▾ and artist on the left, the dot logo in the middle (home), the page's own keys (day / night)
and ko / en on the right. Phones: the logo on the left, the keys, ko / en and a menu key on the right; the menu
opens plugins (flipper), articles (the guide and the manual) and artist; group names bold, links light.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

E = html.escape
GLYPHS = json.loads((Path(__file__).resolve().parent / "tripper_home" / "glyphs.json").read_text(encoding="utf-8"))

# words that change with the language; English words stay the same in both
DOCS = {
    "guide": {"ko": "샘플러가 뭘까?", "en": "what is a sampler?"},
    "manual": {"ko": "flipper 사용설명서", "en": "flipper manual"},
}
MENU = {"ko": "메뉴", "en": "Menu"}


def logo() -> str:
    """The D2 dot logo: 5 x 9 cells per letter, pitch 7, unlit dots at 13 %, in currentColor."""
    pitch, r = 7, 1.3
    dots, x = [], 0
    for ch in "tripper":
        for row, line in enumerate(GLYPHS[ch]):
            for col, c in enumerate(line):
                on = c == "#"
                dots.append(f'<circle cx="{x + col * pitch + pitch / 2:g}" cy="{row * pitch + pitch / 2:g}" '
                            f'r="{r * 1.25 if on else r:g}"{"" if on else " opacity=\".13\""}/>')
        x += 6 * pitch
    return (f'<svg class="tb-logo-svg" viewBox="0 0 {x - pitch} {9 * pitch}" fill="currentColor" aria-hidden="true" '
            f'focusable="false">{"".join(dots)}</svg>')


LOGO = logo()


def bar(lang: str, tint: str, ko_href: str, en_href: str, extra: str = "", fixed: bool = False, night: str = "night") -> str:
    """tint: "blue" (tripper, artist) or "butter" (flipper). extra: the page's own keys, e.g. day / night.
    night: the data-theme value that page's own key sets for night ("night" on flipper, "dark" in the documents)."""
    p = f"/{lang}"

    def doc(kind: str) -> str:
        return (f'<a class="tb-sub" href="{p}/flipper/{kind}/" data-href-en="/en/flipper/{kind}/" '
                f'data-en="{E(DOCS[kind]["en"])}">{E(DOCS[kind][lang])}</a>')

    current = lambda code: ' aria-current="true"' if code == lang else ""
    return f"""<header class="tb tb--{tint}{' tb--fixed' if fixed else ''}" data-tb data-night="{night}">
  <nav class="tb-nav" aria-label="{MENU[lang]}" data-en-label="{MENU['en']}">
    <div class="tb-dd"><button type="button" class="tb-ddk" aria-expanded="false" aria-controls="tb-plugins">plugins<span aria-hidden="true">▾</span></button>
      <div class="tb-ddm" id="tb-plugins" hidden>
        <a class="tb-main" href="{p}/flipper/" data-href-en="/en/flipper/">flipper</a>
      </div>
    </div>
    <div class="tb-dd"><button type="button" class="tb-ddk" aria-expanded="false" aria-controls="tb-articles">articles<span aria-hidden="true">▾</span></button>
      <div class="tb-ddm" id="tb-articles" hidden>
        {doc("guide").replace('class="tb-sub"', 'class="tb-main"')}
        {doc("manual").replace('class="tb-sub"', 'class="tb-main"')}
      </div>
    </div>
    <a href="{p}/artist/" data-href-en="/en/artist/">artist</a>
  </nav>
  <a class="tb-logo" href="{p}/" data-href-en="/en/" aria-label="tripper">{LOGO}</a>
  <div class="tb-r">
    {extra}
    <span class="tb-lang"><a href="{ko_href}" lang="ko" hreflang="ko" data-lang="ko"{current('ko')}>ko</a><span aria-hidden="true">/</span><a href="{en_href}" lang="en" hreflang="en" data-lang="en"{current('en')}>en</a></span>
    <button type="button" class="tb-burger" aria-expanded="false" aria-controls="tb-sheet" aria-label="{MENU[lang]}" data-en-label="{MENU['en']}"><svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true" focusable="false"><path class="tb-b-open" d="M3 4.5h10M3 8h10M3 11.5h10"/><path class="tb-b-shut" d="M4 4l8 8M12 4l-8 8"/></svg></button>
  </div>
  <div class="tb-sheet" id="tb-sheet" hidden>
    <span class="tb-grp">plugins</span>
    <a class="tb-sub" href="{p}/flipper/" data-href-en="/en/flipper/">flipper</a>
    <span class="tb-grp">articles</span>
    {doc("guide")}
    {doc("manual")}
    <a class="tb-grp" href="{p}/artist/" data-href-en="/en/artist/">artist</a>
  </div>
</header>"""


STYLE = """<style>
/* the one top bar (tools/topbar.py): same on every page, tinted per page */
.tb{--tb-ink:#0b2a6f;--tb-soft:#566785;--tb-bg1:rgb(248 251 253/34%);--tb-bg2:rgb(238 243 247/14%);--tb-edge:rgb(255 255 255/70%);
  --tb-drop:rgb(248 251 253/86%);--tb-hover:rgb(31 95 214/10%);
  position:sticky;top:0;z-index:60;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
  padding:14px max(20px,env(safe-area-inset-right,0px)) 14px max(20px,env(safe-area-inset-left,0px));
  background:linear-gradient(180deg,var(--tb-bg1),var(--tb-bg2));
  backdrop-filter:blur(14px) saturate(1.8);-webkit-backdrop-filter:blur(14px) saturate(1.8);
  border-bottom:1px solid var(--tb-edge);box-shadow:0 1px 0 rgb(0 0 0/4%);
  color:var(--tb-ink);font:400 12px/1.4 "tb mono","tb kr",ui-monospace,SFMono-Regular,Menlo,monospace;
  text-transform:lowercase;letter-spacing:0;box-sizing:border-box}
.tb *{box-sizing:border-box}
.tb--fixed{position:fixed;left:0;right:0;top:env(safe-area-inset-top,0px)}
.tb--butter{--tb-ink:#3b2a24;--tb-soft:#766256;--tb-bg1:rgb(255 247 230/62%);--tb-bg2:rgb(255 247 230/34%);--tb-edge:rgb(59 42 36/12%);
  --tb-drop:rgb(255 253 247/94%);--tb-hover:rgb(59 42 36/8%)}
:root[data-theme="night"] .tb--butter[data-night="night"],:root[data-theme="dark"] .tb--butter[data-night="dark"]{--tb-ink:#f7ecd9;--tb-soft:#b59f8b;--tb-bg1:rgb(43 35 30/72%);
  --tb-bg2:rgb(33 27 23/48%);--tb-edge:rgb(255 255 255/8%);--tb-drop:rgb(43 35 30/96%);--tb-hover:rgb(255 255 255/8%)}
.tb a{color:inherit;text-decoration:none}
.tb-nav{display:flex;gap:18px;align-items:center}
.tb-nav>a:hover,.tb-ddk:hover,.tb-nav>a:focus-visible,.tb-ddk:focus-visible{opacity:.65}
.tb-dd{position:relative}
.tb-ddk{font:inherit;text-transform:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;display:inline-flex;gap:4px;align-items:center}
.tb-ddk span{font-size:9px;transition:transform .15s}
.tb-ddk[aria-expanded="true"] span{transform:rotate(180deg)}
.tb-ddm{position:absolute;left:-12px;top:calc(100% + 14px);min-width:220px;padding:6px;display:grid;gap:2px;border:1px solid var(--tb-edge);
  border-radius:10px;background:var(--tb-drop);backdrop-filter:blur(18px) saturate(1.6);-webkit-backdrop-filter:blur(18px) saturate(1.6);
  box-shadow:0 10px 30px rgb(0 0 0/12%)}
.tb-ddm[hidden],.tb-sheet[hidden]{display:none}
.tb-ddm a,.tb-sheet a{display:block;padding:8px 10px;border-radius:6px}
.tb-ddm a:hover,.tb-ddm a:focus-visible,.tb-sheet a:hover,.tb-sheet a:focus-visible{background:var(--tb-hover);outline:none}
.tb-ddm .tb-main{font-weight:400;font-size:13px;text-transform:none}
.tb-ddm{min-width:0;white-space:nowrap}
.tb-ddm .tb-sub{padding:5px 10px 5px 22px;color:var(--tb-soft);text-transform:none}
.tb-logo{display:block;line-height:0;justify-self:center}
.tb-logo-svg{display:block;height:28px;width:auto}
.tb-r{display:flex;align-items:center;gap:14px;justify-self:end}
.tb-lang{display:inline-flex;gap:6px;align-items:center;color:var(--tb-soft)}
.tb-lang a[aria-current="true"]{color:var(--tb-ink);font-weight:700}
.tb-lang a:hover{color:var(--tb-ink)}
.tb-burger{display:none;background:none;border:0;padding:4px;margin-right:-4px;color:inherit;cursor:pointer;line-height:0}
.tb-burger path{fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
.tb-burger .tb-b-shut,.tb-burger[aria-expanded="true"] .tb-b-open{display:none}
.tb-burger[aria-expanded="true"] .tb-b-shut{display:inline}
.tb-sheet{grid-column:1/-1;display:grid;gap:0;padding-top:14px;font-size:15px}
.tb-sheet .tb-grp{font-weight:700}
.tb-sheet .tb-sub{font-weight:400}
.tb-sheet .tb-grp{display:block;padding:8px 10px 2px}
.tb-sheet .tb-sub{text-transform:none}
.tb-sheet .tb-sub+.tb-grp{margin-top:10px}
/* the page's own keys (day / night) sit in the bar as small round keys */
.tb-r>button:not(.tb-burger){width:30px;height:30px;padding:0;display:inline-grid;place-items:center;border-radius:50%;
  border:1px solid var(--tb-edge);background:var(--tb-hover);color:inherit;box-shadow:none;cursor:pointer;margin:0;min-height:0;min-width:0}
.tb-r>button:not(.tb-burger) svg{width:14px;height:14px}
@media (max-width:760px){
  .tb{grid-template-columns:auto 1fr}
  .tb-nav{display:none}
  .tb-logo{justify-self:start;grid-column:1;grid-row:1}
  .tb-logo-svg{height:24px}
  .tb-r{grid-column:2;grid-row:1}
  .tb-burger{display:block}
}
</style>"""

SCRIPT = """<script>
(()=>{const bar=document.querySelector('[data-tb]');if(!bar)return;
 const dds=[...bar.querySelectorAll('.tb-dd')].map(d=>[d.querySelector('.tb-ddk'),d.querySelector('.tb-ddm')]),bg=bar.querySelector('.tb-burger'),sh=bar.querySelector('.tb-sheet');
 const set=(btn,el,on)=>{btn.setAttribute('aria-expanded',String(on));el.hidden=!on;};
 dds.forEach(([k,m])=>k.addEventListener('click',e=>{e.stopPropagation();const on=m.hidden;dds.forEach(([k2,m2])=>set(k2,m2,false));set(k,m,on);}));
 bg.addEventListener('click',e=>{e.stopPropagation();set(bg,sh,sh.hidden);});
 document.addEventListener('click',e=>{dds.forEach(([k,m])=>{if(!m.hidden&&!m.contains(e.target))set(k,m,false);});if(!sh.hidden&&!sh.contains(e.target))set(bg,sh,false);});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){dds.forEach(([k,m])=>set(k,m,false));set(bg,sh,false);}});
 addEventListener('resize',()=>{if(innerWidth>760)set(bg,sh,false);});
 // ko / en remembers the pick, so arcadiatripper.com opens in it next time
 bar.querySelectorAll('.tb-lang a').forEach(a=>a.addEventListener('click',()=>{try{localStorage.setItem('lang',a.dataset.lang);}catch(e){}}));
})();
</script>"""


def _bar_text() -> str:
    """Every character the bar can show, in both languages and all tints."""
    import re
    html = "".join(bar(lang, tint, "/ko/", "/en/") for lang in ("ko", "en") for tint in ("blue", "butter"))
    html = re.sub(r"<svg.*?</svg>", "", html, flags=re.S)
    words = re.sub(r"<[^>]+>", " ", html) + " ".join(re.findall(r'data-en="([^"]*)"', html))
    return "".join(sorted(set(words)))


# the bar's fonts go in the page itself (tools/barfont.py), so the menu never shows in a stand-in font first
import barfont  # noqa: E402
STYLE = barfont.css(_bar_text()) + STYLE
