#!/usr/bin/env python3
"""Writes the flipper pages from one template and the Korean and English words below.

    python3 tools/build_flipper.py

Writes ko/ and en/ (home and flipper/ for each language), plus the small pages at /, /flipper/ and /artist/
that send a visitor to their language. GitHub Pages serves those files as they are; nothing runs on the
server. Change words here, then run this again and commit the output.
While flipper is the only plug-in, each language's home page (/ko/, /en/) shows the flipper page; when a
second plug-in comes, those become pages of plug-in cards and /ko/flipper/, /en/flipper/ stay where they are.
"""

from __future__ import annotations

import html
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://arcadiatripper.com"

# --- switches -------------------------------------------------------------------------------------------------------

# False until the source repository is public and the beta files are on its Releases page.
RELEASED = False
SOURCE_URL = "https://github.com/arcadiatripper/flipper"
RELEASES_URL = SOURCE_URL + "/releases/latest"
INSTALL_URL = {
    "mac": SOURCE_URL + "/blob/main/docs/INSTALL_mac.md",
    "win": SOURCE_URL + "/blob/main/docs/INSTALL_windows.md",
}
# The intro video's YouTube id per language; None leaves the video section out.
VIDEO_ID = {"ko": None, "en": None}

# --- words ----------------------------------------------------------------------------------------------------------

