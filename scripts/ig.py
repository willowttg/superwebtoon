"""Instagram API (Instagram Login) — 게시·댓글·인사이트 관리. 표준 라이브러리만 사용 (export만 Pillow).

  python scripts/ig.py auth-url                  # 브라우저에서 열어 권한 승인 → 주소창의 code 복사
  python scripts/ig.py auth <code>               # code → 장기 토큰(60일) 교환, .env 에 저장
  python scripts/ig.py refresh                   # 장기 토큰 갱신 (24h 지난 뒤, 60일 안에)
  python scripts/ig.py me                        # 계정 확인
  python scripts/ig.py export ep01               # img/slideN.png → slideN.jpg (인스타는 JPEG만 받음)
  python scripts/ig.py publish ep01 [--dry-run]  # GitHub Pages 의 slideN.jpg 8장 + caption.txt → 캐러셀 게시
  python scripts/ig.py media [--limit 10]        # 최근 게시물
  python scripts/ig.py comments ep01|<media_id>  # 댓글 목록
  python scripts/ig.py reply <comment_id> "답글"
  python scripts/ig.py hide <comment_id> [--unhide]
  python scripts/ig.py insights ep01|<media_id>|account
.env 는 자동으로 읽는다. 설정은 docs/instagram-api.md.
"""
import argparse, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT, ".env")
SCOPES = ("instagram_business_basic,instagram_business_content_publish,"
          "instagram_business_manage_comments,instagram_business_manage_insights")
FEED_METRICS = "reach,views,likes,comments,saved,shares,total_interactions,profile_visits,follows"


def load_env():
    if not os.path.exists(ENV_PATH):
        return
    for line in open(ENV_PATH, encoding="utf-8"):
        m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$", line)
        if m and not line.lstrip().startswith("#"):
            os.environ.setdefault(m.group(1), m.group(2).strip('"').strip("'"))


def save_env(**kv):
    """`.env` 의 해당 키 줄을 교체(없으면 추가). 토큰을 셸에 복사·붙여넣기 하지 않기 위함."""
    lines = open(ENV_PATH, encoding="utf-8").read().splitlines() if os.path.exists(ENV_PATH) else []
    for k, v in kv.items():
        os.environ[k] = v
        pat = re.compile(rf"^\s*{k}\s*=")
        idx = [i for i, l in enumerate(lines) if pat.match(l)]
        if idx:
            lines[idx[0]] = f"{k}={v}"
        else:
            lines.append(f"{k}={v}")
    open(ENV_PATH, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f".env 저장: {', '.join(kv)}")


def env(k, default=None, required=False):
    v = os.environ.get(k, default)
    if required and not v:
        sys.exit(f"{k} 없음 (.env 확인, docs/instagram-api.md)")
    return v


def api(path, params=None, method="GET", host=None, token=True):
    host = host or f"https://graph.instagram.com/{env('IG_API_VERSION', 'v25.0')}"
    params = dict(params or {})
    if token:
        params["access_token"] = env("IG_ACCESS_TOKEN", required=True)
    url = f"{host}/{path.lstrip('/')}"
    data = None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method), timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            body = json.dumps(json.loads(body).get("error", body), ensure_ascii=False, indent=1)
        except ValueError:
            pass
        sys.exit(f"HTTP {e.code} {method} /{path}\n{body[:1200]}")


def uid():
    return env("IG_USER_ID") or "me"


def ep_dir(ep):
    d = os.path.join(ROOT, "episodes", ep)
    if not os.path.isdir(d):
        sys.exit(f"{d} 없음")
    return d


def media_id_of(ref):
    """'ep01' 이면 episodes/ep01/ig.json 에서 media_id, 아니면 그대로 id 로 본다."""
    if re.fullmatch(r"ep\d+", ref):
        p = os.path.join(ep_dir(ref), "ig.json")
        if not os.path.exists(p):
            sys.exit(f"{p} 없음 — 아직 게시 전이거나 API 밖에서 올린 편. `media` 로 id 를 찾아 직접 넣는다")
        return json.load(open(p, encoding="utf-8"))["media_id"]
    return ref


def show(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=1))


# ---- 인증 ----

