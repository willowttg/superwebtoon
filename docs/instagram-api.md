# 인스타 API 관리

`scripts/ig.py` 하나로 게시·댓글·인사이트를 다룬다. Meta 의 **Instagram API with Instagram Login** (페이스북 페이지 불필요).

## 1회 설정

1. 인스타 계정을 **프로페셔널(크리에이터)** 로 전환: 앱 > 설정 > 계정 유형 및 도구.
2. https://developers.facebook.com/apps → 앱 만들기 → 사용 사례 "Instagram 비즈니스 관리" (또는 Other → Business) → 제품 **Instagram** 추가.
3. 앱 대시보드 > Instagram > **API setup with Instagram business login**
   - 1단계 "Generate access tokens": 인스타 계정 추가 (계정 쪽에서 초대 수락 필요).
   - 3단계 "Set up Instagram business login" > Business login settings: **OAuth redirect URIs** 에 `https://willowttg.github.io/superwebtoon/` 등록.
   - 같은 화면의 **Instagram app ID / app secret** 을 `.env` 의 `IG_APP_ID` / `IG_APP_SECRET` 에.
4. 토큰 발급 (둘 중 하나)
   - **A. 대시보드에서 바로**: 1단계 계정 옆 "Generate token" → 나온 장기 토큰을 `.env` `IG_ACCESS_TOKEN` 에 붙여넣고 `python scripts/ig.py me` (IG_USER_ID 자동 저장).
   - **B. OAuth**: `python scripts/ig.py auth-url` → 브라우저에서 승인 → 리디렉션된 주소의 `code=` 값 → `python scripts/ig.py auth <code>`. 토큰과 user id 가 `.env` 에 저장된다.
5. 앱이 개발 모드여도 앱 역할(테스터)이 있는 자기 계정에는 전부 동작한다. 앱 검수 불필요.

## 운용

```bash
python scripts/ig.py me                    # 계정·팔로워 확인
python scripts/ig.py export ep01           # slideN.png → slideN.jpg  (커밋·푸시 → Pages 반영 1~2분)
python scripts/ig.py publish ep01 --dry-run
python scripts/ig.py publish ep01          # 캐러셀 8장 + caption.txt 게시 → episodes/ep01/ig.json
python scripts/ig.py comments ep01         # 댓글 / reply <id> "…" / hide <id>
python scripts/ig.py insights ep01         # reach·views·saved·shares·follows 등
python scripts/ig.py insights account      # 계정 일간 reach·팔로워
python scripts/ig.py refresh               # 토큰 60일 만료 전 갱신 (24h 지난 뒤 가능)
```

- 인스타는 **JPEG 공개 URL** 만 받는다. PNG 는 거부 → `export` 로 JPG 를 만들어 Pages 에 올린다.
- 캐러셀 한도: 한 게시물 10장, API 게시 하루 100건. 캡션 2200자·해시태그 30개.
- 실패 시 `HTTP 400 ... code 190` 은 토큰 만료 → `refresh` 또는 재발급. `code 9` 는 하루 게시 한도.
- 앱 시크릿·토큰은 `.env` 에만. 유출 시 대시보드에서 시크릿 재설정(토큰 전부 무효화).
