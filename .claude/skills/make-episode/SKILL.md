---
name: make-episode
description: 「작은 힘에도 작은 책임은 따른다」 에피소드 1편 제작 — MBTI 유형의 단점을 "초능력자 특징"으로 나열한 표지 1 + 특징 컷 5 = 6장 캐러셀. 특징 리스트 → 컷 이미지 생성 → 텍스트 합성 → 프리뷰 → 캡션. "에피소드 만들어", "EP.02", "INTJ 편", "콘티 짜줘", "컷 생성" 등에 사용.
---

# make-episode

입력: MBTI 유형 1개 (+ 선택: 다룰 특징, 폰트 지정). 산출물은 `episodes/epNN/`. **EP.01~06은 이전 포맷이라 예시·템플릿으로 쓰지 않는다** — 참조는 EP.07부터.

## 1. 기획 규칙

- **구성 = 표지 1 + 특징 컷 5 = 6장.** 표지: 제목(초능력 이름) + 두부 그림. 특징 컷: 번호 + 특징 한 줄 + 그 특징을 한 단계 과장한 그림 1장. 컷끼리 서사로 잇지 않고 나열한다. 순서는 가장 보편적으로 찔리는 것부터, 설명이 필요한 것은 뒤로.
- **제목** = 그 유형의 통용되는 단점을 능력처럼 바꾼 후킹 카피. 형식 `[…] 초능력자 특징`. 예: 「No를 Yes로 바꿔 말하는 초능력자 특징」. 핵심 구절만 포인트 컬러 볼드.
- **특징 문장**은 짧은 음슴체 한 줄 (`보험 100개 있음`, `스팸 전화 못 끊음`). 캐릭터 이름 금지(할머니·동생·친구 등 관계어), 느낌표·이모지 금지. MBTI는 작품 어디에도 쓰지 않는다.
- **그림이 펀치다.** 특징 문장을 가리고 그림만 봐서 웃기지 않으면 삽화다 — 과장 장치를 넣거나 특징을 바꾼다. 조연은 그 특징이 드러나는 상황을 공급한다(콩 = 눈치 없는 한마디, 탱자 = 오지랖, 할머니 = 거절 못 하는 호의).
- **대사·속마음**은 캐릭터 옆에 짧게 (`중요한 전화야?`, `재밌어요`). 특징 문장과 같은 정보를 반복하지 않는다.
- **콘티 보고.** 채팅에 컷별 [장면 / 특징 / 대사] 세 열을 모두 담은 표로 보고한다 — 열 생략 금지. 표 승인 후 생성.
- **독립 리뷰 (Codex, 1회).** `python scripts/review_conti.py epNN` → `episodes/epNN/review.md`. 항목마다 반영 또는 `→ 기각: 이유`를 붙이고 커밋.

## 2. 이미지 규칙

- 생성은 **캐릭터 + 소품만**. 프롬프트 끝에 항상 `No text, no letters, no speech bubbles, no captions. Plain white background. One flat light-gray #E6E6E6 ellipse on the ground under each standing character and under any large object resting on the ground, as a contact shadow; no other shadows, no shading on the bodies.` (공중에 뜬 캐릭터는 제외 명시.) **말풍선은 절대 그리지 않는다** — 대사도 텍스트 합성.
- 참조: 등장 캐릭터 시트 `assets/samples/<이름>-sheet.png`(두부 dubu, 미숙 misook, 덕수 deoksu, 콩 kong, 탱자 tangja, 소라 sora, 밤톨 bamtol, 할머니 halmoni) → **2명 이상 동시 출연이면** `python scripts/lineup.py dubu kong --out ref/lineup.png`로 크기 라인업을 만들어 다음 참조로. 깜자 이미지는 컷 생성에 넣지 않는다. 각 시트 프롬프트(`<이름>-sheet-prompt.txt`)의 **LINE QUALITY 블록과 design 블록**을 프롬프트 헤더로 복사하고, 라인업이 있으면 "the lineup image shows their relative sizes"를 덧붙인다.
- 캐스트·크기·색은 `assets/characters.md` 1절. **캐릭터 색은 hex로 고정** — design 블록에 시트 hex를 적고 생성 후 `python scripts/check_colors.py img/cutN.png dubu kong`으로 잰다. 시트 hex ±12 안의 영역이 없으면 재생성.
- **군중·행인**은 시트 없이 고정 문구: `a crowd of many small featureless people-shaped silhouettes in flat medium gray, no faces, no details`. 대사가 있는 엑스트라만 종을 정해 시트를 만든다.
- 표지: 두부 + 망토 `#C77B3F`, 소심하게 긴장한 자세. 특징 컷은 감정 기호(땀방울·눈물·낙서 소용돌이·세로 그늘선·하트·반짝이) 자유. **먹구름은 쓰지 않는다.**
- **밈·명장면**: 특징을 정한 뒤 `assets/memes.md`를 한 번 훑어 맞는 것이 있으면 연기·구도로 옮긴다(억지로 끼우지 않음, 밈 모르는 독자에게도 성립해야 함). 프롬프트 요점에 `밈: ○○`, 쓴 항목은 `memes-used.md`로 이관(재사용 금지). 웹 검색 금지.
- **속마음 장치**: 겉으로 웃는데 속이 다르면 그림에 장치를 넣는다 — 등 뒤 주먹, 살랑거리는 꼬리, 찡그린 얼굴로 댓글 달기 등. 콘티 대사 열에 `장치: ○○`.
- **구도 다양화**: 프롬프트 요점에 `구도: ○○`를 적고 첫 문장에 카메라를 명시(side view / from behind over the shoulder / high angle / low angle / close-up / one large in foreground). 정면 구도 편당 3컷 이하, 같은 구도 연속 금지.
- 배경 흰색, 소품 1~2개로 장소를 표현한다(바닷가 = 파라솔 + 튜브). 텍스트 여백: `character in the lower half, upper 40% empty`.
- 생성: `python scripts/gen_image.py --prompt-file prompts/cutN.txt --ref assets/samples/dubu-sheet.png [--ref …-sheet.png --ref ref/lineup.png] --out img/cutN.png` — **전부 `medium`**. `.env` 로드 필요(`docs/env-setup.md`).

