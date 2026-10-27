# 레네 RENÉ / arcadiatripper

레네 RENÉ(tripper)의 플러그인과 음악, 글, 가이드를 모은 정적 홈페이지입니다.

## 주소

| 한국어 | English | 내용 |
|---|---|---|
| `/` | `/en/` | 지금은 flipper 소개 (플러그인이 둘이 되면 플러그인 카드를 고르는 첫 화면) |
| `/flipper/` | `/en/flipper/` | flipper 소개 |
| `/artist/` | `/en/artist/` | 아티스트 포트폴리오 (예전 첫 화면) |
| `/koala-sampler-kr-manual/` | | Koala Sampler 한국어 가이드 (별도 저장소) |

- 예전 첫 화면의 `#discography` 같은 주소는 첫 화면이 `/artist/#discography`로 넘겨 줍니다.
- 맨 위 막대(`assets/css/global.css`, `assets/js/global.js`)는 모든 페이지에서 같은 자리, 같은 말을 씁니다.
- flipper 페이지 네 개는 `tools/build_flipper.py`가 한 틀과 한국어 · 영어 문구로 만듭니다. 문구를 바꾸면 `python3 tools/build_flipper.py`를 다시 돌리고 결과를 커밋합니다. 베타 공개 날에는 그 파일의 `RELEASED`를 `True`로, 소개 영상이 나오면 `VIDEO_ID`를 채웁니다.
- flipper 화면 그림(`assets/images/flipper/`)은 flipper 저장소의 `flipper_snapshot`으로 뽑습니다. 글꼴(`assets/fonts/flipper-ui/`)은 플러그인의 "flipper ui"(Fredoka + 나눔스퀘어라운드)와 스킨 글꼴을 웹용으로 줄인 것이며 SIL OFL 1.1입니다.
- flipper 코드 저장소에서는 GitHub Pages를 켜지 않습니다. 켜면 그 저장소가 `arcadiatripper.com/flipper` 주소를 차지합니다.

- 공개 주소: <https://arcadiatripper.com/>
- 기술 구성: HTML, CSS, 최소한의 JavaScript
- 배포 방식: GitHub Pages에서 저장소 루트의 정적 파일을 직접 제공
- 글꼴: LINE Seed Sans KR (아티스트 페이지), flipper ui · Barlow · DotGothic16 · Jersey 15 (flipper 페이지), 모두 SIL Open Font License 1.1

## 로컬 확인

저장소 루트에서 간단한 정적 파일 서버를 실행한 뒤 브라우저로 확인합니다. 별도의 빌드 과정이나 패키지 설치는 필요하지 않습니다.

## 콘텐츠 관리

- 디스코그래피와 靈魂都心 아카이브는 Bandcamp의 공식 임베드 플레이어를 사용합니다.
- Flipper 재생목록은 YouTube의 개인정보 보호 강화 임베드 플레이어를 사용합니다.
- 모든 앨범과 재생목록은 JavaScript 없이도 외부 원문 페이지 링크로 이동할 수 있습니다.
- 최적화 이미지는 `assets/images/`에, LINE Seed 글꼴과 라이선스는 `assets/fonts/`에 있습니다.
- 소셜 플랫폼 아이콘은 [Simple Icons](https://simpleicons.org/)의 CC0 벡터 자산을 로컬에 보관해 사용합니다.
- 첨부 원본 이미지는 이 저장소 밖에 보존하며 파생 파일만 사용합니다.

## GitHub Pages 배포

`arcadiatripper.github.io` 저장소의 기본 브랜치 루트를 GitHub Pages 배포 원본으로 사용하며, 루트의 `CNAME` 파일로 커스텀 도메인 `arcadiatripper.com`을 지정합니다. 저장소 생성, 커밋, 푸시와 공개 배포는 별도 승인 후 진행합니다.

Koala Sampler 한국어 가이드는 별도 저장소와 주소를 유지하며 이 홈페이지 프로젝트에서 수정하지 않습니다.