def cmd_auth_url(a):
    q = {"client_id": env("IG_APP_ID", required=True), "redirect_uri": env("IG_REDIRECT_URI", required=True),
         "response_type": "code", "scope": SCOPES, "force_reauth": "true"}
    print("https://www.instagram.com/oauth/authorize?" + urllib.parse.urlencode(q))
    print("→ 승인 뒤 이동한 주소의 ?code=... 값을 (끝의 #_ 제외) `auth <code>` 로 넘긴다. code 는 1시간·1회용.")


def cmd_auth(a):
    short = api("oauth/access_token", method="POST", host="https://api.instagram.com", token=False, params={
        "client_id": env("IG_APP_ID", required=True), "client_secret": env("IG_APP_SECRET", required=True),
        "grant_type": "authorization_code", "redirect_uri": env("IG_REDIRECT_URI", required=True),
        "code": a.code.split("#")[0]})
    long = api("access_token", host="https://graph.instagram.com", token=False, params={
        "grant_type": "ig_exchange_token", "client_secret": env("IG_APP_SECRET"),
        "access_token": short["access_token"]})
    save_env(IG_ACCESS_TOKEN=long["access_token"], IG_USER_ID=str(short["user_id"]))
    print(f"권한: {short.get('permissions')}  만료: {long['expires_in'] // 86400}일 뒤")


def cmd_refresh(a):
    r = api("refresh_access_token", host="https://graph.instagram.com", token=False, params={
        "grant_type": "ig_refresh_token", "access_token": env("IG_ACCESS_TOKEN", required=True)})
    save_env(IG_ACCESS_TOKEN=r["access_token"])
    print(f"만료: {r['expires_in'] // 86400}일 뒤")


def cmd_me(a):
    r = api("me", {"fields": "user_id,username,name,account_type,media_count,followers_count,profile_picture_url"})
    if "user_id" in r and not env("IG_USER_ID"):
        save_env(IG_USER_ID=str(r["user_id"]))
    show(r)


# ---- 게시 ----

def cmd_export(a):
    from PIL import Image
    img = os.path.join(ep_dir(a.ep), "img")
    for n in range(1, 9):
        src = os.path.join(img, f"slide{n}.png")
        if not os.path.exists(src):
            sys.exit(f"{src} 없음")
        im = Image.open(src).convert("RGB")
        if im.size != (1080, 1350):
            print(f"경고: slide{n} 크기 {im.size} (1080×1350 아님)")
        im.save(os.path.join(img, f"slide{n}.jpg"), "JPEG", quality=92, optimize=True)
    print(f"{img}/slide1..8.jpg 저장 — 커밋·푸시 후 publish")


def check_url(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=30) as r:
            ct = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        sys.exit(f"{url} → HTTP {e.code} (푸시했는가? Pages 반영에 1~2분 걸림)")
    if "jpeg" not in ct:
        sys.exit(f"{url} Content-Type={ct} (JPEG 아님)")


def wait_container(cid):
    for _ in range(10):
        r = api(cid, {"fields": "status_code,status"})
        if r["status_code"] == "FINISHED":
            return
        if r["status_code"] in ("ERROR", "EXPIRED"):
            sys.exit(f"컨테이너 {cid}: {r}")
        time.sleep(6)
    sys.exit(f"컨테이너 {cid} 처리 지연 — 잠시 후 다시 시도")