## 3. 텍스트 합성

- `episodes/epNN/compose.html` — 슬라이드 6장을 각각 1080×1350 `<section>`으로. 이미지는 1024×1536 생성본을 중앙 1024×1280 크롭(`object-fit:cover`, `object-position:50% 100%`), **80%로 축소**해 하단 60px·좌우 여백.
- 폰트: **교보손글씨 2019**, `@font-face`는 `assets/fonts.html`에서 복사.
- 표지(slide1): 시리즈명 `.series`(top 40px, 34px 회색) + 제목 상단 가운데 큰 글씨(72px 내외, 2~3줄), 핵심 구절 `<b>`로 포인트 컬러 볼드. 두부 그림 아래.
- 특징 컷(slide2~6): 상단에 `N. 특징 문장` **56px** 가운데 정렬, 긴 줄은 그 슬라이드만 자동 축소. 대사·속마음 **40px** 회색, 박스 없이 캐릭터 옆 — `python scripts/art_bbox.py img/cutN.png`로 그림 영역을 잰 뒤 그 밖에 놓는다.
- 마지막 슬라이드 하단(bottom 44px)에 CTA 40px 볼드 포인트 컬러, 양옆 활자 `♥`: "당신 곁의 두부를 태그해 주세요". 스타일은 `episodes/ep07/compose.html`을 템플릿으로 복사.
- Playwright MCP로 각 `<section>`을 `img/slideN.png`(N=1..6)로 스크린샷 (viewport 1080×1350, `clip`). MCP 브라우저 사용 중이면 `python scripts/shoot_slides.py epNN`.

## 4. 산출물과 마무리

```
episodes/epNN/
  conti.md        제목·컷별 [장면 / 특징 / 대사 / 프롬프트 요점]
  review.md       Codex 독립 리뷰 + 반영/기각 표기
  prompts/coverN.txt, cutN.txt
  img/cover.png, cutN.png, slideN.png
  compose.html
  preview.html    슬라이드 6장 세로 나열 (모바일 확인용)
  caption.txt     한 줄 질문 "몇 개나 해당되나요?" + 특징 5개 목록 → 해시태그
```

- 고정 해시태그: `#작은힘에도작은책임은따른다 #인스타툰 #일상툰 #공감툰` (MBTI 관련 태그 없음)
- `index.html` 콘티 프리뷰 섹션에 카드 추가 → 커밋 → **즉시 `git push origin HEAD:master`** (확인 없이). 결과는 Pages 링크로 전달.
- 인스타 게시는 `instagram` 스킬 (`scripts/ig.py export` → 푸시 → `publish`).

## 5. 체크리스트 (커밋 전)

- [ ] 제목이 단점을 능력처럼 말하고 표지에서 핵심 구절이 포인트 컬러 볼드인가
- [ ] 특징 5개가 각각 친구에게 보낼 만큼 구체적이고, 그림만 봐도 웃긴가
- [ ] 생성 이미지에 글자·말풍선·먹구름이 없는가, 캐릭터 색·눈·입 없음·상대 크기가 유지되는가, 접지 그림자가 있고 몸에 명암은 없는가
- [ ] 정면 구도가 3컷 이하이고 같은 구도가 연속되지 않는가
- [ ] 6장 전부 1080×1350, 텍스트가 잘리지 않는가
- [ ] 쓴 밈이 `memes.md`→`memes-used.md`로 이관됐는가
