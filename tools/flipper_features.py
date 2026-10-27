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
            "ko": "샘플 한 부분을 잘라 새 소리처럼 들리게 하는 것. flipper가 가장 잘하려는 일이에요.",
            "en": "Take one part of a sample and chop it until it sounds new. This is what flipper tries to do best.",
        },
        "features": [
            F("hits", ("hits", TOP),
              ("타격 찾기", [
                  "샘플을 열면 flipper가 소리가 '탁' 하고 시작되는 자리(타격)를 전부 한 번에 찾아 둬요. 새 샘플은 50 %로 바로 잘려서 들어와서, 열자마자 패드로 칠 수 있어요.",
                  "'슬라이스 개수' 노브를 돌리면 다시 분석하지 않고 그 자리에서 다시 잘라요. 올리면 약한 타격까지, 내리면 뚜렷한 타격만 남아요. 1번 슬라이스는 늘 구간 시작에 있고, 너무 많으면 센 타격부터 채워요.",
                  "자르는 곳은 S와 E 사이(작업 구간)예요. 파형 위의 S와 E 탭을 끌어서 쓸 부분만 고르면, 그 안에서만 잘라요.",
              ]),
              ("Hits", [
                  "When a sample opens, flipper finds every place a sound kicks in (a hit) in one go. A new sample comes in already chopped at 50 %, so you can play the pads straight away.",
                  "Turn the slices knob and it re-chops on the spot without analysing again: up for weaker hits too, down for only the clear ones. Slice 1 always sits at the range's start; when there are too many, the strongest hits come first.",
                  "It chops between S and E (the work range). Drag the S and E tabs over the waveform to pick the part you want, and it chops only inside it.",
              ])),
            F("grid", ("grid", TOP),
              ("박자로 자르기", [
                  "'그리드'를 고르면 샘플의 템포에 맞춰 1/16, 1/8, 1/4, 1/2, 한 마디마다 잘라요. 드럼 루프를 정박으로 나누거나, 패드 하나에 한 박씩 놓고 싶을 때예요.",
                  "템포가 없는 샘플은 같은 길이로 나눠요. 스킵한 부분은 다시 잘라도 그대로 남아요.",
              ]),
              ("Beats", [
                  "Pick grid and it chops every 1/16, 1/8, 1/4, 1/2 or bar at the sample's tempo: for a drum loop split on the grid, or one beat per pad.",
                  "A sample without a tempo is cut into equal parts. Skipped parts stay where they are through a re-chop.",
              ])),
            F("lazy", ("lazy", TOP),
              ("레이지 찹", [
                  "'레이지'를 누르면 구간이 재생되고, 듣다가 원하는 순간에 패드든 건반이든 아무거나 치면 그 자리에서 잘려요. 1번 슬라이스는 시작에서 바로 시작하고, 칠 때마다 다음 슬라이스가 시작돼요. 구간이 끝나거나 멈춤을 누르면 끝나요.",
                  "사람은 박보다 조금 일찍 치기도, 늦게 치기도 해요. 그래서 친 순간보다 80 ms 앞부터 60 ms 뒤까지에서 가장 그럴듯한 타격을 찾아 붙여요. 실제 드럼 루프로 시험했을 때 탭의 90–100 %가 제 타격에 붙었어요. 10 ms 안에 두 번 친 건 한 번으로 봐요.",
                  "레이지 찹 한 번이 통째로 되돌리기 한 단계예요. 마음에 안 들면 한 번 되돌리고 다시 치면 돼요.",
              ]),
              ("Lazy chop", [
                  "Press lazy and the range plays; whenever you like, hit any pad or key and it cuts there. Slice 1 starts at the start, and each hit starts the next slice. It ends with the range or when you press stop.",
                  "People tap a little early as often as a little late, so it looks from 80 ms before your tap to 60 ms after for the hit you most likely meant. On real drum loops 90–100 % of taps landed on their hit. Two taps within 10 ms count as one.",
                  "A whole lazy chop is one undo step: don't like it, undo once and tap again.",
              ])),
            F("lit", ("lit", (0, 0.135, 1, 1)),
              ("불 켜진 패드로 치기", [
                  "설정에서 '레이지 찹 치기'를 '불 켜진 패드'로 바꾸면, 다음 슬라이스의 패드에만 불이 들어오고 그 패드를 눌러야 잘려요. 다른 패드와 건반은 아무 일도 하지 않아요.",
                  "아무 키나 치는 대신 옛 기계처럼 패드를 차례로 짚어 가며 자르고 싶을 때예요. 멜로디 모드에서는 어느 건반이든 받아요.",
              ]),
              ("The lit pad", [
                  "Set 'lazy chop taps' to 'the lit pad' in the settings and only the next slice's pad lights up; that pad cuts, other pads and keys do nothing.",
                  "For chopping the old machines' way, pad after pad, instead of any key. Melody mode still takes any key.",
              ])),
            F("dice", ("dice", (0, 0.08, 1, 0.53)),
              ("주사위와 혼돈", [
                  "주사위를 누를 때마다 새 찹이 떨어져요. 주사위가 굴러가고, 새 찹이 놓이면 빛이 패드를 한 번 훑어요. 슬라이스 개수, 잠근 마커, 스킵한 부분은 그대로 두고 나머지만 새로 잘라요.",
                  "주사위를 끌면 혼돈이 0–100 %로 바뀌고, 주사위 눈이 그만큼 늘어요. 눈 하나는 가장 센 타격만 골라 고르게 자르고, 눈 여섯은 아무 데나 잘라요. 50 %를 넘으면 타격이 아닌 자리도 섞이기 시작해요.",
                  "어느 경우든 두 슬라이스가 너무 붙지 않게(고른 슬라이스 길이의 4분의 1, 최대 50 ms) 떨어뜨려요. 한 번 굴린 것은 되돌리기 한 번으로 돌아가요.",
              ]),
              ("The die and its chaos", [
                  "Every press drops a new chop: the die tumbles, the chop lands, and a band of light sweeps the pads. The slice count, locked markers and skipped parts stay; the rest is chopped anew.",
                  "Drag the die to set the chaos, 0–100 %, and its pips follow: one pip keeps to the strongest hits, fairly evenly; six cut anywhere. Past 50 % places that aren't hits creep in.",
                  "Either way no two slices land too close (a quarter of an even slice, at most 50 ms). Each roll is one undo step back.",
              ])),
            F("hand", ("zoomed", TOP),
              ("손으로 다듬기", [
                  "파형을 더블클릭하면 마커가 생기고, 가까운 타격에 붙어요. Alt를 누르면 자석 없이 정확히 그 자리에. 마커를 더블클릭하면 지워지고, 끌어서 옮기고, Shift나 Ctrl(⌘)로 여러 개를 골라 지우기 키로 한꺼번에 지울 수 있어요.",
                  "휠이나 핀치로 마우스 자리를 중심으로 확대하고, Shift + 휠이나 아래 막대로 옆으로 넘겨요. 막대를 더블클릭하면 샘플 전체예요. 확대해 둔 동안은 파형이 재생 자리를 따라가요.",
                  "잠근 마커는 타격 · 그리드 · 레이지 · 주사위로 다시 잘라도 그 자리에 남아요. 꼭 지키고 싶은 자리를 잠가 두고 나머지만 다시 자르는 식으로 써요.",
              ]),
              ("By hand", [
                  "Double-click the waveform for a marker; it snaps to a nearby hit (alt: no magnet, exactly there). Double-click a marker to delete it, drag to move it, shift- or cmd-click to pick several and delete them with the delete key.",
                  "Scroll or pinch zooms around the mouse; shift + scroll or the bar below moves along, and a double-click on the bar shows the whole sample. Zoomed in, the waveform follows the playhead.",
                  "A locked marker stays put through every re-chop (hits, grid, lazy, the die): lock the places you want to keep and re-chop the rest.",
              ])),
            F("skip", ("skip", (0, 0.135, 1, 0.6)),
              ("스킵", [
                  "카운트인, 숨소리, 쓰기 싫은 한 마디처럼 패드에 두고 싶지 않은 부분은 지우지 않고 '스킵'으로 빼 둬요. 빗금으로 보이고, 뒤 슬라이스들이 한 칸씩 당겨져서 패드와 MIDI 음도 따라 움직여요.",
                  "샘플 파일은 손대지 않아서, 언제든 되돌릴 수 있어요. 다시 잘라도 스킵한 부분은 그대로 남고, 그 안에 새 슬라이스가 생기지 않아요. 파형을 오른쪽 클릭해도 같아요.",
              ]),
              ("Skip", [
                  "A count-in, a breath, a bar you don't want: leave it out with skip instead of cutting it out. It shows hatched, the slices after it move up one, and the pads and MIDI notes follow.",
                  "The sample file is never touched, so it can come back any time. Re-chops leave skipped parts as they are, and no new slice lands inside one. A right-click on the waveform does the same.",
              ])),
            F("trims", ("trims", (0, 0.135, 1, 0.6)),
              ("시작과 끝", [
                  "슬라이스마다 시작과 끝을 샘플 단위로 밀고 당겨요. 끌거나 휠로, Shift를 누르면 한 샘플씩, 숫자를 누르면 직접 쳐 넣어요.",
                  "끝을 당기면 꼬리가 잘리고 빗금으로 보여요. 밀면 다음 마커를 넘어 이어서 울려요. 다음 슬라이스는 그대로예요. 설정의 '슬라이스 끝'을 '다음 슬라이스와 붙이기'로 바꾸면 다음 슬라이스의 시작도 같이 움직여요.",
                  "자석을 켜면 가까운 0 교차점에 붙어서 '틱' 소리가 나지 않아요. 여러 슬라이스를 골라 한꺼번에 같은 만큼 옮길 수도 있어요.",
              ]),
              ("Start and end", [
                  "Push and pull each slice's start and end, in samples: drag or scroll, shift for one sample a step, click the number to type it.",
                  "Pull the end in and the tail is trimmed, shown hatched; push it out and the slice plays on past the next marker. The next slice stays where it is; set 'slice end' to 'link to next slice' in the settings and it moves the next slice's start too.",
                  "With the magnet on, they land on a nearby zero crossing, so no clicks. Pick several slices to move them all by the same amount.",
              ])),
            F("slice", ("edit", (0, 0.135, 1, 0.62)),
              ("슬라이스마다 다섯 가지", [
                  "최대 64슬라이스. 슬라이스마다 설정은 음높이(반음, Shift로 센트), 리버스, 볼륨, 페이드 인, 페이드 아웃 다섯 개뿐이에요. 샘플러이지 신시사이저가 아니라서, 필요한 것만 남겼어요.",
                  "페이드는 0 ms에서 시작해요. 들어 보고 이상할 때만 만지는 값이라서요. 대신 모든 소리의 시작과 끝에 0.1 ms 가장자리를 둬서, 파형 중간을 잘라도 클릭이 나지 않아요.",
                  "'전체'를 누르면 노브가 모든 슬라이스를 한꺼번에 바꿔요. 패드를 Shift로 누르면 범위, Ctrl(⌘)로 누르면 하나씩 더 골라서 그 슬라이스들만 같이 바꿔요. 노브 하나, 끌기 하나가 되돌리기 한 단계예요.",
              ]),
              ("Five settings per slice", [
                  "Up to 64 slices, each with five settings and nothing more: pitch (semitones, shift for cents), reverse, level, fade in and fade out. It's a sampler, not a synth, so only what's needed stayed.",
                  "Fades start at 0 ms, because you touch them only when something sounds wrong. Instead every sound starts and ends on a 0.1 ms edge, so cutting mid-wave never clicks.",
                  "Press 'all' and the knobs change every slice at once. Shift-click pads for a range, cmd-click for one more, and only those change together. Every knob turn or drag is one undo step.",
              ])),
            F("truncate", ("hits", (0, 0.09, 1, 0.53)),
              ("잘라내기", [
                  "자르기 줄의 가위 키는 S부터 E까지만 남기고 샘플의 나머지를 잘라 내요. 긴 곡에서 네 마디만 쓸 때, 프로젝트와 플립 파일이 그만큼 가벼워져요.",
                  "원래 파일은 그대로이고, 되돌리기로 언제든 돌아와요.",
              ]),
              ("Truncate", [
                  "The scissors key in the chop row keeps only S to E and cuts the rest of the sample away. Using four bars of a long song, the project and the flip get that much lighter.",
                  "The file itself stays as it is, and undo brings it back.",
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
              ("리피치", [
                  "옛 샘플러처럼 읽는 속도만 바꿔요. 키를 내리면 느려지고 어두워지고, 올리면 빨라지고 밝아져요. 소리를 늘이지 않아서 디지털 잡음이 생기지 않아요. 새 샘플은 리피치로 시작해요.",
                  "clean 엔진은 속도에 맞춰 걸러 내는 주파수가 같이 움직이는 sinc 보간으로 읽어요. 한 옥타브 올려도 접혀 들어오는 잡음이 −85 dB예요.",
                  "grey, black, purple은 그 기계가 읽던 방식 그대로(샘플을 건너뛰고 되풀이하는 등) 일부러 거칠게 읽어요. 엔진 이야기는 아래 '엔진' 칸에 있어요.",
              ]),
              ("Repitch", [
                  "Like an old sampler, only the reading speed changes: pitch it down and it slows down and darkens, up and it speeds up and brightens. Nothing is stretched, so there are no digital artefacts. A new sample starts in repitch.",
                  "clean reads through a sinc interpolator whose cutoff follows the speed: an octave up, what folds back sits at −85 dB.",
                  "grey, black and purple read the way their machine did (skipping and repeating samples and so on), rough on purpose. The engines have their own section below.",
              ])),
            F("keep", ("keep", TOP_ROW),
              ("템포 유지", [
                  "길이와 높이를 따로 움직여요. 템포는 그대로 두고 키만, 또는 키는 그대로 두고 템포만 바꿔요.",
                  "늘이는 데는 두 가지를 써요. Rubber Band R3는 음높이 오차 0센트, 타격 앞에 번지는 소리가 −26 ~ −37 dB로 가장 깨끗하지만 무거워요. Signalsmith Stretch는 오차 5센트 안이고 실시간의 약 50배로 빨라요.",
                  "직접 들어 보고 정했어요. 키만 바꿀 땐 둘이 비슷했고, 템포만 바꿀 땐 R3가 확실히 자연스러웠어요. 그래서 들리는 소리는 R3로 만들어요.",
              ]),
              ("Keep tempo", [
                  "Length and pitch move apart: keep the tempo and move the key, or keep the key and move the tempo.",
                  "Two stretchers do it. Rubber Band R3: 0 cents pitch error, pre-echo on hits at −26 to −37 dB, the cleanest but heavy. Signalsmith Stretch: within 5 cents, about 50× real time.",
                  "We picked by ear: on key-only changes the two sounded close, on tempo-only changes R3 was clearly more natural. So what you hear is made with R3.",
              ])),
            F("bake", ("settings", (0.5, 0.13, 0.97, 0.6)),
              ("미리 굽기", [
                  "키나 속도를 바꾸면 뒤에서 R3로 구워 두고(4초짜리 찹이 약 0.5초), 다음에 칠 때부터 구운 소리를 읽어요. 굽기 전과 노브를 돌리는 동안은 Signalsmith가 바로 들려줘요.",
                  "64슬라이스를 하나씩 굽지 않고 자른 구간 전체를 한 번 구워요. 그래서 마커를 옮겨도 다시 구울 필요가 없어요. 음높이를 따로 바꾼 슬라이스만 따로 구워요. 바운스도 같은 구운 소리를 읽어서, 들은 그대로 나가요.",
                  "속도와 키가 테이프처럼 같이 움직이면 늘일 게 없으니 리피치 길로 읽어서 더 가벼워요. 컴퓨터가 버거우면 설정의 '고품질 타임 스트레치'를 끄면 돼요. 끄면 Signalsmith로 구워서 더 가볍고 빨라요.",
              ]),
              ("Baked ahead", [
                  "Change the key or speed and R3 bakes it in the background (a 4 s chop in about 0.5 s); the next hit plays the bake. Before that, and while a knob turns, Signalsmith plays at once.",
                  "Not 64 bakes for 64 slices: the whole chopped range bakes once, so moving markers needs no new bake. Only slices with their own pitch bake apart. The bounce reads the same bake, so it sounds as heard.",
                  "When speed and key move together like tape there is nothing to stretch, so it reads the repitch way, lighter. If the computer struggles, turn 'high-quality time stretch' off in the settings: it bakes with Signalsmith, lighter and faster.",
              ])),
            F("crisp", ("hits", (0.55, 0, 1, 0.42)),
              ("또렷하게", [
                  "템포 유지로 늘릴 때, 타격과 타격 사이를 따로따로 늘리고 타격의 앞부분은 원래 소리를 그대로 남겨요. 드럼이 흐물흐물해지지 않아요.",
                  "비트와 드럼 루프엔 켜고, 멜로디, 화음, 목소리엔 꺼 두세요.",
              ]),
              ("Crisp", [
                  "When keep tempo stretches, it stretches between the hits, each on its own, and keeps every hit's attack as it was. Drums don't go soft.",
                  "Turn it on for beats and drum loops, leave it off for melodies, chords and voices.",
              ])),
            F("keyknob", ("typing", (0.3, 0, 0.85, 0.3)),
              ("키와 속도 노브", [
                  "키는 반음씩 끌고, Shift를 누르고 끌면 센트예요. 더블클릭하면 0으로 돌아가고, 숫자를 누르면 '−3 20'처럼 반음과 센트를 바로 쳐 넣어요.",
                  "속도는 ×0.750처럼 배속으로 보여요. 리피치에서는 키와 속도가 같이 움직이고, 템포 유지에서는 따로 움직여요.",
              ]),
              ("The key and speed knobs", [
                  "Drag the key by semitones, shift + drag for cents. A double-click takes it back to 0; click the number and type semitones and cents at once, like '-3 20'.",
                  "Speed reads as a factor, like ×0.750. In repitch key and speed move together; in keep tempo they move apart.",
              ])),
            F("tempo", ("dawtempo", (0.3, 0, 1, 0.36)),
              ("샘플의 템포", [
                  "샘플이 원래 몇 BPM인지, 파일 이름과 길이로 먼저 짐작해요. 'dusty keys loop 90 bpm'이면 90 BPM, 길이로는 '2마디면 90 BPM, 4마디면 180 BPM'처럼 맞는 템포를 찾아요.",
                  "BPM을 누르면 이 후보들이 나와서 하나를 고르거나, 직접 쳐 넣어요. '템포 없음'은 원샷이에요.",
              ]),
              ("The sample's tempo", [
                  "flipper first guesses the sample's own BPM from its file name and length: 'dusty keys loop 90 bpm' is 90 BPM, and the length gives tempos that fit, like '90 BPM if it's 2 bars, 180 if it's 4'.",
                  "Click the BPM to pick one of these guesses, or type it. 'no tempo' makes it a one-shot.",
              ])),
            F("calc", None,
              ("템포 계산", [
                  "키를 내리면 템포가 몇이 되는지, 원하는 템포가 되려면 키를 얼마나 내리면 되는지. 리피치에선 이게 늘 같이 움직여서, 미리 알아 두면 편해요. 위 계산기를 직접 움직여 보세요.",
                  "플러그인 안에서는 BPM 칸에 원하는 템포를 치면 키가 그 템포에 맞춰 움직여요. 'DAW 템포'를 켜면 지금 곡의 템포에 맞춰요. 리피치에선 키를, 템포 유지에선 속도를 맞춰요.",
              ]),
              ("Tempo maths", [
                  "Pitch it down and the tempo changes with it; to land on a tempo you want, how far down? In repitch these always move together, so it helps to know. Try the calculator above.",
                  "In the plug-in, type the tempo you want into the BPM field and the key moves to land on it. Turn 'DAW tempo' on and it follows the song's tempo: the key in repitch, the speed in keep tempo.",
              ]), tool="tempo"),
            F("kind", ("kind", TOP_ROW),
              ("루프와 원샷", [
                  "샘플마다 루프인지 원샷인지 정해요. 루프는 템포가 있고 DAW 템포를 따라갈 수 있어요. 원샷은 템포가 없어요.",
                  "파일 이름과 길이로 먼저 짐작하고, 틀리면 바로 바꿀 수 있어요.",
              ]),
              ("Loop or one-shot", [
                  "Each sample is a loop or a one-shot. A loop has a tempo and can follow the DAW's; a one-shot has none.",
                  "The first guess comes from the file name and length, and you can change it right away.",
              ])),
            F("keychip", ("keyhelp", (0.3, 0, 1, 0.32)),
              ("키 찾기", [
                  "S부터 E까지의 키를 찾아서 '원래 키 → 지금 들리는 키'로 보여줘요. 예를 들어 Am → Gm이면, 원래 A 마이너인 샘플이 키 노브 때문에 G 마이너로 들린다는 뜻이에요.",
                  "옛 레코드는 표준 튜닝(A = 440 Hz)에서 조금 어긋나 있곤 해요. 그래서 몇 센트 어긋났는지도 같이 보여줘요. 다른 악기와 맞출 때 그만큼 센트를 돌리면 돼요.",
              ]),
              ("Key detection", [
                  "flipper finds the key from S to E and shows it as 'as recorded → as it sounds': Am → Gm means a sample in A minor sounds in G minor with the key knob.",
                  "Old records often sit a little off standard tuning (A = 440 Hz), so it shows how many cents too. Turn the cents by that much to sit with other instruments.",
              ])),
            F("keymenu", ("keymenu", (0.45, 0.05, 1, 0.55)),
              ("다른 후보와 다시 찾기", [
                  "키 칩을 누르면 다른 후보들이 나와요. 장조와 단조처럼 헷갈리기 쉬운 키를 바로 바꿔 볼 수 있어요.",
                  "구간을 옮겼다면 '다시 감지하기'로 새 구간의 키를 찾아요.",
              ]),
              ("Other guesses", [
                  "Click the key chip for the other guesses, so keys that are easy to mix up, like a major and its relative minor, are one click away.",
                  "Moved the range? 'detect again' finds the key of the new one.",
              ])),
            F("keyhand", ("keyhand", (0.45, 0.05, 1, 0.95)),
              ("키 직접 고르기", [
                  "알고 있는 키가 있으면 '직접 고르기'에서 메이저 12개, 마이너 12개 중에 골라요. 직접 고른 키는 다시 감지해도 바뀌지 않아요.",
              ]),
              ("Set the key by hand", [
                  "If you know the key, 'set by hand' lists the 12 major and 12 minor keys. A key set by hand stays through every new detection.",
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
                  "한 페이지에 패드 16개(8 × 2)나 32개(8 × 4). 페이지를 넘기면 64슬라이스까지 쳐요. 패드 1번이 C3이고, 패드마다 음 이름이 적혀 있어요.",
                  "패드를 누르면 소리가 나고 그 슬라이스가 골라져요. Shift나 Ctrl(⌘)로 누르면 소리 없이 여러 개를 골라 한꺼번에 바꿔요.",
              ]),
              ("Pads", [
                  "16 pads (8 × 2) or 32 (8 × 4) on a page, with pages up to 64 slices. Pad 1 is C3, and each pad shows its note.",
                  "Click a pad and it plays and picks its slice. Shift- or cmd-click picks several without a sound, to change them together.",
              ])),
            F("pages", ("pages", PADS),
              ("페이지", [
                  "슬라이스가 한 페이지보다 많으면 페이지 키로 다음 패드들을 봐요. 화면만 넘어가고, MIDI 음은 언제나 같은 슬라이스를 쳐요.",
              ]),
              ("Pages", [
                  "With more slices than a page holds, the pages key shows the next pads. Only the screen turns: a MIDI note always plays the same slice.",
              ])),
            F("voices", ("voices", PADS),
              ("모노와 폴리", [
                  "모노가 기본이에요. 새 패드가 앞 소리를 5 ms 만에 끊어요. 덱 하나로 찹을 연주하듯이, 소리가 쌓여 뭉개지지 않아요.",
                  "폴리는 소리가 겹쳐요. 멜로디 모드에서 화음을 칠 때 써요.",
              ]),
              ("Mono and poly", [
                  "Mono is the default: a new pad cuts the last sound in 5 ms, like a chop played on one deck, so sounds never pile up into mud.",
                  "Poly lets them ring over each other, for chords in melody mode.",
              ])),
            F("padplays", ("padplays", PADS),
              ("누르는 동안과 슬라이스 전체", [
                  "'누르는 동안'은 누른 만큼만 울리고, 놓으면 멈춰요. 오래 눌러도 슬라이스 끝에서 멈춰요.",
                  "'슬라이스 전체'는 한 번 치면 다음 마커까지 끝까지 울려요. 짧게 톡 쳐도 슬라이스 하나가 다 나와요.",
              ]),
              ("While held and whole slice", [
                  "While held sounds as long as you hold it and stops when you let go, and at the slice's end even if you keep holding.",
                  "Whole slice plays through to the next marker from one hit, however short the tap.",
              ])),
            F("playas", ("playas", PADS),
              ("연주 방법", [
                  "패드는 슬라이스 하나에 패드 하나. 멜로디는 슬라이스 하나를 건반 전체에 깔아요. 스크래치는 패드마다 자기 슬라이스를 판에 올려 긁어요. fx 건반은 패드 1번 자리부터의 음이 fx 패드 16개를 쳐요.",
                  "키스위치: 가장 낮은 음들(기본 C-2부터 넷)이 연주 방법을 바꿔요. 소리는 내지 않아서, DAW 클립 안에서 곡 중간에 패드와 멜로디를 오갈 수 있어요.",
              ]),
              ("Play as", [
                  "Pads: one slice per pad. Melody: one slice across the keyboard. Scratch: each pad puts its slice on the record and scratches it. fx keys: the notes from pad 1's play the 16 fx pads.",
                  "Keyswitches: the lowest four notes (from C-2 by default) switch between them and play nothing, so a DAW clip can switch from pads to melody mid-song.",
              ])),
            F("melody", ("melody", PADS),
              ("멜로디", [
                  "슬라이스 하나를 건반에 깔아서 음을 연주해요. 반음씩, 또는 메이저, 마이너, 하모닉 마이너, 메이저 펜타토닉, 마이너 펜타토닉, 도리안, 프리지안, 믹솔리디안으로.",
                  "화면 건반은 MIDI 음 128개 전부예요. 건반을 따라 끌면 음이 이어지고, 휠로 넘기고, Ctrl(⌘) + 휠이나 핀치로 확대해요. 누르면 진짜 MIDI 음을 보내요. 서스테인 페달도 받아요.",
              ]),
              ("Melody", [
                  "One slice across the keys, played as notes: by semitone, or major, minor, harmonic minor, major and minor pentatonic, dorian, phrygian or mixolydian.",
                  "The screen keyboard holds all 128 MIDI notes. Drag along it for a run, scroll to move, cmd + scroll or pinch to zoom; a click sends the real note. The sustain pedal works too.",
              ])),
            F("scale", ("scale", (0, 0, 0.6, 1)),
              ("스케일과 흰 건반", [
                  "스케일을 고르면 건반에 그 스케일의 음만 놓여요. '흰 건반'을 고르면 어느 스케일이든 C 메이저처럼 흰 건반으로 쳐요. 음악 이론을 몰라도 틀린 음이 나지 않아요.",
                  "패드 컨트롤러처럼 흰 건반 검은 건반이 따로 없는 기기엔 '모든 건반'을 고르면, 건반 하나하나에 스케일의 다음 음이 차례로 놓여요.",
              ]),
              ("Scales and white keys", [
                  "Pick a scale and only its notes are on the keys; with 'white keys' every scale plays like C major on the white keys. No theory needed, no wrong notes.",
                  "For a pad controller with no black and white keys, 'every key' puts the scale's next note on each key in turn.",
              ])),
            F("root", ("root", PADS),
              ("원키 옮기기", [
                  "원래 높이로 소리 나는 건반(원키)은 C3에 묶여 있지 않아요. ‹ ›로 옮기거나, 건반을 오른쪽 클릭하면 그 건반이 원키가 돼요.",
                  "건반을 확대하면 원키 둘레가 크게 보여서, 마우스로 치기 편해요.",
              ]),
              ("Move the root", [
                  "The key that plays the slice at its own pitch (the root) isn't stuck on C3: move it with ‹ ›, or right-click a key to make it the root.",
                  "Zoom the keyboard and the keys around the root get big enough to play with the mouse.",
              ])),
            F("colours", ("colours", (0, 0, 1, 1)),
              ("패드 색", [
                  "기본은 '소리 따라'예요. 슬라이스마다 소리가 밝을수록 밝은 색, 어두울수록 짙은 색으로 칠해서, 보기만 해도 하이햇과 킥이 갈려요. 연못도 같은 색으로 움직여요.",
                  "'16색'은 패드마다 정해진 16가지 색이에요. 설정에서 바꿔요.",
              ]),
              ("Pad colours", [
                  "'by sound' is the default: the brighter a slice sounds, the brighter its colour, so hats and kicks tell apart at a glance. The pond moves in the same colours.",
                  "'16 colours' gives each pad one of 16 fixed colours. Change it in the settings.",
              ])),
            F("velocity", ("settings", (0.5, 0.13, 0.97, 0.36)),
              ("벨로시티", [
                  "패드를 얼마나 세게 쳤는지를 소리 크기로 어떻게 바꿀지 골라요. '그대로'가 기본이에요.",
                  "'부드럽게'는 살살 쳐도 크게, '세게'는 세게 쳐야 크게, '늘 같게'는 어떻게 쳐도 같은 크기예요. 패드 컨트롤러마다 손맛이 달라서 넣었어요.",
              ]),
              ("Velocity", [
                  "How hard you hit becomes how loud it plays; 'as played' is the default.",
                  "'soft' makes light hits louder, 'hard' saves loud for hard hits, 'always full' plays every hit the same. Pad controllers all feel different, so it's a choice.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- sample
    {
        "key": "sample",
        "title": {"ko": "샘플 담기", "en": "Bring a sample in"},
        "lead": {
            "ko": "파일을 끌어 놓거나, DAW의 소리를 바로 녹음해서 샘플로 써요.",
            "en": "Drop a file, or record the DAW's sound straight in as a sample.",
        },
        "features": [
            F("start", ("start", (0.15, 0.05, 0.85, 0.75)),
              ("빈 화면의 두 카드", [
                  "처음 열면 가운데에 카드 두 장이 있어요. '찹할 샘플을 여기에 끌어다 놓으세요'에 파일을 놓으면 샘플러로, '드럼 킷 만들기'에 원샷을 놓으면 드럼 화면의 1번 셀부터 채워요.",
                  "WAV, AIFF, FLAC, MP3, OGG, Opus 같은 파일을 열고, 어느 나라 말의 파일 이름이든 열려요. DAW의 오디오 클립을 바로 끌어 놓아도 돼요.",
              ]),
              ("Two cards to start", [
                  "Opened empty, flipper shows two cards: drop a file on 'drop a sample to chop' for the sampler, or one-shots on 'make a drum kit' to fill the drum cells from 1.",
                  "It opens WAV, AIFF, FLAC, MP3, OGG, Opus and more, with file names in any language, and takes audio clips dragged straight from the DAW.",
              ])),
            F("take", ("take", (0.4, 0, 1, 0.4)),
              ("녹음하기", [
                  "샘플 줄의 빨간 점 키를 누르면 녹음 창이 열려요. 다른 트랙의 소리(사이드체인 입력)나 flipper가 지금 내는 소리(fx 랙 뒤, 리샘플)를 새 샘플로 받아요.",
                  "바로, 또는 다음 마디 첫 박부터 시작하고, 멈출 때까지 또는 1 · 2 · 4 · 8마디(DAW 템포 기준)만큼 담아요. 한 번에 최대 2분이고, 파일은 음악/flipper/recorded에 24비트 WAV로 남아요.",
                  "리샘플은 녹음이 끝난 뒤에야 샘플이 바뀌어서, 자기 소리를 다시 듣는 일이 없어요. 바운스(오프라인 렌더) 중에는 녹음하지 않아요.",
              ]),
              ("Record", [
                  "The red dot in the sample row opens the take panel: another track's sound (the side-chain input) or flipper's own output (after the fx rack: a resample) becomes the new sample.",
                  "Start now or on the next bar's first beat; record until you stop, or 1, 2, 4 or 8 bars at the DAW's tempo. Up to 2 minutes a take, kept as 24-bit WAV in Music/flipper/recorded.",
                  "A resample swaps the sample only after it ends, so flipper never hears itself. Nothing records during an offline bounce.",
              ])),
            F("channels", ("@feature_channels", None),
              ("채널 고르기", [
                  "스테레오 샘플에서 어느 채널을 쓸지 골라요. 스테레오, 왼쪽, 오른쪽, 가운데, 양옆. 가운데는 (L+R)/2, 양옆은 (L−R)/2라서 원래보다 커지지 않아요.",
                  "'oo' 키를 누르면 파형이 왼쪽과 오른쪽 두 줄로 나뉘어 보여요. 한쪽에만 있는 소리, 가운데의 보컬 같은 걸 눈으로 찾고 골라요. 왼쪽, 오른쪽, 가운데, 양옆을 고르면 모노로 나가요.",
              ]),
              ("Channel select", [
                  "Pick which channels of a stereo sample to use: stereo, left, right, mid or side. Mid is (L+R)/2 and side (L−R)/2, so never louder than the source.",
                  "The 'oo' key splits the waveform into left and right, to see a sound on one side or a voice in the middle before you pick. Left, right, mid and side play in mono.",
              ])),
            F("gain", ("hits", (0, 0.53, 0.62, 0.66)),
              ("샘플 게인과 노멀라이즈", [
                  "샘플 게인은 샘플 하나 전체의 크기예요. 엔진 뒤, fx 앞에 있어서 모든 패드와 판에 같이 걸려요. 더블클릭하면 0 dB.",
                  "노멀라이즈는 S부터 E까지의 가장 큰 자리가 0 dBFS가 되게 게인을 맞춰요. 파일은 바꾸지 않고, 되돌리기로 돌아와요. 드럼 셀은 셀마다 따로 있어요.",
              ]),
              ("Sample gain and normalize", [
                  "Sample gain is the whole sample's level, after the engine and before the fx, so it reaches every pad and the record. Double-click for 0 dB.",
                  "Normalize sets the gain so the loudest point from S to E reaches 0 dBFS. The file isn't changed, and undo brings it back. Drum cells have their own.",
              ])),
            F("flips", ("flips", (0, 0, 0.6, 0.55)),
              ("플립 파일", [
                  "샘플, 찹, 설정을 .flip 파일 하나에 담아요. 플립 이름 옆 ‹ ›로 폴더 안의 플립을 차례로 넘기고, 이름을 누르면 저장, 새 이름으로 저장, 열기, 이름 바꾸기, 삭제, 폴더 열기가 있어요.",
                  "바뀐 게 있으면 이름 옆에 표시가 붙어요. 예전 판에서 만든 플립도 같은 소리로 열려요. 다른 프로젝트에서 같은 찹을 쓸 때 편해요.",
              ]),
              ("Flip files", [
                  "The sample, the chop and the settings go into one .flip file. ‹ › by the flip's name steps through the folder's flips; the name opens save, save as, open, rename, delete and the folder.",
                  "A mark by the name shows unsaved changes. Flips from older versions open sounding the same, handy for taking a chop to another project.",
              ])),
            F("standalone", ("standalone", (0, 0, 1, 0.3)),
              ("단독 앱", [
                  "DAW 없이 flipper 하나만 여는 앱도 있어요. DAW가 템포를 알려주지 않으니, 머리줄에 템포 칸이 따로 생겨요.",
                  "MIDI 컨트롤러를 꽂아 패드를 치고, 샘플을 잘라 보고, 플립으로 저장해 두었다가 DAW에서 그대로 열 수 있어요.",
              ]),
              ("The standalone app", [
                  "There's an app that runs flipper on its own, no DAW. With no DAW to tell the tempo, the header gets a tempo field of its own.",
                  "Plug in a MIDI controller, chop and play, save a flip, and open it as it is in the DAW later.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- rack
    {
        "key": "rack",
        "title": {"ko": "fx 랙", "en": "fx rack"},
        "lead": {
            "ko": "fx 화면 위의 열 칸이 소리 순서대로 이어져요. 처음엔 다 꺼져 있고, 노브를 올리면 켜져요. 0인 칸은 CPU를 쓰지 않아요.",
            "en": "The ten slots on the fx screen run in the order the sound goes. All off at first; turn a knob up and it comes on. A slot at 0 costs no CPU.",
        },
        "features": [
            F("slot_filter", ("slot_filter", RACK),
              ("필터", [
                  "직접 만든 필터예요. 노브를 올리면 LP는 어둡게, HP는 얇게, BP는 좁게. 끝까지 내리면 열려서 꺼진 것과 같아요.",
                  "12 dB나 24 dB, 레조넌스. '클린'은 정확하게, '래더'는 옛 신시사이저 필터처럼 둥글고 따뜻하게. '맨 앞'은 다른 칸보다 먼저, '끝'은 모든 칸 뒤라서 에코와 스페이스까지 걸러요.",
              ]),
              ("Filter", [
                  "Our own filter. Turn it up and LP gets darker, HP thinner, BP narrower; all the way down it's open, the same as off.",
                  "12 or 24 dB, with resonance. 'clean' is exact, 'ladder' rounder and warmer like an old synth's filter. 'first' runs before the other slots; 'end' after them all, so the echo and space are filtered too.",
              ])),
            F("slot_punch", ("slot_punch", RACK),
              ("펀치", [
                  "노브 하나짜리 컴프레서예요. 큰 소리와 작은 소리를 모아서 타격이 앞으로 나와요. 직접 만들었어요.",
                  "'피드백'은 눌린 소리를 다시 듣고 또 눌러서 타격의 모양이 바뀌는, 더 음악적인 쪽이에요. '클래식'은 깨끗하고 정확해요. 스냅은 타격이 얼마나 튀어나올지예요.",
              ]),
              ("Punch", [
                  "A one-knob compressor of our own: it pulls the loud and the quiet together, so the hits come forward.",
                  "'feedback' listens to the squeezed sound and squeezes again, so the hits change shape: the more musical one. 'classic' is clean and exact. Snap is how much the hits jump out.",
              ])),
            F("slot_distort", ("slot_distort", RACK),
              ("디스토션", [
                  "다섯 가지예요. 소프트는 둥글게 소리를 앞으로, 튜브는 달고 두껍게, 퍼즈는 거의 네모로(직접 만들었어요), 클립은 꼭대기를 잘라 단단하고 큰 드럼으로, 폴드는 접어서 금속처럼.",
                  "톤, 포커스(어느 대역을 찌그러뜨릴지), 믹스, 흔들림. 2배 오버샘플로 돌아서 높은 음에서 지저분한 잡음이 덜 생겨요.",
              ]),
              ("Distort", [
                  "Five kinds: soft (round, brings the sound forward), tube (sweet and thick), fuzz (nearly square, our own), clip (cuts the peaks: hard, loud drums) and fold (folds them back: metallic).",
                  "Tone, focus (which band gets the grit), mix and flux. It runs 2× oversampled, so the top stays cleaner.",
              ])),
            F("slot_crush", ("slot_crush", RACK),
              ("크러시", [
                  "샘플레이트를 낮추고 비트를 깎아서, 옛 샘플러의 바삭한 소리를 내요.",
                  "레이트와 비트(예: 8비트), '스텝'은 계단처럼 거칠게, '부드럽게'는 계단 사이를 부드럽게. 믹스와 흔들림.",
              ]),
              ("Crush", [
                  "Fewer samples and fewer bits: the crunchy sound of old samplers.",
                  "Rate and bits (8 bits, say); 'steps' are hard and gritty, 'smooth' softer between them. Mix and flux.",
              ])),
            F("slot_tape", ("slot_tape", RACK),
              ("테이프", [
                  "테이프를 얼마나 세게 몰지, 노브 하나예요. 저음은 부풀고, 고음은 눌리고, 위에 부드러운 클립이 걸려요.",
                  "'흔들림'은 테이프를 살아 있게 하는 작은 변화예요. DAW의 박을 따라 움직여서, 바운스해도 들은 그대로 나와요.",
              ]),
              ("Tape", [
                  "One knob for how hard the tape is driven: the lows swell, the highs squeeze, a soft clip on top.",
                  "Flux is the small changes that keep tape alive. It follows the DAW's beat, so a bounce sounds the way you heard it.",
              ])),
            F("slot_chorus", ("slot_chorus", RACK),
              ("코러스", [
                  "소리를 몇 겹 복사해서 천천히 움직여요. 넓고 따뜻해져요.",
                  "속도, 폭, 믹스. 랙의 다른 칸들처럼 노브가 0이면 꺼져요.",
              ]),
              ("Chorus", [
                  "A few copies of the sound, slowly moving: wider and warmer.",
                  "Speed, range and mix. Like every slot, at 0 it's off.",
              ])),
            F("slot_noise", ("slot_noise", RACK),
              ("노이즈", [
                  "더스트(테이프 먼지), 히스(부드러운 쉬익), 크래클(판의 지글거림)을 소리 밑에 깔아요.",
                  "샘플이 울리는 동안만 나고, 멈추면 0.15초 안에 사라져요. 슬라이스 사이 조용한 곳에 잡음이 남지 않아요. 톤과 흔들림.",
              ]),
              ("Noise", [
                  "Dust (tape dust), hiss (a soft hiss) or crackle (a record's crackle) under the sound.",
                  "Only while a sample plays: gone 0.15 s after it stops, so the quiet between slices stays quiet. Tone and flux.",
              ])),
            F("slot_echo", ("slot_echo", RACK),
              ("에코", [
                  "세 가지예요. 테이프는 따뜻하게 닳아 가는 반복, 디지털은 깨끗하게(핑퐁을 켜면 왼쪽 오른쪽 번갈아), 그레인은 작게 부서진 조각으로 반복해요.",
                  "시간은 '싱크'면 박자(1/16부터 한 마디, 점음표 · 셋잇단), 'ms'면 템포와 상관없이 1–2000 ms. 반복 횟수, 톤. 그레인은 조각마다 음높이를 바꾸고(+12면 한 옥타브 위), 거꾸로 돌릴 수도 있어요.",
              ]),
              ("Echo", [
                  "Three kinds: tape (warm repeats that wear away), digital (clean; ping-pong sends them left and right in turn) and grain (repeats in small broken pieces).",
                  "Time in beats with sync (1/16 to a bar, dotted and triplet), or 1–2000 ms whatever the tempo. Repeats and tone. Grain can pitch each grain (+12: an octave up) and play it backwards.",
              ])),
            F("slot_space", ("slot_space", RACK),
              ("스페이스", [
                  "소리 둘레의 공간이에요. 룸(작은 나무 방), 홀(크고 밝은 홀), 갤럭시(아주 넓고 떠 있는), 라이트(가볍고 산뜻한), 타이니(아주 작은 공간).",
                  "디케이, 프리딜레이, 스테레오, 흔들림.",
              ]),
              ("Space", [
                  "A space around the sound: room (a small wooden room), hall (a big bright hall), galaxy (huge and floating), light (light and airy), tiny (a tiny space).",
                  "Decay, pre-delay, stereo and flux.",
              ])),
            F("slot_all", ("slot_all", RACK),
              ("마스터", [
                  "모든 칸이 마지막에 지나는 곳이에요. 노브는 랙 소리를 얼마나 들을지(0 %면 들어온 소리 그대로), 램프는 랙 전체를 켜고 꺼요. 칸들은 자기 램프를 그대로 가지고 있어요.",
                  "입력(밀어 넣는 양), 너비, 톤, 그리고 리미터. '세이프'는 −0.3 dBFS를 넘을 것만 잡고, '빈티지'는 큰 부분을 눌러 둥글게 만들어요. 입력을 올리면 더 눌려요.",
              ]),
              ("Master", [
                  "Where every slot ends up. Its knob is how much of the rack you hear (0 %: the sound as it went in); its lamp turns the whole rack on and off, while the slots keep their own lamps.",
                  "Input (how hard it's pushed), width, tone, and the limiter: 'safe' catches only what would go over −0.3 dBFS, 'vintage' squeezes the loud parts and rounds them off; push the input for more.",
              ])),
            F("fxpads", ("fxpads", (0.35, 0.38, 1, 1)),
              ("fx 패드", [
                  "누르고 있는 동안 소리를 바꾸는 패드예요. 청록은 테이프(멈춤, 되감기, 반속도, 리버스), 보라는 에코와 크러시, 초록은 스크래치 패턴(처프, 베이비). 여러 개를 같이 눌러도 되고, 테이프는 마지막에 누른 것이 이겨요.",
                  "'누르는 동안'과 '켜 두기'(한 번 눌러 켜고, 다시 눌러 끄기). 시작은 바로, 다음 1/16, 다음 박 중에서 골라요. 박에 맞춰 들어가서 바운스해도 들은 그대로예요.",
              ]),
              ("fx pads", [
                  "Pads that change the sound while held: teal for the tape (stop, back, half, reverse), violet for echo and crush, green for the scratch patterns (chirp, baby). Hold several at once; the last tape move wins.",
                  "'while held' or 'latch' (one press on, the next off). They start now, on the next 1/16 or the next beat, so they land in time and the bounce sounds as heard.",
              ])),
            F("strips", ("strips", (0, 0.38, 0.72, 1)),
              ("반복과 필터 스트립", [
                  "반복 스트립은 손가락이 있는 자리의 길이로 소리를 되풀이해요. 왼쪽 끝이 한 마디, 오른쪽 끝이 1/64. 누른 채 밀면 바로 길이가 바뀌고, 놓으면 계속 재생돼요. 셋잇단을 켜면 1/8T처럼 셋으로 나눠요.",
                  "필터 스트립은 가운데가 열려 있고, 왼쪽으로 가면 로우패스, 오른쪽으로 가면 하이패스가 닫혀요. 놓으면 다시 열려요. 둘 다 DAW 오토메이션과 MIDI 지정이 돼요.",
              ]),
              ("The repeat and filter strips", [
                  "The repeat strip repeats the sound at the step under your finger, a bar at the left end to 1/64 at the right. Slide while holding to change the step at once; let go and it plays on. Triplets split the steps in threes (1/8T).",
                  "The filter strip is open in the middle: to the left a low-pass closes, to the right a high-pass. Let go and it opens again. Both can be automated and MIDI-learned.",
              ])),
            F("fxrows", ("fxrows", (0, 0.38, 1, 1)),
              ("윗줄과 두 줄", [
                  "'윗줄'은 fx 패드 아래에 슬라이스 패드 한 줄이 있어서, 마우스로 슬라이스를 치면서 fx를 걸어요. '두 줄'은 fx 패드가 커지고 음 이름이 보여요. 슬라이스는 컨트롤러로 치고요.",
                  "fx 패드 16개 음은 기본으로 C1부터예요. 설정에서 옮기고, 슬라이스와 겹치면 빨간 표시가 떠요.",
              ]),
              ("Top row or two rows", [
                  "'top row' keeps a row of slice pads under the fx pads, to play slices with the mouse while the fx work. '2 rows' makes the fx pads bigger, with their notes; play the slices from a controller.",
                  "The 16 fx pads' notes start at C1 by default. Move them in the settings; a red mark shows where they clash with slices.",
              ])),
            F("fxsource", ("fxhelp", (0.3, 0.38, 1, 1)),
              ("어디서 왔나", [
                  "펀치, 필터, 퍼즈, 크러시의 비트, 히스, 크래클, 디지털 · 그레인 에코는 직접 만들었어요. 나머지는 Airwindows(MIT)의 모델을 가져와 칸마다 귀로 골랐어요.",
                  "? 키를 켜고 아무 칸이나 마우스를 올리면 무엇을 하는지 바로 알려줘요.",
              ]),
              ("Where it comes from", [
                  "Punch, the filter, fuzz, crush's bits, hiss, crackle and the digital and grain echoes are our own. The rest are Airwindows (MIT) models, picked for each slot by ear.",
                  "Turn on the ? key and hover over any slot to see what it does.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- deck
    {
        "key": "deck",
        "title": {"ko": "턴테이블", "en": "Turntable"},
        "lead": {
            "ko": "fx 화면 아래는 덱이에요. 자른 구간을 판처럼 돌리고 긁어요. 지금 엔진의 소리 그대로예요.",
            "en": "Under the fx screen sits a deck: spin and scratch the chopped range like a record, in the sound of the engine you picked.",
        },
        "features": [
            F("record", ("deckrest", DECK),
              ("판", [
                  "작업 구간이 판 한 장이에요. 재생하면 33⅓ rpm(한 바퀴 1.8초)으로 돌아요. 마우스로 플래터를 돌리거나 파형을 끌면 긁혀요.",
                  "리피치, 템포 유지(DAW 템포에 맞춰), 옛 기계 엔진 모두 자기 방식대로 판을 읽어요. 그래서 black으로 긁으면 black의 소리가 나요.",
              ]),
              ("The record", [
                  "The work range is a record. It turns at 33⅓ rpm (1.8 s a turn) while it plays; turn the platter with the mouse, or drag the waveform, to scratch.",
                  "Repitch, keep tempo (on the DAW's tempo) and the old-machine engines each read it their own way, so a scratch on black sounds like black.",
              ])),
            F("deckplay", ("deckplay", DECK),
              ("재생과 바늘", [
                  "▶는 바늘 자리부터 판을 돌려요. DAW가 멈춰 있어도 돌고, 다시 누르면 멈춰요. 파형 아래 슬라이스를 고르면 바늘이 그 슬라이스로 가요.",
                  "톤암은 판에 올린 슬라이스가 시작하는 홈에 앉아요. 소리를 따라 흔들리지 않고, 슬라이스가 바뀔 때만 움직여요.",
              ]),
              ("Play and the needle", [
                  "▶ turns the record from the needle, the DAW stopped or not; press again to stop. Pick a slice under the waveform and the needle goes there.",
                  "The tonearm sits on the groove where the slice on the platter starts. It doesn't wobble with the sound; it moves only when that slice changes.",
              ])),
            F("deckhand", ("deckheld", DECK),
              ("손과 슬립매트", [
                  "마우스나 컨트롤러로 판을 잡으면 손이 움직인 만큼만 판이 움직여요. 바늘이 튀지 않고, 움직임은 부드럽게 이어져요. 설정의 '스크럽 감도'로 마우스가 얼마나 돌릴지 정하고, Shift는 미세하게예요.",
                  "슬립매트처럼, 잡으면 몇 ms 안에 서고 놓으면 25 ms 안에 판 속도를 따라잡아요.",
              ]),
              ("The hand and the slipmat", [
                  "Grab the record with the mouse or a controller and it moves only as far as your hand: the needle never jumps, and moves are smoothed. 'scrub sensitivity' in the settings sets how far the mouse turns it; shift is fine.",
                  "Like a slipmat: grabbed, it stops within a few ms; let go, it catches the platter within 25 ms.",
              ])),
            F("hold", ("deckhold", DECK),
              ("판 잡기", [
                  "누르고 있는 동안 판과 패드가 손으로 판을 누른 것처럼 천천히 서요. 놓으면 다시 돌아 올라와요(곡을 따라 도는 중이면 곡 자리로).",
                  "얼마나 빨리 서고 올라올지는 설정의 '판 멈춤 시간'과 '판 시작 시간'이에요. DAW 오토메이션과 MIDI 지정이 돼요.",
              ]),
              ("Hold", [
                  "While you hold it, the record and the pads slow to a stop like a hand on the record; let go and they spin back up (following the song: back on the song).",
                  "How fast is the settings' record stop time and record start time. It can be automated and MIDI-learned.",
              ])),
            F("fader", ("deckplay", (0, 0.85, 0.75, 1)),
              ("페이더와 커브", [
                  "페이더는 판 소리를 들려주는 문이에요. 기본은 왼쪽(턴테이블 쪽)이 열림, 오른쪽이 닫힘. 긁으면서 끊으면 처프나 트랜스포머 소리가 나요. 반대로 쓰는 분을 위해 설정에서 뒤집을 수 있어요.",
                  "커브는 '부드럽게'(믹스용)부터 '날카롭게'(스크래치용, 조금만 움직여도 다 열림)까지. 설정의 '페이더 컷인'은 닫힌 끝에서 얼마나 가까이서 소리가 들어오기 시작할지예요(0.5–8 %).",
              ]),
              ("The fader and its curve", [
                  "The fader lets the record's sound through: open at the left (the turntable's side), closed at the right by default; cut it while you scratch for chirps and transformers. The settings can reverse it for those who scratch the other way round.",
                  "Its curve runs from smooth (for mixing) to sharp (for scratching: a small move opens it all). 'fader cut-in' in the settings is how close to the closed end the sound comes in (0.5–8 %).",
              ])),
            F("patterns", ("pattern", (0, 0, 0.55, 0.7)),
              ("스크래치 패턴", [
                  "판을 어떻게 긁을지예요. 베이비(밀고 당기기 둘 다 들림), 포워드(밀 때만), 처프, 티어, 트랜스포머, 플레어, 2클릭 플레어, 크랩.",
                  "길이는 한 번 밀고 당기는 데 1/2박부터 한 마디. 패턴은 DAW의 다음 16분음표에서 시작하고, 세게 칠수록 멀리 밀어요.",
              ]),
              ("Scratch patterns", [
                  "How the record gets scratched: baby (you hear both ways), forward (only the push), chirp, tear, transformer, flare, 2-click flare and crab.",
                  "One push and pull lasts 1/2 beat to a bar. Patterns start on the DAW's next 16th, and harder hits push further.",
              ])),
            F("drawer", ("drawer", (0.55, 0.38, 1, 1)),
              ("건반으로 긁기", [
                  "'더 보기'를 열면 모든 패턴, 길이, 건반 설정이 있어요. 이어진 16건반(기본 C-1–D#0)이 슬라이스 1–16을 쳐요. 누르고 있으면 그 슬라이스를 판에 올려 고른 패턴으로 되풀이해 긁어요.",
                  "'듣기' 키를 누르고 있으면 판에 올린 슬라이스를 바로 긁어 봐요. 16건반의 시작 음은 ‹ ›나 직접 입력으로 옮기고, 다른 구역과는 겹치지 않아요.",
              ]),
              ("Scratch on the keys", [
                  "'more' opens every pattern, the length and the keys. 16 keys in a row (C-1 to D#0 by default) play slices 1 to 16: hold one and its slice goes on the record and scratches with the pattern, over and over.",
                  "Hold 'hear' to scratch the slice on the platter right away. Move the 16 keys' first note with ‹ › or by typing; they never overlap the other zones.",
              ])),
            F("padpattern", ("padpattern", (0.45, 0, 1, 0.6)),
              ("슬라이스마다 패턴", [
                  "연주 방법을 '스크래치'로 하면 패드마다 자기 슬라이스를 판에 올려 긁어요. 패드를 오른쪽 클릭하면 그 슬라이스만의 패턴을 줄 수 있어요.",
                  "킥은 베이비로, 보컬은 처프로처럼 슬라이스마다 다르게 정해 두면 패드만 쳐도 루틴이 돼요.",
              ]),
              ("A pattern per slice", [
                  "With play as set to scratch, each pad puts its slice on the record and scratches it. Right-click a pad to give that slice a pattern of its own.",
                  "Babies on the kick, chirps on the vocal: set them per slice and the pads alone play a routine.",
              ])),
            F("scratching", ("scratching", DECK),
              ("긁는 중", [
                  "패턴이 판을 긁는 동안 플래터와 파형이 같이 움직이고, 파형 상자 위 오른쪽에 지금 상태(패턴 이름, 판 잡는 중, 손으로 긁는 중 …)가 나와요.",
                  "판을 한 번도 돌리지 않았을 땐 그 자리에 '← 스크래치 →' 안내가 먼저 보여요.",
              ]),
              ("While it scratches", [
                  "While a pattern scratches, the platter and the waveform move with it, and the top right of the waveform box shows what the deck is doing (the pattern's name, held, by hand …).",
                  "Before the record has ever turned, a '← scratch →' hint sits there instead.",
              ])),
            F("follow", ("deckrest", (0.72, 0.6, 1, 1)),
              ("곡 따라 돌기와 큐", [
                  "'곡 따라 돌기'를 켜면 DAW를 재생할 때 판이 큐부터 곡에 맞춰 돌아요. 손, 패턴, 판 잡기가 잠깐 곡에서 떼어 놓아도, 다시 제 속도가 되면 곡 자리로 돌아와요.",
                  "'큐 놓기'는 지금 바늘 자리를 큐로 정해요(그때의 마디도 기억해요). '큐로 돌아가기'는 바늘을 바로 큐로 보내요. DAW가 재생하면, 멈추면: 천천히(0.45초에 걸쳐 올라오고 서요) 또는 바로.",
              ]),
              ("Follow the song, and the cue", [
                  "With 'follow the song' on, the record runs from its cue in time with the song whenever the DAW plays. A hand, a pattern or the hold takes it off the song for a moment; back at full speed it's in time again.",
                  "'set cue' makes the needle's place the cue (with the bar you set it on); 'back to cue' sends the needle there at once. When the DAW plays and stops: slowly (up and down over 0.45 s) or at once.",
              ])),
            F("speed", ("speed45", DECK),
              ("45와 78", [
                  "grey, black, purple을 고르면 판 속도가 33⅓ 말고 45나 78이 돼요. 옛날 프로듀서들이 판을 빠르게 샘플링하고 낮춰 재생해서 짧은 샘플 시간에 더 긴 소리를 담던 방법이에요.",
                  "키와 템포는 그대로이고, 고음이 더 거칠어져요. clean은 샘플 그대로라서 33⅓만 있어요.",
              ]),
              ("45 and 78", [
                  "With grey, black or purple, the record can run at 45 or 78 instead of 33⅓: the old trick of sampling a record faster and playing it back lower, to fit longer sounds into short sample time.",
                  "The key and tempo stay the same; the top end gets grittier. clean is the sample as it is, so it stays at 33⅓.",
              ])),
            F("controllers", ("deckmidi", DECK),
              ("컨트롤러와 오토메이션", [
                  "플래터를 오른쪽 클릭하면 MIDI 지정: 끝없이 도는 노브는 조그, 터치 스트립은 손 자리, 피치 휠은 밀고 당기기, 패드는 판 잡기. 지정된 컨트롤에는 작은 배지가 붙어요.",
                  "판, 손, 페이더가 DAW 파라미터라서, 긁은 걸 오토메이션으로 쓰고 나중에 고칠 수 있어요. 바운스에도 그대로 들어가요.",
              ]),
              ("Controllers and automation", [
                  "Right-click the platter for MIDI learn: an endless knob is a jog, a touch strip the hand, the pitch wheel pushes and pulls, a pad holds the record. Learned controls wear a small badge.",
                  "The record, the hand and the fader are DAW parameters, so a scratch can be written as automation and edited later, and it ends up in the bounce as played.",
              ])),
            F("decksettings", ("decksettings", (0.5, 0, 1, 0.85)),
              ("판 설정", [
                  "판 시작 시간(▶과 판 잡기를 놓을 때 제 속도까지)과 판 멈춤 시간(■과 판 잡기로 설 때까지), 패턴 길이. 바로부터 몇 박까지 골라요.",
                  "페이더 컷인, 페이더 방향, 스크럽 감도, 큐 모드, DAW가 멈출 때, 바늘(큐 위에 / 고정)도 여기 있어요.",
              ]),
              ("Record settings", [
                  "Record start time (to full speed after ▶ or letting go of the hold) and stop time (to a stop with ■ or the hold), and the pattern length: at once to a few beats.",
                  "Fader cut-in, fader direction, scrub sensitivity, cue mode, when the DAW stops and the needle (on the cue, or fixed) are here too.",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- drum
    {
        "key": "drum",
        "title": {"ko": "드럼", "en": "Drums"},
        "lead": {
            "ko": "원샷 16개로 킷을 짜는 화면이에요. 샘플러와 같은 플러그인 안, 머리줄의 가운데 칸에 있어요.",
            "en": "A screen for building a kit from 16 one-shots, in the same plug-in as the sampler: the middle of the header switch.",
        },
        "features": [
            F("cells", ("drum", (0, 0.09, 0.635, 0.95)),
              ("셀 16개", [
                  "4 × 4 셀, 1번이 왼쪽 아래예요. 파일을 끌어 놓으면 들어가고, 여러 개를 놓으면 그 셀부터 차례로 채워요. 셀을 누르면 소리가 나고 골라져요. 칠 때 패드처럼 불이 들어와요.",
                  "샘플러, 드럼, fx 중 어느 화면을 보든 같은 건반이 같은 소리를 내요. 셀은 기본으로 C6부터(드럼 킷 카드로 시작했으면 C3부터)예요.",
              ]),
              ("16 cells", [
                  "4 × 4 cells, cell 1 at the bottom left. Drop a file in; drop several and they fill in order from that cell. Click a cell to play and pick it; it lights up like a pad when hit.",
                  "Whichever screen shows (sampler, drums or fx), the same key plays the same sound. Cells start at C6 by default (C3 when you started from the drum kit card).",
              ])),
            F("cell", ("drum", (0.63, 0.09, 1, 0.62)),
              ("셀마다 조절", [
                  "볼륨, 팬, 음높이(반음 ±24), 엔진(clean · grey · black · purple), 초크 그룹, 페이드 인 · 아웃. 볼륨, 팬, 음높이, 엔진, 페이드는 DAW 오토메이션이 돼요.",
                  "여러 셀을 골라 한꺼번에 바꿀 수 있어요. 끌면 모두 같은 만큼 움직이고, 숫자를 치면 모두 그 값이 돼요.",
              ]),
              ("Per cell", [
                  "Level, pan, pitch (±24 semitones), engine (clean, grey, black or purple), choke group, fade in and out. Level, pan, pitch, engine and fades can all be automated.",
                  "Pick several cells to change them together: a drag moves them all by the same amount, a typed number sets them all to it.",
              ])),
            F("trim", ("drum", (0.63, 0.09, 1, 0.33)),
              ("시작 · 끝, 잘라내기, 노멀라이즈", [
                  "셀마다 원샷의 파형과 시작 · 끝 마커가 있어요. 샘플러처럼 샘플 단위로 다듬어요.",
                  "가위는 시작부터 끝까지만 남기고, 노멀라이즈는 그 사이 가장 큰 자리를 0 dB로 올려요. 원래 파일은 그대로이고, 되돌리기로 돌아와요.",
              ]),
              ("Start, end, truncate, normalize", [
                  "Each cell shows its one-shot's waveform with start and end markers, trimmed in samples like the sampler.",
                  "The scissors keep only start to end; normalize brings the loudest point between them up to 0 dB. The file stays as it is, and undo brings it back.",
              ])),
            F("inserts", ("drum", (0.63, 0.6, 1, 0.97)),
              ("셀마다 fx와 센드", [
                  "셀마다 필터, 펀치, 디스토션, 크러시, 테이프를 걸어요. 랙과 같은 모델이에요.",
                  "에코와 스페이스는 셀마다 보내는 양만 정하고, 킷 전체에 하나씩만 돌려서 CPU를 아껴요. 그 소리는 메인 출력(1번)으로 나와요.",
              ]),
              ("fx and sends per cell", [
                  "Each cell gets its own filter, punch, distort, crush and tape, the same models as the rack.",
                  "Echo and space are sends: each cell sets how much it sends, and one of each runs for the whole kit to save CPU, on the main output (output 1).",
              ])),
            F("choke", ("drum", (0, 0.05, 1, 1)),
              ("초크와 출력", [
                  "초크 그룹 1–4. 같은 그룹의 셀을 치면 앞 소리가 멈춰요. 닫힌 하이햇이 열린 하이햇을 끊듯이요. 같은 셀을 다시 치면 겹쳐 울려요.",
                  "출력 16개: 셀을 오른쪽 클릭해서 DAW의 다른 트랙으로 보내요. 1번은 fx 랙을 거치고, 2–16번은 따로 나가요. DAW에서 flipper를 멀티 출력 악기로 넣고 '멀티 출력으로 넣음'을 켜야 하고, 꺼진 출력의 셀은 1번으로 나와요.",
              ]),
              ("Choke and outputs", [
                  "Choke groups 1–4: hit a cell and the last one in its group stops, like a closed hat cutting an open one. The same cell hit again rings over itself.",
                  "16 outputs: right-click a cell to send it to its own DAW track. Output 1 runs through the fx rack; 2–16 go out on their own. Insert flipper as a multi-output instrument and turn 'inserted as multi-output' on; a cell on an output that's off plays on output 1.",
              ])),
            F("zones", ("settingskeys", (0, 0.12, 0.5, 0.67)),
              ("건반 구역", [
                  "샘플러 패드, 드럼 셀, fx 패드, 스크래치 구역, 키스위치의 시작 음을 설정에서 옮겨요. 두 구역이 겹치면 빨간 표시가 뜨고, 키스위치, 스크래치, fx 패드, 드럼 셀, 샘플러 순서로 먼저 것이 쳐요.",
                  "MIDI 채널 10으로 보내면 C1–D#2가 셀 1–16을 쳐요(셀에 샘플이 있을 때). '새 flipper 건반'을 '드럼 먼저'로 하면 새로 여는 flipper는 드럼이 C3부터예요. 저장된 프로젝트는 자기 건반 그대로예요.",
              ]),
              ("Key zones", [
                  "Move where the sampler pads, drum cells, fx pads, scratch zone and keyswitches start in the settings. Where two share keys a red mark shows, and the first of keyswitches, scratch, fx pads, drum cells, sampler plays them.",
                  "On MIDI channel 10, C1 to D#2 play cells 1 to 16 (while a cell holds a sample). 'new flipper's keys: drums first' starts a new flipper with the drums from C3; saved projects keep their own keys.",
              ])),
            F("kits", ("drumempty", (0, 0.05, 1, 1)),
              ("킷 파일과 가져오기", [
                  "셀을 오른쪽 클릭하면 킷 저장 · 열기. .flipkit에 샘플과 설정을 함께 담아요. 다른 프로젝트에서 열면 샘플러는 그대로 두고 킷만 들어와요.",
                  "다른 프로그램의 드럼 킷도 가져와요: WAV 폴더, 16슬라이스 WAV, .sfz, .mxgrp, .xpm · .xpn, .adg. 앞의 패드 16개를 셀로, 가장 큰 패드를 0 dB에 맞춰 균형을 지켜요. 내보내기는 들리는 그대로의 WAV 킷(번호 붙은 파일 폴더)이에요.",
              ]),
              ("Kit files and imports", [
                  "Right-click a cell to save or open a kit: a .flipkit holds the samples and settings. Opened in another project, only the kit comes in; the sampler stays.",
                  "Kits from other apps come in too: a WAV folder, a 16-slice WAV, .sfz, .mxgrp, .xpm and .xpn, .adg. The first 16 pads become cells, balanced with the loudest at 0 dB. Export writes a WAV kit as heard (a folder of numbered files).",
              ])),
        ],
    },
    # -------------------------------------------------------------------------------------------- out
    {
        "key": "out",
        "title": {"ko": "내보내기와 안전", "en": "Out, and safe"},
        "lead": {
            "ko": "만든 것은 그대로 DAW로 가고, 갑자기 큰 소리는 나지 않게 했어요.",
            "en": "What you make goes straight to the DAW, and nothing suddenly gets loud.",
        },
        "features": [
            F("chopmidi", ("chopmidi", (0, 0.45, 0.62, 0.82)),
              ("찹을 MIDI로", [
                  "'찹을 MIDI로' 키를 DAW 트랙에 끌어 놓으면, 루프가 각 슬라이스에 닿는 순간 그대로 그 슬라이스를 치는 MIDI 클립이 생겨요(패드 1번 음부터). 원래 그루브에서 출발해서 음만 바꾸며 플립하면 돼요.",
                  "누르면 MIDI 파일로 저장해요. DAW 템포가 샘플과 달라 박자에 안 맞을 땐 몇 BPM으로 맞추면 되는지 알려줘요.",
              ]),
              ("Chop to MIDI", [
                  "Drag the 'chop to MIDI' key onto a DAW track for a clip that plays each slice the moment the loop reaches it (from pad 1's note). Start from the sample's own groove and flip it by moving notes.",
                  "Click it to save a MIDI file instead. When the DAW tempo doesn't fit the sample, it tells you the BPM that lines it up.",
              ])),
            F("learn", ("learning", (0, 0, 1, 0.62)),
              ("MIDI 지정", [
                  "노브, 스위치, 키, 고르기 칸 어디든 오른쪽 클릭하면 MIDI 지정이에요. 컨트롤러를 움직이면 바로 이어지고, 지정된 곳엔 CC나 음 이름이 적힌 배지가 붙어요.",
                  "지정된 음은 어느 건반 구역보다 먼저예요. 프로젝트마다 자기 지정을 가지고, 새 flipper는 이 컴퓨터의 기본 지정으로 시작해요.",
              ]),
              ("MIDI learn", [
                  "Right-click any knob, switch, key or choice for MIDI learn: move the controller and it's linked, with a badge showing its CC or note.",
                  "A learned note wins over every key zone. Each project keeps its own map, and a new flipper starts with this computer's default.",
              ])),
            F("learnmenu", ("learnmenu", (0, 0.4, 0.62, 0.95)),
              ("노브가 보내는 값", [
                  "지정한 컨트롤을 다시 오른쪽 클릭하면 메뉴가 나와요. 노브가 보내는 값(절댓값, 상댓값 몇 가지)을 고르면 끝없이 도는 노브도 맞게 움직여요. 감도도 골라요.",
                  "키와 패드는 '누르는 동안'이나 '켜 두기'로. 지정 지우기도 여기 있어요.",
              ]),
              ("What the knob sends", [
                  "Right-click a learned control again for its menu: pick what the knob sends (absolute, or one of the relative kinds) and endless knobs move right; pick a sensitivity too.",
                  "Keys and pads work 'while held' or as a toggle. Forget is there as well.",
              ])),
            F("midilist", ("settingsmidi", (0, 0, 1, 1)),
              ("MIDI 목록과 8노브", [
                  "설정 아래 MIDI 목록에 지정한 것이 모두 있어요. '값을 지나갈 때'를 고르면 컨트롤러 노브가 화면의 값을 지나갈 때부터 움직여서 소리가 튀지 않아요.",
                  "'노브 8개 차례로'는 컨트롤러의 노브 8개를 왼쪽부터 차례로 돌리기만 하면 슬라이스 시작, 끝, 음높이, 볼륨 … 순서로 지정돼요. '기본으로 저장'하면 새 flipper가 이 지정으로 시작해요.",
              ]),
              ("The MIDI list and eight knobs", [
                  "Everything learned is listed at the bottom of the settings. 'catch when passing' makes a controller knob move its control only once it passes the screen's value, so the sound never jumps.",
                  "'eight knobs in a row': turn your controller's eight knobs one after the other from the left and they take slice start, end, pitch, level … in order. 'save as default' starts every new flipper with it.",
              ])),
            F("meter", ("meter", (0.4, 0, 1, 0.075)),
              ("볼륨과 미터", [
                  "머리줄의 볼륨은 flipper에서 나가는 소리예요. 위 막대가 왼쪽, 아래 막대가 오른쪽, 눈금은 가장 컸던 순간을 잡아 두고, 오른쪽 끝의 빨간 표시는 리미터가 일하는 만큼이에요. 소리가 꼭대기에 닿으면 점이 켜지고, 누르면 꺼져요.",
                  "손잡이를 끌거나(Shift는 미세하게), 더블클릭하면 0 dB, 숫자를 누르면 쳐 넣어요.",
              ]),
              ("Volume and the meter", [
                  "The header's volume is what leaves flipper: the top bar is left, the bottom one right; a tick holds the loudest moment, and the red mark from the right end is the limiter at work. The dot lights when the sound hit the top; click it to clear.",
                  "Drag the handle (shift for finer), double-click for 0 dB, click the number to type one.",
              ])),
            F("safety", ("slot_all", (0.45, 0.1, 1, 0.3)),
              ("큰 소리 규칙", [
                  "갑자기 큰 소리는 스피커와 귀를 다치게 할 수 있어서, 가장 심각한 버그로 다뤄요. 원인을 고치고, 모든 엔진과 fx에 '이보다 커지면 안 된다'는 테스트를 걸었어요. NaN이나 Inf 같은 깨진 값도 막아요.",
                  "평소 소리를 바꾸는 숨은 리미터는 없어요. 맨 끝의 리미터(세이프, 빈티지, 끔)는 직접 골라요. 출력마다 따로라서 DAW에서 여러 출력을 더하면 넘을 수 있어요.",
              ]),
              ("The loudness rule", [
                  "A sudden loud sound can hurt speakers and ears, so it's treated as the worst bug: causes are fixed, and every engine and fx has a test that it never goes above a bound. Broken values like NaN and Inf are stopped too.",
                  "No hidden limiter colours the everyday sound. The limiter at the very end (safe, vintage, off) is your choice. It works per output, so outputs added in the DAW can still go over.",
              ])),
            F("bounce", ("hits", (0, 0, 1, 0.3)),
              ("바운스 = 연주", [
                  "블록 크기 1부터 4096까지, 실시간이든 오프라인이든 같은 소리가 나요. 들은 소리와 바운스한 소리가 다르면 버그예요.",
                  "옛 기계 엔진, 미리 굽기, fx의 흔들림, 판까지 모두 DAW의 박과 샘플 자리를 기준으로 움직여서 가능해요.",
              ]),
              ("Bounce = live", [
                  "The same sound at block sizes from 1 to 4096, real time or offline. If the bounce differs from what you heard, that's a bug.",
                  "The old-machine engines, the bakes, the fx's flux and the record all keep time by the DAW's beat and sample position, which is what makes it hold.",
              ])),
            F("undo", ("settingskeys", (0.5, 0.36, 0.97, 0.58)),
              ("되돌리기와 A | B", [
                  "머리줄의 ↶ ↷. 노브 하나, 끌기 하나, 찹 하나가 한 단계예요.",
                  "A | B 비교는 설정 두 가지를 저장해 두고 바꿔 들어 보는 거예요. 'A를 B로 복사'로 지금 것을 두고 조금씩 바꿔 봐요.",
              ]),
              ("Undo and A | B", [
                  "↶ ↷ in the header. One knob turn, one drag, one chop is one step.",
                  "Compare A | B keeps two settings to switch between and hear the difference; 'copy A to B' to try changes against what you have.",
              ])),
            F("help", ("help", (0, 0, 1, 0.62)),
              ("도움말", [
                  "머리줄의 ? 키를 켜면 마우스를 올린 곳마다 무엇을 하는지 말풍선이 떠요. 모든 노브, 키, 고르기 칸에 있어요.",
                  "설정의 '마우스와 키'에 끌기, Shift, Alt, Ctrl(⌘) 조합이 모두 정리돼 있어요.",
              ]),
              ("Help", [
                  "Turn on the ? key in the header and every place you hover tells you what it does: every knob, key and choice.",
                  "'mouse and keys' in the settings lists every drag, shift, alt and cmd combination.",
              ])),
            F("looks", ("night", (0, 0, 1, 1)),
              ("낮과 밤, 스킨", [
                  "머리줄의 달 키로 낮과 밤을 바꿔요. 엔진을 바꾸면 화면 스킨도 그 기계처럼 바뀌어요(clean, grey, black, purple). 늘 버터 색으로 두고 싶으면 설정의 '스킨'에서요.",
                  "스킨은 색과 재질만 달라요. 같은 컨트롤은 어느 스킨에서나 같은 자리, 같은 크기, 같은 말, 같은 동작이에요.",
              ]),
              ("Day, night and skins", [
                  "The moon key in the header switches day and night. Change the engine and the screen wears that machine's skin (clean, grey, black, purple); 'skin: always clean' in the settings keeps it plain.",
                  "Skins differ only in colour and material: the same control keeps its place, size, words and behaviour in every skin.",
              ])),
            F("settings", ("settings", (0, 0.13, 0.5, 0.6)),
              ("언어, 창 크기, 연못", [
                  "화면 전체가 한국어와 영어예요. 창 크기는 75, 100, 125, 150 %.",
                  "머리줄 가운데의 연못은 슬라이스가 울릴 때마다 움직여요. 누르면 종이 꽃가루, 줄 울림, 잉어 연못, 먹물 마블링으로 바뀌고, 끌 수도 있어요.",
              ]),
              ("Language, window size, the pond", [
                  "The whole screen in Korean and English. The window at 75, 100, 125 or 150 %.",
                  "The pond in the middle of the header answers every slice that plays. Click it for paper confetti, plucked strings, a koi pond or marbled ink, or turn it off.",
              ])),
            F("report", ("report", (0, 0, 1, 1)),
              ("버그 제보", [
                  "오른쪽 아래 '버그 제보'를 누르면 무슨 일이 있었는지 적는 창이 열려요. 보내기 전에 보내는 내용(버전, DAW, 샘플레이트 같은 기술 정보)을 전부 보여주고, 동의를 눌러야 익명으로 보내져요.",
                  "보내고 싶지 않으면 파일로 저장해도 돼요. 하루 한 번 새 버전이 나왔는지 보고, 있으면 이름 옆에 작은 점을 켜요. 확인 요청 말고는 아무 정보도 보내지 않아요.",
              ]),
              ("Bug report", [
                  "'report a bug' at the bottom right opens a form for what went wrong. Everything that would be sent (version, DAW, sample rate and such) is shown first, and it goes anonymously only once you tick the box.",
                  "Or save it as a file instead. Once a day flipper checks for a newer version and shows a small dot by its name; it sends nothing of yours but the request itself.",
              ])),
        ],
    },
]


def feature_count() -> int:
    return sum(len(p["features"]) for p in PARTS)
