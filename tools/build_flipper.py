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
# The screen recording that plays behind the hero: assets/video/flipper/<name>.webm, .mp4 and .webp (poster).
# None, or no file yet, shows the sampler screenshot instead.
HERO_VIDEO = {"ko": "hero_ko", "en": "hero_en"}

# --- words ----------------------------------------------------------------------------------------------------------

T = {
    "ko": {
        "lang": "ko",
        "locale": "ko_KR",
        "title": "flipper — 자르고, 뒤집고, 두드리는 무료 샘플러",
        "description": "샘플 하나로 오래 노는 사람을 위한 무료 오픈소스 샘플러 플러그인. Mac · Windows, AU · VST3.",
        "skip": "본문으로 바로가기",
        "nav_label": "사이트 메뉴",
        "lang_label": "언어",
        "flipper_tag": "찹 샘플러",
        "theme_label": "화면 밝기",
        "day": "낮",
        "night": "밤",
        "hero_alt": "flipper 샘플러 화면: 위에는 자른 샘플의 파형, 아래에는 패드",
        "lang_hint": "English version",
        "lang_hint_close": "닫기",
        "kicker": "FREE · OPEN SOURCE · BETA",
        "lead": "자르고, 뒤집고,<br>두드리는 샘플러.",
        "sub": "샘플 하나로 오래 노는 사람을 위해 만든 무료 샘플러 플러그인이에요. 들으면서 톡톡 두드리면 그 자리가 잘리고, 자른 조각은 바로 패드가 돼요. 키를 내리면 템포가 몇 BPM이 되는지 알려주고, 엔진을 바꾸면 80–90년대 기계의 결이 입혀져요.",
        "meta": ["Mac · Windows", "AU · VST3", "한국어 · English"],
        "get_mac": "Mac용 받기",
        "get_win": "Windows용 받기",
        "soon": "베타 준비 중이에요",
        "soon_note": "곧 여기서 받을 수 있어요. 소식은 YouTube와 Instagram에 먼저 올릴게요.",
        "free_note": "돈도, 가입도 필요 없어요.",
        "video_label": "VIDEO",
        "video_title": "flipper 소개 영상",
        "flow_label": "001 / HOW IT GOES",
        "flow_title": "샘플 하나가<br>비트가 되기까지",
        "flow_sub": "flipper는 샘플을 잘라서(chop) 뒤집어(flip) 새 비트로 만드는 플러그인이에요. 순서는 이렇게 흘러가요.",
        "flow": [
            ("불러오기", "오디오 파일을 끌어다 놓으면 파형이 뜨고, 샘플의 키를 찾아 보여줘요. 루프인지 원샷인지도 샘플마다 골라요."),
            ("자르기", "들으면서 패드를 톡톡 치면 그 자리가 잘려요(레이지 찹). 때리는 소리를 찾아 자르는 오토, 박자대로 나누는 그리드, 손으로 마커 찍기, 아무렇게나 섞는 주사위도 있어요. 64조각까지 돼요."),
            ("연주하기", "자른 조각은 바로 패드에 깔려요. 패드로 두드리거나, 한 조각을 건반 전체에 깔아 멜로디로 쳐요. 스케일을 고르면 그 음들만 건반에 놓여요."),
            ("색 입히기", "엔진을 바꿔 옛 샘플러의 거친 결을 입히고, 키를 내려 느긋한 템포로 끌어내려요. fx 화면에서는 필터, 테이프, 에코를 걸고 판을 긁어요."),
            ("내보내기", "자른 순서를 MIDI로 DAW에 끌어다 놓고, 지금 상태를 .flip 파일로 통째로 저장해요. 바운스해도 들리던 소리 그대로 나와요."),
        ],
        "screens_label": "002 / SCREENS",
        "screens_title": "화면은 세 개",
        "screens_sub": "맨 위 스위치로 샘플러, 드럼, fx를 오가요. 어느 화면을 보든 같은 건반은 같은 소리를 내요.",
        "screens": [
            ("sampler", "샘플러", "샘플 하나를 잘라서 연주하는 곳이에요.",
             ["들으면서 두드려 자르기, 오토 · 그리드 · 주사위", "4×4, 8×4 패드와 128건반 멜로디", "조각마다 음높이, 볼륨, 페이드, 채널(ST · L · R · M · S)"]),
            ("drum", "드럼", "원샷 16개로 드럼 킷을 짜는 곳이에요.",
             ["칸마다 엔진, 다듬기, 노멀라이즈, 효과", "초크 그룹과 출력 16개로 DAW에 따로 보내기", "킷은 .flipkit 파일로 저장하고 다른 곡에서 열기"]),
            ("fx", "fx", "판을 잡고 긁고, 효과를 거는 곳이에요.",
             ["필터부터 스페이스까지 이어지는 효과 랙", "fx 패드, 터치 스트립, 페이더", "베이비, 처프 같은 스크래치 패턴과 판 되감기"]),
        ],
        "engines_label": "003 / ENGINES",
        "engines_title": "엔진을 바꾸면,<br>소리도 옷도 바뀌어요",
        "engines_sub": "엔진이 넷이에요. 바꾸면 소리의 결이 바뀌고, 화면도 그 엔진의 옷으로 갈아입어요. 기계 엔진 셋은 옛 샘플러가 소리를 담고 내보내던 방식을 회로까지 따라 만들었고, 엔진마다 필터, 드라이브, 담는 판 속도(33 · 45 · 78)를 따로 골라요.",
        "engines_when": "이럴 때",
        "engines": [
            ("clean", "clean", "샘플 그대로. 늘이고 줄여도 맑게.", "CLEAN · THE SAMPLE AS IT IS",
             "원래 소리를 지키고 싶을 때. 템포 유지 모드에서 길이를 바꿔도 소리가 뭉개지지 않아요."),
            ("black", "black", "거칠고 어둡게. 80년대 후반 12비트 샘플러의 결.", "BLACK · 12-BIT · 26 kHz",
             "드럼을 묵직하고 지저분하게 만들고 싶을 때. 판 속도를 올려 담으면 윗소리가 더 바스락거려요."),
            ("grey", "grey", "단단하고 따뜻하게. 80년대 후반 12비트 샘플러의 결.", "GREY · 12-BIT · 40 kHz",
             "킥과 스네어를 단단하게 붙이고 전체를 따뜻하게 뭉치고 싶을 때."),
            ("purple", "purple", "부드럽고 먹먹하게. 90년대 초 게임기의 4비트 소리.", "PURPLE · 4-BIT · 32 kHz",
             "소리를 동글고 아련하게 만들고 싶을 때. 건반이나 보컬 조각에 잘 어울려요."),
        ],
        "engines_tab_label": "엔진 고르기",
        "tempo_label": "004 / KEY & TEMPO",
        "tempo_title": "키를 내리면,<br>템포도 알려줘요",
        "tempo_sub": "리피치 모드에서는 키와 빠르기가 함께 움직여요. 예전엔 메트로놈을 켜 두고 귀로 맞췄지만, flipper는 몇 BPM이 되는지 바로 보여줘요. 템포 유지 모드에서는 키와 템포를 따로 바꿔요.",
        "tempo_bpm": "원래 BPM",
        "tempo_key": "키",
        "tempo_result": "이렇게 돼요",
        "tempo_reverse": "원하는 BPM",
        "tempo_reverse_result": "이만큼 내리면 돼요",
        "tempo_st": "반음",
        "tempo_ct": "센트",
        "features_label": "005 / MORE",
        "features_title": "그리고 이런 것도",
        "features": [
            ("키 찾기", "샘플을 불러오면 키를 찾아서 보여줘요. 다른 샘플과 맞출 때 귀로 더듬지 않아도 돼요."),
            ("찹을 MIDI로", "자른 순서를 MIDI 노트로 DAW에 끌어다 놓아요. 거기서 순서를 바꿔 새 플립을 만들어요."),
            ("멜로디", "한 조각을 건반 전체에 깔아 멜로디로 쳐요. 스케일을 고르면 그 음들만 건반에 놓여요."),
            ("조각마다 따로", "조각마다 음높이, 볼륨, 페이드, 채널(ST · L · R · M · S)을 따로 정해요."),
            ("두 가지 모드", "리피치는 옛날처럼 키와 빠르기가 같이, 템포 유지는 따로 움직여요. 샘플마다 골라요."),
            ("스크래치", "판을 잡고 긁거나, 베이비 · 처프 같은 손동작 패턴을 패드 하나로 쳐요."),
            ("fx 랙", "필터, 펀치, 디스토션, 크러시, 테이프, 코러스, 노이즈, 에코, 스페이스. 고른 순서대로 이어져요."),
            ("MIDI learn", "컨트롤러의 노브와 패드를 눌러서 바로 연결해요. 무한 노브로 판을 되감을 수도 있어요."),
            (".flip 파일", "샘플, 자른 자리, 설정을 한 파일로 저장해요. 다른 곡, 다른 컴퓨터에서 그대로 열려요."),
            ("되돌리기", "자르기, 옮기기, 지우기 모두 되돌릴 수 있어요. 마음 놓고 이것저것 눌러 보세요."),
            ("낮과 밤", "버튼 하나로 낮 화면과 밤 화면을 바꿔요. 엔진마다 밤 옷이 따로 있어요. 이 페이지도 오른쪽 위에서 바꿔 볼 수 있어요."),
            ("한국어 · English", "메뉴부터 도움말 팁까지 두 언어로 나와요."),
        ],
        "install_label": "006 / INSTALL",
        "install_title": "설치",
        "install_mac_title": "Mac",
        "install_mac": [
            "macOS, Apple Silicon과 Intel 모두 (유니버설)",
            "AU (Logic Pro 등) · VST3",
            "베타는 Apple 서명 전이라 처음 열 때 macOS가 막을 수 있어요. 설치 안내대로 한 번만 허용하면 돼요.",
        ],
        "install_win_title": "Windows",
        "install_win": [
            "64비트 Windows 10 · 11 (ARM 노트북용은 아직이에요)",
            "VST3",
            "SmartScreen 경고가 뜨면 '추가 정보 → 실행'을 누르면 돼요.",
        ],
        "install_guide": "설치 안내 보기",
        "install_ai": "AI 도우미에게 맡기는 방법도 안내에 있어요.",
        "install_hosts": "Logic Pro, REAPER, Cubase에서 확인했어요. AU나 VST3를 쓰는 다른 DAW도 대부분 돼요.",
        "beta_label": "007 / BETA",
        "beta_title": "베타예요",
        "beta": [
            ("버그 제보", "이상한 점이 있으면 플러그인 오른쪽 아래 버그 제보 버튼으로 알려주세요. 이름도 계정도 필요 없어요."),
            ("업데이트 알림", "새 버전이 나오면 플러그인 위쪽 로고 옆에 작은 점이 켜져요. 눌러서 받으러 가면 돼요."),
            ("보내는 것 없음", "플러그인은 사용 기록을 보내지 않아요. 버그 제보도 직접 누르고 동의했을 때만 보내져요."),
        ],
        "faq_label": "008 / FAQ",
        "faq_title": "자주 묻는 것",
        "faq": [
            ("정말 무료예요?", "네. 돈도 가입도 필요 없고, 소스 코드도 모두 공개해요."),
            ("flipper로 만든 곡을 팔아도 되나요?", "네. flipper로 만든 소리와 곡은 만든 사람의 것이에요. 라이선스는 플러그인 프로그램에 붙는 것이고, 결과물에는 붙지 않아요."),
            ("제 컴퓨터에서 돌아가나요?", "Mac은 Apple Silicon과 Intel 모두, Windows는 64비트 Windows 10과 11에서 돌아가요. ARM Windows는 아직이에요."),
            ("어떤 DAW에서 쓸 수 있나요?", "AU나 VST3 플러그인을 여는 DAW면 돼요. Logic Pro, REAPER, Cubase에서 확인했어요."),
            ("소스 코드는 어디 있나요?", "GitHub에 있어요. 우리가 쓴 코드는 MIT, 배포하는 플러그인은 함께 묶인 라이브러리 때문에 AGPL-3.0이에요."),
        ],
        "source": "소스 코드 (GitHub)",
        "source_soon": "소스 코드는 베타와 함께 공개해요",
        "license": "우리 코드 MIT · 배포하는 플러그인 AGPL-3.0",
        "built_with": "JUCE, Rubber Band, Signalsmith Stretch, Airwindows, FLAC, Ogg Vorbis, Opus로 만들었어요.",
        "fonts": "글꼴: Fredoka, 나눔스퀘어라운드, Barlow, DotGothic16, Jersey 15 · SIL OFL 1.1",
        "made_by": "레네 RENÉ가 만들었어요",
    },
    "en": {
        "lang": "en",
        "locale": "en_US",
        "title": "flipper — a free sampler to chop, flip and tap",
        "description": "A free, open-source sampler plug-in for people who can play with one sample all day. Mac · Windows, AU · VST3.",
        "skip": "Skip to content",
        "nav_label": "Site menu",
        "lang_label": "Language",
        "flipper_tag": "chop sampler",
        "theme_label": "Day or night",
        "day": "day",
        "night": "night",
        "hero_alt": "flipper's sampler screen: the chopped sample's waveform on top, the pads below",
        "lang_hint": "",
        "lang_hint_close": "",
        "kicker": "FREE · OPEN SOURCE · BETA",
        "lead": "Chop it, flip it,<br>tap it.",
        "sub": "A free sampler plug-in for people who can play with one sample all day. Tap along while it plays and it chops right there, and the slices land on the pads. Pitch it down and it tells you the tempo it lands on; change the engine and it takes on the grain of a late-80s or early-90s machine.",
        "meta": ["Mac · Windows", "AU · VST3", "English · 한국어"],
        "get_mac": "Get it for Mac",
        "get_win": "Get it for Windows",
        "soon": "The beta is almost here",
        "soon_note": "You'll get it right here soon. News goes up on YouTube and Instagram first.",
        "free_note": "No money, no sign-up.",
        "video_label": "VIDEO",
        "video_title": "flipper intro video",
        "flow_label": "001 / HOW IT GOES",
        "flow_title": "From one sample<br>to a beat",
        "flow_sub": "flipper chops a sample and flips the pieces into a new beat. It goes like this.",
        "flow": [
            ("Load", "Drop an audio file and the waveform comes up, with the sample's key. Set each sample to loop or one-shot."),
            ("Chop", "Tap the pads along while it plays and it chops where you tap (lazy chop). Or let auto find the hits, cut it on a grid, place markers by hand, or roll the dice. Up to 64 slices."),
            ("Play", "The slices land on the pads right away. Tap them, or spread one slice across the keyboard and play a melody. Pick a scale and only its notes are on the keys."),
            ("Colour", "Change the engine for the grit of an old sampler, and pitch it down to a laid-back tempo. On the fx screen, add filter, tape and echo, and scratch the record."),
            ("Take it out", "Drag the chop order into your DAW as MIDI, and save the whole thing as a .flip file. A bounce sounds exactly like what you heard."),
        ],
        "screens_label": "002 / SCREENS",
        "screens_title": "Three screens",
        "screens_sub": "The switch at the top moves between sampler, drum and fx. Whichever screen you look at, the same key plays the same sound.",
        "screens": [
            ("sampler", "sampler", "Where you chop one sample and play it.",
             ["Tap to chop, or auto · grid · dice", "4×4 and 8×4 pads, and a 128-key melody", "Pitch, volume, fades and channel (ST · L · R · M · S) per slice"]),
            ("drum", "drum", "Where you build a kit from 16 one-shots.",
             ["Engine, trims, normalize and effects per cell", "Choke groups and 16 outputs to your DAW", "Save kits as .flipkit files and open them in other songs"]),
            ("fx", "fx", "Where you grab the record and add effects.",
             ["An effect rack from filter to space", "fx pads, touch strips and a fader", "Scratch patterns like baby and chirp, and a rewind"]),
        ],
        "engines_label": "003 / ENGINES",
        "engines_title": "Change the engine,<br>change the sound and the look",
        "engines_sub": "Four engines. Each one changes the grain of the sound, and the screen changes into that engine's clothes. The three machine engines follow the way old samplers took sound in and played it out, down to the circuits, and each has its own filter, drive and record speed (33 · 45 · 78).",
        "engines_when": "Reach for it",
        "engines": [
            ("clean", "clean", "The sample as it is. Stays clear however far you stretch it.", "CLEAN · THE SAMPLE AS IT IS",
             "when you want to keep the sound as it is. In keep-tempo mode it stays clean however much you change its length."),
            ("black", "black", "Gritty and dark: the grain of a late-80s 12-bit sampler.", "BLACK · 12-BIT · 26 kHz",
             "when drums should hit heavy and dirty. Sample it in at a faster record speed and the top gets crunchier."),
            ("grey", "grey", "Tight and warm: the grain of a late-80s 12-bit sampler.", "GREY · 12-BIT · 40 kHz",
             "when you want the kick and snare to sit tight and the whole loop to glue warm."),
            ("purple", "purple", "Soft and muffled: the 4-bit sound of an early-90s console.", "PURPLE · 4-BIT · 32 kHz",
             "when you want it round and hazy. Lovely on keys and vocal chops."),
        ],
        "engines_tab_label": "Pick an engine",
        "tempo_label": "004 / KEY & TEMPO",
        "tempo_title": "Pitch it down,<br>it tells you the tempo",
        "tempo_sub": "In repitch mode, key and speed move together. Producers used to match it by ear against a metronome; flipper shows the BPM it lands on. In keep-tempo mode, key and tempo change apart.",
        "tempo_bpm": "Original BPM",
        "tempo_key": "Key",
        "tempo_result": "You get",
        "tempo_reverse": "BPM you want",
        "tempo_reverse_result": "Pitch it by",
        "tempo_st": "st",
        "tempo_ct": "ct",
        "features_label": "005 / MORE",
        "features_title": "And also",
        "features": [
            ("Key detection", "Load a sample and it finds the key. No more guessing by ear to match another sample."),
            ("Chop to MIDI", "Drag the chop order into your DAW as MIDI notes, then shuffle them into a new flip."),
            ("Melody", "Spread one slice across the keyboard and play it as a melody. Pick a scale and only its notes are on the keys."),
            ("Per slice", "Set pitch, volume, fades and channel (ST · L · R · M · S) for each slice."),
            ("Two modes", "Repitch moves key and speed together, the old way; keep tempo moves them apart. Pick per sample."),
            ("Scratch", "Grab the record and scratch, or play hand patterns like baby and chirp from one pad."),
            ("fx rack", "Filter, punch, distortion, crush, tape, chorus, noise, echo and space, chained in the order you pick."),
            ("MIDI learn", "Click a control, touch a knob or pad on your controller, done. An endless knob can rewind the record."),
            (".flip files", "The sample, the chops and the settings in one file. Opens the same in another song or on another computer."),
            ("Undo", "Chops, moves and deletes can all be undone, so go ahead and press things."),
            ("Day and night", "One button switches between the day and night looks, and every engine has its own night look. Try it on this page too, at the top right."),
            ("English · 한국어", "Menus and help tips in both languages."),
        ],
        "install_label": "006 / INSTALL",
        "install_title": "Install",
        "install_mac_title": "Mac",
        "install_mac": [
            "macOS, Apple Silicon and Intel (universal)",
            "AU (Logic Pro and others) · VST3",
            "The beta isn't signed by Apple yet, so macOS may block it the first time. Allow it once as the guide shows.",
        ],
        "install_win_title": "Windows",
        "install_win": [
            "64-bit Windows 10 · 11 (no ARM laptop build yet)",
            "VST3",
            "If SmartScreen warns you, click 'More info → Run anyway'.",
        ],
        "install_guide": "Read the install guide",
        "install_ai": "The guide also shows how to let an AI assistant do it.",
        "install_hosts": "Checked in Logic Pro, REAPER and Cubase. Most other DAWs that open AU or VST3 work too.",
        "beta_label": "007 / BETA",
        "beta_title": "It's a beta",
        "beta": [
            ("Bug report", "If something looks wrong, tell us with the bug report key at the bottom right of the plug-in. No name or account needed."),
            ("Update notice", "When a new version is out, a small dot lights up by the logo. Click it to go and get it."),
            ("Nothing sent", "The plug-in sends no usage data. A bug report goes out only when you press send and agree."),
        ],
        "faq_label": "008 / FAQ",
        "faq_title": "Questions",
        "faq": [
            ("Is it really free?", "Yes. No money, no sign-up, and all of the source code is public."),
            ("Can I sell music I make with flipper?", "Yes. The sounds and songs you make are yours. The licence covers the plug-in program, not what you make with it."),
            ("Will it run on my computer?", "On Macs with Apple Silicon or Intel, and on 64-bit Windows 10 and 11. Not on ARM Windows yet."),
            ("Which DAWs?", "Any DAW that opens AU or VST3 plug-ins. Checked in Logic Pro, REAPER and Cubase."),
            ("Where is the source code?", "On GitHub. The code we wrote is MIT; the plug-in we ship is AGPL-3.0 because of the libraries bundled with it."),
        ],
        "source": "Source code (GitHub)",
        "source_soon": "The source code goes public with the beta",
        "license": "Our code MIT · the shipped plug-in AGPL-3.0",
        "built_with": "Built with JUCE, Rubber Band, Signalsmith Stretch, Airwindows, FLAC, Ogg Vorbis and Opus.",
        "fonts": "Fonts: Fredoka, NanumSquareRound, Barlow, DotGothic16, Jersey 15 · SIL OFL 1.1",
        "made_by": "Made by RENÉ (레네)",
    },
}