T = {
    "ko": {
        "lang": "ko",
        "locale": "ko_KR",
        "title": "flipper — 모두를 위한 무료 샘플러 플러그인",
        "description": "모두를 위한 무료 오픈소스 샘플러 플러그인. Chop it. Flip it. Cook it. Mac · Windows, AU · VST3.",
        "skip": "본문으로 바로가기",
        "nav_label": "사이트 메뉴",
        "lang_label": "언어",
        "theme_label": "화면 밝기",
        "day": "낮",
        "night": "밤",
        "lang_hint": "English version",
        "lang_hint_close": "닫기",
        "badges": ["FREE", "OPEN SOURCE", "BETA"],
        "lead": "모두를 위한 무료 샘플러 플러그인.",
        "slogan": "Chop it. Flip it. Cook it.",
        "meta": ["Mac · Windows", "AU · VST3", "한국어 · English"],
        "get_mac": "Mac용 받기",
        "get_win": "Windows용 받기",
        "soon": "베타 준비 중",
        "soon_note": "곧 여기서 받을 수 있어요.",
        "free_note": "돈도, 가입도 필요 없어요.",
        "video_title": "flipper 소개 영상",
        "video_soon": "소개 영상 준비 중",
        "screens_title": "화면은 세 개",
        "screens": [
            ("sampler", "샘플러", "샘플 하나를 잘라서 연주해요."),
            ("drum", "드럼", "원샷 16개로 킷을 짜요."),
            ("fx", "fx", "판을 긁고 효과를 걸어요."),
        ],
        "engines_title": "엔진을 바꾸면, 옷도 바뀌어요",
        "engines_sub": "전설적인 샘플러 두 대와 90년대 게임기 소리 칩을, 회로까지 따라 만들었어요.",
        "engines": [
            ("clean", "clean", "샘플 그대로. 늘여도 맑게.", "CLEAN · THE SAMPLE AS IT IS", ""),
            ("black", "black", "80년대 후반의 전설적인 샘플러. 거칠고 묵직하게.", "BLACK · 12-BIT · 26 kHz",
             "회로도대로 만들었어요. 12비트로 담는 방식, 샘플을 건너뛰고 되풀이하는 음정, 출력마다 다른 필터, 움직이는 필터까지. "
             "움직이는 필터는 실제 기계의 녹음과 비교해 맞췄어요."),
            ("grey", "grey", "80년대 후반의 또 다른 전설적인 샘플러. 단단하고 따뜻하게.", "GREY · 12-BIT · 40 kHz",
             "공개된 자료가 적어서 추정한 곳이 있어요: 12비트로 담는 방식, 음정을 바꾸는 방식, 출력 필터의 모양, 잡음 크기. "
             "실제 기계 녹음으로 맞춰 갈 거예요."),
            ("purple", "purple", "90년대 초 게임기의 소리 칩. 동글고 먹먹하게.", "PURPLE · 4-BIT · 32 kHz",
             "칩의 계산(BRR 디코딩, 가우스 보간, 32,040 Hz)은 오픈소스 에뮬레이터 ares와 7,300가지 경우를 비교해 비트 하나까지 같아요. "
             "보드의 필터는 회로도대로예요. 추정은 샘플을 칩의 형식으로 바꾸는 인코더 하나예요."),
        ],
        "engines_tab_label": "엔진 고르기",
        "tempo_title": "키를 내리면, 템포를 알려줘요",
        "tempo_sub": "몇 BPM이 되는지 귀로 맞추지 않아도 돼요.",
        "tempo_bpm": "원래 BPM",
        "tempo_key": "키",
        "tempo_result": "이렇게 돼요",
        "tempo_reverse": "원하는 BPM",
        "tempo_reverse_result": "이만큼 내리면 돼요",
        "tempo_st": "반음",
        "tempo_ct": "센트",
        "slides_title": "핵심 기능",
        "slides": [
            ("lazy", "레이지 찹", "들으면서 톡톡. 친 자리가 잘려요.", ""),
            ("key", "키 찾기", "샘플의 키를 찾고, 튜닝이 몇 센트 어긋났는지도 알려줘요.",
             "직접 만든 분석기(MIT)예요. 음 높이 분포(크로마)를 Albrecht–Shanahan 키 프로필과 맞춰 보고, 키가 적힌 루프 158개로 다듬었어요. "
             "음이 없는 소리엔 키를 붙이지 않아요."),
            ("repitch", "리피치와 템포 유지", "리피치는 옛 샘플러처럼 키와 속도가 같이. 템포 유지는 템포는 그대로 두고 키만.",
             "템포 유지는 Rubber Band R3(GPL)로 미리 구워 두고, 굽는 동안엔 Signalsmith Stretch(MIT)로 바로 들려줘요. "
             "바운스도 구운 소리를 그대로 써서, 들은 그대로 나가요."),
            ("crisp", "또렷하게", "템포 유지로 늘려도 타격이 뭉개지지 않게. 비트와 드럼 루프는 켜고, 멜로디·코드·목소리는 꺼 두세요.",
             "켜면 타격과 타격 사이를 한 조각씩 따로 늘리고, 타격의 앞부분은 원래 소리를 그대로 남겨요. Signalsmith Stretch(MIT)."),
            ("channels", "채널 고르기", "샘플마다 스테레오, 왼쪽, 오른쪽, 가운데, 양옆 중에서 골라요. 다른 샘플러에선 보기 힘든 기능이에요.",
             "가운데 = (L+R)/2, 양옆 = (L−R)/2. 엔진보다 앞, 샘플이 들어오는 자리에서 바꾸고 원래보다 커지지 않아요. 샘플러 화면에서 써요."),
            ("melody", "멜로디", "한 조각을 건반에 깔고, 스케일을 골라요.", ""),
            ("midi", "찹을 MIDI로", "자른 순서를 DAW로 끌어다 놓아요.", ""),
            ("drum", "드럼 킷", "원샷 16개를 칸마다 따로 다듬어요.", ""),
            ("fx", "fx 랙", "필터부터 스페이스까지, 아홉 칸.", "Airwindows(MIT) 모델에 직접 만든 펀치, 퍼즈, 필터를 더했어요."),
            ("scratch", "스크래치", "판을 잡고 긁어요. 베이비, 처프 패턴도.", ""),
            ("night", "낮과 밤", "버튼 하나로 밤 화면.", ""),
        ],
        "slides_prev": "이전",
        "slides_next": "다음",
        "install_title": "설치",
        "install_mac_title": "Mac",
        "install_mac": "Apple Silicon · Intel / AU · VST3",
        "install_win_title": "Windows",
        "install_win": "Windows 10 · 11 (64비트) / VST3",
        "install_guide": "설치 안내",
        "install_note": "베타예요. 이상한 점은 플러그인 오른쪽 아래 버그 제보로 알려주세요. 사용 기록은 보내지 않아요.",
        "faq_title": "자주 묻는 것",
        "faq": [
            ("정말 무료예요?", "네. 돈도 가입도 필요 없고, 소스 코드도 모두 공개해요."),
            ("flipper로 만든 곡을 팔아도 되나요?", "네. flipper로 만든 소리와 곡은 만든 사람의 것이에요. 라이선스는 플러그인 프로그램에 붙는 것이고, 결과물에는 붙지 않아요."),
            ("제 컴퓨터에서 돌아가나요?", "Mac은 Apple Silicon과 Intel 모두, Windows는 64비트 Windows 10과 11에서 돌아가요. ARM Windows는 아직이에요."),
            ("어떤 DAW에서 쓸 수 있나요?", "AU나 VST3 플러그인을 여는 DAW면 돼요. Logic Pro, REAPER, Cubase에서 확인했어요."),
            ("베타라서 조심할 게 있나요?", "macOS는 처음 열 때 한 번 허용해야 하고, Windows는 SmartScreen에서 '추가 정보 → 실행'을 누르면 돼요. 새 버전이 나오면 플러그인 로고 옆에 점이 켜져요."),
            ("소스 코드는 어디 있나요?", "GitHub에 있어요. 우리가 쓴 코드는 MIT, 배포하는 플러그인은 함께 묶인 라이브러리 때문에 AGPL-3.0이에요."),
        ],
        "close_title": "샘플 하나, 꺼내 볼까요?",
        "source": "소스 코드 (GitHub)",
        "source_soon": "소스 코드는 베타와 함께 공개",
        "license": "우리 코드 MIT · 배포하는 플러그인 AGPL-3.0",
        "built_with": "JUCE, Rubber Band, Signalsmith Stretch, Airwindows, FLAC, Ogg Vorbis, Opus로 만들었어요.",
        "fonts": "글꼴: Fredoka, 나눔스퀘어라운드, Barlow, DotGothic16, Jersey 15 · SIL OFL 1.1",
        "made_by": "레네 RENÉ가 만들었어요",
        "foot_line": "모두를 위한 무료 샘플러 플러그인.",
        "foot_links": "LINKS",
        "foot_notes": "MADE WITH",
    },
    "en": {
        "lang": "en",
        "locale": "en_US",
        "title": "flipper — a free sampler plug-in for everyone",
        "description": "A free, open-source sampler plug-in for everyone. Chop it. Flip it. Cook it. Mac · Windows, AU · VST3.",
        "skip": "Skip to content",
        "nav_label": "Site menu",
        "lang_label": "Language",
        "theme_label": "Day or night",
        "day": "day",
        "night": "night",
        "lang_hint": "",
        "lang_hint_close": "",
        "badges": ["FREE", "OPEN SOURCE", "BETA"],
        "lead": "A free sampler plug-in for everyone.",
        "slogan": "Chop it. Flip it. Cook it.",
        "meta": ["Mac · Windows", "AU · VST3", "English · 한국어"],
        "get_mac": "Get it for Mac",
        "get_win": "Get it for Windows",
        "soon": "Beta coming soon",
        "soon_note": "You'll get it right here soon.",
        "free_note": "No money, no sign-up.",
        "video_title": "flipper intro video",
        "video_soon": "Intro video coming soon",
        "screens_title": "Three screens",
        "screens": [
            ("sampler", "sampler", "Chop one sample and play it."),
            ("drum", "drum", "Build a kit from 16 one-shots."),
            ("fx", "fx", "Scratch the record, add effects."),
        ],
        "engines_title": "Change the engine, change the look",
        "engines_sub": "Two legendary samplers and an early-90s console's sound chip, modelled down to the circuits.",
        "engines": [
            ("clean", "clean", "The sample as it is. Clear however far you stretch it.", "CLEAN · THE SAMPLE AS IT IS", ""),
            ("black", "black", "The legendary late-80s sampler. Gritty and heavy.", "BLACK · 12-BIT · 26 kHz",
             "Built to the schematics: how it stores 12 bits, pitch by skipping and repeating samples, a different filter "
             "on each output, and the moving filter, which was checked against recordings of a real unit."),
            ("grey", "grey", "The other legendary late-80s sampler. Tight and warm.", "GREY · 12-BIT · 40 kHz",
             "Little is published about it, so these are estimates: its 12-bit storage, how it changes pitch, the output "
             "filter's shape and the noise level. Recordings of a real unit will tune them."),
            ("purple", "purple", "An early-90s console's sound chip. Round and hazy.", "PURPLE · 4-BIT · 32 kHz",
             "The chip's maths (BRR decoding, gaussian interpolation, 32,040 Hz) matches the open-source emulator ares bit for "
             "bit, across 7,300 test cases. The board's filter follows the schematic. The one estimate: the encoder that turns "
             "a sample into the chip's format."),
        ],
        "engines_tab_label": "Pick an engine",
        "tempo_title": "Pitch it down, it tells you the tempo",
        "tempo_sub": "No more matching the BPM by ear.",
        "tempo_bpm": "Original BPM",
        "tempo_key": "Key",
        "tempo_result": "You get",
        "tempo_reverse": "BPM you want",
        "tempo_reverse_result": "Pitch it by",
        "tempo_st": "st",
        "tempo_ct": "ct",
        "slides_title": "What it does",
        "slides": [
            ("lazy", "Lazy chop", "Tap along. It chops where you tap.", ""),
            ("key", "Key detection", "It finds the sample's key, and how many cents it is off tune.",
             "Our own analyser (MIT): it matches the pitch-class profile (chroma) against the Albrecht–Shanahan key profiles, "
             "tuned on 158 key-labelled loops. A sound with no notes in it gets no key."),
            ("repitch", "Repitch and keep tempo", "Repitch moves key and speed together, like the old samplers. Keep tempo moves the key only.",
             "Keep tempo is baked ahead with Rubber Band R3 (GPL); until the bake is ready you hear Signalsmith Stretch (MIT). "
             "Bounces use the same bake, so what you hear is what you get."),
            ("crisp", "Crisp", "Hits stay sharp when keep tempo stretches. On for beats and drum loops, off for melodies, chords and voices.",
             "When on, each stretch between two hits is done on its own and every hit's attack keeps the original sound. Signalsmith Stretch (MIT)."),
            ("channels", "Channel select", "Per sample: stereo, left, right, mid or side. Something you rarely find in other samplers.",
             "Mid = (L+R)/2, side = (L−R)/2. Picked where the sample comes in, before the engine, and never louder than the source. On the sampler screen."),
            ("melody", "Melody", "One slice across the keys, in the scale you pick.", ""),
            ("midi", "Chop to MIDI", "Drag the chop order into your DAW.", ""),
            ("drum", "Drum kit", "16 one-shots, each trimmed on its own.", ""),
            ("fx", "fx rack", "Nine slots, from filter to space.", "Airwindows (MIT) models, plus our own punch, fuzz and filter."),
            ("scratch", "Scratch", "Grab the record. Baby and chirp patterns too.", ""),
            ("night", "Day and night", "One button for the night look.", ""),
        ],
        "slides_prev": "Previous",
        "slides_next": "Next",
        "install_title": "Install",
        "install_mac_title": "Mac",
        "install_mac": "Apple Silicon · Intel / AU · VST3",
        "install_win_title": "Windows",
        "install_win": "Windows 10 · 11 (64-bit) / VST3",
        "install_guide": "Install guide",
        "install_note": "It's a beta. If something looks wrong, use the bug report key at the bottom right of the plug-in. It sends no usage data.",
        "faq_title": "Questions",
        "faq": [
            ("Is it really free?", "Yes. No money, no sign-up, and all of the source code is public."),
            ("Can I sell music I make with flipper?", "Yes. The sounds and songs you make are yours. The licence covers the plug-in program, not what you make with it."),
            ("Will it run on my computer?", "On Macs with Apple Silicon or Intel, and on 64-bit Windows 10 and 11. Not on ARM Windows yet."),
            ("Which DAWs?", "Any DAW that opens AU or VST3 plug-ins. Checked in Logic Pro, REAPER and Cubase."),
            ("Anything to know about the beta?", "macOS asks you to allow it once the first time; on Windows, click 'More info → Run anyway' in SmartScreen. When a new version is out, a dot lights up by the plug-in's logo."),
            ("Where is the source code?", "On GitHub. The code we wrote is MIT; the plug-in we ship is AGPL-3.0 because of the libraries bundled with it."),
        ],
        "close_title": "Got a sample? Let's flip it.",
        "source": "Source code (GitHub)",
        "source_soon": "Source code goes public with the beta",
        "license": "Our code MIT · the shipped plug-in AGPL-3.0",
        "built_with": "Built with JUCE, Rubber Band, Signalsmith Stretch, Airwindows, FLAC, Ogg Vorbis and Opus.",
        "fonts": "Fonts: Fredoka, NanumSquareRound, Barlow, DotGothic16, Jersey 15 · SIL OFL 1.1",
        "made_by": "Made by RENÉ (레네)",
        "foot_line": "A free sampler plug-in for everyone.",
        "foot_links": "LINKS",
        "foot_notes": "MADE WITH",
    },
}

