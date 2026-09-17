# 영상툰 제작 비용 절감 — 다각 검토

> **결정 (2026-09-17): 영상툰은 기각.** 비용 부담으로 제작하지 않는다. 정적 캐러셀만 발행한다. 아래는 검토 기록으로만 남긴다.

기준: 한 편 = 표지 + 6컷, 릴스 30초 내외, 세로 9:16. 가격은 2026-09 시점 공개 자료 기준 (출처 하단).

## 0. 진단 — 왜 비싼가

30초짜리 릴스를 **생성형 비디오 API로 통째로** 만들면:

| 모델 | 단가 | 30초 | 재생성 3회 포함 |
|---|---|---|---|
| Veo 3.1 (오디오 포함) | $0.75/초 | $22.5 | **$67** |
| Sora 2 Pro | $0.30~0.50/초 | $9~15 | $27~45 |
| Kling 3.0 | $0.07~0.14/초 | $2~4 | $6~13 |

게다가 생성형 비디오는 (1) 캐릭터 일관성이 컷마다 깨지고, (2) 자막·나레이션을 얹기 위해 어차피 후편집이 필요하며, (3) 실패율 때문에 재생성 배수가 크다. **비용의 90%는 "필요 없는 생성형 비디오"에서 나온다.**

핵심: 영상툰(키크니 등)은 **정적 컷 + 팬/줌 + 자막 + 나레이션 + BGM**이다. 생성형 비디오가 아니라 *모션 그래픽*이다. 정적 캐러셀용 컷 이미지는 이미 만들고 있으니, 영상은 그 재활용이어야 한다.

## 1. 해결책 — 축별 검토

### A. 생성형 비디오를 빼고 프로그래밍 모션으로 조립 (1순위)

이미 만든 7장 이미지에 Ken Burns(팬/줌), 컷 전환, 자막 타이밍, 포인트 컬러 컷의 이펙트(망토 펄럭임·빛)를 코드로 입힌다.

- **Remotion** (React, Node 24 설치돼 있음): 프레임 단위 정밀 제어, 개인/3인 이하 무료. 한 편 렌더 = 로컬 CPU 수십 초, **$0**.
- **HTML/CSS 애니메이션 → Playwright 녹화**: `conti-preview.html` 방식의 연장. 이미 갖춘 도구로 가장 빠르게 시작 가능하나 프레임 드롭·오디오 싱크가 약함. 프로토타입용.
- **ffmpeg 단독** (zoompan·xfade·subtitles 필터): 의존성 최소. 표현력이 낮아 "이펙트" 컷이 밋밋함.

→ **Remotion 추천.** 한 번 템플릿을 만들면 이후 매 편은 이미지 7장 + 나레이션 텍스트만 넣으면 끝. 재시도 비용 0이라 연출을 무한히 다듬을 수 있다.

### B. 나레이션·BGM은 사실상 무료

| 항목 | 선택지 | 편당 비용 |
|---|---|---|
| 나레이션 TTS | OpenAI `gpt-4o-mini-tts` $0.015/분 | **~$0.01** |
| | edge-tts (MS, 비공식·무료, 한국어 SunHi/InJoon) | $0 |
| | ElevenLabs 무료 10k자/월 → 편당 ~200자면 50편 | $0 |
| BGM | **인스타 앱에서 업로드 시 인스타 음원 붙이기** — 트렌딩 오디오가 도달에 유리, 저작권 문제 없음 | $0 |
| | 파일에 직접 넣어야 하면 Pixabay/YouTube 오디오 라이브러리 | $0 |

→ 나레이션은 `gpt-4o-mini-tts`(이미 OpenAI 키 있음)로 고정. BGM은 파일에 굽지 말고 인스타에서 붙이는 것을 기본으로 (릴스 알고리즘 관점에서도 이쪽이 정석).

### C. 생성형 비디오는 "반전 컷 1개, 3~5초"로 한정

3컷(망토 등장) 같은 하이라이트 하나만 Image-to-Video로 살리면 "AI 영상" 느낌은 확보하면서 비용은 무시할 수준이 된다. 나머지 컷은 A로.

| 모델 (I2V, 5초) | 단가 | 클립당 | 비고 |
|---|---|---|---|
| Hailuo 02 Standard 768p | $0.045/초 | **$0.23** | 최저가, 2D 일러스트 모션 무난 |
| Wan 2.5 | $0.05/초 | $0.25 | |
| Kling 3.0 (오디오 off) | $0.07/초 | $0.35 | 모션 품질 상위 |
| Runway Gen-4 Turbo | $0.05/초 | $0.25 | |
| Veo 3.1 | $0.75/초 | $3.75 | **사용 금지** — 이 용도엔 15배 비쌈 |