def cmd_publish(a):
    d = ep_dir(a.ep)
    caption = open(os.path.join(d, a.caption), encoding="utf-8").read().strip()
    base = env("SITE_URL", "https://willowttg.github.io/superwebtoon").rstrip("/")
    urls = [f"{base}/episodes/{a.ep}/img/slide{n}.jpg" for n in range(1, 9)]
    if len(caption) > 2200:
        sys.exit(f"캡션 {len(caption)}자 > 2200")
    for u in urls:
        check_url(u)
    print(f"캡션 {len(caption)}자, 해시태그 {caption.count('#')}개, 이미지 8장 확인")
    if a.dry_run:
        print(caption); print(*urls, sep="\n"); return

    limit = api(f"{uid()}/content_publishing_limit", {"fields": "quota_usage,config"})
    print(f"24h 게시 한도 사용: {limit.get('data', [{}])[0]}")
    children = []
    for i, u in enumerate(urls, 1):
        r = api(f"{uid()}/media", {"image_url": u, "is_carousel_item": "true"}, "POST")
        children.append(r["id"]); print(f"item {i}/8 {r['id']}")
    for c in children:
        wait_container(c)
    car = api(f"{uid()}/media", {"media_type": "CAROUSEL", "children": ",".join(children), "caption": caption}, "POST")
    wait_container(car["id"])
    pub = api(f"{uid()}/media_publish", {"creation_id": car["id"]}, "POST")
    info = api(pub["id"], {"fields": "id,permalink,timestamp"})
    rec = {"media_id": pub["id"], "permalink": info.get("permalink"), "timestamp": info.get("timestamp"),
           "published_by": "api", "slides": urls}
    json.dump(rec, open(os.path.join(d, "ig.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"게시 완료 {info.get('permalink')}  → {a.ep}/ig.json 기록")


# ---- 조회·관리 ----

def cmd_media(a):
    r = api(f"{uid()}/media", {"fields": "id,media_type,timestamp,permalink,caption,like_count,comments_count",
                               "limit": a.limit})
    for m in r.get("data", []):
        cap = (m.get("caption") or "").split("\n")[0][:40]
        print(f"{m['id']}  {m['timestamp'][:10]}  {m['media_type']:<8} 좋아요 {m.get('like_count', 0):>4} "
              f"댓글 {m.get('comments_count', 0):>3}  {cap}  {m['permalink']}")


def cmd_comments(a):
    mid = media_id_of(a.ref)
    r = api(f"{mid}/comments", {"fields": "id,username,text,timestamp,like_count,hidden,"
                                          "replies{id,username,text,timestamp}", "limit": 50})
    for c in r.get("data", []):
        flag = " [숨김]" if c.get("hidden") else ""
        print(f"{c['id']}  {c['timestamp'][:16]}  @{c.get('username')}{flag}: {c['text']}")
        for rp in c.get("replies", {}).get("data", []):
            print(f"    ↳ {rp['id']}  @{rp.get('username')}: {rp['text']}")
    if not r.get("data"):
        print("댓글 없음")


def cmd_reply(a):
    show(api(f"{a.comment_id}/replies", {"message": a.text}, "POST"))


def cmd_hide(a):
    show(api(a.comment_id, {"hide": "false" if a.unhide else "true"}, "POST"))


def cmd_insights(a):
    if a.ref == "account":
        r = api(f"{uid()}/insights", {"metric": a.metric or "reach,views,follower_count,profile_views",
                                      "period": "day", "metric_type": "total_value"})
    else:
        r = api(f"{media_id_of(a.ref)}/insights", {"metric": a.metric or FEED_METRICS})
    for m in r.get("data", []):
        v = m.get("total_value", {}).get("value") if "total_value" in m else (m.get("values") or [{}])[-1].get("value")
        print(f"{m['name']:<20} {v}")


def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("auth-url").set_defaults(f=cmd_auth_url)
    p = sp.add_parser("auth"); p.add_argument("code"); p.set_defaults(f=cmd_auth)
    sp.add_parser("refresh").set_defaults(f=cmd_refresh)
    sp.add_parser("me").set_defaults(f=cmd_me)
    p = sp.add_parser("export"); p.add_argument("ep"); p.set_defaults(f=cmd_export)
    p = sp.add_parser("publish"); p.add_argument("ep"); p.add_argument("--caption", default="caption.txt")
    p.add_argument("--dry-run", action="store_true"); p.set_defaults(f=cmd_publish)
    p = sp.add_parser("media"); p.add_argument("--limit", type=int, default=10); p.set_defaults(f=cmd_media)
    p = sp.add_parser("comments"); p.add_argument("ref"); p.set_defaults(f=cmd_comments)
    p = sp.add_parser("reply"); p.add_argument("comment_id"); p.add_argument("text"); p.set_defaults(f=cmd_reply)
    p = sp.add_parser("hide"); p.add_argument("comment_id"); p.add_argument("--unhide", action="store_true")
    p.set_defaults(f=cmd_hide)
    p = sp.add_parser("insights"); p.add_argument("ref"); p.add_argument("--metric"); p.set_defaults(f=cmd_insights)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