# --- pieces ---------------------------------------------------------------------------------------------------------

E = html.escape


def hero_media(lang: str, t: dict) -> str:
    """The plug-in playing behind the hero: a screen recording when there is one, else the real sampler screen."""
    stem = HERO_VIDEO.get(lang) or HERO_VIDEO.get("ko")
    folder = ROOT / "assets/video/flipper"
    if stem and (folder / f"{stem}.mp4").exists():
        poster = f"/assets/video/flipper/{stem}.webp"
        sources = "".join(
            f'<source src="/assets/video/flipper/{stem}.{ext}" type="video/{ext}">'
            for ext in ("webm", "mp4") if (folder / f"{stem}.{ext}").exists()
        )
        return (f'<video class="hero__video" autoplay muted loop playsinline preload="metadata" poster="{poster}"'
                f' aria-label="{E(t["hero_alt"])}">{sources}</video>')
    return shot("screen_sampler", lang, t["hero_alt"], eager=True)


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
    vid = VIDEO_ID.get(lang)
    if not vid:
        return ""
    return f"""
      <section class="band" id="video" aria-label="{E(t['video_title'])}">
        <div class="shell">
          <div class="video card">
            <iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(t['video_title'])}" loading="lazy"
              referrerpolicy="strict-origin-when-cross-origin"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
          </div>
        </div>
      </section>"""


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


