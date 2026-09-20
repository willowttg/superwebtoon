---
name: make-episode
description: 「작은 힘에도 작은 책임은 따른다」 에피소드 1편 제작 — MBTI 유형의 단점을 초능력으로 재해석한 표지 + 7컷 캐러셀. 콘티 → 컷 이미지 생성 → 텍스트 합성 → 프리뷰 → 캡션. "에피소드 만들어", "EP.02", "INTJ 편", "콘티 짜줘", "컷 생성" 등에 사용.
---

# make-episode

입력: MBTI 유형 1개 (+ 선택: 다룰 단점 특징, 폰트 지정). 산출물은 `episodes/epNN/`.

## 1. 기획 규칙

- **제목** = 그 유형의 통용되는 단점을 능력처럼 바꾼 후킹 카피. 형식 `[…] 초능력`. 예: INFP 「알고 싶지 않은 마음까지 읽을 수 있는 초능력」. 시리즈명을 에피소드 제목 위에 작게 `- 작은 힘에도 작은 책임은 따른다 -`(앞뒤 하이픈)로 넣는다.
- **MBTI는 작품 어디에도 쓰지 않는다** (표지·컷·캡션·해시태그). 유형은 기획 입력값일 뿐이다.
- 내용은 해당 유형 독자가 "이거 나잖아"라고 느껴야 한다. 유형 밈이 아니라 **구체적 상황**(약치기그림식)으로 쓴다.
- 내레이션·속마음은 **1인칭 "나는 …"**. "우리는"·3인칭 설명("이 유형은 …")은 쓰지 않는다. 내레이션은 **컷당 2줄 고정**(긴 줄은 합성 시 자동 축소). CTA만 독자에게 말한다. 어미는 문어체·구어체를 섞어 리듬을 준다("…한다!", "…않을래.").
- **속마음 대사를 적극 쓴다.** 필수는 아니지만 내레이션만으로 끝내는 컷을 기본값으로 두지 않는다 — 상황이 있는 컷(2–6)은 캐릭터 옆에 짧은 속마음 한 줄을 붙일 수 있는지 먼저 살핀다. 내레이션은 상황을, 속마음은 그 순간의 감정·본심을 맡아 둘이 겹치지 않게 한다. 조연 대사도 같은 방식으로 캐릭터 옆에 놓는다.
- **이모지 금지** (컷·캡션·CTA 전부).
- **표지 + 7컷 = 8장** (인스타 상한).

| 컷 | 역할 | 비고 |
|---|---|---|
| 표지 | 시리즈명(작게) + 제목 + 두부 (에피소드 소품, POWER ACTIVATED 포즈) | 제목의 핵심 단어 1개만 포인트 컬러 |
| 1 | 초능력 설명 — "나는 ○○이 된다" | 담담한 내레이션 |
| 2–3 | 장점 — 능력이 남에게 좋게 작용하는 장면 | 조연이 수혜자 |
| 4 | **단점 첫 등장 = 공유 유도 컷.** 가장 구체적이고 찔리는 상황 | "이거 너잖아" 하고 친구에게 보내게 되는 컷. 여기에 가장 공을 들인다 |
| 5–6 | 단점 심화 — 힘들고 불편한 부분 | 5는 상황, 6은 속마음 |
| 7 | 마무리 = **저장 유도 문장** + 태그 CTA | "그래도 그 능력 덕분에 누군가는…" 한 줄 위로 → "당신 옆의 초능력자를 태그해 주세요" |

톤 전환: 1–3 밝음 → 4–6 저채도·먹구름 → 7 망토 + 포인트 컬러 복귀.

## 2. 이미지 규칙

