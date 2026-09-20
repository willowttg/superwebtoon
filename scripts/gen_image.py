"""OpenAI 이미지 생성 (표준 라이브러리만 사용).

사용:
  python scripts/gen_image.py --prompt "..." --out assets/samples/x.png
  python scripts/gen_image.py --prompt-file p.txt --out x.png --quality high

환경변수: OPENAI_API_KEY, IMAGE_MODEL, IMAGE_SIZE, IMAGE_QUALITY (.env 참조)
"""
import argparse, base64, json, os, sys, time, urllib.request

OUTPUT_USD_PER_M = 30.0  # gpt-image-2.5 출력 토큰 단가


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt")
    ap.add_argument("--prompt-file")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=os.environ.get("IMAGE_MODEL", "gpt-image-2.5-sunburst"))
    ap.add_argument("--size", default=os.environ.get("IMAGE_SIZE", "1024x1536"))
    ap.add_argument("--quality", default=os.environ.get("IMAGE_QUALITY", "medium"))
    a = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY 없음 (.env 로드 필요)")
    prompt = a.prompt or open(a.prompt_file, encoding="utf-8").read()

    body = {"model": a.model, "prompt": prompt, "size": a.size,
            "quality": a.quality, "n": 1, "output_format": "png"}
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:800]}")
    sec = time.time() - t0

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "wb") as f:
        f.write(base64.b64decode(res["data"][0]["b64_json"]))
    with open(os.path.splitext(a.out)[0] + ".prompt.txt", "w", encoding="utf-8") as f:
        f.write(f"model={a.model} size={a.size} quality={a.quality}\n\n{prompt}\n")

    u = res.get("usage", {})
    out_tok = u.get("output_tokens", 0)
    print(f"saved {a.out}  {sec:.0f}s  usage={json.dumps(u)}  "
          f"~${out_tok * OUTPUT_USD_PER_M / 1e6:.4f} (출력 토큰 기준)")


if __name__ == "__main__":
    main()
