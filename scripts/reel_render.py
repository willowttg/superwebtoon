"""릴스 렌더 — reel/script.json + reel/tts/(reel_tts.py 결과)로 1080×1920 영상을 만든다. BGM 은 넣지 않는다(인스타 앱에서 인기 음원을 붙인다).

  python scripts/reel_render.py episodes/ep08
타임라인: 대사가 나올 때 그 자막이 뜬다. 특징 자막은 컷 안에서 쌓이고, 대사 자막은 compose.html 위치(pos)를 릴스 좌표로 옮겨 띄운다.
상태마다 reel.html?s=N 을 헤드리스 셸로 찍어(reel/frames/) ffmpeg 으로 이어 붙이고, 음성은 같은 타임라인에 깐다 → reel/reel.mp4
"""
import json, pathlib, subprocess, sys

import numpy as np
import soundfile as sf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from shoot_slides import chrome  # noqa: E402

ART_TOP, SUB_TOP, FPS = 140, 810, 30
SPEED = 1.15  # sohee 기본 속도가 느려서 피치는 두고 빠르게 (ffmpeg atempo)
GAP = {"title": 0.25, "narr": 0.12, "line": 0.3, "cta": 0.3}
LEAD, SLIDE_END, TAIL = 0.1, 0.35, 1.5  # 컷이 바뀌고 첫 말까지, 컷 끝 여운, 마지막 여운
IMG = ["cover", "cut1", "cut2", "cut3", "cut4", "cut5"]


def reel_pos(x, y, w):
    """compose.html(1080×1350, 그림 0.8배 아래 정렬)의 대사 상자 → 릴스(그림 1080폭, 위 ART_TOP)의 가운데 x·위 y"""
    return dict(cx=round(540 + (x + w / 2 - 540) * 1.25), y=round(ART_TOP + 330 + 1290 + (y - 1290) * 1.25))


def fast(src, dst):
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-filter:a", f"atempo={SPEED}", str(dst)], check=True)
    return sf.read(dst, dtype="float32")


def main():
    ep = pathlib.Path(sys.argv[1]).resolve()
    R = ep / "reel"
    S = json.load(open(R / "script.json", encoding="utf-8"))["lines"]

    states, t, voice, sr = [], 0.0, [], None
    for n, L in enumerate(S, 1):
        new_slide = n == 1 or S[n - 2]["slide"] != L["slide"]
        if new_slide:
            if n > 1:
                t += SLIDE_END
            cur = dict(img=IMG[L["slide"]], title=L["slide"] == 0, sub=None, narr=[], lines=[], cta=None)
            start = t  # 컷의 첫 자막은 컷과 함께 뜬다
            t += LEAD
        else:
            cur = json.loads(json.dumps(cur))
            start = t
        k = L["kind"]
        if k == "title" and not new_slide:
            cur["sub"] = L["text"]
        elif k == "narr":
            cur["narr"].append(L["text"])
        elif k == "line":
            cur["lines"].append(dict(text=L["text"], **reel_pos(*L["pos"])))
        elif k == "cta":
            cur["cta"] = L["text"]
        states.append(dict(cur, t=start))
        (R / "tts/fast").mkdir(exist_ok=True)
        wav, sr = fast(R / f"tts/{n:02d}.wav", R / f"tts/fast/{n:02d}.wav")
        voice.append((t, wav))
        t += len(wav) / sr + GAP[k]
    t += TAIL

    # 음성 트랙
    track = np.zeros(int(t * sr) + 1, np.float32)
    for s, w in voice:
        i = int(s * sr)
        track[i:i + len(w)] += w
    track *= 0.9 / max(1e-6, np.abs(track).max())
    sf.write(R / "voice.wav", track, sr)

    # 프레임
    js = dict(artTop=ART_TOP, subTop=SUB_TOP, states=states)
    (R / "states.js").write_text("const REEL = " + json.dumps(js, ensure_ascii=False) + ";\n", encoding="utf-8")
    fr = R / "frames"
    fr.mkdir(exist_ok=True)
    for old in fr.glob("*.png"):
        old.unlink()
    exe = chrome()
    for i, st in enumerate(states):
        subprocess.run([exe, "--headless", "--hide-scrollbars", "--window-size=1080,1920", "--virtual-time-budget=10000",
                        "--allow-file-access-from-files", "--default-background-color=FFFFFFFF",
                        f"--screenshot={fr / f's{i:02d}.png'}", (R / "reel.html").as_uri() + f"?s={i}"],
                       check=True, capture_output=True)

    # 이어 붙이기
    lst = []
    for i, st in enumerate(states):
        end = states[i + 1]["t"] if i + 1 < len(states) else t
        lst += [f"file 'frames/s{i:02d}.png'", f"duration {end - st['t']:.3f}"]
    lst.append(f"file 'frames/s{len(states) - 1:02d}.png'")
    (R / "frames.txt").write_text("\n".join(lst) + "\n", encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", "frames.txt", "-i", "voice.wav",
                    "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", "-movflags", "+faststart", "reel.mp4"],
                   cwd=R, check=True)
    print(f"{R / 'reel.mp4'}  {t:.1f}s  상태 {len(states)}개")


if __name__ == "__main__":
    main()
