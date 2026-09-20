---
name: make-episode
description: 「당신은 약간 초능력자?」 에피소드 1편 제작 — MBTI 유형의 단점을 초능력으로 재해석한 표지 + 7컷 캐러셀. 콘티 → 컷 이미지 생성 → 텍스트 합성 → 프리뷰 → 캡션. "에피소드 만들어", "EP.02", "INTJ 편", "콘티 짜줘", "컷 생성" 등에 사용.
---

# make-episode

입력: MBTI 유형 1개 (+ 선택: 다룰 단점 특징, 폰트 지정). 산출물은 `episodes/epNN/`.

## 1. 기획 규칙

- **제목** = 그 유형의 통용되는 단점을 능력처럼 바꾼 후킹 카피. 형식 `[…] 초능력자`. 예: INFP 「알고 싶지 않은 마음까지 읽는 초능력자」. 시리즈명 「당신은 약간 초능력자?」는 표지에 넣지 않는다.
- **부제** = `- INFP -` 소문자 크기로 제목 아래.
- 내용은 해당 유형 독자가 "이거 나잖아"라고 느껴야 한다. 유형 밈이 아니라 **구체적 상황**(약치기그림식)으로 쓴다.
- **표지 + 7컷 = 8장** (인스타 상한).

| 컷 | 역할 | 비고 |
|---|---|---|
| 표지 | 제목 + 부제 + 보리 (망토, POWER ACTIVATED 포즈) | 제목의 핵심 단어 1개만 포인트 컬러 |
| 1 | 초능력 설명 — "이 유형은 ○○이 된다" | 담담한 내레이션 |
| 2–3 | 장점 — 능력이 남에게 좋게 작용하는 장면 | 조연이 수혜자 |
| 4 | **단점 첫 등장 = 공유 유도 컷.** 가장 구체적이고 찔리는 상황 | "이거 너잖아" 하고 친구에게 보내게 되는 컷. 여기에 가장 공을 들인다 |
| 5–6 | 단점 심화 — 힘들고 불편한 부분 | 5는 상황, 6은 속마음 |
| 7 | 마무리 = **저장 유도 문장** + 태그 CTA | "그래도 그 능력 덕분에 누군가는…" 한 줄 위로 → "당신 곁의 INFP를 태그해 주세요" |

톤 전환: 1–3 밝음 → 4–6 저채도·먹구름 → 7 망토 + 포인트 컬러 복귀.

## 2. 이미지 규칙

- 생성은 **캐릭터 + 소품만**. 프롬프트 끝에 항상 `No text, no letters, no speech bubbles, no captions. Plain white background.` 말풍선 꼬리가 캐릭터와 안 맞는 문제가 있어 **말풍선은 절대 그리지 않는다** — 속마음도 텍스트 합성으로.
- 참조: 첫 이미지 `assets/samples/bori-sheet2-high.png`(캐릭터), 이어서 `assets/ref/kkamja-1~3.jpg`(스타일). `assets/samples/bori-sheet2-prompt.txt`의 Bori design 블록을 프롬프트 공통 헤더로 복사.
- 조연은 `assets/characters.md` 2절 기준. 단색 바디 + 마커 1개.
- 초능력 발동(표지·2–3·7): 테라코타 망토 `#C77B3F` + 반짝이. 단점 컷(4–6): 먹구름·땀방울, 망토 없음.
- 텍스트가 들어갈 여백을 프롬프트로 확보: 내레이션 컷은 `character in the lower half, upper 40% empty`.
- 생성: `python scripts/gen_image.py --prompt-file prompts/cutN.txt --ref assets/samples/bori-sheet2-high.png --ref assets/ref/kkamja-1.jpg --ref assets/ref/kkamja-2.jpg --out img/cutN.png` — 컷 `medium`, 표지 `high`. `.env` 로드 필요(`docs/env-setup.md`).

## 3. 텍스트 합성

- `episodes/epNN/compose.html` — 슬라이드 8장을 각각 1080×1350 `<section>`으로. 이미지는 1024×1536 생성본을 중앙 1024×1280 크롭(`object-fit:cover`).
- 폰트: `assets/fonts.md` 후보 중 지정(확정 전) 또는 확정 폰트. `@font-face`는 `assets/fonts.html`에서 복사.
- 표지: 제목 3줄 이내, 핵심 단어 `<b>`로 포인트 컬러, 부제 회색 소문자.
- 컷: 상단 내레이션 1–2줄. 속마음은 캐릭터 옆에 작은 회색 글자, 말풍선·박스 없이.
- Playwright MCP로 각 `<section>`을 `img/slideN.png`로 스크린샷 (viewport 1080×1350, `clip`). MCP 브라우저가 사용 중이면 `chrome-headless-shell.exe --headless --window-size=1080,1350 --virtual-time-budget=10000 --screenshot=img/slideN.png compose.html?only=N` (N은 0부터; `?only`는 compose.html에 그 슬라이드만 남기는 스크립트로 처리).
- 이미지 크롭은 `object-position:50% 100%`(하단 기준)로 발이 안 잘리게 하고, 표지는 `object-fit:contain`.
- 속마음 등 그림 옆 텍스트는 `python scripts/art_bbox.py img/cutN.png`로 그림 영역을 잰 뒤 그 밖에 놓는다. 프롬프트의 "상단 40% 비움"은 대략만 지켜지고(30~47%), 글자 폭은 폰트마다 달라 눈대중으로 두면 겹친다.

## 4. 산출물과 마무리

```
episodes/epNN/
  conti.md        제목·부제·컷별 [장면 / 내레이션 / 속마음 / 프롬프트 요점]
  prompts/cutN.txt
  img/cutN.png, slideN.png
  compose.html
  preview.html    슬라이드 8장 세로 나열 (모바일 확인용)
  caption.txt     캡션 1–2줄 + 고정 해시태그
```

- 고정 해시태그: `#당신은약간초능력자 #INFP(해당 유형) #인스타툰 #일상툰 #MBTI툰`
- `index.html` 콘티 프리뷰 섹션에 카드 추가 → 커밋. **푸시는 사용자 확인 후.**

## 5. 체크리스트 (커밋 전)

- [ ] 제목이 단점을 능력처럼 말하는가, 시리즈명이 표지에 없는가
- [ ] 4컷이 친구에게 보낼 만큼 구체적인가 / 7컷이 저장할 만한 한 문장인가
- [ ] 생성 이미지에 글자·말풍선이 없는가, 보리 색·눈·입 없음이 유지되는가
- [ ] 8장 전부 1080×1350, 텍스트가 잘리지 않는가