# --- pieces ---------------------------------------------------------------------------------------------------------

E = html.escape


def download_block(t: dict) -> str:
    if RELEASED:
        return f"""
          <div class="get">
            <a class="key key--pick" href="{RELEASES_URL}">{E(t['get_mac'])}</a>
            <a class="key" href="{RELEASES_URL}">{E(t['get_win'])}</a>
          </div>
          <p class="get__note">{E(t['free_note'])}</p>"""
    return f"""
          <div class="get">
            <span class="key key--waiting" aria-disabled="true">{E(t['soon'])}</span>
          </div>
          <p class="get__note">{E(t['soon_note'])}</p>"""


def video_block(lang: str, t: dict) -> str:
    """The intro video, big under the title. Until it is out, its frame shows the plug-in and says it is coming."""
    vid = VIDEO_ID.get(lang)
    if vid:
        inner = (f'<iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(t["video_title"])}" loading="lazy"'
                 ' referrerpolicy="strict-origin-when-cross-origin"'
                 ' allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"'
                 ' allowfullscreen></iframe>')
    else:
        inner = (f'{shot("screen_sampler", lang, t["video_title"], eager=True)}'
                 f'<span class="video__soon"><i aria-hidden="true">▶</i>{E(t["video_soon"])}</span>')
    return f"""
        <div class="video card" id="video">{inner}</div>"""

def shot(name: str, lang: str, alt: str, link: bool = False, eager: bool = False) -> str:
    """A plug-in screen: the English picture on English pages when there is one, and the night picture next to
    it when there is one (the page's day / night button shows one of the two)."""
    folder = ROOT / "assets/images/flipper"

    def pick(stem: str) -> str | None:
        for candidate in (f"{stem}_{lang}.webp", f"{stem}_ko.webp"):
            if (folder / candidate).exists():
                return candidate
        return None

    day = pick(name)
    night = pick(f"{name}_night")
    loading = "eager" if eager else "lazy"
    img = (f'<img class="shot{" shot--day" if night else ""}" src="/assets/images/flipper/{day}" width="960" height="639"'
           f' alt="{E(alt)}" loading="{loading}">')
    if night:
        img += (f'<img class="shot shot--night" src="/assets/images/flipper/{night}" width="960" height="639"'
                f' alt="{E(alt)}" loading="lazy">')
    return f'<a class="zoom" href="/assets/images/flipper/{day}">{img}</a>' if link else img


def slides_block(lang: str, t: dict) -> str:
    """The main features, one picture and one line each, turned like pages (scroll-snap, arrows and dots)."""
    slides, dots = [], []
    count = len(t["slides"])
    for i, (key, name, text, how) in enumerate(t["slides"]):
        how_line = f'<p class="slide__how">{E(how)}</p>' if how else ""
        slides.append(f"""
            <li class="slide" id="feature-{key}" aria-roledescription="slide" aria-label="{i + 1} / {count}">
              <div class="slide__shot card">{shot(f'feature_{key}', lang, name)}</div>
              <div class="slide__body"><p class="slide__n">{i + 1:02d} / {count:02d}</p><h3>{E(name)}</h3><p class="slide__text">{E(text)}</p>{how_line}</div>
            </li>""")
        dots.append(f'<button type="button" class="slides__dot" aria-label="{E(name)}" data-slide-to="{i}"></button>')
    return f"""
          <div class="slides" data-slides aria-roledescription="carousel">
            <ul class="slides__track" data-slides-track tabindex="0">{''.join(slides)}
            </ul>
            <div class="slides__controls">
              <button type="button" class="slides__arrow" data-slides-prev aria-label="{E(t['slides_prev'])}">←</button>
              <div class="slides__dots">{''.join(dots)}</div>
              <button type="button" class="slides__arrow" data-slides-next aria-label="{E(t['slides_next'])}">→</button>
            </div>
          </div>"""


def engines_block(lang: str, t: dict) -> str:
    tabs, panels = [], []
    for i, (key, name, text, plate, how) in enumerate(t["engines"]):
        how_line = f'<p class="engine__how">{E(how)}</p>' if how else ""
        selected = "true" if i == 0 else "false"
        hidden = "" if i == 0 else " hidden"
        tabs.append(
            f'<button class="seg__item" type="button" role="tab" id="engine-tab-{key}" aria-controls="engine-{key}"'
            f' aria-selected="{selected}" data-skin="{key}"><i class="led" aria-hidden="true"></i>{E(name)}</button>'
        )
        panels.append(f"""
            <div class="engine" role="tabpanel" id="engine-{key}" aria-labelledby="engine-tab-{key}"{hidden}>
              <div class="engine__shot">{shot(f'engine_{key}', lang, name)}</div>
              <div class="engine__body">
                <p class="engine__plate">{E(plate)}</p>
                <p class="engine__text">{E(text)}</p>{how_line}
              </div>
            </div>""")
    return f"""
          <div class="engines__keys">
            <div class="seg" role="tablist" aria-label="{E(t['engines_tab_label'])}">{''.join(tabs)}</div>
            {night_key(t, "data-look-toggle", " night-key--engines")}
          </div>
          {''.join(panels)}"""


