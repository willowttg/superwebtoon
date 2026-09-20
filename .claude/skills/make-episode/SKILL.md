---
name: make-episode
description: 「당신은 약간 초능력자?」 에피소드 1편 제작 — MBTI 유형의 단점을 초능력으로 재해석한 표지 + 7컷 캐러셀. 콘티 → 컷 이미지 생성 → 텍스트 합성 → 프리뷰 → 캡션. "에피소드 만들어", "EP.02", "INTJ 편", "콘티 짜줘", "컷 생성" 등에 사용.
---

# make-episode

입력: MBTI 유형 1개 (+ 선택: 다룰 단점 특징, 폰트 지정). 산출물은 `episodes/epNN/`.

## 1. 기획 규칙

- **제목** = 그 유형의 통용되는 단점을 능력처럼 바꾼 후킹 카피. 형식 `[단점이 드러나는 수식절] 초능력` — "초능력자"가 아니라 **"초능력"으로 끝낸다**. 예: INFP 「알고 싶지 않은 마음까지 읽는 초능력」. 수식절에 단점의 불편함이 보여야 한다. 시리즈명 「당신은 약간 초능력자?」는 표지에 넣지 않는다.
- **MBTI는 작품 어디에도 쓰지 않는다** (표지·컷·캡션·해시태그). 유형은 기획 입력값일 뿐이다.
- 내용은 해당 유형 독자가 "이거 나잖아"라고 느껴야 한다. 유형 밈이 아니라 **구체적 상황**(약치기그림식)으로 쓴다.
- 내레이션·속마음은 **1인칭**("나는 …"). 3인칭 설명("이 유형은 …")으로 쓰지 않는다. CTA만 독자에게 말한다.
- **이모지 금지** (컷·캡션·CTA 전부).
- **소품** = 에피소드마다 그 초능력을 상징하는 소품 1개를 정한다 (예: 마음 읽기 → 헤드폰). 두부가 착용하는 형태여야 하며, 표지와 능력 발동 컷에서 착용한다.
- **표지 + 7컷 = 8장** 고정.

| 컷 | 역할 | 비고 |
|---|---|---|
| 표지 | 제목 + 두부 (망토 + 소품, POWER ACTIVATED 포즈) | 제목의 핵심 단어 1개만 포인트 컬러 |
| 1 | 초능력 설명 — "나는 ○○이 된다" | 담담한 내레이션 |
| 2–3 | 장점 — 능력이 남에게 좋게 작용하는 장면 | 조연이 수혜자 |
| 4 | **단점 첫 등장 = 공유 유도 컷.** 가장 구체적이고 찔리는 상황 | "이거 너잖아" 하고 친구에게 보내게 되는 컷. 여기에 가장 공을 들인다 |
| 5–6 | 단점 심화 — 힘들고 불편한 부분 | 5는 상황, 6은 속마음 |
| 7 | 마무리 = **저장 유도 문장** + 태그 CTA | "그래도 그 능력 덕분에 누군가는…" 한 줄 위로 → "당신 곁의 두부를 태그해 주세요" (캐릭터 이름이 정체성 태그) |

톤 전환: 1–3 밝음 → 4–6 저채도·먹구름 → 7 망토 + 포인트 컬러 복귀.

## 2. 이미지 규칙