재생성 3회 잡아도 편당 **$1 미만**. fal.ai에서 위 모델들을 한 키로 쓸 수 있다.

### D. 로컬 GPU (RTX 4060 8GB) — 조건부

- Wan 2.2 14B rapid-distilled + `--lowvram`: 2초 클립 ≈ 111초. 5B fp8는 8GB에 들어가지만 12분/클립 수준으로 느림.
- 품질·시간 대비 API 클립 $0.25가 낫다. **C의 클립을 밤에 배치로 여러 후보 뽑는 용도**라면 의미 있음. 지금 단계에선 세팅 비용(ComfyUI 구성) 대비 이득 없음 → 보류.

### E. 낭비 제거 — 프로세스

유료 호출은 "확정된 것"에 대해 1회만. 확정은 무료 단계에서 끝낸다.

1. 콘티 HTML 프리뷰(무료)에서 대사·자막 타이밍·컷 길이 확정
2. 이미지: `gpt-image-1-mini` / quality `low`로 구도 검증 → 확정 후 `high` 1회
3. 영상 조립(A)은 무료이므로 여기서 연출을 반복
4. 생성형 클립(C)은 확정된 high 이미지로만, 후보 2개까지
5. 나레이션은 텍스트 확정 후 1회

이미지 비용이 이제 지배 항목이 된다 (gpt-image-1 high 세로 ≈ $0.25/장 → 7장 ≈ $1.75). 캐릭터 시트를 고정해 재생성 횟수를 줄이는 것이 다음 절감 포인트.

### F. 구독 vs API

Kling/Hailuo 월 구독(≈$10/월)은 월 30클립 넘게 뽑을 때만 유리. 자동화 파이프라인엔 종량제 API가 맞고, C 수준(편당 1~3클립)이면 월 몇 달러라 구독이 오히려 손해.

## 2. 편당 비용 비교

| 구성 | 이미지 | 영상 | 나레이션 | 합계 |
|---|---|---|---|---|
| 현재 우려 (Veo로 전체) | $1.75 | $22~67 | — | **$25~70** |
| A+B (모션 조립만) | $1.75 | $0 | $0.01 | **≈$1.8** |
| A+B+C (하이라이트 1클립) | $1.75 | $0.25~1 | $0.01 | **≈$2~3** |

주 2편 발행 시 월 $15~25. 이미지 재생성까지 포함해도 $30 안쪽.

## 3. 결론

1. **생성형 비디오를 기본 파이프라인에서 제거.** 영상툰 = 정적 컷의 모션 조립.
2. **Remotion 템플릿**을 한 번 만든다: 세로 1080×1920, 컷당 3~5초, 상단 자막, Ken Burns, 포인트 컬러 컷 이펙트, 마지막 CTA. 이후 편당 재료는 이미지 7장 + 텍스트.
3. 나레이션 `gpt-4o-mini-tts`, BGM은 인스타에서.
4. 반전 컷 1개만 Hailuo/Wan I2V(5초, ~$0.25)로 선택적 강화. Veo/Sora는 쓰지 않는다.
5. 로컬 GPU·구독은 물량이 생기면 재검토.

다음 스텝: 로드맵 2번(생성 파이프라인 스킬)에 "영상 조립" 단계를 Remotion으로 넣고, EP.01 컷 이미지가 나오면 그걸로 첫 템플릿을 만든다.

### 출처
- [AI Video API Pricing 2026 — Apiframe](https://apiframe.ai/blog/ai-video-api-pricing-2026)
- [Veo 3.1 vs Kling 3.0 vs Sora 2 — ModelsLab](https://modelslab.com/blog/api/veo-3-1-vs-kling-3-sora-2-ai-video-api-cost-2026)
- [AI Video API Pricing (July 2026) — buildmvpfast](https://www.buildmvpfast.com/api-costs/ai-video)
- [Cheapest AI Video Generators 2026 — AVB](https://aivideobootcamp.com/blog/cheapest-ai-video-generators-2026/)
- [fal.ai 가격 — costbench](https://costbench.com/software/ai-media-apis/fal-ai/), [CloudPrice](https://cloudprice.net/models/providers/fal)
- [WAN 2.2 I2V on RTX 4060 8GB — lilting](https://lilting.ch/en/articles/wan22-comfyui-rtx4060-i2v)
- [Wan 2.2 TI2V 5B VRAM — WillItRunAI](https://willitrunai.com/video-models/wan-video-2-2-ti2v-5b)
- [OpenAI API Pricing](https://developers.openai.com/api/docs/pricing), [gpt-4o-mini-tts 단가 — TokenMix](https://tokenmix.ai/blog/gpt-4o-mini-tts-cheapest-tts-api-2026)
- [ElevenLabs Pricing](https://elevenlabs.io/pricing)