# The long read: each part of the plug-in, what it does and why it is that way. Every claim here is in the plug-in's
# design notes (flipper docs/DESIGN.md, DRUM.md, DECK.md, RECORDING.md); the quotes are 레네's own words from them.
DEEP = {
    "ko": {
        "title": "하나하나, 직접 다듬었어요",
        "lead": "요즘 나오는 샘플러를 따라 만든 게 아니에요. 비트를 만들면서 걸리던 것들을 하나씩 정해서 만들었어요. "
                "아래는 그 결정들이에요.",
        "quote_by": "만든 사람의 메모",
        "parts": [
            {
                "key": "chop", "shot": "feature_lazy",
                "title": "자르기",
                "lead": "샘플 한 부분을 잘라 새 소리처럼 들리게 하는 것. flipper가 가장 잘하려는 일이에요.",
                "points": [
                    "네 가지 방법: 타격 찾기(감도를 움직이면 바로 다시 잘림), 박자(1/16부터 한 마디), 레이지 찹, 주사위.",
                    "레이지 찹: 재생하면서 패드든 건반이든 치면 그 자리에서 잘려요. 박보다 조금 일찍 쳐도 80 ms 앞부터 60 ms 뒤까지의 "
                    "타격을 찾아 붙여서, 실제 드럼 루프에서 탭의 90–100 %가 제자리에 붙어요.",
                    "불 켜진 패드 방식: 다음 조각의 패드만 불이 들어오고, 그 패드를 눌러야 잘려요. 옛 기계처럼.",
                    "주사위: 굴릴 때마다 새 찹. 끌어서 혼돈을 0–100 %로 정해요. 0 %는 뚜렷한 타격만 고르게, 100 %는 완전히 마음대로.",
                    "건너뛰기: 카운트인이나 숨소리는 지우지 않고 빼 둬요. 파일은 그대로고, 언제든 되돌릴 수 있어요.",
                    "최대 64조각. 조각마다 설정은 다섯 개뿐이에요: 음높이, 리버스, 볼륨, 페이드 인, 페이드 아웃.",
                ],
                "quote": "레이지찹 기능이 있는 샘플러가 없어서 이걸 만들고 있는 거기도 하거든.",
            },
            {
                "key": "keys", "shot": "feature_repitch",
                "title": "키와 템포",
                "lead": "키와 속도는 패드마다가 아니라 샘플 하나에 있어요. 샘플 하나를 통째로 다른 곡처럼 만들기 위해서예요.",
                "points": [
                    "리피치: 옛 샘플러처럼 키를 내리면 느려지고 어두워져요. 디지털 잡음이 생기지 않아요.",
                    "템포 유지: 템포는 그대로 두고 키만 바꿔요. 소리는 미리 구워 두고, 굽는 동안에도 바로 들려요.",
                    "키를 내리면 몇 BPM이 되는지 알려주고, 반대로 원하는 BPM을 치면 몇 반음 몇 센트를 내리면 되는지 알려줘요. "
                    "메트로놈에 귀로 맞추던 계산이에요.",
                    "DAW 템포 키 하나로 지금 곡의 템포에 맞춰요.",
                    "키 칩: 샘플의 키와, 지금 키 노브로 들리는 키를 같이 보여줘요(예: Am → Gm).",
                ],
                "tempo": True,
                "quote": "",
            },
            {
                "key": "play", "shot": "feature_melody",
                "title": "연주",
                "lead": "샘플러는 덱 하나처럼 움직여요. 패드마다 따로 놀지 않아요.",
                "points": [
                    "패드 16개나 32개, 페이지를 넘겨 64조각까지. 패드 1번이 C3이에요.",
                    "모노(기본): 새 패드가 앞 소리를 5 ms 만에 끊어요. 덱 하나로 찹을 연주하듯이. 폴리: 소리가 겹쳐요.",
                    "누르는 동안 / 슬라이스 전체: 누른 만큼만, 또는 다음 마커까지 끝까지. 어느 쪽이든 조각은 자기 끝에서 멈춰요.",
                    "멜로디: 한 조각을 건반에 깔아요. 반음씩, 또는 스케일 여덟 가지(장조, 단조, 도리안, 프리지안, 믹솔리디안, "
                    "화성 단조, 장 · 단 펜타토닉). 흰 건반 배치를 고르면 어느 스케일이든 C장조처럼 쳐요.",
                    "원키는 C3에 묶여 있지 않아요. 옮기거나, 건반을 오른쪽 클릭해 그 건반을 원키로.",
                ],
                "quote": "키보드 연주할 때 온음계가 편하거든.",
            },
            {
                "key": "sample", "shot": "feature_channels",
                "title": "샘플 담기",
                "lead": "샘플은 파일을 끌어 놓거나, DAW의 소리를 바로 녹음해서 들어와요.",
                "points": [
                    "녹음: 다른 트랙(사이드체인)이나 flipper 자신의 출력(리샘플). 바로 또는 다음 마디부터, 멈출 때까지 또는 1 · 2 · 4 · 8마디.",
                    "채널 고르기: 스테레오, 왼쪽, 오른쪽, 가운데, 양옆. 가운데를 고르면 가운데에 있는 소리가, 양옆을 고르면 넓게 퍼진 소리가 남아요.",
                    "전체 샘플 게인: 엔진 뒤, fx 앞에서 샘플 하나의 크기를 맞춰요. 노멀라이즈도 여기로.",
                    "어느 나라 말의 파일 이름이든 열려요.",
                ],
                "quote": "",
            },
            {
                "key": "deck", "shot": "feature_fx",
                "title": "fx와 턴테이블",
                "lead": "fx 화면에는 이펙트 랙과, 자른 구간을 판처럼 돌리는 턴테이블이 있어요.",
                "points": [
                    "랙 열 칸: 필터, 펀치, 디스토트, 크러시, 테이프, 코러스, 노이즈, 에코, 스페이스, 전체. 처음엔 다 꺼져 있고, "
                    "노브를 올리면 켜져요. 꺼진 칸은 CPU를 쓰지 않아요.",
                    "에코와 흔들림은 DAW의 박을 따라가서, 바운스해도 들은 그대로예요.",
                    "fx 패드: 누르는 동안만 걸리는 효과.",
                    "판: 33⅓ rpm. 마우스나 컨트롤러로 잡아서 긁어요. 손 움직임은 부드럽게 이어져서, 바늘이 튀지 않아요.",
                    "스크래치 패턴: 베이비, 처프, 트랜스, 플레어 등. 건반 16개로 조각을 골라 긁고, 세게 칠수록 멀리 밀어요.",
                    "곡 따라 돌기: DAW를 재생하면 판도 큐부터 곡에 맞춰 돌아요.",
                ],
                "quote": "",
            },
            {
                "key": "drum", "shot": "feature_drum",
                "title": "드럼",
                "lead": "원샷 16개로 킷을 짜는 화면이에요. 샘플러와 같은 플러그인 안에 있어요.",
                "points": [
                    "셀마다 엔진(clean · grey · black · purple), 볼륨, 팬, 음높이 ±24, 페이드, 초크 그룹 1–4.",
                    "출력 16개: 셀마다 DAW의 다른 트랙으로 보낼 수 있어요.",
                    "에코와 스페이스는 셀마다 보내는 양만 정하고, 무거운 이펙트는 하나만 돌려요(CPU).",
                    "MIDI 채널 10의 C1부터 셀 1–16. 샘플러 패드와 겹치지 않게 구역이 나뉘어 있어요.",
                    "킷 파일(.flipkit)로 저장하고 다른 프로젝트에서 열어요. 파일 여러 개를 한 번에 끌어 놓으면 차례로 채워져요.",
                ],
                "quote": "",
            },
            {
                "key": "out", "shot": "feature_midi",
                "title": "내보내기와 안전",
                "lead": "만든 것은 그대로 DAW로 가고, 갑자기 큰 소리는 나지 않게 했어요.",
                "points": [
                    "찹을 MIDI로: 루프가 각 조각에 닿는 순간 그대로 MIDI 클립을 만들어, DAW 트랙에 끌어 놓아요. 원래 그루브에서 시작해요.",
                    "바운스 = 연주: 블록 크기 1부터 4096까지, 실시간이든 오프라인이든 같은 소리예요.",
                    "MIDI 지정: 연주에 쓰는 컨트롤은 모두 MIDI로 지정할 수 있어요.",
                    ".flip 파일 하나에 샘플과 찹, 설정이 다 들어가요.",
                    "갑자기 큰 소리를 가장 심각한 버그로 다뤄요. 원인을 고치고 테스트로 막았어요. 평소 소리를 바꾸는 리미터는 넣지 않았고, "
                    "맨 끝의 안전 리미터(세이프 · 빈티지 · 끔)는 고를 수 있어요.",
                ],
                "quote": "",
            },
        ],
    },
    "en": {
        "title": "Shaped by hand, one decision at a time",
        "lead": "flipper is not a copy of today's samplers. It was built by fixing, one at a time, the things that got in "
                "the way of making beats. These are those decisions.",
        "quote_by": "maker's note",
        "parts": [
            {
                "key": "chop", "shot": "feature_lazy",
                "title": "Chop",
                "lead": "Take one part of a sample and chop it until it sounds new. This is what flipper tries to do best.",
                "points": [
                    "Four ways: hits (move the sensitivity and it re-chops at once), beats (1/16 to a bar), lazy chop and the die.",
                    "Lazy chop: it plays, you tap a pad or any key, it cuts there. Tap a little early and it finds the hit "
                    "from 80 ms before to 60 ms after; on real drum loops 90–100 % of taps land on their hit.",
                    "Lit pad: only the next slice's pad lights up and cuts, as on the old machines.",
                    "The die: a new chop on every roll. Drag to set the chaos, 0–100 %: 0 % picks only clear hits, evenly; "
                    "100 % is pure chance.",
                    "Skip: a count-in or a breath is left out, not cut out. The file is untouched and it can come back any time.",
                    "Up to 64 slices, and only five settings each: pitch, reverse, level, fade in, fade out.",
                ],
                "quote": "There was no sampler with a lazy chop. That's part of why I'm making this.",
            },
            {
                "key": "keys", "shot": "feature_repitch",
                "title": "Key and tempo",
                "lead": "Key and speed belong to the whole sample, not to each pad, so one sample can become a different track.",
                "points": [
                    "Repitch: like the old samplers, pitch it down and it slows down and darkens. No digital artefacts.",
                    "Keep tempo: the tempo stays and only the key moves. The sound is baked ahead, and you hear it at once while it bakes.",
                    "Pitch it down and it tells you the tempo you land on. Type the BPM you want and it tells you the "
                    "semitones and cents. The sum producers used to do by ear against a metronome.",
                    "One DAW tempo key matches the song's tempo.",
                    "The key chip shows the sample's key and the key it sounds in with the key knob (e.g. Am → Gm).",
                ],
                "tempo": True,
                "quote": "",
            },
            {
                "key": "play", "shot": "feature_melody",
                "title": "Play",
                "lead": "The sampler moves like one deck. The pads don't each go their own way.",
                "points": [
                    "16 or 32 pads, with pages up to 64 slices. Pad 1 is C3.",
                    "Mono (the default): a new pad cuts the last sound in 5 ms, like a chop played on one deck. Poly: sounds overlap.",
                    "While held / whole slice: as long as you hold it, or on to the next marker. Either way a slice stops at its own end.",
                    "Melody: one slice across the keys, by semitone or in one of eight scales (major, minor, dorian, "
                    "phrygian, mixolydian, harmonic minor, major and minor pentatonic). With the white-keys layout, every scale plays like C major.",
                    "The root isn't stuck on C3: move it, or right-click a key to make it the root.",
                ],
                "quote": "A diatonic scale is easier when you play it on a keyboard.",
            },
            {
                "key": "sample", "shot": "feature_channels",
                "title": "Bring a sample in",
                "lead": "Drop a file, or record the DAW's sound straight in.",
                "points": [
                    "Record: another track (side-chain) or flipper's own output (resample). Now or from the next bar; "
                    "until you stop, or 1, 2, 4 or 8 bars.",
                    "Channel select: stereo, left, right, mid or side. Mid keeps what sits in the centre, side keeps what is spread wide.",
                    "Whole sample gain: one sample's level, after the engine and before the fx. Normalize sets it.",
                    "File names in any language open.",
                ],
                "quote": "",
            },
            {
                "key": "deck", "shot": "feature_fx",
                "title": "fx and the turntable",
                "lead": "The fx screen has the effect rack, and a turntable that plays the chopped range like a record.",
                "points": [
                    "Ten rack slots: filter, punch, distort, crush, tape, chorus, noise, echo, space, all. All off at first; "
                    "turn a knob up and it comes on. An off slot uses no CPU.",
                    "Echoes and wobbles follow the DAW's beat, so a bounce sounds as it was heard.",
                    "fx pads: effects that last while you hold them.",
                    "The record: 33⅓ rpm. Grab it with the mouse or a controller and scratch. Hand moves are smoothed, so the needle never jumps.",
                    "Scratch patterns: baby, chirp, transformer, flare and more. 16 keys pick the slice; harder hits push further.",
                    "Follow the song: when the DAW plays, the record starts from its cue, in time.",
                ],
                "quote": "",
            },
            {
                "key": "drum", "shot": "feature_drum",
                "title": "Drums",
                "lead": "A screen for building a kit from 16 one-shots, inside the same plug-in as the sampler.",
                "points": [
                    "Each cell: its own engine (clean, grey, black, purple), level, pan, pitch ±24, fades, choke group 1–4.",
                    "16 outputs: send any cell to its own DAW track.",
                    "Echo and space: each cell sets only how much it sends; one heavy effect runs for all (CPU).",
                    "MIDI channel 10 from C1 plays cells 1–16. The zones are laid out so they never clash with the sampler's pads.",
                    "Save as a kit file (.flipkit) and open it in another project. Drop several files at once and they fill in order.",
                ],
                "quote": "",
            },
            {
                "key": "out", "shot": "feature_midi",
                "title": "Out, and safe",
                "lead": "What you make goes straight to the DAW, and nothing suddenly gets loud.",
                "points": [
                    "Chop to MIDI: a clip that plays each slice at the moment the loop reaches it, dragged onto a DAW track. "
                    "Start from the sample's own groove.",
                    "Bounce = live: the same sound at block sizes from 1 to 4096, real time or offline.",
                    "MIDI learn: every control you perform with can be learned.",
                    "One .flip file holds the sample, the chop and the settings.",
                    "A sudden loud sound is treated as the worst bug: the causes are fixed and tests guard them. No limiter colours "
                    "the everyday sound; the safety limiter at the very end (safe, vintage, off) is your choice.",
                ],
                "quote": "",
            },
        ],
    },
}


