"""생성된 컷에서 캐릭터 바디 색이 시트 hex와 얼마나 다른지 잰다.

  python scripts/check_colors.py episodes/ep05/img/cut4.png dubu bamtol
이름: dubu misook deoksu kong tangja sora bamtol clerk (assets/characters.md 1절의 hex)
출력: 캐릭터별 실제 우세 색과 시트 hex의 채널 최대 차. ±12 안에 큰 영역이 없으면 색이 틀어진 것.
"""
import sys
import numpy as np
from PIL import Image

SHEET = {
    "dubu": "#F6F2E6", "misook": "#F6CA9E", "deoksu": "#EACEAA", "kong": "#DED6DA",
    "tangja": "#F5E08C", "sora": "#C2C6CA", "bamtol": "#C9A582", "clerk": "#BCD0DA",
}
TOL = 12  # 이 안의 픽셀만 그 캐릭터로 봄 (더 넓히면 이웃 캐릭터·회색을 집는다)


def hex2rgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])


def dominant(px, target):
    near = px[(np.abs(px - target).max(1) <= TOL) & ~(px.min(1) >= 250)]  # 흰 배경 제외
    if len(near) < 500:
        return None, 0
    v, c = np.unique(near, axis=0, return_counts=True)
    return v[c.argmax()], int(c.max())


if __name__ == "__main__":
    path, names = sys.argv[1], sys.argv[2:]
    px = np.array(Image.open(path).convert("RGB")).reshape(-1, 3).astype(int)
    for n in names:
        t = hex2rgb(SHEET[n])
        d, cnt = dominant(px, t)
        if d is None:
            print(f"{n}: 시트 hex ±12 안의 영역 없음 -> 색이 틀어졌거나 미등장. 눈으로 확인 후 재생성")
            continue
        diff = int(np.abs(d - t).max())
        flag = ""
        print(f"{n}: 실제 #{d[0]:02X}{d[1]:02X}{d[2]:02X}  시트 {SHEET[n]}  차 {diff}  ({cnt}px){flag}")
