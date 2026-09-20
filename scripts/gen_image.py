"""OpenAI 이미지 생성 (표준 라이브러리만 사용).

  python scripts/gen_image.py --prompt-file p.txt --out x.png
  python scripts/gen_image.py --prompt-file p.txt --ref a.jpg --ref b.jpg --out x.png   # 참조 이미지 → edits 엔드포인트
  옵션: --model --size --quality (기본값은 환경변수 IMAGE_MODEL / IMAGE_SIZE / IMAGE_QUALITY)
"""
import argparse, base64, json, mimetypes, os, sys, time, uuid, urllib.request

OUTPUT_USD_PER_M = 30.0  # gpt-image-2.5 출력 토큰 단가
INPUT_IMG_USD_PER_M = 8.0


def multipart(fields, files):
    b = uuid.uuid4().hex
    body = bytearray()
    for k, v in fields.items():
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, path in files:
        ct = mimetypes.guess_type(path)[0] or "application/octet-stream"
        body += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                 f"filename=\"{os.path.basename(path)}\"\r\nContent-Type: {ct}\r\n\r\n").encode()
        body += open(path, "rb").read() + b"\r\n"
    body += f"--{b}--\r\n".encode()
    return bytes(body), f"multipart/form-data; boundary={b}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt")
    ap.add_argument("--prompt-file")
    ap.add_argument("--ref", action="append", default=[], help="참조 이미지 (반복 가능)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default=os.environ.get("IMAGE_MODEL", "gpt-image-2.5-sunburst"))
    ap.add_argument("--size", default=os.environ.get("IMAGE_SIZE", "1024x1536"))
    ap.add_argument("--quality", default=os.environ.get("IMAGE_QUALITY", "medium"))
    a = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY 없음 (.env 로드 필요)")
    prompt = a.prompt or open(a.prompt_file, encoding="utf-8").read()
    fields = {"model": a.model, "prompt": prompt, "size": a.size,
              "quality": a.quality, "n": "1", "output_format": "png"}

    if a.ref:
        data, ct = multipart(fields, [("image[]", p) for p in a.ref])
        url = "https://api.openai.com/v1/images/edits"
    else:
        data, ct = json.dumps(fields).encode(), "application/json"
        url = "https://api.openai.com/v1/images/generations"
    req = urllib.request.Request(url, data=data,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": ct})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:800]}")
    sec = time.time() - t0

    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "wb") as f:
        f.write(base64.b64decode(res["data"][0]["b64_json"]))

    u = res.get("usage", {})
    out_tok = u.get("output_tokens", 0)
    in_img = u.get("input_tokens_details", {}).get("image_tokens", 0)
    cost = out_tok * OUTPUT_USD_PER_M / 1e6 + in_img * INPUT_IMG_USD_PER_M / 1e6
    print(f"saved {a.out}  {sec:.0f}s  {a.model}/{a.quality}/{a.size}  "
          f"out_tok={out_tok} in_img_tok={in_img}  ~${cost:.4f}")


if __name__ == "__main__":
    main()