- 생성은 **캐릭터 + 소품만**. 프롬프트 끝에 항상 `No text, no letters, no speech bubbles, no captions. Plain white background.` 말풍선 꼬리가 캐릭터와 안 맞는 문제가 있어 **말풍선은 절대 그리지 않는다** — 속마음도 텍스트 합성으로.
- 참조: 등장 캐릭터 시트 `assets/samples/<이름>-sheet-high.png`(두부 dubu, 미숙 misook, 덕수 deoksu, 콩 kong, 탱자 tangja, 소라 sora, 밤톨 bamtol) → **2명 이상 동시 출연이면** `python scripts/lineup.py dubu misook --out ref/lineup.png`로 그 컷의 캐릭터만 담은 크기 라인업을 만들어 다음 참조로 → `assets/ref/kkamja-1~2.jpg`(스타일). 각 시트 프롬프트(`<이름>-sheet-prompt.txt`)의 design 블록을 프롬프트 헤더로 복사하고, 라인업이 있으면 "the lineup image shows their relative sizes"를 덧붙인다.
- **소품 시트**: 컷 생성 전에 소품을 착용한 두부 시트 `img/dubu-prop.png`를 먼저 만든다 (`dubu-sheet-high.png`를 참조로, 같은 턴어라운드·표정 구성, `high`). 표지와 소품 착용 컷은 두부 참조를 `img/dubu-prop.png`로 바꾸고 헤더에 소품 설명 1줄을 추가한다. 미착용 컷은 기본 시트 그대로. 망토는 시트에 없으므로 컷 프롬프트에서 지정.
- 캐스트·크기·색은 `assets/characters.md` 1절.
- 초능력 발동(표지·2–3·7): 테라코타 망토 `#C77B3F` + 반짝이. 단점 컷(4–6): 먹구름·땀방울, 망토 없음.
- 텍스트가 들어갈 여백을 프롬프트로 확보: 내레이션 컷은 `character in the lower half, upper 40% empty`.
- 생성: `python scripts/gen_image.py --prompt-file prompts/cutN.txt --ref assets/samples/dubu-sheet-high.png [--ref assets/samples/misook-sheet-high.png --ref ref/lineup.png] --ref assets/ref/kkamja-1.jpg --ref assets/ref/kkamja-2.jpg --out img/cutN.png` — 컷 `medium`, 표지 `high`. `.env` 로드 필요(`docs/env-setup.md`).

## 3. 텍스트 합성

- `episodes/epNN/compose.html` — 슬라이드 8장을 각각 1080×1350 `<section>`으로. 이미지는 1024×1536 생성본을 중앙 1024×1280 크롭(`object-fit:cover`).
- 폰트: 본문(내레이션·속마음·CTA) **교보손글씨 2019** 확정, 내레이션은 가운데 정렬. 표지 제목은 미확정(현재 나눔손글씨 펜). `@font-face`는 `assets/fonts.html`에서 복사.
- 표지: 제목 3줄 이내, 핵심 단어 `<b>`로 포인트 컬러.
- 컷: 상단 내레이션 1–2줄. 속마음은 캐릭터 옆에 작은 회색 글자, 말풍선·박스 없이.
- Playwright MCP로 각 `<section>`을 `img/slideN.png`로 스크린샷 (viewport 1080×1350, `clip`). MCP 브라우저가 사용 중이면 `chrome-headless-shell.exe --headless --window-size=1080,1350 --virtual-time-budget=10000 --screenshot=img/slideN.png compose.html?only=N` (N은 0부터; `?only`는 compose.html에 그 슬라이드만 남기는 스크립트로 처리).
- 이미지 크롭은 `object-position:50% 100%`(하단 기준)로 발이 안 잘리게 하고, 표지는 `object-fit:contain`.
- 속마음 등 그림 옆 텍스트는 `python scripts/art_bbox.py img/cutN.png`로 그림 영역을 잰 뒤 그 밖에 놓는다. 프롬프트의 "상단 40% 비움"은 대략만 지켜지고(30~47%), 글자 폭은 폰트마다 달라 눈대중으로 두면 겹친다.

## 4. 산출물과 마무리

```
episodes/epNN/
  conti.md        제목·소품·컷별 [장면 / 소품 착용 여부 / 내레이션 / 속마음 / 프롬프트 요점]
  prompts/dubu-prop.txt, cutN.txt
  img/dubu-prop.png, cutN.png, slideN.png
  compose.html
  preview.html    슬라이드 8장 세로 나열 (모바일 확인용)
  caption.txt     캡션 1–2줄 + 고정 해시태그
```

- 고정 해시태그: `#당신은약간초능력자 #인스타툰 #일상툰 #공감툰` (MBTI 관련 태그 없음)
- `index.html` 콘티 프리뷰 섹션에 카드 추가 → 커밋. **푸시는 사용자 확인 후.**

## 5. 체크리스트 (커밋 전)

- [ ] 제목이 단점을 능력처럼 말하고 "초능력"으로 끝나는가, 시리즈명이 표지에 없는가
- [ ] 8장·캡션·해시태그에 MBTI 문자열·이모지가 없는가
- [ ] 4컷이 친구에게 보낼 만큼 구체적인가 / 7컷이 저장할 만한 한 문장인가
- [ ] 생성 이미지에 글자·말풍선이 없는가, 캐릭터 색·눈·입 없음·상대 크기가 유지되는가
- [ ] 표지·소품 착용 컷이 소품 시트를 참조했고 소품 형태가 컷 간 일치하는가
- [ ] 8장 전부 1080×1350, 텍스트가 잘리지 않는가
