# SPDX-License-Identifier: MIT
"""Every flipper feature, one by one: its own picture of the plug-in and a few paragraphs, in Korean and English.

The site's long read is built from this (tools/build_flipper.py), and the manual can take it as it is later. The
words follow the plug-in's own (flipper docs/GLOSSARY.md: 슬라이스, 스킵, 되돌리기, 음높이, 멈춤 …).

Each part: key, title, lead and its features. Each feature:
    key   the slide's id and its picture's name (assets/images/flipper/feat_<key>_<lang>.webp)
    shot  (the flipper_snapshot site render, the crop as fractions: left, top, right, bottom), or
          ("@<picture>", None) for a picture the site already has, or None with tool="tempo" (the calculator
          stands in for the picture)
    ko    (name, [paragraphs])
    en    (name, [paragraphs])
Pictures: ONLY_SITE=1 flipper_snapshot <shots> 2 (flipper tools/snapshot.cpp), then tools/make_site_shots.py.
"""

TOP = (0, 0.135, 1, 0.53)          # the chop area: the chop row and the waveform
TOP_ROW = (0, 0, 1, 0.3)            # the header and the sample row
PADS = (0, 0.5, 1, 1)               # the play row and the pads
RACK = (0, 0.04, 1, 0.3)            # the fx screen's rack and the picked slot's row
DECK = (0, 0.38, 1, 1)              # the deck under the waveform


def F(key, shot, ko, en, **extra):
    return {"key": key, "shot": shot, "ko": ko, "en": en, **extra}


