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
            ("clean", "clean", "얼마나 늘여도 맑게.", "CLEAN · THE SAMPLE AS IT IS", ""),
            ("black", "black", "80년대 후반의 전설적인 샘플러. 거칠고 묵직하게.", "BLACK · 12-BIT · 26 kHz",
             "회로도대로 만들었어요. 12비트로 담는 방식, 샘플을 건너뛰고 되풀이하는 음정, 출력마다 다른 필터, 움직이는 필터까지. "
             "움직이는 필터는 실제 기계의 녹음과 비교해 맞췄어요."),
            ("grey", "grey", "80년대 후반의 또 다른 전설적인 샘플러. 단단하고 따뜻하게.", "GREY · 12-BIT · 40 kHz",
             "공개된 자료가 적어서 추정한 곳이 있어요: 12비트로 담는 방식, 음정을 바꾸는 방식, 출력 필터의 모양, 잡음 크기."),
            ("purple", "purple", "90년대 초 게임기의 소리 칩. 동글고 먹먹하게.", "PURPLE · 4-BIT · 32 kHz",
             "칩의 계산(BRR 디코딩, 가우스 보간, 32,040 Hz)은 오픈소스 에뮬레이터 ares와 7,300가지 경우를 비교해 비트 하나까지 같아요. "
             "보드의 필터는 회로도대로예요."),
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
            ("clean", "clean", "Clear however far you stretch it.", "CLEAN · THE SAMPLE AS IT IS", ""),
            ("black", "black", "The legendary late-80s sampler. Gritty and heavy.", "BLACK · 12-BIT · 26 kHz",
             "Built to the schematics: how it stores 12 bits, pitch by skipping and repeating samples, a different filter "
             "on each output, and the moving filter, which was checked against recordings of a real unit."),
            ("grey", "grey", "The other legendary late-80s sampler. Tight and warm.", "GREY · 12-BIT · 40 kHz",
             "Little is published about it, so these are estimates: its 12-bit storage, how it changes pitch, the output "
             "filter's shape and the noise level."),
            ("purple", "purple", "An early-90s console's sound chip. Round and hazy.", "PURPLE · 4-BIT · 32 kHz",
             "The chip's maths (BRR decoding, gaussian interpolation, 32,040 Hz) matches the open-source emulator ares bit for "
             "bit, across 7,300 test cases. The board's filter follows the schematic."),
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


