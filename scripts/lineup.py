"""캐릭터 시트에서 FRONT 도를 잘라 크기 비교 라인업을 만든다 (컷 생성 참조용).
크기는 실제 동물이 아니라 역할 기준: 얼굴 기준선(눈·눈썹·코·안경 등 안쪽 검정 요소의 평균 높이)→발끝 거리를 맞춰 귀·뿔·털 길이에 영향받지 않는다.

  python scripts/lineup.py dubu misook --out episodes/ep02/ref/lineup.png
  python scripts/lineup.py all --out assets/cast/lineup-all.png
이름: dubu misook deoksu kong tangja sora bamtol clerk (고양이 3인조 시트는 3행이라 미지원)
"""
import argparse, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CAST = {  # 이름: (시트, 상대 크기, 캡션)
    "dubu":   ("assets/samples/dubu-sheet.png",   1.0, "DUBU 100"),
    "misook": ("assets/samples/misook-sheet.png", 1.05, "MISOOK 105"),
    "deoksu": ("assets/samples/deoksu-sheet.png", 1.10, "DEOKSU 110"),
    "kong":   ("assets/samples/kong-sheet.png",   1.00, "KONG 100"),
    "tangja": ("assets/samples/tangja-sheet.png", 1.0, "TANGJA 100"),
    "sora":   ("assets/samples/sora-sheet.png",   1.0, "SORA 100"),
    "bamtol": ("assets/samples/bamtol-sheet.png", 1.05, "BAMTOL 105"),
    "clerk":  ("assets/samples/clerk-sheet-high.png",  1.0, "CLERK 100"),
}
ORDER = ["misook", "deoksu", "dubu", "kong", "tangja", "sora", "bamtol", "clerk"]
BASE_H = 210  # 크기 1.0 캐릭터의 얼굴 기준선→발끝 픽셀 거리 (귀·뿔·털 제외, 역할 기준 크기)


def _components(mask):
    """4-연결 성분 목록: (pts, y0, y1, x0, x1)."""
    H, W = mask.shape; seen = np.zeros_like(mask); out = []
    for y in range(H):
        for x in range(W):
            if mask[y, x] and not seen[y, x]:
                st = [(y, x)]; seen[y, x] = True; pts = []
                while st:
                    cy, cx = st.pop(); pts.append((cy, cx))
                    for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                        if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; st.append((ny, nx))
                ys = [q[0] for q in pts]; xs = [q[1] for q in pts]
                out.append((pts, min(ys), max(ys), min(xs), max(xs)))
    return out


def front_figure(sheet):
    """시트 1행 1열(FRONT) 도를 잘라 반환. 1행의 세로 범위를 빈 행으로 찾아 캡션·2행을 제외한다."""
    im = Image.open(sheet).convert("RGB")
    W, H = im.size
    band = np.array(im.crop((0, 0, int(W / 4) + 40, H)))
    dark_rows = (band < 200).any(axis=2).any(axis=1)
    ys = np.where(dark_rows)[0]
    y0 = ys[0]; y1 = y0
    for y in ys[1:]:
        if y - y1 > 12:
            break
        y1 = y
    a = band[y0:y1 + 1]
    ok = (a < 240).any(axis=2)
    cols = np.where(ok.any(axis=0))[0]
    cx = int(W / 8)
    xs = [c for c in cols if c <= cx]; x0 = cx
    while x0 - 1 in cols: x0 -= 1
    x1 = cx
    while x1 + 1 in cols: x1 += 1
    out = a[:, x0:x1 + 1].copy()
    out[~ok[:, x0:x1 + 1]] = 255
    return Image.fromarray(out)


def eye_line(im):
    """얼굴 기준선: 외곽선과 떨어진 안쪽 검정 요소(눈·눈썹·코·안경 등)의 평균 y.
    점 눈뿐 아니라 대시·호·안경테도 잡히도록 성분 크기만으로 거른다."""
    a = np.array(im.convert("L")); dark = a < 90
    H, W = dark.shape
    comps = _components(dark)
    if not comps:
        return None
    big = max(comps, key=lambda c: len(c[0]))
    feats = [c for c in comps if c is not big and 15 < len(c[0]) < 3000
             and c[1] > big[1] and c[2] < big[2] and c[3] > big[3] and c[4] < big[4]
             and (c[1] + c[2]) / 2 < H * 0.65]
    if not feats:
        return None
    return sum((c[1] + c[2]) / 2 for c in feats) / len(feats)


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