def deep_block(lang: str, t: dict) -> str:
    """The long read: one row per part, a picture and what it does (the tempo calculator inside key and tempo)."""
    d = DEEP[lang]
    rows = []
    for i, part in enumerate(d["parts"]):
        points = "".join(f"<li>{E(p)}</li>" for p in part["points"])
        quote = (f'<blockquote class="deep__quote"><p>“{E(part["quote"])}”</p><cite>{E(d["quote_by"])}</cite></blockquote>'
                 if part["quote"] else "")
        tool = tempo_block(t) if part.get("tempo") else ""
        rows.append(f"""
          <article class="deep__part{' deep__part--flip' if i % 2 else ''}" id="more-{part['key']}" data-reveal>
            <div class="deep__shot card">{shot(part['shot'], lang, part['title'])}</div>
            <div class="deep__body">
              <p class="deep__n">{i + 1:02d}</p>
              <h3>{E(part['title'])}</h3>
              <p class="deep__lead">{E(part['lead'])}</p>
              <ul class="deep__points">{points}</ul>{quote}{tool}
            </div>
          </article>""")
    return f"""
          <header class="heading heading--center" data-reveal><h2 id="more-title">{E(d['title'])}</h2><p>{E(d['lead'])}</p></header>
          <div class="deep">{''.join(rows)}
          </div>"""