# The long read: each part of the plug-in, a picture and its features as cards to turn. Every claim here is in the
# plug-in's design notes (flipper docs/DESIGN.md, DRUM.md, DECK.md, RECORDING.md, third_party/airwindows/README.md).
DEEP = {
    "ko": {
        "title": "하나하나, 직접 다듬었어요",
        "lead": "요즘 나오는 샘플러를 따라 만든 게 아니에요. 비트를 만들면서 걸리던 것들을 하나씩 정해서 만들었어요.",
        "prev": "이전 카드", "next": "다음 카드",
        "parts": [
            {
                "key": "chop", "shot": "feature_lazy", "title": "자르기",
                "lead": "샘플 한 부분을 잘라 새 소리처럼 들리게 하는 것. flipper가 가장 잘하려는 일이에요.",
                "cards": [
                    ("타격 찾기", "샘플을 열 때 타격을 한 번 찾아 두고, 감도를 움직이면 다시 분석하지 않고 바로 다시 잘라요. 새 샘플은 50 %로 잘려서 들어와요."),
                    ("박자", "1/16, 1/8, 1/4, 1/2, 한 마디마다. 샘플의 템포를 따라요."),
                    ("레이지 찹", "재생하면서 패드든 건반이든 치면 그 자리에서 잘려요. 1번 조각은 시작에서 바로 시작해요. 전체가 되돌리기 한 번이에요."),
                    ("일찍 쳐도 제자리", "탭보다 80 ms 앞부터 60 ms 뒤까지의 타격을 찾아 붙여요. 실제 드럼 루프에서 탭의 90–100 %가 제 타격에 붙어요."),
                    ("불 켜진 패드", "다음 조각의 패드만 불이 들어오고, 그 패드를 눌러야 잘려요. 옛 기계처럼 치고 싶을 때."),
                    ("주사위", "굴릴 때마다 새 찹이에요. 잠근 마커와 건너뛴 부분은 그대로 두고 나머지만 새로 잘라요."),
                    ("혼돈", "주사위를 끌어서 0–100 %. 0 %는 뚜렷한 타격만 고르게, 50 %부터는 아무 데나 섞이고, 100 %는 완전히 마음대로예요. 주사위 눈이 혼돈을 보여줘요."),
                    ("손으로", "더블클릭으로 마커를 더하고(가까운 타격에 붙음), 끌어서 옮기고, 드래그로 여러 개를 골라 지워요. alt를 누르면 붙지 않아요."),
                    ("잠금", "잠근 마커는 다시 잘라도 그 자리에 남아요."),
                    ("건너뛰기", "카운트인이나 숨소리는 지우지 않고 빼 둬요. 뒤 조각이 한 칸씩 당겨지고, 파일은 그대로라 언제든 되돌려요."),
                    ("시작과 끝", "조각마다 시작과 끝을 ms로 밀고 당겨요. 0은 언제나 '자른 그대로'. 자석을 켜면 10 ms 안의 0 교차점에 붙어요."),
                    ("다섯 가지만", "최대 64조각. 조각마다 설정은 음높이, 리버스, 볼륨, 페이드 인, 페이드 아웃뿐이에요. 페이드는 0에서 시작해요."),
                    ("클릭 없이", "모든 소리의 시작과 끝에 0.1 ms 가장자리를 둬서, 파형 중간을 잘라도 '틱' 소리가 나지 않아요."),
                ],
            },
            {
                "key": "keys", "shot": "feature_repitch", "title": "키와 템포", "tempo": True,
                "lead": "키와 속도는 패드마다가 아니라 샘플 하나에 있어요. 샘플 하나를 통째로 다른 곡처럼 만들기 위해서예요.",
                "cards": [
                    ("리피치", "옛 샘플러처럼 키를 내리면 느려지고 어두워져요. 늘이기를 하지 않아서 디지털 잡음이 없어요."),
                    ("템포 유지", "템포는 그대로 두고 키만. 소리는 미리 구워 두고, 굽는 동안에도 바로 들려요."),
                    ("템포 계산", "키를 내리면 몇 BPM이 되는지 보여줘요. 원하는 BPM을 치면 몇 반음 몇 센트를 내리면 되는지 알려줘요."),
                    ("DAW 템포", "키 하나로 지금 곡의 템포에 맞춰요. 리피치에선 키를, 템포 유지에선 속도를 맞춰요."),
                    ("키 칩", "샘플의 키와, 지금 키 노브로 들리는 키를 같이 보여줘요. 예: Am → Gm. 튜닝이 몇 센트 어긋났는지도요."),
                    ("또렷하게", "템포 유지로 늘릴 때 타격과 타격 사이를 따로 늘리고, 타격의 앞부분은 원래 소리를 남겨요. 비트에 켜고, 멜로디엔 꺼요."),
                    ("루프와 원샷", "샘플마다 루프(템포 있음)인지 원샷인지. 파일 이름과 길이로 먼저 짐작하고, 바꿀 수 있어요."),
                ],
            },
            {
                "key": "play", "shot": "feature_melody", "title": "연주",
                "lead": "샘플러는 덱 하나처럼 움직여요. 패드마다 따로 놀지 않아요.",
                "cards": [
                    ("패드", "16개나 32개, 페이지를 넘겨 64조각까지. 패드 1번이 C3이에요."),
                    ("모노", "기본이에요. 새 패드가 앞 소리를 5 ms 만에 끊어요. 덱 하나로 찹을 연주하듯이."),
                    ("폴리", "소리가 겹쳐요. 멜로디에서 화음을 칠 때."),
                    ("누르는 동안", "누른 만큼만 울려요. 조각은 자기 끝에서 멈춰요."),
                    ("슬라이스 전체", "한 번 치면 다음 마커까지 끝까지 울려요."),
                    ("멜로디", "한 조각을 건반에 깔아요. 반음씩, 또는 장조, 단조, 도리안, 프리지안, 믹솔리디안, 화성 단조, 장 · 단 펜타토닉."),
                    ("흰 건반 배치", "고르면 어느 스케일이든 C장조처럼 흰 건반으로 쳐요. 패드 컨트롤러엔 '모든 건반'."),
                    ("원키", "C3에 묶여 있지 않아요. ‹ ›로 옮기거나, 건반을 오른쪽 클릭하면 그 건반이 원키예요."),
                    ("128건반", "화면 건반은 MIDI 음 전부. 휠로 넘기고, 확대하고, 누르면 진짜 MIDI 음을 보내요."),
                    ("서스테인", "멜로디에서 서스테인 페달이 돼요."),
                    ("패닉", "머리줄 키나 MIDI CC 120 · 123으로 모든 소리를 5 ms 만에 꺼요."),
                ],
            },
            {
                "key": "sample", "shot": "feature_channels", "title": "샘플 담기",
                "lead": "파일을 끌어 놓거나, DAW의 소리를 바로 녹음해서 샘플로 써요.",
                "cards": [
                    ("녹음", "다른 트랙(사이드체인)이나 flipper 자신의 출력(리샘플)을 받아 새 샘플로."),
                    ("언제, 얼마나", "바로 또는 다음 마디 첫 박부터. 멈출 때까지 또는 1 · 2 · 4 · 8마디(DAW 템포 기준)."),
                    ("채널 고르기", "스테레오, 왼쪽, 오른쪽, 가운데, 양옆. 가운데 = (L+R)/2, 양옆 = (L−R)/2. 원래보다 커지지 않아요."),
                    ("전체 샘플 게인", "엔진 뒤, fx 앞에서 샘플 하나의 크기를 맞춰요. 노멀라이즈도 여기로."),
                    ("어떤 파일 이름이든", "어느 나라 말의 파일 이름이든 열려요."),
                ],
            },
            {
                "key": "rack", "shot": "feature_fx", "title": "fx 랙",
                "lead": "열 칸이 소리 순서대로 이어져요. 처음엔 다 꺼져 있고, 노브를 올리면 켜져요. 꺼진 칸은 CPU를 쓰지 않아요.",
                "cards": [
                    ("필터", "직접 만든 필터. LP · BP · HP, 12 또는 24 dB, 레조넌스. 깨끗하게 또는 살짝 찌그러지는 래더. 랙 맨 앞이나 맨 끝."),
                    ("펀치", "노브 하나짜리 컴프레서. 직접 만들었고, 피드백과 클래식 두 가지예요."),
                    ("디스토트", "다섯 가지: soft, tube, clip, fold, 그리고 직접 만든 fuzz. 2배 오버샘플로 돌아요."),
                    ("크러시", "샘플레이트를 낮추고 비트를 깎아요. 계단처럼, 또는 부드럽게."),
                    ("테이프", "테이프에 녹음한 듯한 노브 하나. '흔들림'은 테이프를 살아 있게 하는 작은 변화예요."),
                    ("코러스", "앙상블 코러스. 빠르기, 폭, 섞기."),
                    ("노이즈", "먼지, 히스, 크래클. 샘플이 울리는 동안만 나서, 조용한 곳에 잡음이 남지 않아요."),
                    ("에코", "테이프, 디지털(핑퐁 포함), 그레인. 시간은 박자(1/16–한 마디, 점 · 셋잇단)."),
                    ("스페이스", "리버브 다섯 가지(작은 방부터 넓은 공간까지). 프리딜레이와 스테레오 폭."),
                    ("전체", "랙 전체를 한 번에. 입력(클리퍼), 폭, 톤, 출력, fx 켜고 끄기."),
                    ("fx 패드", "누르는 동안 걸리는 16개. 빨강 컷, 노랑 스터터, 청록 테이프(멈춤 · 뒤로 · 반속 · 거꾸로), 파랑 던지기(LP · HP · 에코 · 크러시)."),
                    ("박자에 맞게", "fx 패드는 바로, 다음 1/16, 다음 박 중에 시작해요. 에코와 흔들림은 DAW의 박을 따라서, 바운스해도 들은 그대로예요."),
                    ("어디서 왔나", "펀치, 필터, fuzz, 비트, 히스, 크래클, 디지털 · 그레인 에코는 직접 만들었어요. 나머지는 Airwindows(MIT) 모델이에요."),
                ],
            },
            {
                "key": "deck", "shot": "feature_scratch", "title": "턴테이블",
                "lead": "자른 구간을 판처럼 돌리고 긁어요. 지금 엔진의 소리 그대로예요.",
                "cards": [
                    ("판", "33⅓ rpm, 한 바퀴에 1.8초. 리피치, 템포 유지, 옛 기계 엔진 모두 자기 방식대로 읽어요."),
                    ("손", "마우스나 컨트롤러로 잡아요. 손이 움직인 만큼만 판이 움직여서 바늘이 튀지 않고, 움직임은 부드럽게 이어져요."),
                    ("슬립매트", "잡으면 몇 ms 안에 서고, 놓으면 25 ms 안에 판 속도를 따라잡아요."),
                    ("모터", "▶ ■의 시작과 멈춤 시간. 바로, 또는 테이프처럼 천천히 서요."),
                    ("페이더", "부드럽게(믹스용)부터 날카롭게(스크래치용)까지 곡선. 소리가 열리는 지점과 거꾸로도 골라요."),
                    ("스크래치 패턴", "베이비, 처프, 트랜스, 플레어 등. 누르는 동안 판에 올린 조각을 그 패턴으로 긁어요."),
                    ("16건반", "건반 16개가 조각 1–16을 골라 긁어요. 세게 칠수록 멀리 밀어요. 다음 16분음표에서 시작해요."),
                    ("곡 따라 돌기", "DAW를 재생하면 판이 큐부터 곡에 맞춰 돌아요. 잠깐 떼어 놓아도 다시 곡 자리로 돌아와요."),
                    ("컨트롤러", "끝없이 도는 노브는 조그, 스트립은 손 위치, 피치 휠은 밀고 당기기. MIDI 지정할 때 알아서 맞춰요."),
                    ("오토메이션", "판, 손, 페이더가 DAW 파라미터라서, 긁은 것까지 바운스에 그대로 들어가요."),
                ],
            },
            {
                "key": "drum", "shot": "feature_drum", "title": "드럼",
                "lead": "원샷 16개로 킷을 짜는 화면이에요. 샘플러와 같은 플러그인 안에 있어요.",
                "cards": [
                    ("셀 16개", "파일을 끌어 놓으면 들어가요. 여러 개를 놓으면 그 셀부터 차례로 채워요."),
                    ("셀마다 엔진", "clean, grey, black, purple을 셀마다 따로."),
                    ("셀마다 조절", "볼륨, 팬, 음높이 ±24, 페이드 인 · 아웃. 모두 DAW 오토메이션이 돼요."),
                    ("초크", "그룹 1–4. 같은 그룹을 치면 앞 소리가 멈춰요. 오픈 · 클로즈 하이햇처럼."),
                    ("출력 16개", "셀마다 DAW의 다른 트랙으로 보내요. 1번은 fx 랙을 거쳐요."),
                    ("에코 · 스페이스", "셀마다 보내는 양만 정하고, 무거운 이펙트는 하나만 돌려요(CPU)."),
                    ("건반 구역", "셀은 C6부터, MIDI 채널 10이면 C1부터. 샘플러 패드와 겹치지 않게 나뉘어 있어요."),
                    ("킷 파일", ".flipkit에 샘플과 설정을 함께. 다른 프로젝트에서 열면 킷만 들어와요."),
                ],
            },
            {
                "key": "out", "shot": "feature_midi", "title": "내보내기와 안전",
                "lead": "만든 것은 그대로 DAW로 가고, 갑자기 큰 소리는 나지 않게 했어요.",
                "cards": [
                    ("찹을 MIDI로", "루프가 각 조각에 닿는 순간 그대로 MIDI 클립을 만들어 DAW 트랙에 끌어 놓아요. 원래 그루브에서 시작해요."),
                    ("바운스 = 연주", "블록 크기 1부터 4096까지, 실시간이든 오프라인이든 같은 소리예요."),
                    ("MIDI 지정", "연주에 쓰는 컨트롤은 모두 MIDI로 지정해요. 누르는 동안 / 눌러서 켜고 끄기도 골라요."),
                    (".flip 파일", "샘플, 찹, 설정을 파일 하나에. 예전 판의 flip도 같은 소리로 열려요."),
                    ("되돌리기", "노브 하나, 끌기 하나가 한 단계. 찹도 되돌려요."),
                    ("큰 소리 규칙", "갑자기 큰 소리는 가장 심각한 버그로 다뤄요. 원인을 고치고 테스트로 막았어요."),
                    ("안전 리미터", "평소 소리를 바꾸는 리미터는 없어요. 맨 끝의 안전 리미터(세이프 · 빈티지 · 끔)는 고를 수 있어요."),
                    ("한국어 · 영어", "화면 전체가 두 언어예요. 낮과 밤, 엔진마다 스킨도 바뀌어요."),
                ],
            },
        ],
    },
    "en": {
        "title": "Shaped by hand, one decision at a time",
        "lead": "flipper is not a copy of today's samplers. It was built by settling, one at a time, the things that got "
                "in the way of making beats.",
        "prev": "Previous card", "next": "Next card",
        "parts": [
            {
                "key": "chop", "shot": "feature_lazy", "title": "Chop",
                "lead": "Take one part of a sample and chop it until it sounds new. This is what flipper tries to do best.",
                "cards": [
                    ("Hits", "The hits are found once when the sample opens; move the sensitivity and it re-chops at once. A new sample comes in chopped at 50 %."),
                    ("Beats", "Every 1/16, 1/8, 1/4, 1/2 or bar, at the sample's tempo."),
                    ("Lazy chop", "It plays; tap a pad or any key and it cuts there. Slice 1 starts at the start. The whole take is one undo."),
                    ("Early taps land", "It finds the hit from 80 ms before your tap to 60 ms after. On real drum loops 90–100 % of taps land on their hit."),
                    ("Lit pad", "Only the next slice's pad lights up and cuts, for playing it the old machines' way."),
                    ("The die", "A new chop on every roll. Locked markers and skipped parts stay; the rest is chopped anew."),
                    ("Chaos", "Drag the die, 0–100 %. 0 % picks only clear hits, evenly; past 50 % chance creeps in; 100 % is pure chance. The pips show it."),
                    ("By hand", "Double-click to add a marker (it snaps to a nearby hit), drag to move, drag across to pick several and delete. Alt: no snap."),
                    ("Lock", "A locked marker stays where it is through every re-chop."),
                    ("Skip", "A count-in or a breath is left out, not cut out. The slices after it move up; the file is untouched, so it can come back any time."),
                    ("Start and end", "Push and pull each slice's start and end in ms; 0 is always 'as chopped'. With the magnet on, they land on a zero crossing within 10 ms."),
                    ("Only five", "Up to 64 slices, each with pitch, reverse, level, fade in and fade out. Nothing more. Fades start at 0."),
                    ("No clicks", "Every sound starts and ends on a 0.1 ms edge, so cutting mid-wave never ticks."),
                ],
            },
            {
                "key": "keys", "shot": "feature_repitch", "title": "Key and tempo", "tempo": True,
                "lead": "Key and speed belong to the whole sample, not to each pad, so one sample can become a different track.",
                "cards": [
                    ("Repitch", "Like the old samplers: pitch it down and it slows down and darkens. No stretching, so no digital artefacts."),
                    ("Keep tempo", "The tempo stays, only the key moves. The sound is baked ahead, and you hear it at once while it bakes."),
                    ("Tempo maths", "Pitch it down and it shows the tempo you land on. Type the BPM you want and it gives the semitones and cents."),
                    ("DAW tempo", "One key matches the song's tempo: the key in repitch, the speed in keep tempo."),
                    ("Key chip", "The sample's key and the key it sounds in with the key knob, e.g. Am → Gm, and how many cents it is off tune."),
                    ("Crisp", "Keep tempo stretches between the hits, each on its own, and keeps every hit's attack. On for beats, off for melodies."),
                    ("Loop or one-shot", "Each sample is a loop (with a tempo) or a one-shot. The first guess comes from the file name and length; you can change it."),
                ],
            },
            {
                "key": "play", "shot": "feature_melody", "title": "Play",
                "lead": "The sampler moves like one deck. The pads don't each go their own way.",
                "cards": [
                    ("Pads", "16 or 32, with pages up to 64 slices. Pad 1 is C3."),
                    ("Mono", "The default: a new pad cuts the last sound in 5 ms, like a chop played on one deck."),
                    ("Poly", "Sounds overlap, for chords in melody mode."),
                    ("While held", "It sounds as long as you hold it, and stops at the slice's own end."),
                    ("Whole slice", "One hit plays it through to the next marker."),
                    ("Melody", "One slice across the keys: by semitone, or major, minor, dorian, phrygian, mixolydian, harmonic minor, major and minor pentatonic."),
                    ("White keys", "Pick it and every scale plays like C major on the white keys. 'Every key' is for pad controllers."),
                    ("Root", "Not stuck on C3: move it with ‹ ›, or right-click a key to make it the root."),
                    ("128 keys", "The screen keyboard holds every MIDI note. Scroll, zoom, and a click sends the real note."),
                    ("Sustain", "The sustain pedal works in melody mode."),
                    ("Panic", "The header key, or MIDI CC 120 and 123, fades every sound out in 5 ms."),
                ],
            },
            {
                "key": "sample", "shot": "feature_channels", "title": "Bring a sample in",
                "lead": "Drop a file, or record the DAW's sound straight in as a sample.",
                "cards": [
                    ("Record", "Another track (side-chain) or flipper's own output (resample) becomes the new sample."),
                    ("When, how long", "Now, or from the next bar's first beat. Until you stop, or 1, 2, 4 or 8 bars at the DAW's tempo."),
                    ("Channel select", "Stereo, left, right, mid or side. Mid = (L+R)/2, side = (L−R)/2. Never louder than the source."),
                    ("Whole sample gain", "One sample's level, after the engine and before the fx. Normalize sets it."),
                    ("Any file name", "File names in any language open."),
                ],
            },
            {
                "key": "rack", "shot": "feature_fx", "title": "fx rack",
                "lead": "Ten slots in the order the sound runs. All off at first; turn a knob up and it comes on. An off slot uses no CPU.",
                "cards": [
                    ("Filter", "Our own: LP, BP or HP, 12 or 24 dB, resonance. Clean, or a ladder that saturates a little. First in the rack or last."),
                    ("Punch", "A one-knob compressor of our own, in feedback or classic."),
                    ("Distort", "Five kinds: soft, tube, clip, fold, and our own fuzz. Runs 2× oversampled."),
                    ("Crush", "Lowers the sample rate and cuts the bits, in steps or smooth."),
                    ("Tape", "One knob of tape. Its flux is the small changes that keep tape alive."),
                    ("Chorus", "An ensemble chorus: speed, range, mix."),
                    ("Noise", "Dust, hiss and crackle, only while a sample sounds, so no noise is left in the gaps."),
                    ("Echo", "Tape, digital (ping-pong too) or grain. Times in beats: 1/16 to a bar, dotted and triplet."),
                    ("Space", "Five reverbs, from a small room to a huge space, with pre-delay and stereo width."),
                    ("All", "The whole rack at once: input (a clipper), width, tone, output, fx on and off."),
                    ("fx pads", "16 that act while held: red cut, yellow stutter, teal tape (stop, back, half, reverse), blue throw (LP, HP, echo, crush)."),
                    ("On the beat", "fx pads kick in now, on the next 1/16 or the next beat. Echoes and wobbles follow the DAW's beat, so a bounce sounds as heard."),
                    ("Where it comes from", "Punch, filter, fuzz, bits, hiss, crackle and the digital and grain echoes are our own. The rest are Airwindows (MIT) models."),
                ],
            },
            {
                "key": "deck", "shot": "feature_scratch", "title": "Turntable",
                "lead": "Spin and scratch the chopped range like a record, in the sound of the engine you picked.",
                "cards": [
                    ("The record", "33⅓ rpm, one turn = 1.8 s. Repitch, keep tempo and the old-machine engines each read it their own way."),
                    ("The hand", "Grab it with the mouse or a controller. The record moves only as far as your hand, so the needle never jumps, and moves are smoothed."),
                    ("Slipmat", "Grabbed, it stops within a few ms; let go, it catches the platter within 25 ms."),
                    ("Motor", "Start and stop times for ▶ ■: at once, or slowing down like a tape."),
                    ("Fader", "A curve from smooth (for mixing) to sharp (for scratching), with the cut-in and a reversed setting."),
                    ("Scratch patterns", "Baby, chirp, transformer, flare and more. Hold to scratch the slice on the record in that pattern."),
                    ("16 keys", "16 keys pick slices 1–16 to scratch; harder hits push further. They start on the next 1/16."),
                    ("Follow the song", "When the DAW plays, the record runs from its cue in time with the song, and finds its way back after you take over."),
                    ("Controllers", "An endless knob is a jog, a strip is the hand, the pitch wheel pushes and pulls. MIDI learn works it out."),
                    ("Automation", "The record, the hand and the fader are DAW parameters, so scratches end up in the bounce as played."),
                ],
            },
            {
                "key": "drum", "shot": "feature_drum", "title": "Drums",
                "lead": "A screen for building a kit from 16 one-shots, inside the same plug-in as the sampler.",
                "cards": [
                    ("16 cells", "Drop a file in. Drop several and they fill in order from that cell."),
                    ("An engine each", "clean, grey, black or purple, per cell."),
                    ("Per cell", "Level, pan, pitch ±24, fade in and out. All automatable in the DAW."),
                    ("Choke", "Groups 1–4: hit one and the last in its group stops, like open and closed hats."),
                    ("16 outputs", "Send any cell to its own DAW track. Output 1 runs through the fx rack."),
                    ("Echo and space", "Each cell sets only how much it sends; one heavy effect runs for all (CPU)."),
                    ("Key zones", "Cells from C6, or from C1 on MIDI channel 10, laid out never to clash with the sampler's pads."),
                    ("Kit files", "A .flipkit holds the samples and settings. Opened in another project, only the kit comes in."),
                ],
            },
            {
                "key": "out", "shot": "feature_midi", "title": "Out, and safe",
                "lead": "What you make goes straight to the DAW, and nothing suddenly gets loud.",
                "cards": [
                    ("Chop to MIDI", "A clip that plays each slice at the moment the loop reaches it, dragged onto a DAW track. Start from the sample's own groove."),
                    ("Bounce = live", "The same sound at block sizes from 1 to 4096, real time or offline."),
                    ("MIDI learn", "Every control you perform with can be learned, as held or as a toggle."),
                    (".flip files", "The sample, the chop and the settings in one file. Older flips open sounding the same."),
                    ("Undo", "One step per knob turn or drag, chops included."),
                    ("The loudness rule", "A sudden loud sound is treated as the worst bug: the causes are fixed and tests guard them."),
                    ("Safety limiter", "No limiter colours the everyday sound. The safety limiter at the very end (safe, vintage, off) is your choice."),
                    ("Korean and English", "The whole screen in both. Day and night, and a skin for each engine."),
                ],
            },
        ],
    },
}


