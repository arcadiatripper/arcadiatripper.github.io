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
             "회로도를 따라 만들었어요. 12비트로 담는 방식, 샘플을 건너뛰고 되풀이하는 음정, 출력마다 다른 필터, 움직이는 필터까지. "
             "아직 추정인 곳은 움직이는 필터가 머무는 시간과 담을 때의 레벨이에요."),
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
             "Built from the schematics: how it stores 12 bits, pitch by skipping and repeating samples, a different filter "
             "on each output, and the moving filter. Still estimated: how long the moving filter holds, and the recording level."),
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
            <div class="seg seg--look" role="group" aria-label="{E(t['theme_label'])}">
              <button class="seg__item" type="button" data-look-set="day" aria-pressed="true">{E(t['day'])}</button>
              <button class="seg__item" type="button" data-look-set="night" aria-pressed="false">{E(t['night'])}</button>
            </div>
          </div>
          {''.join(panels)}"""


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

# The menu words in the same dots: capitals on a 5 x 7 grid.
MENU_GLYPHS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "▾": [".....", ".....", "#####", ".###.", "..#..", ".....", "....."],
}


def dot_word(word: str) -> str:
    """A menu word in dots (svg in currentColor); the word itself stays for screen readers."""
    lit, off = [], []
    for n, ch in enumerate(word):
        for y, row in enumerate(MENU_GLYPHS[ch]):
            for x, c in enumerate(row):
                dot = f'<circle cx="{(n * 6 + x) * 10 + 5}" cy="{y * 10 + 5}" r="3.8"/>'
                (lit if c == "#" else off).append(dot)
    w = len(word) * 60 - 10
    text = word.rstrip("▾")
    return (f'<svg class="gnav__dots" viewBox="0 0 {w} 70" style="width:{w / 70 * 1.0:.3f}em" aria-hidden="true" focusable="false">'
            f'<g class="gnav__logo-off">{"".join(off)}</g><g>{"".join(lit)}</g></svg><span class="gnav__said">{text}</span>')


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
        <div class="gnav__theme" role="group" aria-label="{E(t['theme_label'])}">
          <button type="button" data-theme-set="day" aria-pressed="true">{E(t['day'])}</button>
          <button type="button" data-theme-set="night" aria-pressed="false">{E(t['night'])}</button>
        </div>"""
    return f"""    <header class="gnav">
      <div class="gnav__inner">
        <a class="gnav__home" href="{prefix}/" aria-label="tripper">{TRIPPER_LOGO}</a>
        <nav class="gnav__links" aria-label="{E(t['nav_label'])}">
          <div class="gnav__menu" data-menu>
            <button type="button" class="gnav__menu-key" aria-expanded="false" aria-controls="menu-plugins"{plugins_on}>{dot_word("PLUGINS▾")}</button>
            <div class="gnav__drop" id="menu-plugins" hidden>
              <a href="{prefix}/flipper/"{here if current == 'flipper' else ''}><b>flipper<i>.</i></b></a>
            </div>
          </div>
          <a href="{prefix}/artist/"{here if current == 'artist' else ''}>{dot_word("ARTIST")}</a>
        </nav>{theme_keys}
        <div class="gnav__lang" aria-label="{E(t['lang_label'])}">
          <a href="{ko_href}" lang="ko" hreflang="ko"{' aria-current="true"' if lang == 'ko' else ''}>한</a>
          <span aria-hidden="true">/</span>
          <a href="{en_href}" lang="en" hreflang="en"{' aria-current="true"' if lang == 'en' else ''}>EN</a>
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

      <section class="band" id="tempo" aria-labelledby="tempo-title">
        <div class="shell shell--split">
          <header class="heading" data-reveal><h2 id="tempo-title">{E(t['tempo_title'])}</h2><p>{E(t['tempo_sub'])}</p></header>
{tempo_block(t)}
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