def tempo_block(t: dict) -> str:
    return f"""
          <div class="tempo card" data-tempo>
            <div class="tempo__row">
              <label class="field">
                <span>{E(t['tempo_bpm'])}</span>
                <input type="number" inputmode="decimal" min="40" max="300" step="0.1" value="120" data-tempo-bpm>
              </label>
              <label class="field field--wide">
                <span>{E(t['tempo_key'])} <output data-tempo-key-out>−5 {E(t['tempo_st'])}</output></span>
                <input type="range" min="-12" max="12" step="1" value="-5" data-tempo-key>
              </label>
              <div class="tempo__result">
                <span>{E(t['tempo_result'])}</span>
                <output data-tempo-out>89.9 BPM</output>
              </div>
            </div>
            <div class="tempo__row tempo__row--reverse">
              <label class="field">
                <span>{E(t['tempo_reverse'])}</span>
                <input type="number" inputmode="decimal" min="40" max="300" step="0.1" value="90" data-tempo-target>
              </label>
              <div class="tempo__result tempo__result--small">
                <span>{E(t['tempo_reverse_result'])}</span>
                <output data-tempo-rev-out data-st="{E(t['tempo_st'])}" data-ct="{E(t['tempo_ct'])}">−5 {E(t["tempo_st"])} +2 {E(t["tempo_ct"])}</output>
              </div>
            </div>
          </div>"""


def install_block(t: dict) -> str:
    def card(os_key: str, title: str, line: str) -> str:
        guide = (f'<a class="text-key" href="{INSTALL_URL[os_key]}">{E(t["install_guide"])} →</a>' if RELEASED else "")
        return f"""
            <article class="card install" data-reveal>
              <h3>{E(title)}</h3>
              <p>{E(line)}</p>
              {guide}
            </article>"""
    return card("mac", t["install_mac_title"], t["install_mac"]) + card("win", t["install_win_title"], t["install_win"])

def faq_block(t: dict) -> str:
    return "".join(
        f'<details class="faq__item"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in t["faq"]
    )


GTAG = """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-EK4GXNHFLS"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-EK4GXNHFLS');
    </script>"""

# The pages at /, /flipper/ and /artist/ have no language of their own: they send the visitor to /ko/… or /en/…
# by the language they last picked on the site, else their browser's. The old portfolio lived at / with
# anchors (arcadiatripper.com/#discography …); those go on to the artist page.
CHOOSER = """<!doctype html>
<!-- Written by tools/build_flipper.py. -->
<html lang="en">
  <head>
{gtag}
    <script>
      (function () {{
        var lang = null;
        try {{ lang = localStorage.getItem('lang'); }} catch (error) {{}}
        if (lang !== 'ko' && lang !== 'en') {{
          var list = navigator.languages || [navigator.language || ''];
          lang = /^ko\\b/i.test(list[0] || '') || list.some(function (l) {{ return /^ko\\b/i.test(l); }}) ? 'ko' : 'en';
        }}
        var page = '{page}';
        var hash = location.hash;
        var old = ['#top', '#discography', '#guides', '#writing', '#credits', '#playlists', '#legacy', '#about'];
        if (page === '' && old.indexOf(hash) > -1) {{ page = 'artist/'; if (hash === '#top') hash = ''; }}
        location.replace('/' + lang + '/' + page + hash);
      }})();
    </script>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="alternate" hreflang="ko" href="{site}/ko/{page}">
    <link rel="alternate" hreflang="en" href="{site}/en/{page}">
    <link rel="alternate" hreflang="x-default" href="{site}/{page}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{site}/{page}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="arcadiatripper">
    <meta property="og:image" content="{site}/assets/images/{image}">
    <meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="/assets/images/favicon.ico" sizes="any">
  </head>
  <body>
    <p><a href="/ko/{page}" lang="ko" hreflang="ko">한국어</a> · <a href="/en/{page}" lang="en" hreflang="en">English</a></p>
  </body>
</html>
"""

CHOOSERS = {
    "": ("flipper — 무료 샘플러 · free sampler plug-in",
         "모두를 위한 무료 오픈소스 샘플러 플러그인. A free, open-source sampler plug-in for everyone. Chop it. Flip it. Cook it.",
         "flipper/og-flipper.png"),
    "flipper/": ("flipper — 무료 샘플러 · free sampler plug-in",
                 "모두를 위한 무료 오픈소스 샘플러 플러그인. A free, open-source sampler plug-in for everyone. Chop it. Flip it. Cook it.",
                 "flipper/og-flipper.png"),
    "artist/": ("레네 RENÉ / arcadiatripper", "Music, guides and playlists by 레네 (tripper).", "og-arcadiatripper.jpg"),
}


