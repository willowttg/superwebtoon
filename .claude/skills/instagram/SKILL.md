---
name: instagram
description: 인스타 계정 API 관리 — 에피소드 캐러셀 게시, 댓글 확인·답글·숨김, 인사이트 조회, 토큰 갱신. "인스타에 올려", "EP.01 게시", "댓글 확인", "인사이트", "토큰 갱신" 등에 사용.
---

# instagram

도구: `python scripts/ig.py` (사용법은 `--help`, 설정은 `docs/instagram-api.md`). `.env` 는 본 저장소 것을 자동으로 찾는다 (워크트리 포함).

## 게시

1. `export epNN` → `episodes/epNN/img/slideN.jpg` 생성 → 커밋·푸시 (Pages 반영 1~2분).
2. `schedule epNN --dry-run` 으로 URL 8개·캡션·예정 시각 확인. 기본은 다음 빈 21:00 KST 슬롯(하루 한 편, 월·목 권장) — 사용자가 시각을 말하면 `--at`.
3. **실제 `schedule`(또는 즉시 `publish`) 은 사용자 확인 후.** `schedule.json` 커밋. 게시 뒤 `ig.json` 이 생기면 커밋.
4. `queue` 로 현황. 작업이 「없음」이면 PC 재부팅 등으로 사라진 것 — 다시 `schedule`.

## 관리

- `comments epNN` → 답글은 1인칭·이모지 금지 규칙 그대로. 답글 문구는 사용자에게 보여주고 승인 후 `reply`.
- `insights epNN` / `insights account` — 숫자를 표로 요약해 전달.
- `HTTP 400 code 190` → `refresh` 시도, 실패하면 재발급 안내 (docs/instagram-api.md 4단계).
