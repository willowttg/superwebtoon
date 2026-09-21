"""콘티 독립 리뷰 — Codex CLI(다른 모델)로 conti.md를 읽기 전용 검토.

사용: python scripts/review_conti.py ep07 [--out episodes/ep07/review.md] [--model MODEL]
결과: 지적 사항을 심각도 순으로 담은 마크다운. 작성 세션의 판단은 넘기지 않는다(독립성).
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

PROMPT = """당신은 한국 인스타툰 편집자다. 아래 콘티를 작성자와 무관하게 처음 읽는 독자 겸 편집자로서 검토한다.
모든 파일은 직접 읽어라. 파일을 수정하거나 만들지 말고, 최종 답변만 마크다운(한국어)으로 낸다.

읽을 파일 (순서대로):
1. `.claude/skills/make-episode/SKILL.md`의 `## 1. 기획 규칙` 절 전체 — 검토 기준. (2절 이후는 이미지·합성 규칙이라 참고만.)
2. `assets/characters.md` 1절 — 캐스트 성격·관계. 캐릭터가 성격에 맞지 않는 말·행동을 하는지 본다.
3. `assets/props.md`, `assets/memes-used.md` — 소품·밈이 이전 편과 겹치는지 본다.
4. `episodes/ep01`~ 의 다른 편 `conti.md` — 상황·개그·내레이션이 이전 편과 비슷하면 지적한다.
5. 검토 대상: `{conti}`

검토 관점 (기획 규칙의 항목을 하나씩 대조하되, 규칙에 없어도 독자로서 걸리는 것은 적는다):
- 장점 → 단점 첫 등장 → 단점 심화 흐름. 단점 첫 등장 컷이 "이거 너잖아" 하고 친구에게 보낼 만큼 구체적인가.
- 단점이 능력의 반대가 아니라 같은 능력의 오발동인가. 억지 역접이 없는가.
- 컷마다 웃음 포인트가 있는가. 단점 구간 끝이 우울이 아니라 자폭 개그로 끝나는가.
- 내레이션·속마음이 1인칭이고 사람이 실제로 하는 말인가. SKILL.md의 AI 말투 금지 패턴에 걸리는 줄을 **원문 그대로 인용**해서 지적한다.
- 대사가 내레이션을 반복하지 않는가. 그 캐릭터가 그 순간 실제로 할 법한 길이·어투인가.
- 장면만으로 상황이 성립하는가. 감정 기호 중복, 정면 구도 3컷 초과·연속, 소품 사용 컷 지정 여부.
- MBTI 노출, 이모지, 3인칭 설명, 표지 컷(폐지됨) 같은 금지 사항.
- 그 유형 독자가 "이거 나잖아"라고 느낄 만큼 구체적인가, 아니면 유형 밈 수준인가.

출력 형식:
# EP 리뷰
## 반드시 고칠 것
- **컷N** — 문제 (근거 규칙 한 구절). 수정안: 구체적 대체 문장 또는 장면.
## 고치면 좋은 것
- 같은 형식
## 잘된 점
- 두세 줄, 유지해야 할 강점
## 한 줄 총평
독자로서 저장·태그하고 싶은가, 왜.

규칙: 지적마다 수정안을 반드시 붙인다. 칭찬은 짧게, 지적은 구체적으로. 문제가 없는 항목은 나열하지 않는다.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ep", help="에피소드 폴더명 (예: ep07)")
    ap.add_argument("--out", help="결과 파일 (기본 episodes/<ep>/review.md)")
    ap.add_argument("--model", help="codex 모델 override (기본 ~/.codex/config.toml)")
    args = ap.parse_args()
    for stream in (sys.stdout, sys.stderr):  # Windows 콘솔 cp949 회피
        stream.reconfigure(encoding="utf-8")

    conti = ROOT / "episodes" / args.ep / "conti.md"
    if not conti.exists():
        sys.exit(f"없음: {conti}")
    out = pathlib.Path(args.out) if args.out else conti.parent / "review.md"
    if not shutil.which("codex"):
        sys.exit("codex CLI를 찾을 수 없음 (PATH 확인)")

    cmd = [
        "codex", "exec", "--ephemeral", "-s", "read-only", "--color", "never",
        "-C", str(ROOT), "-o", str(out),
    ]
    if args.model:
        cmd += ["-m", args.model]
    cmd.append("-")  # 프롬프트는 stdin

    prompt = PROMPT.format(conti=conti.relative_to(ROOT).as_posix())
    print(f"codex 리뷰 중... (xhigh 기준 5~10분) -> {out}", flush=True)
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", cwd=ROOT)
    if proc.returncode != 0 or not out.exists():
        sys.exit(f"codex 실패 (exit {proc.returncode})\n{proc.stderr[-2000:]}")
    print(out.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
