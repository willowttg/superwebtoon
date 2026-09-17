# 환경 변수 · API 키 관리

## 설정

```bash
cp .env.example .env
# .env 를 열어 실제 키를 채운다
```

`.env` 는 `.gitignore` 로 막혀 있다. **저장소가 공개이므로 실제 키는 절대 커밋하지 않는다.** `.env.example` 에는 형식만 남긴다.

## 변수

| 변수 | 설명 |
|---|---|
| `OPENAI_API_KEY` | 이미지 생성용. [platform.openai.com/api-keys](https://platform.openai.com/api-keys) 에서 발급 |
| `IMAGE_MODEL` | `gpt-image-1` (기본) / `gpt-image-1-mini` (초안·저비용) |
| `IMAGE_SIZE` | `1024x1536` — 모델이 지원하는 세로 사이즈. 4:5가 아니므로 **1024×1280으로 크롭 후 1080×1350 업스케일**해서 캐러셀에 넣는다 |
| `IMAGE_QUALITY` | `low` / `medium` / `high`. 콘티 검증은 `low`, 발행본은 `high` |
| `OUTPUT_DIR` | 생성 결과 저장 루트 |

## 사용

```bash
set -a && . ./.env && set +a    # 셸에 로드
echo $OPENAI_API_KEY | head -c 12   # 확인 (전체 출력 금지)
```

## 키가 유출됐다면

즉시 [API keys 페이지](https://platform.openai.com/api-keys)에서 해당 키를 revoke 하고 재발급한다. 커밋에 섞여 들어갔다면 키 교체가 먼저이고, 히스토리 정리는 그다음이다.