# The tripper logo (D2, picked 2026-10-27): "tripper" in round dots on a 5 x 9 grid, as on an mp3 player's
# screen. The unlit dots of each letter's cell stay faintly visible, like an LCD that is switched on.
TRIPPER_GLYPHS = {
    "t": [".#...", ".#...", "####.", ".#...", ".#...", ".#..#", "..##.", ".....", "....."],
    "r": [".....", ".....", "#.##.", "##..#", "#....", "#....", "#....", ".....", "....."],
    "i": ["..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###.", ".....", "....."],
    "p": [".....", ".....", "####.", "#...#", "#...#", "#...#", "####.", "#....", "#...."],
    "e": [".....", ".....", ".###.", "#...#", "#####", "#....", ".###.", ".....", "....."],
}


def tripper_logo() -> str:
    """The logo as inline svg in currentColor, so it follows the top bar's ink by day and by night."""
    lit, off = [], []
    for n, ch in enumerate("tripper"):
        for y, row in enumerate(TRIPPER_GLYPHS[ch]):
            for x, c in enumerate(row):
                dot = f'<circle cx="{(n * 6 + x) * 10 + 5}" cy="{y * 10 + 5}" r="3.8"/>'
                (lit if c == "#" else off).append(dot)
    return ('<svg class="gnav__logo" viewBox="0 0 410 90" aria-hidden="true" focusable="false">'
            f'<g class="gnav__logo-off">{"".join(off)}</g><g>{"".join(lit)}</g></svg>')


TRIPPER_LOGO = tripper_logo()

# The plug-in's own day / night icons (clean skin, Icons.cpp): on its 12-unit grid, strokes 1.75 with round ends.
MOON_PATH = "M10.42 7.59 L10.30 7.89 L10.16 8.19 L10.00 8.47 L9.81 8.75 L9.61 9.01 L9.39 9.25 L9.16 9.48 L8.91 9.69 L8.64 9.89 L8.37 10.06 L8.08 10.22 L7.78 10.35 L7.47 10.46 L7.16 10.56 L6.84 10.63 L6.51 10.67 L6.18 10.70 L5.86 10.70 L5.53 10.68 L5.20 10.63 L4.88 10.57 L4.57 10.48 L4.26 10.36 L3.96 10.23 L3.67 10.08 L3.39 9.91 L3.12 9.72 L2.87 9.51 L2.63 9.28 L2.41 9.04 L2.21 8.78 L2.02 8.51 L1.86 8.22 L1.71 7.93 L1.59 7.63 L1.49 7.31 L1.41 7.00 L1.35 6.67 L1.31 6.35 L1.30 6.02 L1.31 5.69 L1.34 5.36 L1.40 5.04 L1.48 4.72 L1.58 4.41 L1.70 4.11 L1.84 3.81 L2.00 3.53 L2.19 3.25 L2.39 2.99 L2.61 2.75 L2.84 2.52 L3.09 2.31 L3.36 2.11 L3.63 1.94 L3.92 1.78 L4.22 1.65 L4.53 1.54 L4.84 1.44 L5.16 1.37 L5.49 1.33 L5.68 1.40 L5.50 1.61 L5.34 1.82 L5.18 2.05 L5.05 2.28 L4.93 2.53 L4.83 2.78 L4.75 3.04 L4.68 3.30 L4.64 3.57 L4.61 3.84 L4.60 4.12 L4.61 4.39 L4.64 4.66 L4.69 4.93 L4.76 5.19 L4.84 5.45 L4.94 5.70 L5.06 5.95 L5.20 6.18 L5.35 6.41 L5.52 6.62 L5.71 6.82 L5.90 7.01 L6.11 7.18 L6.33 7.34 L6.56 7.49 L6.80 7.61 L7.05 7.72 L7.31 7.81 L7.57 7.89 L7.84 7.94 L8.11 7.98 L8.38 8.00 L8.65 8.00 L8.92 7.98 L9.19 7.94 L9.46 7.88 L9.72 7.80 L9.98 7.71 L10.22 7.60 L10.46 7.47Z"
SUN_RAYS = "M6.00 1.90L6.00 0.80M8.90 3.10L9.68 2.32M10.10 6.00L11.20 6.00M8.90 8.90L9.68 9.68M6.00 10.10L6.00 11.20M3.10 8.90L2.32 9.68M1.90 6.00L0.80 6.00M3.10 3.10L2.32 2.32"


def day_night_icon(name: str) -> str:
    if name == "moon":
        body = f'<path d="{MOON_PATH}"/>'
    else:
        body = (f'<circle cx="6" cy="6" r="2.3"/><path d="{SUN_RAYS}" fill="none" stroke="currentColor"'
                ' stroke-width="1.5" stroke-linecap="round"/>')
    return (f'<svg class="dn-icon dn-icon--{name}" viewBox="0 0 12 12" width="16" height="16" aria-hidden="true"'
            f' focusable="false">{body}</svg>')


def night_key(t: dict, attr: str, extra_class: str = "") -> str:
    """One key, as in the plug-in's header: the moon by day (press for night), the sun by night."""
    return (f'<button type="button" class="night-key{extra_class}" {attr} aria-pressed="false" aria-label="{E(t["night"])}"'
            f' title="{E(t["day"])} / {E(t["night"])}">{day_night_icon("moon")}{day_night_icon("sun")}</button>')


def gnav(lang: str, current: str, ko_href: str, en_href: str, theme: bool) -> str:
    """The bar at the top of every page: the tripper logo, the menu (plug-ins, artist), day / night on pages that
    have a night look, and the language switch. current is "flipper" or "artist"."""
    t = T[lang]
    prefix = f"/{lang}"
    here = ' aria-current="page"'
    plugins_on = ' data-current="true"' if current == "flipper" else ""
    theme_keys = ""
    if theme:
        theme_keys = f"""
        <div class="gnav__theme">{night_key(t, "data-theme-toggle")}</div>"""
    return f"""    <header class="gnav">
      <div class="gnav__inner">
        <a class="gnav__home" href="{prefix}/" aria-label="tripper">{TRIPPER_LOGO}</a>
        <nav class="gnav__links" aria-label="{E(t['nav_label'])}">
          <div class="gnav__menu" data-menu>
            <button type="button" class="gnav__menu-key" aria-expanded="false" aria-controls="menu-plugins"{plugins_on}>PLUGINS<span aria-hidden="true">▾</span></button>
            <div class="gnav__drop" id="menu-plugins" hidden>
              <a href="{prefix}/flipper/"{here if current == 'flipper' else ''}><b>flipper<i>.</i></b></a>
            </div>
          </div>
          <a href="{prefix}/artist/"{here if current == 'artist' else ''}>ARTIST</a>
        </nav>{theme_keys}
        <div class="gnav__lang" aria-label="{E(t['lang_label'])}">
          <a href="{ko_href}" lang="ko" hreflang="ko"{' aria-current="true"' if lang == 'ko' else ''}>ko</a>
          <span aria-hidden="true">/</span>
          <a href="{en_href}" lang="en" hreflang="en"{' aria-current="true"' if lang == 'en' else ''}>en</a>
        </div>
      </div>
    </header>"""


THEME_EARLY = """    <script>try { if (localStorage.getItem('theme') === 'night') document.documentElement.dataset.theme = 'night'; } catch (error) {}</script>"""


