#!/usr/bin/env python3
"""Writes the flipper pages from one template and the Korean and English words below.

    python3 tools/build_flipper.py

Writes ko/flipper/ and en/flipper/, plus the small pages at /, /flipper/ and /artist/
that send a visitor to their language. GitHub Pages serves those files as they are; nothing runs on the
server. Change words here, then run this again and commit the output.
Each language's home page (/ko/, /en/) is the tripper page, written by tools/build_home.py.
"""

from __future__ import annotations

import html
import math
import random
from pathlib import Path

from PIL import Image

from flipper_features import PARTS

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
# The guide (샘플러 안내서) and the manual (사용 설명서) per language; None shows the card with "coming soon".
DOCS_URL = {
    "guide": {"ko": "/ko/flipper/guide/", "en": "/en/flipper/guide/"},
    "manual": {"ko": "/ko/flipper/manual/", "en": "/en/flipper/manual/"},
}
# Where support goes, per language: (label key in T, url), first one = the main key and the footer link.
# Toonation takes Korean payments; Ko-fi takes cards and PayPal from abroad. Empty shows "coming soon".
TOONATION_URL = "https://toon.at/donate/arcadiatripper"
KOFI_URL = "https://ko-fi.com/arcadiatripper"
# Set once GitHub Sponsors approves the account (https://github.com/sponsors/arcadiatripper); None leaves it out.
SPONSORS_URL = None
SUPPORT_LINKS = {
    "ko": [("support_toon", TOONATION_URL), ("support_kofi", KOFI_URL)],
    "en": [("support_kofi", KOFI_URL)],
}
if SPONSORS_URL:
    for _lang in SUPPORT_LINKS:
        SUPPORT_LINKS[_lang].append(("support_sponsors", SPONSORS_URL))

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
        "lead": "모두를 위한\n무료 샘플러 플러그인",
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
        "screens_sub": "플러그인 하나에 샘플러, 드럼, fx가 다 들어 있어요. 머리줄의 탭으로 오가요.",
        "screens_tab_label": "화면 고르기",
        "screens": [
            ("sampler", "샘플러", "샘플 하나를 잘라서 연주해요.",
             "타격을 찾아 바로 자르고, 레이지 찹으로 들으면서 치고, 키와 템포를 바꿔 플립해요."),
            ("drum", "드럼", "원샷 16개로 킷을 짜요.",
             "셀마다 음높이, 엔진, 초크, fx를 따로 두고, 출력 16개로 DAW 트랙에 나눠 보내요."),
            ("fx", "fx", "판을 긁고 효과를 걸어요.",
             "열 칸짜리 fx 랙, 누르는 동안만 걸리는 fx 패드, 33⅓ rpm으로 도는 판과 스크래치 패턴이 있어요."),
        ],
        "pro_title": "쓰던 대로 가져오세요",
        "pro_sub": "다른 샘플러를 오래 써 온 분도 환영해요. 쓰던 킷과 컨트롤러를 그대로 가져올 수 있어요.",
        "pro": [
            ("킷 가져오기", "다른 프로그램의 드럼 킷을 그대로 불러와요.",
             ["WAV 폴더", ".sfz", ".mxgrp", ".xpm · .xpn", ".adg"],
             "만든 킷은 .flipkit으로 저장하고, 들리는 그대로 WAV 킷으로 내보낼 수도 있어요."),
            ("MIDI 지정(MIDI Learn)", "노브, 스위치, 키 어디든 오른쪽 클릭해서 CC를 지정해요.",
             ["끝없이 도는 노브(상댓값)", "노브 8개 차례로", "조그 · 터치 스트립으로 긁기"],
             "끝없이 도는 노브도 맞게 움직이고, 노브 여덟 개를 돌리기만 해도 차례로 지정돼요. 판은 조그, 터치 스트립, 피치 휠로 긁을 수 있어요."),
            ("DAW와 함께", "만든 것은 DAW 안에서 그대로 이어져요.",
             ["찹을 MIDI로", "키스위치", "출력 16개", "채널 10"],
             "찹은 MIDI 클립으로 끌어 놓고, 키스위치로 곡 중간에 연주 방법을 바꾸고, 드럼 셀은 따로 출력해요. 노브는 모두 오토메이션돼요."),
        ],
        "engines_title": "엔진을 바꾸면, 옷도 바뀌어요",
        "engines_sub": "전설적인 샘플러 두 대와 90년대 게임기 소리 칩을, 회로까지 따라 만들었어요.",
        "engines": [
            ("clean", "clean", "아무리 늘여도 소리가 맑아요.", "clean · the sample as it is", ""),
            ("black", "black", "80년대 후반의 전설적인 샘플러예요. 소리가 거칠고 묵직해요.", "black · 12-bit · 26 kHz",
             "회로도를 보고 그대로 만들었어요. 12비트로 담는 방식, 샘플을 건너뛰고 되풀이하며 바꾸는 음정, 출력마다 다른 필터, 움직이는 필터까지 원본과 똑같아요. "
             "움직이는 필터는 실제 기계의 녹음과 비교해 맞췄어요."),
            ("grey", "grey", "80년대 후반의 또 다른 전설적인 샘플러예요. 소리가 단단하고 따뜻해요.", "grey · 12-bit · 40 kHz",
             "공개된 자료가 적어서 추정한 곳이 있어요(12비트로 담는 방식, 음정을 바꾸는 방식, 출력 필터의 모양, 잡음 크기)."),
            ("purple", "purple", "90년대 초 게임기의 소리 칩이에요. 소리가 동글고 먹먹해요.", "purple · 4-bit · 32 kHz",
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
        "pond_title": "슬라이스가 울리면, 비주얼라이저가 움직여요",
        "pond_sub": "플러그인 위쪽에 비주얼라이저가 있어요. 슬라이스가 울릴 때마다 움직이고, 모양은 네 가지예요.",
        "pond_looks": [
            ("paper", "종이 꽃가루", "색종이가 톡 튀어 올라 빙글빙글 떨어지고, 바닥에 붙었다가 스티커처럼 떼어져요."),
            ("strings", "줄 울림", "가는 줄 세 가닥이 소리 난 자리에서 튕겨지고, 떨리는 동안 패드 색으로 물들어요."),
            ("koi", "잉어 연못", "느긋하게 헤엄치던 잉어들이 소리가 떨어진 곳으로 꼬리를 치며 달려와요."),
            ("ink", "먹물 마블링", "먹물이 똑 떨어져 동그랗게 번지고, 물결을 따라 무늬로 말리다가 맑아져요."),
        ],
        "pond_pause": "일시정지",
        "pond_resume": "재생",
        "pond_rev": "거꾸로",
        "slides_title": "핵심 기능",
        "slides": [
            ("lazy", "레이지 찹", "들으면서 원하는 순간에 치면, 친 자리가 잘려요.", ""),
            ("key", "키 찾기", "샘플의 키를 찾고, 튜닝이 몇 센트 어긋났는지도 알려줘요.",
             "직접 만든 분석기(MIT)예요. 음 높이 분포(크로마)를 Albrecht–Shanahan 키 프로필과 맞춰 보고, "
             "키가 적힌 루프 158개로 다듬었어요. 음이 없는 소리엔 키를 붙이지 않아요."),
            ("repitch", "리피치와 템포 유지", "리피치(Repitch)는 옛 샘플러처럼 키와 속도가 같이 움직여요. 템포 유지는 템포를 그대로 두고 키만 바꿔요.",
             "템포 유지는 고품질 타임 스트레치 알고리즘인 Rubber Band R3(GPL)를 사용하고, 해당 부분의 소리를 만드는 동안엔 "
             "빠른 속도의 알고리즘인 Signalsmith Stretch(MIT)로 바로 들려줘요. 바운스도 들은 그대로 나가요."),
            ("crisp", "또렷하게", "템포 유지에서 켤 수 있는 기능이에요. 비트와 드럼 루프에서 타격이 또렷해져요.",
             "원리는 타격 앞부분의 원래 소리를 그대로 남기는 방식이에요. Signalsmith Stretch(MIT)."),
            ("channels", "채널 고르기", "샘플마다 스테레오, 왼쪽, 오른쪽, 미드, 사이드 중에서 골라요.", ""),
            ("melody", "멜로디", "슬라이스 하나를 건반에 깔고, 스케일을 골라 연주해요.", ""),
            ("midi", "찹을 MIDI로", "자른 순서 그대로 MIDI 클립이 돼요. DAW 트랙에 끌어다 놓으면 돼요.", ""),
            ("drum", "드럼 킷", "원샷 16개로 킷을 짜고, 셀마다 따로 다듬어요.", ""),
            ("fx", "fx 랙", "필터, 펀치, 디스토션, 크러시, 테이프, 코러스, 노이즈, 에코, 스페이스, 마스터 열 칸이에요.", "일부는 Airwindows(MIT)의 모델을 귀로 골라 가져왔어요."),
            ("scratch", "스크래치", "판을 잡고 긁어요. 베이비, 처프 같은 스크래치 패턴도 있어요.", ""),
            ("night", "낮과 밤", "키 하나로 밤 화면이 돼요.", ""),
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
        "faq_title": "자주 묻는 질문",
        "faq": [
            ("정말 무료예요?", "네. 돈도 가입도 필요 없고, 소스 코드도 모두 공개해요."),
            ("flipper로 만든 곡을 팔아도 되나요?", "네. flipper로 만든 소리와 곡은 만든 사람의 것이에요. 라이선스는 플러그인 프로그램에 붙는 것이고, 결과물에는 붙지 않아요."),
            ("제 컴퓨터에서 돌아가나요?", "Mac은 Apple Silicon과 Intel 모두, Windows는 64비트 Windows 10과 11에서 돌아가요. ARM Windows는 아직이에요."),
            ("어떤 DAW에서 쓸 수 있나요?", "AU나 VST3 플러그인을 여는 DAW면 돼요. Logic Pro, REAPER, Cubase에서 확인했어요."),
            ("베타라서 조심할 게 있나요?", "macOS는 처음 열 때 한 번 허용해야 하고, Windows는 SmartScreen에서 '추가 정보 → 실행'을 누르면 돼요. 새 버전이 나오면 플러그인 로고 옆에 점이 켜져요."),
            ("소스 코드는 어디 있나요?", "GitHub에 있어요. 우리가 쓴 코드는 MIT, 배포하는 플러그인은 함께 묶인 라이브러리 때문에 AGPL-3.0이에요."),
        ],
        "docs_title": "더 알아보기",
        "docs_sub": "샘플링이 처음이라면 안내서부터, 기능을 찾는다면 설명서를 펴 보세요.",
        "docs": [
            ("guide", "샘플러 안내서", "샘플러는 어떻게 소리를 만들까",
             "샘플링이 처음이어도 괜찮아요. 리피치, 타임 스트레치, 옛 샘플러의 소리를 직접 들어 보며 배워요.", "안내서 보기"),
            ("manual", "사용 설명서", "flipper의 모든 기능",
             "화면마다 키 하나하나가 하는 일, 설정과 건반 배치, 자주 묻는 질문까지 담았어요.", "설명서 보기"),
        ],
        "docs_soon": "곧 열려요",
        "support_line": "flipper는 무료예요. 마음에 드셨다면 후원으로 응원해 주세요.",
        "support": "후원하기",
        "support_toon": "투네이션으로 후원하기",
        "support_kofi": "Ko-fi로 후원하기 (해외)",
        "support_sponsors": "GitHub Sponsors",
        "support_soon": "후원 준비 중",
        "close_title": "샘플 하나, 꺼내 볼까요?",
        "source": "소스 코드 (GitHub)",
        "source_soon": "소스 코드는 베타와 함께 공개",
        "made_by": "레네 RENÉ가 만들었어요",
        "maker_role": "MADE BY",
        "maker_art": "레네 RENÉ의 캐릭터, 우주 고양이 트리퍼",
        "foot_line": "모두를 위한 무료 샘플러 플러그인.",
        "foot_links": "LINKS",
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
        "lead": "A free sampler plug-in\nfor everyone",
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
        "screens_sub": "Sampler, drums and fx, all in one plug-in. The tabs in the header switch between them.",
        "screens_tab_label": "Pick a screen",
        "screens": [
            ("sampler", "sampler", "Chop one sample and play it.",
             "Hits found and chopped right away, lazy chop to tap along, then change the key and tempo to flip it."),
            ("drum", "drum", "Build a kit from 16 one-shots.",
             "Pitch, engine, choke and fx for each cell, and 16 outputs to split them over DAW tracks."),
            ("fx", "fx", "Scratch the record, add effects.",
             "A ten-slot fx rack, fx pads that work while held, and a record spinning at 33⅓ rpm with scratch patterns."),
        ],
        "pro_title": "Bring what you already use",
        "pro_sub": "Long-time sampler users are welcome too. Your kits and controllers come along as they are.",
        "pro": [
            ("Kit import", "Open drum kits from other software as they are.",
             ["WAV folder", ".sfz", ".mxgrp", ".xpm · .xpn", ".adg"],
             "Save your kits as .flipkit, or export one as WAVs that sound as you hear them."),
            ("MIDI learn", "Right-click any knob, switch or key to map a CC.",
             ["endless knobs (relative)", "eight knobs in turn", "scratch from a jog or touch strip"],
             "Endless knobs move the right way, and eight knobs map just by turning them one after another. Scratch the record from a jog wheel, touch strip or pitch wheel."),
            ("With your DAW", "What you make carries on inside the DAW.",
             ["chop to MIDI", "keyswitches", "16 outputs", "channel 10"],
             "Drag the chop out as a MIDI clip, switch the way you play mid-song with keyswitches, and send drum cells out on their own. Every knob can be automated."),
        ],
        "engines_title": "Change the engine, change the look",
        "engines_sub": "Two legendary samplers and an early-90s console's sound chip, modelled down to the circuits.",
        "engines": [
            ("clean", "clean", "Clear however far you stretch it.", "clean · the sample as it is", ""),
            ("black", "black", "The legendary late-80s sampler. Gritty and heavy.", "black · 12-bit · 26 kHz",
             "Built straight from the schematics. How it stores 12 bits, pitch by skipping and repeating samples, a different filter "
             "on each output and the moving filter all match the original. The moving filter was checked against recordings of a real unit."),
            ("grey", "grey", "The other legendary late-80s sampler. Tight and warm.", "grey · 12-bit · 40 kHz",
             "Little is published about it, so these are estimates: its 12-bit storage, how it changes pitch, the output "
             "filter's shape and the noise level."),
            ("purple", "purple", "An early-90s console's sound chip. Round and hazy.", "purple · 4-bit · 32 kHz",
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
        "pond_title": "Every slice moves the visualizer",
        "pond_sub": "The visualizer sits at the top of the plug-in. It moves with every slice that plays, in four looks.",
        "pond_looks": [
            ("paper", "paper confetti", "Paper shapes pop up, tumble down, stick to the floor and peel away like stickers."),
            ("strings", "strings", "Three thin strings are plucked where the sound lands and take the pad's colour while they ring."),
            ("koi", "koi pond", "Koi drift around, then flick their tails and dash to where the sound dropped."),
            ("ink", "ink marbling", "A drop of ink blooms into rings, curls into marbled patterns and clears away."),
        ],
        "pond_pause": "pause",
        "pond_resume": "play",
        "pond_rev": "reverse",
        "slides_title": "What it does",
        "slides": [
            ("lazy", "Lazy chop", "Tap along. It chops where you tap.", ""),
            ("key", "Key detection", "It finds the sample's key, and how many cents it is off tune.",
             "Our own analyser (MIT). It matches the spread of pitches (chroma) against the Albrecht–Shanahan key profiles, "
             "tuned on 158 key-labelled loops. A sound with no notes gets no key."),
            ("repitch", "Repitch and keep tempo", "Repitch moves key and speed together, like the old samplers. Keep tempo moves the key only.",
             "Keep tempo uses Rubber Band R3 (GPL), a high-quality time-stretch algorithm; while that part's sound is being made, "
             "you hear Signalsmith Stretch (MIT), a fast one, straight away. Bounces come out as you heard them too."),
            ("crisp", "Crisp", "A switch in keep tempo. Hits in beats and drum loops come out sharp.",
             "It works by keeping the front of each hit as the original sound. Signalsmith Stretch (MIT)."),
            ("channels", "Channel select", "Per sample: stereo, left, right, mid or side.", ""),
            ("melody", "Melody", "One slice across the keys, in the scale you pick.", ""),
            ("midi", "Chop to MIDI", "Drag the chop order into your DAW.", ""),
            ("drum", "Drum kit", "16 one-shots, each trimmed on its own.", ""),
            ("fx", "fx rack", "Ten slots: filter, punch, distortion, crush, tape, chorus, noise, echo, space and master.", "Some are Airwindows (MIT) models, picked by ear."),
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
        "faq_title": "FAQ",
        "faq": [
            ("Is it really free?", "Yes. No money, no sign-up, and all of the source code is public."),
            ("Can I sell music I make with flipper?", "Yes. The sounds and songs you make are yours. The licence covers the plug-in program, not what you make with it."),
            ("Will it run on my computer?", "On Macs with Apple Silicon or Intel, and on 64-bit Windows 10 and 11. Not on ARM Windows yet."),
            ("Which DAWs?", "Any DAW that opens AU or VST3 plug-ins. Checked in Logic Pro, REAPER and Cubase."),
            ("Anything to know about the beta?", "macOS asks you to allow it once the first time; on Windows, click 'More info → Run anyway' in SmartScreen. When a new version is out, a dot lights up by the plug-in's logo."),
            ("Where is the source code?", "On GitHub. The code we wrote is MIT; the plug-in we ship is AGPL-3.0 because of the libraries bundled with it."),
        ],
        "docs_title": "Read more",
        "docs_sub": "New to sampling? Start with the guide. Looking for a feature? Open the manual.",
        "docs": [
            ("guide", "sampler guide", "How does a sampler make its sound?",
             "No sampling experience needed. Learn repitch, time stretch and the old samplers' sound by listening.", "Read the guide"),
            ("manual", "manual", "Everything flipper does",
             "What every key on every screen does, the settings, the keyboard layout and the common questions.", "Open the manual"),
        ],
        "docs_soon": "Coming soon",
        "support_line": "flipper is free. If you like it, you can support it.",
        "support": "Support flipper",
        "support_kofi": "Support me on Ko-fi",
        "support_sponsors": "or GitHub Sponsors",
        "support_soon": "Support coming soon",
        "close_title": "Got a sample? Let's flip it.",
        "source": "Source code (GitHub)",
        "source_soon": "Source code goes public with the beta",
        "made_by": "Made by RENÉ (레네)",
        "maker_role": "MADE BY",
        "maker_art": "Tripper the cosmic cat, RENÉ's character",
        "foot_line": "A free sampler plug-in for everyone.",
        "foot_links": "LINKS",
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
    with Image.open(folder / day) as im:
        w, h = im.size
    w, h = 960, round(h * 960 / w)
    loading = "eager" if eager else "lazy"
    img = (f'<img class="shot{" shot--day" if night else ""}" src="/assets/images/flipper/{day}" width="{w}" height="{h}"'
           f' alt="{E(alt)}" loading="{loading}">')
    if night:
        img += (f'<img class="shot shot--night" src="/assets/images/flipper/{night}" width="{w}" height="{h}"'
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
    "ko": {"title": "하나하나, 직접 다듬었어요",
           "lead": ["'하나의 플러그인에서 모든 것을 할 수 없을까?' 하는 의문에서 시작한 플러그인이에요.",
                    "10년의 비트메이킹 경험에서 나온 실제 필요한 기능들을 압축해서 담았어요.",
                    "Claude와 함께 100% 바이브코딩으로 제작했어요.",
                    "직접 사용하기 위해 만들었기에 디테일을 하나하나 검수하며 모두 취향대로 만들었어요."]},
    "en": {"title": "Shaped by hand, one decision at a time",
           "lead": ["It started with one question: could a single plug-in do it all?",
                    "Ten years of making beats, boiled down to the features that are actually needed.",
                    "Made entirely by vibe coding, with Claude.",
                    "Built to be used by its maker, so every detail was checked one by one and shaped to taste."]},
}


def features_block(lang: str, t: dict, part: dict) -> str:
    """One part's features as slides: per feature its own picture of the plug-in (or the tempo calculator) and a few
    paragraphs; on a phone they read down the page."""
    key, title = part["key"], part["title"][lang]
    items = part["features"]
    slides, dots = [], []
    count = len(items)
    for i, f in enumerate(items):
        name, paras = f[lang]
        body = "".join(f"<p>{E(p)}</p>" for p in paras)
        if f.get("tool") == "tempo":
            picture = f'<div class="slide__tool">{tempo_block(t)}</div>'
        else:
            stem = f["shot"][0][1:] if f["shot"][0].startswith("@") else f"feat_{f['key']}"
            picture = f'<div class="slide__shot card">{shot(stem, lang, name, link=True)}</div>'
        slides.append(f"""
              <li class="slide slide--feature" id="{key}-{f['key']}" aria-roledescription="slide" aria-label="{i + 1} / {count}">
                {picture}
                <div class="slide__body"><p class="slide__n">{i + 1:02d} / {count:02d}</p><h4>{E(name)}</h4><div class="slide__text">{body}</div></div>
              </li>""")
        dots.append(f'<button type="button" class="slides__dot" aria-label="{E(name)}" data-slide-to="{i}"></button>')
    return f"""
            <div class="slides slides--features" data-slides aria-roledescription="carousel" aria-label="{E(title)}">
              <ul class="slides__track" data-slides-track tabindex="0">{''.join(slides)}
              </ul>
              <div class="slides__controls">
                <button type="button" class="slides__arrow" data-slides-prev aria-label="{E(t['slides_prev'])}">←</button>
                <div class="slides__dots">{''.join(dots)}</div>
                <button type="button" class="slides__arrow" data-slides-next aria-label="{E(t['slides_next'])}">→</button>
              </div>
            </div>"""


def pond_block(t: dict) -> str:
    """The four visualizer looks, live (assets/js/flipper-pond.js plays a silent beat into them), with small pause and reverse keys."""
    looks = "".join(f"""
            <figure class="pond__look">
              <div class="pond__well" data-pond-look="{key}"></div>
              <figcaption><b>{E(name)}</b> {E(line)}</figcaption>
            </figure>""" for key, name, line in t["pond_looks"])
    return f"""          <div class="pond" data-pond>
            <div class="pond__looks">{looks}
            </div>
            <div class="pond__deck">
              <button type="button" class="pond__key" aria-pressed="false" data-pond-pause data-pause="{E(t['pond_pause'])}" data-resume="{E(t['pond_resume'])}"><span aria-hidden="true">❚❚</span> <b>{E(t['pond_pause'])}</b></button>
              <button type="button" class="pond__key" aria-pressed="false" data-pond-rev><span aria-hidden="true">⇆</span> <b>{E(t['pond_rev'])}</b></button>
            </div>
          </div>"""


def deep_block(lang: str, t: dict) -> str:
    """The long read: per part its number, title and words, then every feature of it (tools/flipper_features.py)."""
    d = DEEP[lang]
    rows = []
    for i, part in enumerate(PARTS):
        n = len(part["features"])
        fold_open = f"기능 {n}개 보기" if lang == "ko" else f"Show {n} features"
        fold_shut = "접기" if lang == "ko" else "Fold"
        rows.append(f"""
          <article class="deep__part" id="more-{part['key']}" data-reveal>
            <div class="deep__top deep__top--alone">
              <div class="deep__body">
                <p class="deep__n">{i + 1:02d}</p>
                <h3>{E(part['title'][lang])}</h3>
                <p class="deep__lead">{E(part['lead'][lang])}</p>
                <button type="button" class="deep__fold" aria-expanded="true" aria-controls="feat-{part['key']}" data-fold
                        data-open="{E(fold_open)}" data-shut="{E(fold_shut)}">{E(fold_shut)}</button>
              </div>
            </div>
            <div class="deep__features" id="feat-{part['key']}" data-fold-body>{features_block(lang, t, part)}
            </div>
          </article>""")
    return f"""
          <header class="heading heading--center" data-reveal><h2 id="more-title">{E(d['title'])}</h2><p>{'<br>'.join(E(p) for p in d['lead'])}</p></header>
{pro_block(T[lang])}"""
    # The parts below (PARTS, features_block) are off since 2026-10-28: the manual and the guide carry the details now,
    # and the page keeps to what it does. Add `<div class="deep">{''.join(rows)}</div>` back to show them again.


def screens_block(lang: str, t: dict) -> str:
    """The three screens as tabs, like the plug-in's header: a full picture of each and a line or two."""
    tabs, panels = [], []
    for i, (key, name, text, more) in enumerate(t["screens"]):
        selected = "true" if i == 0 else "false"
        hidden = "" if i == 0 else " hidden"
        tabs.append(
            f'<button class="seg__item" type="button" role="tab" id="screen-tab-{key}" aria-controls="screen-{key}"'
            f' aria-selected="{selected}">{E(name)}</button>'
        )
        panels.append(f"""
            <div class="screen" role="tabpanel" id="screen-{key}" aria-labelledby="screen-tab-{key}"{hidden}>
              <div class="screen__shot">{shot(f'tab_{key}', lang, name)}</div>
              <div class="screen__body">
                <p class="screen__text">{E(text)}</p>
                <p class="screen__more">{E(more)}</p>
              </div>
            </div>""")
    return f"""
          <div class="seg" role="tablist" aria-label="{E(t['screens_tab_label'])}">{''.join(tabs)}</div>
          {''.join(panels)}"""


def pro_block(t: dict) -> str:
    """For people coming from other samplers: kits, MIDI learn, the DAW."""
    cards = []
    for name, lead, chips, more in t["pro"]:
        chip_html = "".join(f"<li>{E(c)}</li>" for c in chips)
        cards.append(f"""
            <article class="card pro" data-reveal>
              <h3>{E(name)}</h3>
              <p class="pro__lead">{E(lead)}</p>
              <ul class="pro__chips">{chip_html}</ul>
              <p class="pro__more">{E(more)}</p>
            </article>""")
    return f"""
          <header class="heading heading--center pro__head" data-reveal><h3 class="pro__title">{E(t['pro_title'])}</h3><p>{E(t['pro_sub'])}</p></header>
          <div class="pros">{''.join(cards)}
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

def docs_block(lang: str, t: dict) -> str:
    """The guide and the manual, side by side."""
    cards = []
    for key, name, title, text, go in t["docs"]:
        url = DOCS_URL[key][lang]
        action = (f'<a class="key key--pick" href="{url}">{E(go)} →</a>' if url
                  else f'<span class="key key--waiting" aria-disabled="true">{E(t["docs_soon"])}</span>')
        cards.append(f"""
            <article class="card doc" data-reveal>
              <p class="doc__tag">{E(name)}</p>
              <h3>{E(title)}</h3>
              <p class="doc__text">{E(text)}</p>
              <div class="doc__go">{action}</div>
            </article>""")
    return "".join(cards)


SUPPORT_LOGO = {"support_toon": "toonation", "support_kofi": "kofi"}


def support_logo(label: str) -> str:
    name = SUPPORT_LOGO.get(label)
    return f'<img src="/assets/images/support/{name}.webp" alt="" width="20" height="20">' if name else "♥ "


def support_block(lang: str, t: dict) -> str:
    links = SUPPORT_LINKS.get(lang) or []
    if links:
        # each service as its own button, in its own colour and with its own logo
        keys = [f'<a class="donate donate--{SUPPORT_LOGO.get(label, "plain")}" href="{url}">{support_logo(label)}{E(t[label])}</a>'
                for label, url in links]
        action = '<div class="support__keys">' + "\n            ".join(keys) + "</div>"
    else:
        action = f'<span class="key key--waiting support__key" aria-disabled="true">♥ {E(t["support_soon"])}</span>'
    return f"""
          <div class="support">
            <p>{E(t['support_line'])}</p>
            {action}
          </div>"""


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
    "": ("tripper",
         "tripper의 프로젝트를 하나씩 모아 두는 곳. tripper's projects, one by one. 001 flipper, a free, open-source sampler plug-in.",
         "og-tripper.jpg"),
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

# the same logo for the copyright line at the bottom right of every flipper page, unlit dots and all
FOOT_LOGO = TRIPPER_LOGO.replace('class="gnav__logo"', 'class="gnav__logo foot__logo"')

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
      <canvas class="gnav__dots" aria-hidden="true"></canvas>
      <div class="gnav__inner">
        <a class="gnav__home" href="{prefix}/" aria-label="tripper">{TRIPPER_LOGO}</a>
        <div class="gnav__panel" id="gnav-panel">
        <nav class="gnav__links" aria-label="{E(t['nav_label'])}">
          <div class="gnav__menu" data-menu>
            <button type="button" class="gnav__menu-key" aria-expanded="false" aria-controls="menu-plugins"{plugins_on}>plugins<span aria-hidden="true">▾</span></button>
            <div class="gnav__drop" id="menu-plugins" hidden>
              <a href="{prefix}/flipper/"{here if current == 'flipper' else ''}><b>flipper<i>.</i></b></a>
            </div>
          </div>
          <a href="{prefix}/artist/"{here if current == 'artist' else ''}>artist</a>
        </nav>{theme_keys}
        <div class="gnav__lang" aria-label="{E(t['lang_label'])}">
          <a href="{ko_href}" lang="ko" hreflang="ko"{' aria-current="true"' if lang == 'ko' else ''}>ko</a>
          <span aria-hidden="true">/</span>
          <a href="{en_href}" lang="en" hreflang="en"{' aria-current="true"' if lang == 'en' else ''}>en</a>
        </div>
        </div>
        <button type="button" class="gnav__burger" aria-expanded="false" aria-controls="gnav-panel" aria-label="{E(t['nav_label'])}" data-burger>
          <svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true" focusable="false"><path class="gnav__burger-open" d="M3 4.5h10M3 8h10M3 11.5h10"/><path class="gnav__burger-shut" d="M4 4l8 8M12 4l-8 8"/></svg>
        </button>
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
    for key, name, _title, _text, _go in t["docs"]:
        if DOCS_URL[key][lang]:
            source += f'\n            <a href="{DOCS_URL[key][lang]}">{E(name)} →</a>'
    for label, url in SUPPORT_LINKS.get(lang) or []:  # the footer names the service only
        source += f'\n            <a class="foot__support" href="{url}">{support_logo(label)}{ {"support_toon": "투네이션", "support_kofi": "Ko-fi"}.get(label, "GitHub Sponsors") } ↗</a>'


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
    <script src="/assets/js/flipper-pond.js" defer></script>
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
          <p class="hero__lead">{E(t['lead']).replace(chr(10), "<br>")}</p>
          <p class="hero__slogan" lang="en">{E(t['slogan'])}</p>
{download_block(t)}
{video_block(lang, t)}
          <ul class="hero__meta">{meta}</ul>
        </div>
      </section>

      <section class="band band--screens" id="screens" aria-labelledby="screens-title" data-tabs>
        <div class="shell">
          <header class="heading heading--center" data-reveal><h2 id="screens-title">{E(t['screens_title'])}</h2><p>{E(t['screens_sub'])}</p></header>
{screens_block(lang, t)}
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

      <section class="band band--pond" id="pond" aria-labelledby="pond-title">
        <div class="shell">
          <header class="heading heading--center" data-reveal><h2 id="pond-title">{E(t['pond_title'])}</h2><p>{E(t['pond_sub'])}</p></header>
{pond_block(t)}
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

      <section class="band" id="docs" aria-labelledby="docs-title">
        <div class="shell">
          <header class="heading heading--center" data-reveal><h2 id="docs-title">{E(t['docs_title'])}</h2><p>{E(t['docs_sub'])}</p></header>
          <div class="docs">{docs_block(lang, t)}
          </div>
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
{support_block(lang, t)}
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
          </div>
        </div>
        <div>
          <h2>{E(t['maker_role'])}</h2>
          <div class="foot__maker">
            <img src="/assets/images/profile-tripper-256.webp" width="256" height="256" alt="{E(t['maker_art'])}" loading="lazy">
            <div>
              <strong>레네 RENÉ</strong>
              <p lang="en">a sound chef floating in space.</p>
              <div class="foot__maker-links">
                <a href="https://www.youtube.com/@arcadiatripper">YouTube ↗</a>
                <a href="https://www.instagram.com/arcadiatripper">Instagram ↗</a>
                <a class="foot__mail" href="mailto:contact@arcadiatripper.com">contact@arcadiatripper.com</a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="foot__legal" lang="en">
        <div class="shell">
          <p>Source code: MIT License. Plug-in binaries: GNU AGPL-3.0.
            Includes JUCE, Rubber Band, Signalsmith Stretch, Airwindows, FLAC, Ogg Vorbis and Opus, each under its own licence.</p>
          <div class="foot__mark" role="img" aria-label="tripper">{FOOT_LOGO}</div>
        </div>
      </div>
    </footer>
  </body>
</html>
"""


def main() -> None:
    outputs = {
        # /ko/ and /en/ are the tripper home page now (tools/build_home.py)
        "ko/flipper/index.html": page("ko", home=False),
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