def flow_block(t: dict) -> str:
    return "".join(
        f'<li class="step" data-reveal><span class="step__n" aria-hidden="true">{n}</span>'
        f'<h3>{E(name)}</h3><p>{E(text)}</p></li>'
        for n, (name, text) in enumerate(t["flow"], 1)
    )


def screens_block(lang: str, t: dict) -> str:
    cards = []
    for key, name, text, points in t["screens"]:
        lis = "".join(f"<li>{E(x)}</li>" for x in points)
        cards.append(f"""
            <article class="card screen" data-reveal>
              <div class="screen__shot">{shot(f'screen_{key}', lang, name, link=True)}</div>
              <div class="screen__body">
                <h3><span class="tab">{E(name)}</span></h3>
                <p>{E(text)}</p>
                <ul>{lis}</ul>
              </div>
            </article>""")
    return "".join(cards)


def engines_block(lang: str, t: dict) -> str:
    tabs, panels = [], []
    for i, (key, name, text, plate, when) in enumerate(t["engines"]):
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
                <p class="engine__text">{E(text)}</p>
                <p class="engine__when"><b>{E(t['engines_when'])}</b> {E(when)}</p>
              </div>
            </div>""")
    return f"""
          <div class="seg" role="tablist" aria-label="{E(t['engines_tab_label'])}">{''.join(tabs)}</div>
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