def page(lang: str, home: bool) -> str:
    t = T[lang]
    prefix = f"/{lang}"
    here = f"{prefix}/" if home else f"{prefix}/flipper/"
    ko_here = "/ko/" if home else "/ko/flipper/"
    en_here = "/en/" if home else "/en/flipper/"
    canonical = f"{SITE}{prefix}/flipper/"
    lang_hint = ""
    if lang == "ko":
        lang_hint = f"""
    <div class="lang-hint" data-lang-hint lang="en"><a href="{en_here}">{E(t['lang_hint'])} →</a><button type="button" aria-label="{E(t['lang_hint_close'])}">×</button></div>"""
    meta = "".join(f"<li>{E(m)}</li>" for m in t["meta"])
    source = (f'<a href="{SOURCE_URL}">{E(t["source"])} ↗</a>' if RELEASED else f'<span>{E(t["source_soon"])}</span>')

    return f"""<!doctype html>
<!-- Written by tools/build_flipper.py: change the words there, not here. -->
<html lang="{lang}" class="no-js">
  <head>
{GTAG}
{THEME_EARLY}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{E(t['title'])}</title>
    <meta name="description" content="{E(t['description'])}">
    <meta name="theme-color" content="#ffde7a">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="ko" href="{SITE}/ko/flipper/">
    <link rel="alternate" hreflang="en" href="{SITE}/en/flipper/">
    <link rel="alternate" hreflang="x-default" href="{SITE}/flipper/">

    <meta property="og:type" content="website">
    <meta property="og:locale" content="{t['locale']}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{E(t['title'])}">
    <meta property="og:description" content="{E(t['description'])}">
    <meta property="og:site_name" content="arcadiatripper">
    <meta property="og:image" content="{SITE}/assets/images/flipper/og-flipper.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{E(t['title'])}">
    <meta name="twitter:description" content="{E(t['description'])}">
    <meta name="twitter:image" content="{SITE}/assets/images/flipper/og-flipper.png">

    <link rel="icon" href="/assets/images/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" href="/assets/images/favicon-32.png" sizes="32x32">
    <link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
    <link rel="preload" href="/assets/fonts/flipper-ui/flipperui-semibold.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/assets/fonts/flipper-ui/flipperui-bold.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/assets/css/global.css">
    <link rel="stylesheet" href="/assets/css/flipper.css">
    <script>document.documentElement.classList.remove('no-js'); document.documentElement.classList.add('js');</script>
    <script src="/assets/js/global.js" defer></script>
    <script src="/assets/js/flipper.js" defer></script>
    <script type="application/ld+json">
      {{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "flipper",
        "applicationCategory": "MultimediaApplication",
        "operatingSystem": "macOS, Windows",
        "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "USD" }},
        "url": "{canonical}",
        "author": {{ "@type": "Person", "name": "레네 RENÉ", "alternateName": "@arcadiatripper" }}
      }}
    </script>
  </head>
  <body class="flipper-page" data-skin="clean">
    <a class="skip-link" href="#main-content">{E(t['skip'])}</a>
{lang_hint}
{gnav(lang, "flipper", ko_here, en_here, theme=True)}

    <main id="main-content">
      <section class="hero" id="top">
        <div class="shell hero__shell">
          <ul class="badges">{''.join(f'<li>{E(b)}</li>' for b in t['badges'])}</ul>
          <h1 class="logo">flipper<i>.</i></h1>
          <p class="hero__lead">{E(t['lead'])}</p>
          <p class="hero__slogan" lang="en">{E(t['slogan'])}</p>
{download_block(t)}
{video_block(lang, t)}
          <ul class="hero__meta">{meta}</ul>
        </div>
      </section>

      <section class="band" id="features" aria-labelledby="features-title">
        <div class="shell">
          <h2 class="heading heading--center" id="features-title" data-reveal>{E(t['slides_title'])}</h2>
{slides_block(lang, t)}
        </div>
      </section>

      <section class="band band--engines" id="engines" aria-labelledby="engines-title" data-engines data-skin="clean">
        <div class="shell">
          <header class="heading heading--center" data-reveal><h2 id="engines-title">{E(t['engines_title'])}</h2><p>{E(t['engines_sub'])}</p></header>
{engines_block(lang, t)}
        </div>
      </section>

      <section class="band band--deep" id="more" aria-labelledby="more-title">
        <div class="shell">
{deep_block(lang, t)}
        </div>
      </section>

      <section class="band" id="install" aria-labelledby="install-title">
        <div class="shell">
          <h2 class="heading heading--center" id="install-title" data-reveal>{E(t['install_title'])}</h2>
          <div class="installs">{install_block(t)}
          </div>
          <p class="install__note">{E(t['install_note'])}</p>
        </div>
      </section>

      <section class="band" id="faq" aria-labelledby="faq-title">
        <div class="shell">
          <h2 class="heading heading--center" id="faq-title" data-reveal>{E(t['faq_title'])}</h2>
          <div class="faq">{faq_block(t)}
          </div>
        </div>
      </section>

      <section class="band close" aria-labelledby="close-title">
        <div class="shell close__inner">
          <p class="logo">flipper<i>.</i></p>
          <h2 id="close-title">{E(t['close_title'])}</h2>
{download_block(t)}
        </div>
      </section>
    </main>

    <footer class="foot">
      <div class="foot__chips" aria-hidden="true">{''.join(f'<span style="--i: {n}">{n + 1}</span>' for n in range(16))}</div>
      <div class="shell foot__inner">
        <div class="foot__brand">
          <p class="logo logo--small">flipper<i>.</i></p>
          <p>{E(t['foot_line'])}</p>
        </div>
        <div>
          <h2>{E(t['foot_links'])}</h2>
          <div class="foot__links">
            {source}
            <a href="https://www.youtube.com/@arcadiatripper">YouTube ↗</a>
            <a href="https://www.instagram.com/arcadiatripper">Instagram ↗</a>
          </div>
        </div>
        <div>
          <h2>{E(t['foot_notes'])}</h2>
          <div class="foot__notes">
            <span>{E(t['license'])}</span>
            <span>{E(t['built_with'])}</span>
            <span>{E(t['fonts'])}</span>
            <span>{E(t['made_by'])}</span>
          </div>
        </div>
      </div>
      <div class="foot__bottom">
        <div class="shell">
          <span class="foot__credit">© tripper / <em>@arcadiatripper</em></span>
          <span class="foot__plate">clean · the sample as it is</span>
        </div>
      </div>
    </footer>
  </body>
</html>
"""


def main() -> None:
    outputs = {
        "ko/index.html": page("ko", home=True),
        "ko/flipper/index.html": page("ko", home=False),
        "en/index.html": page("en", home=True),
        "en/flipper/index.html": page("en", home=False),
    }
    for where, (title, description, image) in CHOOSERS.items():
        outputs[f"{where}index.html"] = CHOOSER.format(gtag=GTAG, page=where, title=E(title),
                                                       description=E(description), site=SITE, image=image)
    for lang in ("ko", "en"):
        rel = f"{lang}/artist/index.html"
        text = (ROOT / rel).read_text(encoding="utf-8")
        start = text.index('    <header class="gnav">')
        end = text.index("    </header>", start) + len("    </header>")
        outputs[rel] = text[:start] + gnav(lang, "artist", "/ko/artist/", "/en/artist/", theme=False) + text[end:]
    for rel, text in outputs.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        # drop the blank lines left by empty pieces
        path.write_text("\n".join(line for line in text.splitlines() if line.strip() or line == "") + "\n", encoding="utf-8")
        print("wrote", rel)


if __name__ == "__main__":
    main()
