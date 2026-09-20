"""캐릭터 시트에서 FRONT 도를 잘라 크기 비교 라인업을 만든다 (컷 생성 참조용).
크기는 실제 동물이 아니라 역할 기준: 눈높이→발끝 거리를 기준으로 맞춰 귀·뿔·털 길이에 영향받지 않는다.

  python scripts/lineup.py dubu misook --out episodes/ep02/ref/lineup.png
  python scripts/lineup.py all --out assets/cast/lineup-all.png
이름: dubu misook deoksu kong tangja sora bamtol
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CAST = {  # 이름: (시트, 상대 크기, 캡션)
    "dubu":   ("assets/samples/dubu-sheet-high.png",   1.0, "DUBU 100"),
    "misook": ("assets/samples/misook-sheet-high.png", 1.05, "MISOOK 105"),
    "deoksu": ("assets/samples/deoksu-sheet-high.png", 1.10, "DEOKSU 110"),
    "kong":   ("assets/samples/kong-sheet-high.png",   1.00, "KONG 100"),
    "tangja": ("assets/samples/tangja-sheet-high.png", 1.0, "TANGJA 100"),
    "sora":   ("assets/samples/sora-sheet-high.png",   1.0, "SORA 100"),
    "bamtol": ("assets/samples/bamtol-sheet-high.png", 1.05, "BAMTOL 105"),
}
ORDER = ["misook", "deoksu", "dubu", "kong", "tangja", "sora", "bamtol"]
BASE_H = 210  # 크기 1.0 캐릭터의 눈높이→발끝 픽셀 거리 (귀·뿔·털 제외, 역할 기준 크기)


def grow(seed, ok):
    m = np.zeros_like(ok); m[seed] = True
    while True:
        d = (m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)) & ok
        if (d == m).all():
            return m
        m = d


def front_figure(sheet):
    """시트 1행 1열(FRONT) 도를 연결 성분으로 잘라 반환. 캡션 제외."""
    im = Image.open(sheet).convert("RGB")
    W, H = im.size
    band = im.crop((0, 30, int(W / 4) + 60, int(H * 0.47)))
    a = np.array(band)
    ok = (a < 240).any(axis=2)
    ok2 = ok.copy()
    for _ in range(2):
        ok2 = ok2 | np.roll(ok2, 1, 0) | np.roll(ok2, -1, 0) | np.roll(ok2, 1, 1) | np.roll(ok2, -1, 1)
    cx = int(W / 8)
    ys = np.where(ok[:, cx])[0]
    m = grow((ys[0] + 2, cx), ok2) & ok
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    out = a[y0:y1 + 1, x0:x1 + 1].copy()
    out[~m[y0:y1 + 1, x0:x1 + 1]] = 255
    return Image.fromarray(out)


def eye_line(im):
    """점 눈 2개의 y 평균. 눈은 채워진 작은 검은 원이라 외곽선과 구분된다."""
    a = np.array(im.convert("L")); dark = a < 70
    H, W = dark.shape; seen = np.zeros_like(dark); dots = []
    for y in range(H):
        for x in range(W):
            if dark[y, x] and not seen[y, x]:
                st = [(y, x)]; seen[y, x] = True; pts = []
                while st:
                    cy, cx = st.pop(); pts.append((cy, cx))
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < H and 0 <= nx < W and dark[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; st.append((ny, nx))
                ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                h = max(ys) - min(ys) + 1; w = max(xs) - min(xs) + 1
                if 30 < len(pts) < 600 and 0.6 < w / h < 1.6 and len(pts) / (w * h) > 0.55:
                    dots.append((len(pts), sum(ys) / len(ys)))
    dots.sort(reverse=True)
    return (dots[0][1] + dots[1][1]) / 2 if len(dots) >= 2 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-caption", action="store_true")
    a = ap.parse_args()
    names = ORDER if a.names == ["all"] else [n for n in ORDER if n in a.names]
    figs = []
    for n in names:
        sheet, scale, cap = CAST[n]
        f = front_figure(sheet)
        ey = eye_line(f)
        body = (f.height - ey) if ey else f.height * 0.6  # 눈높이→발끝
        k = BASE_H * scale / body
        h = int(f.height * k); w = int(f.width * k)
        figs.append((f.resize((w, h), Image.LANCZOS), cap))
    gap = 40; cap_h = 0 if a.no_caption else 34
    W = sum(f.width for f, _ in figs) + gap * (len(figs) + 1)
    H = max(f.height for f, _ in figs) + gap + cap_h
    M = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(M)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    x = gap; base = H - cap_h - gap // 2
    for f, cap in figs:
        M.paste(f, (x, base - f.height))
        if not a.no_caption:
            tw = d.textlength(cap, font=font)
            d.text((x + (f.width - tw) / 2, base + 8), cap, fill=(120, 120, 120), font=font)
        x += f.width + gap
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    M.save(a.out); print("saved", a.out, M.size)


if __name__ == "__main__":
    main()