def features_block(t: dict) -> str:
    return "".join(
        f'<li class="feature" data-reveal><h3>{E(name)}</h3><p>{E(text)}</p></li>' for name, text in t["features"]
    )


def install_block(t: dict) -> str:
    def card(os_key: str, title: str, items: list[str]) -> str:
        lis = "".join(f"<li>{E(x)}</li>" for x in items)
        guide = (f'<a class="text-key" href="{INSTALL_URL[os_key]}">{E(t["install_guide"])} →</a>'
                 if RELEASED else "")
        return f"""
            <article class="card install" data-reveal>
              <h3>{E(title)}</h3>
              <ul>{lis}</ul>
              {guide}
            </article>"""
    return (card("mac", t["install_mac_title"], t["install_mac"])
            + card("win", t["install_win_title"], t["install_win"]))


def beta_block(t: dict) -> str:
    return "".join(
        f'<article class="beta-item" data-reveal><h3>{E(name)}</h3><p>{E(text)}</p></article>' for name, text in t["beta"]
    )


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
         "자르고, 뒤집고, 두드리는 무료 오픈소스 샘플러. Chop it, flip it, play it: a free open-source sampler.",
         "flipper/og-flipper.png"),
    "flipper/": ("flipper — 무료 샘플러 · free sampler plug-in",
                 "자르고, 뒤집고, 두드리는 무료 오픈소스 샘플러. Chop it, flip it, play it: a free open-source sampler.",
                 "flipper/og-flipper.png"),
    "artist/": ("레네 RENÉ / arcadiatripper", "Music, guides and playlists by 레네 (tripper).", "og-arcadiatripper.jpg"),
}