PARTS = [
    # ------------------------------------------------------------------------------------------------- chop
    {
        "key": "chop",
        "title": {"ko": "자르기", "en": "Chop"},
        "lead": {
            "ko": "샘플링의 핵심 부분을 직관적이고 쉽게 할 수 있도록 만들었어요.",
            "en": "Built so the heart of sampling is direct and easy.",
        },
        "features": [
            F("hits", ("hits", TOP),
              ("타격 찾기", [
                  "샘플을 열면 flipper가 소리의 타격(transient)을 한 번에 찾아 둬서, 열자마자 패드로 칠 수 있어요.",
                  "'감도(Sensitivity)' 노브를 돌리면 다시 분석하지 않고 그 자리에서 다시 잘라요. 올리면 약한 타격까지, 내리면 뚜렷한 타격만 남아요.",
                  "자르는 곳은 시작 지점(S)과 끝 지점(E) 사이예요.",
              ]),
              ("Hits", [
                  "When a sample opens, flipper finds its hits (transients) in one go, so you can play the pads straight away.",
                  "Turn the sensitivity knob and it re-chops on the spot without analysing again: up for weaker hits too, down for only the clear ones.",
                  "It chops between the start point (S) and the end point (E).",
              ])),
            F("grid", ("grid", TOP),
              ("박자로 자르기", [
                  "'그리드(grid)'를 고르면 샘플의 템포에 맞춰 1/16, 1/8, 1/4, 1/2, 한 마디마다 잘라요. 드럼 루프를 정박으로 나누거나, 패드 하나에 한 박씩 놓고 싶을 때 사용하세요.",
                  "템포가 없는 샘플은 같은 길이로 나눠요. 스킵한 부분은 다시 잘라도 그대로 남아요.",
              ]),
              ("Beats", [
                  "Pick grid and it chops every 1/16, 1/8, 1/4, 1/2 or bar at the sample's tempo. Use it to split a drum loop on the grid, or to put one beat on each pad.",
                  "A sample without a tempo is cut into equal parts. Skipped parts stay where they are through a re-chop.",
              ])),
            F("lazy", ("lazy", TOP),
              ("레이지 찹(Lazy Chop)", [
                  "'레이지(Lazy)'를 누르면 구간이 재생되고, 듣다가 원하는 순간에 아무 키를 누르면 그 자리에서 잘려요.",
              ]),
              ("Lazy chop", [
                  "Press lazy and the range plays. Whenever you like, hit any key and it cuts right there.",
              ])),
            F("lit", ("lit", (0, 0.135, 1, 1)),
              ("불 켜진 패드", [
                  "설정에서 켜면 다음 슬라이스의 패드에만 불이 들어오고, 그 패드를 눌러야 잘려요. 옛 샘플러처럼 패드를 차례로 짚어 가며 자를 수 있어요.",
              ]),
              ("The lit pad", [
                  "Turn it on in the settings and only the next slice's pad lights up; that pad is the one that cuts. Chop pad after pad, the old samplers' way.",
              ])),
            F("dice", ("dice", (0, 0.08, 1, 0.53)),
              ("주사위(Dice)", [
                  "누를 때마다 새로운 찹이 나와요. 감도, 잠근 마커, 스킵한 부분은 그대로 두고 나머지만 새로 잘라요.",
                  "주사위를 끌면 혼돈(chaos)이 0–100 %로 바뀌어요. 낮으면 센 타격만 골라 고르게 자르고, 높을수록 타격이 아닌 자리까지 섞어 잘라요.",
              ]),
              ("Dice", [
                  "Every press gives a new chop. Sensitivity, locked markers and skipped parts stay; the rest is chopped anew.",
                  "Drag the die to set the chaos, 0–100 %. Low keeps to the strongest hits, fairly evenly; the higher it goes, the more places that aren't hits get mixed in.",
              ])),
            F("hand", ("zoomed", TOP),
              ("마커 다듬기", [
                  "파형을 더블클릭하면 마커가 생기고, 가까운 타격에 자석처럼 붙어요. 마커는 끌어서 옮기고, 더블클릭하면 지워요.",
                  "잠근 마커는 다시 잘라도 그 자리에 남아요. 확대한 동안에는 파형이 재생 위치를 따라가요.",
              ]),
              ("Markers", [
                  "Double-click the waveform for a marker; it snaps to a nearby hit like a magnet. Drag a marker to move it, double-click it to delete it.",
                  "Locked markers stay put through a re-chop. While zoomed in, the waveform follows the playhead.",
              ])),
            F("skip", ("skip", (0, 0.135, 1, 0.6)),
              ("스킵(Skip)", [
                  "카운트인, 숨소리처럼 패드에 두고 싶지 않은 부분은 지우지 않고 스킵해요. 뒤 슬라이스들이 한 칸씩 당겨지고, 다시 잘라도 스킵한 부분은 그대로 남아요.",
              ]),
              ("Skip", [
                  "A count-in, a breath, anything you don't want on a pad: skip it instead of deleting it. The slices after it move up one, and the skipped part stays skipped through a re-chop.",
              ])),
            F("trims", ("trims", (0, 0.135, 1, 0.6)),
              ("슬라이스 시작과 끝", [
                  "슬라이스마다 시작과 끝을 샘플 단위로 다듬어요. 끝을 당기면 꼬리가 잘리고, 밀면 다음 마커를 넘어 이어서 울려요.",
                  "자석을 켜면 0 교차점(zero crossing)에 붙어서 클릭이 생기지 않아요.",
              ]),
              ("Slice start and end", [
                  "Trim each slice's start and end to the sample. Pull the end in to cut the tail; push it out and the slice rings on past the next marker.",
                  "With the magnet on they snap to zero crossings, so there are no clicks.",
              ])),
            F("slice", ("edit", (0, 0.135, 1, 0.62)),
              ("슬라이스마다 다섯 가지", [
                  "최대 64개 슬라이스까지 자를 수 있어요. 슬라이스마다 음높이, 리버스, 볼륨, 페이드 인, 페이드 아웃 다섯 가지만 있어요. 신시사이저가 아니라 샘플러라서 필요한 것만 남겼어요.",
                  "모든 소리의 시작과 끝을 아주 짧게 다듬어서, 페이드가 0이어도 클릭이 나지 않아요. 여러 슬라이스를 골라 한꺼번에 바꿀 수도 있어요.",
              ]),
              ("Five things per slice", [
                  "Up to 64 slices. Each has just five things: pitch, reverse, volume, fade in and fade out. It's a sampler, not a synth, so only what's needed stays.",
                  "Every sound's start and end is smoothed very briefly, so even a fade of 0 doesn't click. Pick several slices to change them all at once.",
              ])),
            F("truncate", ("hits", (0, 0.09, 1, 0.53)),
              ("잘라내기(Truncate)", [
                  "S부터 E까지만 남기고 나머지를 잘라 내요. 프로젝트와 플립 파일이 그만큼 가벼워져요.",
              ]),
              ("Truncate", [
                  "Keep only S to E and cut the rest away. The project and the flip get that much lighter.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- keys
    {
        "key": "keys",
        "title": {"ko": "키와 템포", "en": "Key and tempo"},
        "lead": {
            "ko": "키와 속도는 패드마다가 아니라 샘플 하나에 있어요. 샘플 하나를 통째로 다른 곡처럼 만들기 위해서예요.",
            "en": "Key and speed belong to the whole sample, not to each pad, so one sample can become a different track.",
        },
        "features": [
            F("repitch", ("repitch", TOP_ROW),
              ("리피치(Repitch)", [
                  "옛 샘플러처럼 읽는 속도를 바꿔요. 키를 내리면 느리고 어둡게, 올리면 빠르고 밝게 울려요. 새 샘플은 리피치로 시작해요.",
                  "clean은 키를 많이 올려도 날카로운 잡음이 끼지 않게 읽고, grey, black, purple은 그 기계가 읽던 방식 그대로 거칠게 읽어요.",
              ]),
              ("Repitch", [
                  "Changes the playback speed, like the old samplers. Pitch down and it plays slower and darker; up, faster and brighter. A new sample starts in repitch.",
                  "clean reads it so that even a big pitch-up stays free of harsh noise; grey, black and purple read it rough, the way each machine did.",
              ])),
            F("keep", ("keep", TOP_ROW),
              ("템포 유지(Keep Tempo)", [
                  "키와 템포를 따로 바꿔요. 템포는 그대로 두고 키만, 또는 키는 그대로 두고 템포만 바꿀 수 있어요.",
                  "고품질 타임 스트레치 알고리즘인 Rubber Band R3와 빠른 Signalsmith Stretch를 직접 들어 보고 골랐어요. 키만 바꿀 땐 비슷했고, 템포를 바꿀 땐 R3가 확실히 자연스러웠어요. 그래서 들리는 소리는 R3로 만들어요.",
              ]),
              ("Keep tempo", [
                  "Key and tempo move apart: the key alone with the tempo kept, or the tempo alone with the key kept.",
                  "We listened to Rubber Band R3, a high-quality time-stretch algorithm, and the fast Signalsmith Stretch side by side. For key changes alone they were close; for tempo changes R3 was clearly more natural. So the sound you hear is made with R3.",
              ])),
            F("bake", ("settings", (0.5, 0.13, 0.97, 0.6)),
              ("미리 굽기(Bake)", [
                  "키나 속도를 바꾸면 R3로 소리를 미리 만들어 두고, 다음에 칠 때부터 그 소리를 써요. 굽는 동안에는 Signalsmith Stretch로 바로 들려줘요.",
                  "자른 구간 전체를 한 번에 구워서, 마커를 옮겨도 다시 굽지 않아요. 바운스도 같은 소리라 들은 그대로 나가요.",
                  "컴퓨터가 버겁다면 설정에서 '고품질 타임 스트레치'를 끄면 돼요. Signalsmith Stretch로 더 가볍고 빠르게 구워요.",
              ]),
              ("Bake", [
                  "Change the key or speed and R3 makes the sound ahead of time; from the next hit on, that's what plays. While it bakes you hear Signalsmith Stretch straight away.",
                  "The whole chopped range is baked at once, so moving a marker doesn't bake again. Bounces use the same sound, so they come out as you heard them.",
                  "If your computer struggles, turn off 'high-quality time stretch' in the settings and it bakes lighter and faster with Signalsmith Stretch.",
              ])),
            F("crisp", ("hits", (0.55, 0, 1, 0.42)),
              ("또렷하게(Crisp)", [
                  "템포 유지에서 타격의 앞부분을 원래 소리 그대로 남겨서, 늘려도 드럼이 흐물흐물해지지 않아요. 비트와 드럼 루프에 잘 맞고, 멜로디와 목소리에는 끄는 게 좋아요.",
              ]),
              ("Crisp", [
                  "In keep tempo, the front of each hit keeps the original sound, so drums don't go soft when stretched. Good for beats and drum loops; better off for melodies and voices.",
              ])),
            F("keyknob", ("typing", (0.3, 0, 0.85, 0.3)),
              ("키와 속도 노브", [
                  "키는 반음 단위로, Shift를 누르면 센트 단위로 움직여요. 속도는 ×0.750처럼 배속으로 보여요.",
              ]),
              ("Key and speed knobs", [
                  "The key moves in semitones, or in cents with shift. Speed shows as a rate, like ×0.750.",
              ])),
            F("tempo", ("dawtempo", (0.3, 0, 1, 0.36)),
              ("샘플의 템포", [
                  "샘플의 원래 BPM을 파일 이름과 길이로 짐작해요. 'dusty keys loop 90 bpm'이면 90 BPM이고, 이름에 없으면 길이에 맞는 후보(2마디면 90, 4마디면 180 등)를 보여줘요. 직접 입력할 수도 있어요.",
              ]),
              ("The sample's tempo", [
                  "flipper guesses the sample's original BPM from its file name and length. 'dusty keys loop 90 bpm' is 90 BPM; if the name doesn't say, it offers what fits the length (90 for 2 bars, 180 for 4, and so on). Or type it in.",
              ])),
            F("calc", None,
              ("템포 계산", [
                  "리피치에서 키를 내리면 템포가 얼마가 되는지, 원하는 템포가 되려면 키를 얼마나 내려야 하는지 계산해요.",
                  "플러그인에서는 BPM 칸에 원하는 템포를 치면 키가 따라 움직이고, 'DAW 템포'를 켜면 지금 곡의 템포에 맞춰요.",
              ]),
              ("Tempo maths", [
                  "In repitch: what tempo you get when you pitch down, and how far to pitch down for the tempo you want.",
                  "In the plug-in, type the tempo you want in the BPM field and the key follows; turn on 'DAW tempo' to match the song.",
              ]), tool="tempo"),
            F("kind", ("kind", TOP_ROW),
              ("루프와 원샷(Loop / One-shot)", [
                  "샘플마다 루프인지 원샷인지 정해요. 루프는 템포가 있어서 DAW 템포를 따라갈 수 있고, 원샷은 템포 없이 그대로 울려요. 처음에는 파일 이름과 길이로 짐작해요.",
              ]),
              ("Loop and one-shot", [
                  "Each sample is a loop or a one-shot. A loop has a tempo and can follow the DAW's; a one-shot just plays as it is. At first flipper guesses from the file name and length.",
              ])),
            F("keychip", ("keyhelp", (0.3, 0, 1, 0.32)),
              ("키 찾기(Key Detection)", [
                  "S부터 E까지의 키를 찾아 '원래 키 → 지금 들리는 키'로 보여줘요. Am → Gm이면 원래 A 마이너인 샘플이 지금 G 마이너로 들린다는 뜻이에요.",
                  "옛 레코드는 표준 튜닝(A = 440 Hz)에서 조금 어긋나 있곤 해서, 몇 센트 어긋났는지도 같이 보여줘요.",
              ]),
              ("Key detection", [
                  "It finds the key from S to E and shows 'original key → the key you hear now'. Am → Gm means a sample in A minor now sounds in G minor.",
                  "Old records are often a little off standard tuning (A = 440 Hz), so it shows by how many cents too.",
              ])),
            F("keymenu", ("keymenu", (0.45, 0.05, 1, 0.55)),
              ("다른 후보와 직접 고르기", [
                  "키 칩을 누르면 다른 후보들이 나와서, 헷갈리기 쉬운 장조와 단조를 바로 바꿔 볼 수 있어요. 알고 있는 키가 있으면 24개 키 중에서 직접 고르고, 직접 고른 키는 다시 감지해도 바뀌지 않아요.",
              ]),
              ("Other candidates, or pick it yourself", [
                  "Click the key chip for the other candidates, so you can flip between a major and a minor that are easy to mix up. If you know the key, pick it from all 24; a key you picked stays through a new detection.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- play
    {
        "key": "play",
        "title": {"ko": "연주", "en": "Play"},
        "lead": {
            "ko": "샘플러는 덱 하나처럼 움직여요. 패드마다 따로 놀지 않아요.",
            "en": "The sampler moves like one deck. The pads don't each go their own way.",
        },
        "features": [
            F("pads", ("pads16", PADS),
              ("패드", [
                  "한 페이지에 패드 16개(8 × 2)나 32개(8 × 4)가 있고, 페이지를 넘기면 슬라이스 64개까지 칠 수 있어요. 패드 1번은 C3예요. 여러 패드를 골라 한꺼번에 바꿀 수도 있어요.",
              ]),
              ("Pads", [
                  "16 pads (8 × 2) or 32 (8 × 4) on a page; turn the page to play up to 64 slices. Pad 1 is C3. Pick several pads to change them all at once.",
              ])),
            F("voices", ("voices", PADS),
              ("모노와 폴리(Mono / Poly)", [
                  "모노가 기본이에요. 새 패드가 앞 소리를 끊어서, 찹을 연주해도 소리가 쌓여 뭉개지지 않아요. 폴리는 소리가 겹쳐 울려서 멜로디의 화음에 써요.",
              ]),
              ("Mono and poly", [
                  "Mono is the default: each new pad cuts the last sound, so a played chop doesn't pile up into mush. Poly lets sounds overlap, for chords in a melody.",
              ])),
            F("padplays", ("padplays", PADS),
              ("누르는 동안과 슬라이스 전체", [
                  "'누르는 동안'은 누른 만큼만, '슬라이스 전체'는 한 번 치면 슬라이스 끝까지 울려요.",
              ]),
              ("While held, or the whole slice", [
                  "'while held' plays only as long as you hold; 'whole slice' plays to the slice's end from one hit.",
              ])),
            F("playas", ("playas", PADS),
              ("연주 방법", [
                  "패드(슬라이스 하나를 패드 하나에), 멜로디(슬라이스 하나를 건반 전체에), 스크래치(패드마다 자기 슬라이스를 판에 올려 긁기), fx 건반(건반으로 fx 패드 치기) 네 가지예요. 가장 낮은 건반 넷은 키스위치(keyswitch)라서, DAW 클립 안에서 곡 중간에 연주 방법을 바꿀 수 있어요.",
              ]),
              ("Play as", [
                  "Four ways: pads (one slice per pad), melody (one slice across the keys), scratch (each pad puts its slice on the record and scratches it) and fx keys (play the fx pads from the keys). The lowest four keys are keyswitches, so a DAW clip can change the way mid-song.",
              ])),
            F("melody", ("melody", PADS),
              ("멜로디(Melody)", [
                  "슬라이스 하나를 건반에 깔아 음을 연주해요. 반음 단위로 치거나 메이저, 마이너, 하모닉 마이너, 메이저 · 마이너 펜타토닉, 도리안, 프리지안, 믹솔리디안 스케일을 골라요. 화면 건반은 MIDI 음 128개 전부이고, 서스테인 페달도 받아요.",
              ]),
              ("Melody", [
                  "One slice across the keys, to play notes. Play in semitones or pick a scale: major, minor, harmonic minor, major and minor pentatonic, dorian, phrygian or mixolydian. The on-screen keyboard has all 128 MIDI notes, and the sustain pedal works.",
              ])),
            F("scale", ("scale", (0, 0, 0.6, 1)),
              ("스케일과 흰 건반", [
                  "스케일을 고르면 그 스케일의 음만 건반에 놓여요. '흰 건반'을 고르면 어떤 스케일이든 흰 건반만으로 칠 수 있어요. 흰 건반과 검은 건반의 구분이 없는 패드 컨트롤러라면 '모든 건반'을 고르면 돼요.",
              ]),
              ("Scales and white keys", [
                  "Pick a scale and only its notes sit on the keys. Pick 'white keys' to play any scale on the white keys alone. On a pad controller with no black and white keys, pick 'all keys'.",
              ])),
            F("root", ("root", PADS),
              ("원키(Root) 옮기기", [
                  "원래 높이로 울리는 건반(원키)은 C3에 묶여 있지 않고, 원하는 건반으로 옮길 수 있어요.",
              ]),
              ("Move the root", [
                  "The key that plays at the original pitch (the root) isn't tied to C3; move it to any key you like.",
              ])),
            F("colours", ("colours", (0, 0, 1, 1)),
              ("패드 색", [
                  "기본은 '소리 따라'예요. 밝은 소리는 밝은 색, 어두운 소리는 짙은 색으로 칠해서 하이햇과 킥이 한눈에 구분돼요. 비주얼라이저도 같은 색으로 움직여요. 패드마다 정해진 '16색'도 있어요.",
              ]),
              ("Pad colours", [
                  "'by sound' is the default: bright sounds get bright colours and dark sounds deep ones, so hats and kicks stand apart at a glance. The visualizer moves in the same colours. There's also '16 colours', fixed per pad.",
              ])),
            F("velocity", ("settings", (0.5, 0.13, 0.97, 0.36)),
              ("벨로시티(Velocity)", [
                  "치는 세기를 소리 크기로 어떻게 바꿀지 골라요. 그대로, 부드럽게, 세게, 늘 같게 네 가지예요.",
              ]),
              ("Velocity", [
                  "How hard you hit becomes how loud it plays, four ways: as is, soft, hard, or always the same.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- sample
    {
        "key": "sample",
        "title": {"ko": "샘플 담기", "en": "Bring a sample in"},
        "lead": {
            "ko": "파일을 끌어 놓거나, DAW의 소리를 바로 녹음해서 샘플로 써요.",
            "en": "Drop a file in, or record straight from the DAW.",
        },
        "features": [
            F("start", ("start", (0.15, 0.05, 0.85, 0.75)),
              ("빈 화면", [
                  "처음 열면 카드 두 장이 있어요. 샘플을 놓으면 샘플러로, 원샷을 놓으면 드럼 킷으로 시작해요. WAV, AIFF, FLAC, MP3, OGG, Opus를 열 수 있고, DAW의 오디오 클립을 바로 끌어 놓아도 돼요.",
              ]),
              ("The empty screen", [
                  "It opens with two cards: drop a sample to start in the sampler, or one-shots to start a drum kit. It opens WAV, AIFF, FLAC, MP3, OGG and Opus, and you can drag an audio clip straight from the DAW.",
              ])),
            F("take", ("take", (0.4, 0, 1, 0.4)),
              ("녹음하기(Record)", [
                  "다른 트랙의 소리(사이드체인)나 flipper가 지금 내는 소리(리샘플)를 새 샘플로 받아요. 바로 또는 다음 마디부터, 멈출 때까지 또는 1 · 2 · 4 · 8마디만큼 담고, 24비트 WAV로 남아요.",
              ]),
              ("Record", [
                  "Take another track's sound (sidechain) or what flipper is playing right now (resample) as a new sample. Start now or on the next bar, stop by hand or after 1, 2, 4 or 8 bars; it's kept as a 24-bit WAV.",
              ])),
            F("channels", ("@feature_channels", None),
              ("채널 고르기", [
                  "스테레오 샘플에서 스테레오, 왼쪽, 오른쪽, 미드, 사이드 중 하나를 골라요. 'oo' 키를 누르면 파형이 왼쪽과 오른쪽 두 줄로 나뉘어서, 한쪽에만 있는 소리나 가운데 보컬을 눈으로 찾을 수 있어요.",
              ]),
              ("Channel select", [
                  "From a stereo sample pick stereo, left, right, mid or side. Press the 'oo' key and the waveform splits into left and right, so you can spot a sound on one side only, or a vocal in the middle.",
              ])),
            F("gain", ("hits", (0, 0.53, 0.62, 0.66)),
              ("샘플 게인과 노멀라이즈(Normalize)", [
                  "샘플 게인은 샘플 전체의 크기예요. 노멀라이즈는 가장 큰 순간이 0 dBFS에 닿도록 크기를 맞춰요.",
              ]),
              ("Sample gain and normalize", [
                  "Sample gain is the level of the whole sample. Normalize sets it so the loudest moment touches 0 dBFS.",
              ])),
            F("flips", ("flips", (0, 0, 0.6, 0.55)),
              ("플립 파일(.flip)", [
                  "샘플, 찹, 설정을 .flip 파일 하나에 담아요. 폴더 안의 플립을 차례로 넘겨 들을 수 있고, 예전 버전에서 만든 플립도 같은 소리로 열려요.",
              ]),
              ("Flip files (.flip)", [
                  "The sample, the chop and the settings in one .flip file. Step through the flips in a folder by ear; a flip made in an older version opens sounding the same.",
              ])),
            F("standalone", ("standalone", (0, 0, 1, 0.3)),
              ("단독 앱(Standalone)", [
                  "DAW 없이 flipper만 여는 앱도 있어요.",
              ]),
              ("Standalone", [
                  "There's also an app that opens flipper on its own, without a DAW.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- rack
    {
        "key": "rack",
        "title": {"ko": "fx 랙", "en": "fx rack"},
        "lead": {
            "ko": "fx 화면 위의 열 칸이 소리 순서대로 이어져요. 노브를 올리면 켜지고, 꺼진 칸은 CPU를 쓰지 않아요. 직접 만든 것과 Airwindows(MIT)에서 가져온 모델이 섞여 있고, 가져온 모델은 칸마다 귀로 들어 보고 골랐어요.",
            "en": "Ten slots across the top of the fx screen, in the order the sound flows. Turn a knob up and the slot comes on; a slot that's off uses no CPU. Some are our own, some are models from Airwindows (MIT), each picked slot by slot by ear.",
        },
        "features": [
            F("slot_filter", ("slot_filter", RACK),
              ("필터(Filter)", [
                  "직접 만든 필터예요. LP는 고음을, HP는 저음을 깎고, BP는 가운데만 남겨요. 12 dB와 24 dB 기울기, 레조넌스가 있고, '클린'은 정확하게, '래더'는 옛 신시사이저처럼 둥글고 따뜻하게 걸러요. 랙 맨 앞이나 맨 끝에 둘 수 있어요.",
              ]),
              ("Filter", [
                  "Our own filter. LP cuts the highs, HP the lows, BP keeps the middle. 12 dB and 24 dB slopes and resonance; 'clean' filters exactly, 'ladder' round and warm like an old synth. It can sit at the front of the rack or at the end.",
              ])),
            F("slot_punch", ("slot_punch", RACK),
              ("펀치(Punch)", [
                  "직접 만든 노브 하나짜리 컴프레서예요. 타격을 앞으로 끌어내요. '피드백'은 더 음악적이고, '클래식'은 깨끗하고 정확해요.",
              ]),
              ("Punch", [
                  "Our own one-knob compressor. It pulls the hits forward. 'feedback' is more musical, 'classic' clean and exact.",
              ])),
            F("slot_distort", ("slot_distort", RACK),
              ("디스토션(Distortion)", [
                  "다섯 가지예요. 소프트는 둥글게(Airwindows PurestSaturation), 튜브는 달고 두껍게(Density3), 클립은 꼭대기를 잘라 단단하게(ClipOnly3), 폴드는 꼭대기를 접어 금속처럼(Fracture2) 울려요. 거의 네모난 소리의 퍼즈는 직접 만들었어요.",
              ]),
              ("Distortion", [
                  "Five kinds. Soft is round (Airwindows PurestSaturation), tube sweet and thick (Density3), clip cuts the peaks off, hard (ClipOnly3), and fold folds them over, metallic (Fracture2). Fuzz, almost square, is our own.",
              ])),
            F("slot_crush", ("slot_crush", RACK),
              ("크러시(Crush)", [
                  "샘플레이트와 비트를 깎아 옛 샘플러의 바삭한 소리를 내요. 레이트는 Airwindows DeRez5를 쓰고, 비트는 직접 만들었어요.",
              ]),
              ("Crush", [
                  "Cuts the sample rate and the bits for the crunch of an old sampler. The rate is Airwindows DeRez5; the bits are our own.",
              ])),
            F("slot_tape", ("slot_tape", RACK),
              ("테이프(Tape)", [
                  "테이프를 얼마나 세게 몰지 정하는 노브 하나예요. 저음은 부풀고 고음은 눌려요. Airwindows ToTape9를 써요.",
              ]),
              ("Tape", [
                  "One knob for how hard the tape is driven. The lows swell and the highs settle. Airwindows ToTape9.",
              ])),
            F("slot_chorus", ("slot_chorus", RACK),
              ("코러스(Chorus)", [
                  "소리를 몇 겹 복사해 천천히 흔들어서 넓고 따뜻하게 만들어요. Airwindows ChorusEnsemble을 써요.",
              ]),
              ("Chorus", [
                  "A few copies of the sound, slowly swaying, for something wide and warm. Airwindows ChorusEnsemble.",
              ])),
            F("slot_noise", ("slot_noise", RACK),
              ("노이즈(Noise)", [
                  "더스트(테이프 먼지, Airwindows TapeDust), 히스(쉬익), 크래클(판의 지글거림)을 소리 밑에 깔아요. 히스와 크래클은 직접 만들었고, 샘플이 울리는 동안에만 나요.",
              ]),
              ("Noise", [
                  "Dust (tape dust, Airwindows TapeDust), hiss and crackle (the sizzle of a record) under the sound. Hiss and crackle are our own, and they sound only while a sample plays.",
              ])),
            F("slot_echo", ("slot_echo", RACK),
              ("에코(Echo)", [
                  "테이프는 따뜻하게 닳아 가는 반복(Airwindows TapeDelay2), 디지털은 깨끗한 반복, 그레인은 잘게 부서진 조각의 반복이에요. 디지털과 그레인은 직접 만들었어요. 박자에 맞추거나 ms로 정할 수 있어요.",
              ]),
              ("Echo", [
                  "Tape repeats wear warmly away (Airwindows TapeDelay2), digital repeats stay clean, grain repeats in small broken pieces. Digital and grain are our own. Set it to the beat or in ms.",
              ])),
            F("slot_space", ("slot_space", RACK),
              ("스페이스(Space)", [
                  "소리 둘레에 공간을 만들어요. 룸(Airwindows kWoodRoom), 홀(kRockstar2), 갤럭시(Galactic3), 라이트(Ultralight2), 타이니(VerbTiny) 다섯 가지예요.",
              ]),
              ("Space", [
                  "A space around the sound, five kinds: room (Airwindows kWoodRoom), hall (kRockstar2), galaxy (Galactic3), light (Ultralight2) and tiny (VerbTiny).",
              ])),
            F("slot_all", ("slot_all", RACK),
              ("마스터(Master)", [
                  "모든 칸이 마지막에 지나는 곳이에요. 입력(Airwindows ADClip9), 너비(SweetWide), 톤, 리미터가 있어요. 리미터 '세이프'는 −0.3 dBFS를 넘는 소리만 잡고, '빈티지'는 큰 소리를 둥글게 눌러요.",
              ]),
              ("Master", [
                  "Where every slot ends up. Input (Airwindows ADClip9), width (SweetWide), tone and a limiter. The 'safe' limiter catches only what goes past −0.3 dBFS; 'vintage' rounds loud sounds down.",
              ])),
            F("fxpads", ("fxpads", (0.35, 0.38, 1, 1)),
              ("fx 패드", [
                  "누르고 있는 동안 소리를 바꾸는 패드 16개예요. 테이프(멈춤, 되감기, 반속도, 리버스), 에코와 크러시, 스크래치 패턴(처프, 베이비)이 있고, 박에 맞춰 들어가서 바운스해도 들은 그대로예요.",
              ]),
              ("fx pads", [
                  "16 pads that change the sound while held: tape (stop, rewind, half speed, reverse), echo and crush, and scratch patterns (chirp, baby). They come in on the beat, so a bounce sounds as you heard it.",
              ])),
            F("strips", ("strips", (0, 0.38, 0.72, 1)),
              ("반복과 필터 스트립", [
                  "반복 스트립은 손가락이 닿은 자리의 길이(한 마디부터 1/64까지)로 소리를 되풀이해요. 필터 스트립은 가운데가 열려 있고, 왼쪽으로 가면 로우패스, 오른쪽으로 가면 하이패스가 닫혀요.",
              ]),
              ("Repeat and filter strips", [
                  "The repeat strip repeats the sound at the length under your finger, from a bar down to 1/64. The filter strip is open in the middle; to the left a low-pass closes, to the right a high-pass.",
              ])),
            F("fxrows", ("fxrows", (0, 0.38, 1, 1)),
              ("윗줄과 두 줄", [
                  "'윗줄'은 fx 패드 아래에 슬라이스 패드가 한 줄 있어서 마우스로도 연주할 수 있어요. '두 줄'은 fx 패드를 크게 보여줘요.",
              ]),
              ("Top row and two rows", [
                  "'top row' puts a row of slice pads under the fx pads, so you can play with the mouse too. 'two rows' shows the fx pads big.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- deck
    {
        "key": "deck",
        "title": {"ko": "턴테이블", "en": "Turntable"},
        "lead": {
            "ko": "fx 화면 아래는 덱이에요. 자른 구간을 판처럼 돌리고 긁어요.",
            "en": "Under the fx screen is the deck. The chopped range spins like a record, and you scratch it.",
        },
        "features": [
            F("record", ("deckrest", DECK),
              ("판", [
                  "작업 구간이 판 한 장이에요. 33⅓ rpm으로 돌고, 플래터를 돌리거나 파형을 끌면 긁혀요. 지금 엔진의 소리 그대로라서 black으로 긁으면 black의 소리가 나요.",
              ]),
              ("The record", [
                  "The work range is one record. It spins at 33⅓ rpm; turn the platter or drag the waveform to scratch. It plays through the current engine, so a scratch on black sounds like black.",
              ])),
            F("deckhand", ("deckheld", DECK),
              ("손과 슬립매트", [
                  "판을 잡으면 손이 움직인 만큼만 판이 움직이고, 놓으면 슬립매트처럼 바로 제 속도를 따라잡아요.",
              ]),
              ("Hand and slipmat", [
                  "Grab the record and it moves only as far as your hand; let go and it catches up to speed at once, like on a slipmat.",
              ])),
            F("hold", ("deckhold", DECK),
              ("판 잡기", [
                  "누르고 있는 동안 판이 손으로 누른 것처럼 천천히 서고, 놓으면 다시 올라와요. 서고 올라오는 시간은 설정에서 정해요.",
              ]),
              ("Hold the record", [
                  "While held, the record slows to a stop as if pressed by hand; let go and it spins back up. Set how long both take in the settings.",
              ])),
            F("fader", ("deckplay", (0, 0.85, 0.75, 1)),
              ("페이더와 커브(Fader / Curve)", [
                  "페이더로 판 소리를 끊었다 열었다 해요. 커브는 믹스용 '부드럽게'부터 스크래치용 '날카롭게'까지 고를 수 있고, 방향을 뒤집을 수도 있어요.",
              ]),
              ("Fader and curve", [
                  "The fader cuts the record's sound in and out. The curve goes from 'smooth' for mixing to 'sharp' for scratching, and the direction can be flipped.",
              ])),
            F("patterns", ("pattern", (0, 0, 0.55, 0.7)),
              ("스크래치 패턴", [
                  "베이비, 포워드, 처프, 티어, 트랜스포머, 플레어, 2클릭 플레어, 크랩이 있어요. 패턴은 박에 맞춰 시작하고, 세게 칠수록 멀리 밀어요.",
              ]),
              ("Scratch patterns", [
                  "Baby, forward, chirp, tear, transformer, flare, 2-click flare and crab. A pattern starts on the beat, and the harder you hit, the further it pushes.",
              ])),
            F("drawer", ("drawer", (0.55, 0.38, 1, 1)),
              ("건반으로 긁기", [
                  "이어진 건반 16개가 슬라이스 1–16을 판에 올려 고른 패턴으로 긁어요.",
              ]),
              ("Scratch from the keys", [
                  "16 keys in a row put slices 1–16 on the record and scratch them with the pattern you picked.",
              ])),
            F("padpattern", ("padpattern", (0.45, 0, 1, 0.6)),
              ("슬라이스마다 패턴", [
                  "킥은 베이비로, 보컬은 처프로처럼 슬라이스마다 패턴을 정해 두면 패드만 쳐도 루틴이 돼요.",
              ]),
              ("A pattern per slice", [
                  "Baby on the kick, chirp on the vocal: give each slice its own pattern and just playing the pads becomes a routine.",
              ])),
            F("follow", ("deckrest", (0.72, 0.6, 1, 1)),
              ("곡 따라 돌기와 큐(Sync / Cue)", [
                  "'곡 따라 돌기'를 켜면 DAW를 재생할 때 판이 큐부터 곡에 맞춰 돌아요. 손이나 패턴으로 잠깐 떼어 놓아도 다시 곡 자리로 돌아와요.",
              ]),
              ("Sync and cue", [
                  "Turn on sync and when the DAW plays, the record spins from the cue in time with the song. Pull it away by hand or with a pattern and it comes back to the song's place.",
              ])),
            F("speed", ("speed45", DECK),
              ("45와 78", [
                  "grey, black, purple에서는 판 속도를 45나 78로 바꿀 수 있어요. 옛 프로듀서들이 짧은 샘플 시간에 더 긴 소리를 담으려고 판을 빠르게 샘플링하던 방법이에요. 키와 템포는 그대로이고 고음이 더 거칠어져요.",
              ]),
              ("45 and 78", [
                  "On grey, black and purple the record can run at 45 or 78. Old producers sampled records fast to fit more sound into short sample time. Key and tempo stay; the highs get rougher.",
              ])),
            F("controllers", ("deckmidi", DECK),
              ("컨트롤러와 오토메이션", [
                  "플래터에 조그, 터치 스트립, 피치 휠, 패드를 MIDI로 지정할 수 있어요. 판, 손, 페이더가 모두 DAW 파라미터라서 긁은 걸 오토메이션으로 남기고 고칠 수 있어요.",
              ]),
              ("Controllers and automation", [
                  "Map a jog wheel, touch strip, pitch wheel or pads to the platter over MIDI. The record, the hand and the fader are all DAW parameters, so a scratch can be kept and edited as automation.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- drum
    {
        "key": "drum",
        "title": {"ko": "드럼", "en": "Drums"},
        "lead": {
            "ko": "원샷 16개로 킷을 짜는 화면이에요. 샘플러와 같은 플러그인 안에 있어요.",
            "en": "The screen for building a kit from 16 one-shots, in the same plug-in as the sampler.",
        },
        "features": [
            F("cells", ("drum", (0, 0.09, 0.635, 0.95)),
              ("셀 16개", [
                  "4 × 4 셀에 원샷을 끌어 놓아요. 여러 개를 한 번에 놓으면 차례로 채워져요. 어느 화면을 보고 있든 같은 건반이 같은 소리를 내요.",
              ]),
              ("16 cells", [
                  "Drag one-shots onto the 4 × 4 cells; drop several at once and they fill in order. Whichever screen you're on, the same key plays the same sound.",
              ])),
            F("cell", ("drum", (0.63, 0.09, 1, 0.62)),
              ("셀마다 조절", [
                  "셀마다 볼륨, 팬, 음높이(±24 반음), 엔진, 초크 그룹, 페이드가 있고, 여러 셀을 골라 한꺼번에 바꿀 수 있어요.",
              ]),
              ("Per cell", [
                  "Each cell has volume, pan, pitch (±24 semitones), engine, choke group and fades. Pick several cells to change them all at once.",
              ])),
            F("trim", ("drum", (0.63, 0.09, 1, 0.33)),
              ("시작 · 끝, 잘라내기, 노멀라이즈", [
                  "셀마다 원샷의 시작과 끝을 샘플 단위로 다듬고, 필요 없는 부분을 잘라 내거나 크기를 맞춰요.",
              ]),
              ("Start, end, truncate, normalize", [
                  "Trim each one-shot's start and end to the sample, cut away what you don't need, or even out the level.",
              ])),
            F("inserts", ("drum", (0.63, 0.6, 1, 0.97)),
              ("셀마다 fx와 센드(Send)", [
                  "셀마다 필터, 펀치, 디스토션, 크러시, 테이프를 걸 수 있어요. 에코와 스페이스는 킷 전체에 하나씩 두고 셀마다 보내는 양만 정해서 CPU를 아껴요.",
              ]),
              ("fx and sends per cell", [
                  "Each cell can take filter, punch, distortion, crush and tape. Echo and space are one each for the whole kit, with a send amount per cell, to save CPU.",
              ])),
            F("choke", ("drum", (0, 0.05, 1, 1)),
              ("초크와 출력 16개", [
                  "초크 그룹은 넷이에요. 셀을 DAW의 다른 트랙으로 따로 보내는 출력이 16개 있어요.",
              ]),
              ("Choke and 16 outputs", [
                  "Four choke groups. 16 outputs send cells to their own tracks in the DAW.",
              ])),
            F("zones", ("settingskeys", (0, 0.12, 0.5, 0.67)),
              ("건반 구역", [
                  "샘플러, 드럼, fx 패드, 스크래치, 키스위치의 건반 자리를 설정에서 옮길 수 있고, 겹치면 표시해 줘요. MIDI 채널 10으로 보내면 드럼 셀을 바로 칠 수 있어요.",
              ]),
              ("Key zones", [
                  "Move where the sampler, drums, fx pads, scratch and keyswitches sit on the keyboard in the settings; overlaps are marked. Send on MIDI channel 10 to play the drum cells directly.",
              ])),
            F("kits", ("drumempty", (0, 0.05, 1, 1)),
              ("킷 파일과 가져오기", [
                  "킷을 .flipkit 파일로 저장하고 열어요. 다른 프로그램의 드럼 킷(WAV 폴더, .sfz, .mxgrp, .xpm · .xpn, .adg 등)도 가져올 수 있고, 들리는 그대로 WAV 킷으로 내보낼 수도 있어요.",
              ]),
              ("Kit files and import", [
                  "Save and open kits as .flipkit files. Bring in kits from other software too (a WAV folder, .sfz, .mxgrp, .xpm and .xpn, .adg and more), and export a kit as WAVs that sound as you hear them.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- out
    {
        "key": "out",
        "title": {"ko": "내보내기와 안전", "en": "Out, and safe"},
        "lead": {
            "ko": "만든 것은 그대로 DAW로 가고, 갑자기 큰 소리는 나지 않게 했어요.",
            "en": "What you make goes to the DAW as it is, and nothing gets suddenly loud.",
        },
        "features": [
            F("chopmidi", ("chopmidi", (0, 0.45, 0.62, 0.82)),
              ("찹을 MIDI로", [
                  "'찹을 MIDI로' 키를 DAW 트랙에 끌어 놓으면, 원래 루프의 그루브 그대로 슬라이스를 치는 MIDI 클립이 생겨요. 거기서 음만 바꾸며 플립하면 돼요.",
              ]),
              ("Chop to MIDI", [
                  "Drag the 'chop to MIDI' key onto a DAW track and you get a MIDI clip that plays the slices with the original loop's groove. Flip it from there by moving notes.",
              ])),
            F("learn", ("learning", (0, 0, 1, 0.62)),
              ("MIDI 지정(MIDI Learn)", [
                  "노브, 스위치, 키 어디든 오른쪽 클릭해서 컨트롤러를 지정해요. 끝없이 도는 노브도 맞게 움직이고, '노브 8개 차례로'를 쓰면 노브 여덟 개를 돌리기만 해도 차례로 지정돼요.",
              ]),
              ("MIDI learn", [
                  "Right-click any knob, switch or key to map a controller. Endless knobs move the right way too, and 'eight knobs in turn' maps eight knobs just by turning them one after another.",
              ])),
            F("meter", ("meter", (0.4, 0, 1, 0.075)),
              ("볼륨과 미터", [
                  "머리줄의 미터는 왼쪽 · 오른쪽 크기와 가장 컸던 순간, 리미터가 일하는 양을 보여줘요.",
              ]),
              ("Volume and meter", [
                  "The meter in the header shows left and right level, the loudest moment, and how much the limiter is working.",
              ])),
            F("safety", ("slot_all", (0.45, 0.1, 1, 0.3)),
              ("큰 소리 규칙", [
                  "갑자기 큰 소리는 스피커와 귀를 다치게 할 수 있어서 가장 심각한 버그로 다뤄요. 모든 엔진과 fx에 '이보다 커지면 안 된다'는 테스트를 걸고, NaN이나 Inf 같은 깨진 값도 막아요. 평소 소리를 바꾸는 숨은 리미터는 없어요.",
              ]),
              ("The loudness rule", [
                  "A sudden loud sound can hurt speakers and ears, so it counts as the most serious bug. Every engine and fx has a 'never louder than this' test, and broken values like NaN or Inf are blocked. There's no hidden limiter changing the normal sound.",
              ])),
            F("bounce", ("hits", (0, 0, 1, 0.3)),
              ("바운스 = 연주", [
                  "실시간이든 오프라인이든 같은 소리가 나요. 들은 소리와 바운스한 소리가 다르면 버그로 다뤄요.",
              ]),
              ("Bounce = playback", [
                  "Real time or offline, it sounds the same. If a bounce differs from what you heard, that's a bug.",
              ])),
            F("undo", ("settingskeys", (0.5, 0.36, 0.97, 0.58)),
              ("A | B 비교", [
                  "설정 두 벌을 두고 오가며 비교해요.",
              ]),
              ("Compare A | B", [
                  "Two sets of settings to switch between and compare.",
              ])),
            F("help", ("help", (0, 0, 1, 0.62)),
              ("도움말", [
                  "? 키를 켜면 마우스를 올린 곳마다 설명이 떠요.",
              ]),
              ("Help", [
                  "Turn on the ? key and wherever you hover, an explanation pops up.",
              ])),
            F("looks", ("night", (0, 0, 1, 1)),
              ("낮과 밤, 스킨", [
                  "달 키로 낮과 밤을 바꿔요. 엔진을 바꾸면 화면도 그 기계처럼 바뀌고, 늘 버터 색으로 두고 싶으면 설정에서 고정할 수 있어요.",
              ]),
              ("Day, night and skins", [
                  "The moon key switches day and night. Change the engine and the screen changes to look like that machine; to keep it butter-coloured, lock it in the settings.",
              ])),
            F("settings", ("settings", (0, 0.13, 0.5, 0.6)),
              ("언어, 창 크기, 비주얼라이저", [
                  "화면은 한국어와 영어로 볼 수 있고, 창 크기는 75–150 %예요. 머리줄 가운데의 비주얼라이저는 슬라이스가 울릴 때마다 움직이고, 모양은 네 가지예요.",
              ]),
              ("Language, window size, the visualizer", [
                  "The screen comes in Korean and English, and the window from 75 to 150 %. The visualizer in the middle of the header moves with every slice that plays, in four looks.",
              ])),
            F("report", ("report", (0, 0, 1, 1)),
              ("버그 제보", [
                  "오른쪽 아래 '버그 제보'로 무슨 일이 있었는지 보내요. 보내는 내용을 전부 미리 보여주고, 동의해야 익명으로 보내져요. 하루 한 번 새 버전이 있는지만 확인하고, 그 밖의 정보는 보내지 않아요.",
              ]),
              ("Bug report", [
                  "'report a bug' at the bottom right sends what went wrong. Everything that would be sent is shown first, and it goes anonymously only once you agree. Once a day flipper checks whether there's a new version, and sends nothing else.",
              ])),
        ],
    },
]


def feature_count() -> int:
    return sum(len(p["features"]) for p in PARTS)