- 생성은 **캐릭터 + 소품만**. 프롬프트 끝에 항상 `No text, no letters, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies.` (접지 그림자는 EP.03부터. 공중에 뜬 캐릭터는 그 컷 프롬프트에서 제외 명시.) 말풍선 꼬리가 캐릭터와 안 맞는 문제가 있어 **말풍선은 절대 그리지 않는다** — 속마음도 텍스트 합성으로.
- 참조: 등장 캐릭터 시트 `assets/samples/<이름>-sheet-high.png`(두부 dubu, 미숙 misook, 덕수 deoksu, 콩 kong, 탱자 tangja, 소라 sora, 밤톨 bamtol) → **2명 이상 동시 출연이면** `python scripts/lineup.py dubu misook --out ref/lineup.png`로 그 컷의 캐릭터만 담은 크기 라인업을 만들어 다음 참조로 . **깜자 스타일 이미지는 캐릭터 시트 제작용이지 컷 생성엔 넣지 않는다** (시트가 이미 그 문법을 담고 있음). 각 시트 프롬프트(`<이름>-sheet-prompt.txt`)의 design 블록을 프롬프트 헤더로 복사하고, 라인업이 있으면 "the lineup image shows their relative sizes"를 덧붙인다.
- 캐스트·크기·색은 `assets/characters.md` 1절.
- **군중·행인(이름 없는 다수)은 시트 없이 프롬프트 문구를 고정**해서 그린다 (참조 이미지가 늘수록 결과가 흐려짐): `a crowd of many small featureless people-shaped silhouettes in flat medium gray, no faces, no details` — 사람 형태여도 된다. 대사·속마음이 있는 엑스트라만 종을 정해 시트를 만든다.
- 초능력 발동(표지·2–3·7): 에피소드 소품 + 반짝이. 소품은 `assets/props.md`에서 기존 편과 종류·색이 겹치지 않게 정하고 콘티 전에 표에 추가한다. 색은 크림색 몸과 대비되게 **화려해도 좋다**(EP.01 연두+보라 선글라스). 착용 위치를 프롬프트에 명시(선글라스는 눈을 덮게). **소품은 매 컷 넣지 않고 장면에 필요한 컷에만** 쓰며, 콘티 상단에 쓰는 컷 번호를 적는다. 7컷 망토 `#C77B3F`는 공통. 단점 컷(4–6): 감정 기호. **감정 기호(먹구름·땀방울·낙서 소용돌이·세로 그늘선·눈물·하트·반짝이 등)는 한 에피소드 안에서 컷마다 다른 것을 쓰고 중복시키지 않는다** — 콘티의 속마음 열에 `감정: ○○`로 컷별 배정을 적고 프롬프트에 그 하나만 넣는다. 먹구름은 편당 1컷까지.
- **밈·명장면 활용**: 콘티에서 내레이션을 다 쓴 뒤, 장면 구상 전에 `assets/memes.md`를 한 번 훑어 상황에 맞는 것이 있으면 캐릭터 연기·구도로 옮긴다(그림 쪽만, 내레이션엔 안 씀. 억지로 끼우지 않음. **밈을 모르는 독자에게도 장면이 성립해야 한다** — 밈은 덤이지 장면의 전제가 아니다). 프롬프트 요점에 `밈: ○○`로 적고, 쓴 항목은 `memes.md`에서 지워 `memes-used.md`로 옮긴다(한 번 쓴 밈은 다른 컷·에피소드에서 재사용 금지). 웹 검색은 하지 않는다 — 리스트는 매월 갱신.
- **사회생활 컷**: 캐릭터가 겉으로 웃거나 예의상 멘트를 하는데 진짜 속마음이 다르면, 그림에 속마음 장치를 함께 넣는다 — 등 뒤로 숨긴 손의 주먹·브이, 살랑거리는 꼬리, 등 뒤로 새는 반짝이, 작은 생각 구름(안의 글자는 합성) 등. 콘티 속마음 열에 `속마음 장치: ○○`로 적는다.
- **구도 다양화**: 정면 나열(테이블 뒤에 일렬로 앉아 카메라를 보는 식)이 기본값이 되지 않게 한다. 콘티 프롬프트 요점에 `구도: ○○`로 컷별 배정을 적고, 프롬프트 첫 문장에 카메라를 명시한다 — 예: 측면(side view, profile), 3/4 뒤에서(seen from behind over Dubu's shoulder), 약간 위에서 내려다봄(high angle looking down at the table), 낮은 앵글(low angle from floor level), 얼굴·소품 클로즈업(extreme close-up on the menu and her hands), 한 명만 크게 + 나머지 멀리(Dubu large in the foreground, others small in the back). 정면 구도는 **편당 표지 포함 3컷 이하**, 같은 구도가 연속 두 컷에 오지 않게 한다. 좌석 배치·소품 위치가 앵글에 따라 바뀌므로 그 컷의 참조 시트는 그대로 두되 lineup 이미지는 크기 참고용임을 문구로 남긴다.
- 텍스트가 들어갈 여백을 프롬프트로 확보: 내레이션 컷은 `character in the lower half, upper 40% empty`.
- 생성: `python scripts/gen_image.py --prompt-file prompts/cutN.txt --ref assets/samples/dubu-sheet-high.png [--ref assets/samples/misook-sheet-high.png --ref ref/lineup.png] --out img/cutN.png` — 표지 포함 **전부 `medium`** (`high` 금지). `.env` 로드 필요(`docs/env-setup.md`).

## 3. 텍스트 합성

- `episodes/epNN/compose.html` — 슬라이드 8장을 각각 1080×1350 `<section>`으로. 이미지는 1024×1536 생성본을 중앙 1024×1280 크롭(`object-fit:cover`).
- 폰트: 본문(내레이션·속마음·CTA) **교보손글씨 2019** 확정, 내레이션은 가운데 정렬. 표지 제목은 미확정(현재 나눔손글씨 펜). `@font-face`는 `assets/fonts.html`에서 복사.
- 표지: 제목 3줄 이내, 핵심 단어 `<b>`로 포인트 컬러. 시리즈명과 제목 사이 약간의 행간(시리즈명 top 84px/44px, 제목 top 166px).
- 컷: 상단 내레이션, **줄바꿈은 콘티에 적힌 그대로** (임의로 줄 수를 늘리지 않는다). 크기는 레퍼런스 실측(솜비 글자 높이 56px, 서밤 40px) 기준 내레이션 **56px**, 긴 줄은 그 슬라이드만 폭에 맞춰 자동 축소. 속마음·대사 **40px** 회색, 말풍선·박스 없이 캐릭터 옆에. CTA 38px.
- Playwright MCP로 각 `<section>`을 `img/slideN.png`로 스크린샷 (viewport 1080×1350, `clip`). MCP 브라우저가 사용 중이면 `chrome-headless-shell.exe --headless --window-size=1080,1350 --virtual-time-budget=10000 --screenshot=img/slideN.png compose.html?only=N` (N은 0부터; `?only`는 compose.html에 그 슬라이드만 남기는 스크립트로 처리).
- 이미지 크롭은 `object-position:50% 100%`(하단 기준)로 발이 안 잘리게 하고, 표지는 `object-fit:contain`. 그림은 **80%로 축소**해 하단 60px·좌우 여백을 두고(`transform:scale(.8)`, 하단 기준), 모든 컷 동일 적용 — 군중처럼 프레임에 닿는 컷도 예외 없음.
- 속마음 등 그림 옆 텍스트는 `python scripts/art_bbox.py img/cutN.png`로 그림 영역을 잰 뒤 그 밖에 놓는다. 프롬프트의 "상단 40% 비움"은 대략만 지켜지고(30~47%), 글자 폭은 폰트마다 달라 눈대중으로 두면 겹친다.

## 4. 산출물과 마무리

```
episodes/epNN/
  conti.md        제목·컷별 [장면 / 내레이션 / 속마음 / 프롬프트 요점]
  prompts/cutN.txt
  img/cutN.png, slideN.png
  compose.html
  preview.html    슬라이드 8장 세로 나열 (모바일 확인용)
  caption.txt     한 줄 후킹 질문 "[제목]을 가진 당신, 오늘도 ○○하진 않았나요?" → 해시태그 (내레이션 전문 넣지 않음)
```

- 고정 해시태그: `#작은힘에도작은책임은따른다 #인스타툰 #일상툰 #공감툰` (MBTI 관련 태그 없음)
- `index.html` 콘티 프리뷰 섹션에 카드 추가 → 커밋 → **즉시 `git push origin HEAD:master`** (확인 없이). 결과는 Pages 링크로 전달.
- 인스타 게시는 `instagram` 스킬 (`scripts/ig.py export` → 푸시 → `publish`).

## 5. 체크리스트 (커밋 전)

- [ ] 제목이 단점을 능력처럼 말하는가, 시리즈명이 표지에 없는가
- [ ] 4컷이 친구에게 보낼 만큼 구체적인가 / 7컷이 저장할 만한 한 문장인가
- [ ] 생성 이미지에 글자·말풍선이 없는가, 캐릭터 색·눈·입 없음·상대 크기가 유지되는가, 접지 그림자가 전 컷에 있고 몸에 명암은 없는가
- [ ] 정면 구도가 3컷 이하이고 같은 구도가 연속되지 않는가
- [ ] 8장 전부 1080×1350, 텍스트가 잘리지 않는가
- [ ] 쓴 밈이 `memes.md`→`memes-used.md`로 이관됐는가