TRIPPER_LOGO = ((ROOT / "assets/images/tripper-logo.svg").read_text(encoding="utf-8").strip()
                .replace('role="img" aria-label="tripper"', 'aria-hidden="true" focusable="false"'))


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
            <button type="button" class="gnav__menu-key" aria-expanded="false" aria-controls="menu-plugins"{plugins_on}>PLUGINS<span aria-hidden="true">▾</span></button>
            <div class="gnav__drop" id="menu-plugins" hidden>
              <a href="{prefix}/flipper/"{here if current == 'flipper' else ''}><b>flipper<i>.</i></b><span>{E(t['flipper_tag'])}</span></a>
            </div>
          </div>
          <a href="{prefix}/artist/"{here if current == 'artist' else ''}>ARTIST</a>
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
        <div class="hero__media" aria-hidden="true">{hero_media(lang, t)}</div>
        <div class="shell hero__shell">
        <div class="hero__copy">
          <p class="label">{E(t['kicker'])}</p>
          <h1 class="logo">flipper<i>.</i></h1>
          <p class="hero__lead">{t['lead']}</p>
          <p class="hero__sub">{E(t['sub'])}</p>
          <ul class="hero__meta">{meta}</ul>
{download_block(t)}
        </div>
        </div>
      </section>
{video_block(lang, t)}
      <section class="band" id="flow" aria-labelledby="flow-title">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['flow_label'])}</p><h2 id="flow-title">{t['flow_title']}</h2><p>{E(t['flow_sub'])}</p></header>
          <ol class="flow">{flow_block(t)}</ol>
        </div>
      </section>

      <section class="band" id="screens" aria-labelledby="screens-title">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['screens_label'])}</p><h2 id="screens-title">{t['screens_title']}</h2><p>{E(t['screens_sub'])}</p></header>
          <div class="screens">{screens_block(lang, t)}
          </div>
        </div>
      </section>

      <section class="band band--engines" id="engines" aria-labelledby="engines-title" data-engines data-skin="clean">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['engines_label'])}</p><h2 id="engines-title">{t['engines_title']}</h2><p>{E(t['engines_sub'])}</p></header>
{engines_block(lang, t)}
        </div>
      </section>

      <section class="band" id="tempo" aria-labelledby="tempo-title">
        <div class="shell shell--split">
          <header class="heading" data-reveal><p class="label">{E(t['tempo_label'])}</p><h2 id="tempo-title">{t['tempo_title']}</h2><p>{E(t['tempo_sub'])}</p></header>
{tempo_block(t)}
        </div>
      </section>

      <section class="band" id="features" aria-labelledby="features-title">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['features_label'])}</p><h2 id="features-title">{t['features_title']}</h2></header>
          <ul class="features">{features_block(t)}</ul>
        </div>
      </section>

      <section class="band" id="install" aria-labelledby="install-title">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['install_label'])}</p><h2 id="install-title">{t['install_title']}</h2></header>
          <div class="installs">{install_block(t)}
          </div>
          <p class="install__note">{E(t['install_hosts'])}{(' ' + E(t['install_ai'])) if RELEASED else ''}</p>
        </div>
      </section>

      <section class="band" id="beta" aria-labelledby="beta-title">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['beta_label'])}</p><h2 id="beta-title">{t['beta_title']}</h2></header>
          <div class="beta">{beta_block(t)}
          </div>
        </div>
      </section>

      <section class="band" id="faq" aria-labelledby="faq-title">
        <div class="shell">
          <header class="heading" data-reveal><p class="label">{E(t['faq_label'])}</p><h2 id="faq-title">{t['faq_title']}</h2></header>
          <div class="faq">{faq_block(t)}
          </div>
        </div>
      </section>
    </main>

    <footer class="foot">
      <div class="shell foot__inner">
        <p class="logo logo--small">flipper<i>.</i></p>
        <div class="foot__links">
          {source}
          <a href="https://www.youtube.com/@arcadiatripper">YouTube ↗</a>
          <a href="https://www.instagram.com/arcadiatripper">Instagram ↗</a>
        </div>
        <div class="foot__notes">
          <span>{E(t['license'])}</span>
          <span>{E(t['built_with'])}</span>
          <span>{E(t['fonts'])}</span>
          <span>{E(t['made_by'])}</span>
          <span class="foot__credit">© tripper / <em>@arcadiatripper</em></span>
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
