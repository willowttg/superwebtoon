"""컷 이미지에서 그림이 차지하는 영역을 슬라이드 좌표(1080×1350)로 출력.
텍스트 위치를 눈대중이 아니라 측정값으로 잡기 위한 도구.

  python scripts/art_bbox.py episodes/ep01/img/cut4.png [...]
  --anchor bottom|center : compose.html의 object-position 기준 (기본 bottom)
"""
import argparse
from PIL import Image

def bbox(path, anchor):
    im = Image.open(path).convert("L")
    w, h = im.size                      # 1024×1536
    ch = round(w * 1350 / 1080)         # 4:5 크롭 높이 1280
    top = h - ch if anchor == "bottom" else (h - ch) // 2
    crop = im.crop((0, top, w, top + ch))
    box = crop.point(lambda v: 255 if v < 235 else 0).getbbox()  # 흰 배경 제외
    s = 1080 / w
    return [round(v * s) for v in box] if box else None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--anchor", default="bottom", choices=["bottom", "center"])
    a = ap.parse_args()
    for f in a.files:
        b = bbox(f, a.anchor)
        print(f"{f}: x {b[0]}-{b[2]}  y {b[1]}-{b[3]}  (빈 상단 {b[1]}px = {b[1]/13.5:.0f}%)")