def deep_block(lang: str, t: dict) -> str:
    """The long read: per part a picture and its words, then its features as cards to turn (the tempo calculator
    sits under key and tempo's words)."""
    d = DEEP[lang]
    rows = []
    for i, part in enumerate(d["parts"]):
        count = len(part["cards"])
        cards = "".join(
            f'<li class="fcard"><p class="fcard__n">{n + 1:02d} / {count:02d}</p><h4>{E(name)}</h4><p>{E(text)}</p></li>'
            for n, (name, text) in enumerate(part["cards"]))
        tool = tempo_block(t) if part.get("tempo") else ""
        rows.append(f"""
          <article class="deep__part" id="more-{part['key']}" data-reveal>
            <div class="deep__top">
              <div class="deep__body">
                <p class="deep__n">{i + 1:02d}</p>
                <h3>{E(part['title'])}</h3>
                <p class="deep__lead">{E(part['lead'])}</p>{tool}
              </div>
              <div class="deep__shot card">{shot(part['shot'], lang, part['title'])}</div>
            </div>
            <div class="fcards" data-cards>
              <ul class="fcards__track" data-cards-track tabindex="0" aria-label="{E(part['title'])}">{cards}</ul>
              <div class="fcards__keys">
                <button type="button" class="slides__arrow" data-cards-prev aria-label="{E(d['prev'])}">←</button>
                <button type="button" class="slides__arrow" data-cards-next aria-label="{E(d['next'])}">→</button>
              </div>
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
