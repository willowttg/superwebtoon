"""compose.html의 각 <section>을 img/slideN.png(1080×1350)로 찍는다 (Playwright 헤드리스 셸, MCP 브라우저 불필요).

  python scripts/shoot_slides.py episodes/ep07 6        # slide1..6
  python scripts/shoot_slides.py episodes/ep07 6 --only 3
compose.html은 ?only=N(0부터)으로 그 슬라이드만 남기는 스크립트를 갖고 있어야 한다.
"""
import argparse, glob, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def chrome():
    for p in glob.glob(os.path.expanduser("~/AppData/Local/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-win64/chrome-headless-shell.exe")):
        return p
    sys.exit("chrome-headless-shell.exe 없음 (npx playwright install chromium)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep", help="episodes/epNN")
    ap.add_argument("n", type=int, help="슬라이드 수")
    ap.add_argument("--only", type=int, help="이 슬라이드만 (1부터)")
    a = ap.parse_args()
    ep = (ROOT / a.ep).resolve()
    html = ep / "compose.html"
    (ep / "img").mkdir(exist_ok=True)
    exe = chrome()
    for i in range(1, a.n + 1):
        if a.only and i != a.only:
            continue
        out = ep / "img" / f"slide{i}.png"
        url = html.as_uri() + f"?only={i - 1}"
        subprocess.run([exe, "--headless", "--hide-scrollbars", "--window-size=1080,1350", "--virtual-time-budget=10000",
                        "--default-background-color=FFFFFFFF", f"--screenshot={out}", url],
                       check=True, capture_output=True)
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
