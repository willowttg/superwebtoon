---
name: instagram
description: 인스타 계정 API 관리 — 에피소드 캐러셀 게시, 댓글 확인·답글·숨김, 인사이트 조회, 토큰 갱신. "인스타에 올려", "EP.01 게시", "댓글 확인", "인사이트", "토큰 갱신" 등에 사용.
---

# instagram

도구: `python scripts/ig.py` (사용법은 `--help`, 설정은 `docs/instagram-api.md`). `.env` 자동 로드 — 워크트리에는 `.env`가 없으므로 `set -a && . C:/Users/SIJIN/superwebtoon/.env && set +a` 후 실행.

## 게시

1. `export epNN` → `episodes/epNN/img/slideN.jpg` 생성 → 커밋·푸시 (Pages 반영 1~2분).
2. `publish epNN --dry-run` 으로 URL 8개·캡션 확인.
3. **실제 `publish` 는 사용자 확인 후.** 결과 `episodes/epNN/ig.json` 커밋.

## 관리

- `comments epNN` → 답글은 1인칭·이모지 금지 규칙 그대로. 답글 문구는 사용자에게 보여주고 승인 후 `reply`.
- `insights epNN` / `insights account` — 숫자를 표로 요약해 전달.
- `HTTP 400 code 190` → `refresh` 시도, 실패하면 재발급 안내 (docs/instagram-api.md 4단계).
