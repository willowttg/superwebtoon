"""Instagram API (Instagram Login) — 게시·댓글·인사이트 관리. 표준 라이브러리만 사용 (export만 Pillow).

  python scripts/ig.py auth-url                  # 브라우저에서 열어 권한 승인 → 주소창의 code 복사
  python scripts/ig.py auth <code>               # code → 장기 토큰(60일) 교환, .env 에 저장
  python scripts/ig.py refresh                   # 장기 토큰 갱신 (24h 지난 뒤, 60일 안에)
  python scripts/ig.py me                        # 계정 확인
  python scripts/ig.py export ep01               # img/slideN.png → slideN.jpg (인스타는 JPEG만 받음)
  python scripts/ig.py publish ep01 [--dry-run]  # GitHub Pages 의 slideN.jpg 전부 + caption.txt → 캐러셀 게시 (지금)
  python scripts/ig.py schedule ep01 [--at 2026-09-24T21:00:00+09:00] [--dry-run]
                                                 # 예약: 다음 빈 슬롯(매일 21:00 KST)에 윈도우 작업 스케줄러 등록
  python scripts/ig.py queue                     # 예약·게시 현황과 다음 빈 슬롯
  python scripts/ig.py unschedule ep01           # 예약 취소
  python scripts/ig.py media [--limit 10]        # 최근 게시물
  python scripts/ig.py comments ep01|<media_id>  # 댓글 목록
  python scripts/ig.py reply <comment_id> "답글"
  python scripts/ig.py hide <comment_id> [--unhide]
  python scripts/ig.py insights ep01|<media_id>|account
.env 는 자동으로 읽는다. 설정은 docs/instagram-api.md.
"""
import argparse, base64, datetime, glob, json, os, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8"); sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KST = datetime.timezone(datetime.timedelta(hours=9))
SLOTS = {"weekday": [(7, 30), (21, 0)],   # 하루 2편 KST — docs/research/posting-times/README.md
         "weekend": [(10, 30), (21, 0)]}
PRE = datetime.timedelta(minutes=5)       # 슬롯 몇 분 전에 깨어나 컨테이너를 만드나
WAIT_MAX = datetime.timedelta(minutes=20) # 이 안이면 작업 등록 없이 프로세스가 기다린다
TASK_PREFIX = "superwebtoon-ig-"


def find_env():
    """ROOT/.env — 워크트리에는 없으므로 .git 파일의 gitdir 로 본 저장소의 .env 를 찾는다."""
    p = os.path.join(ROOT, ".env")
    g = os.path.join(ROOT, ".git")
    if not os.path.exists(p) and os.path.isfile(g):
        gitdir = open(g, encoding="utf-8").read().split("gitdir:", 1)[1].strip()
        p = os.path.join(gitdir.split(".git", 1)[0], ".env")
    return p


ENV_PATH = find_env()
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
    n_slides = slide_count(img, "png")
    for n in range(1, n_slides + 1):
        src = os.path.join(img, f"slide{n}.png")
        im = Image.open(src).convert("RGB")
        if im.size != (1080, 1350):
            print(f"경고: slide{n} 크기 {im.size} (1080×1350 아님)")
        im.save(os.path.join(img, f"slide{n}.jpg"), "JPEG", quality=92, optimize=True)
    print(f"{img}/slide1..{n_slides}.jpg 저장 — 커밋·푸시 후 publish")


def slide_count(img, ext):
    """img/slide1.ext 부터 연속으로 있는 장수 (표지 없는 편은 컷 수 4~7, 표지 있는 구편은 8)."""
    n = 0
    while os.path.exists(os.path.join(img, f"slide{n + 1}.{ext}")):
        n += 1
    if not 2 <= n <= 10:
        sys.exit(f"{img}/slide1..N.{ext} 이 {n}장 — 캐러셀은 2~10장")
    return n


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


def prepare(ep, caption_name):
    """캡션·슬라이드 URL 을 모으고 검사한다 (publish·schedule 공통)."""
    d = ep_dir(ep)
    caption = open(os.path.join(d, caption_name), encoding="utf-8").read().strip()
    base = env("SITE_URL", "https://willowttg.github.io/superwebtoon").rstrip("/")
    n_slides = slide_count(os.path.join(d, "img"), "jpg")
    urls = [f"{base}/episodes/{ep}/img/slide{n}.jpg" for n in range(1, n_slides + 1)]
    if len(caption) > 2200:
        sys.exit(f"캡션 {len(caption)}자 > 2200")
    if os.path.exists(os.path.join(d, "ig.json")):
        sys.exit(f"{ep} 은 이미 게시됨 ({json.load(open(os.path.join(d, 'ig.json'), encoding='utf-8')).get('permalink')})")
    for u in urls:
        check_url(u)
    print(f"캡션 {len(caption)}자, 해시태그 {caption.count('#')}개, 이미지 {len(urls)}장 확인")
    return d, caption, urls


def do_publish(ep, d, caption, urls, at=None):
    """컨테이너 생성 → 처리 대기 → (at 까지 대기) → 게시. 결과는 ig.json."""
    limit = api(f"{uid()}/content_publishing_limit", {"fields": "quota_usage,config"})
    print(f"24h 게시 한도 사용: {limit.get('data', [{}])[0]}")
    children = []
    for i, u in enumerate(urls, 1):
        r = api(f"{uid()}/media", {"image_url": u, "is_carousel_item": "true"}, "POST")
        children.append(r["id"]); print(f"item {i}/{len(urls)} {r['id']}")
    for c in children:
        wait_container(c)
    car = api(f"{uid()}/media", {"media_type": "CAROUSEL", "children": ",".join(children), "caption": caption}, "POST")
    wait_container(car["id"])
    if at:
        sleep_until(at, "게시")
    pub = api(f"{uid()}/media_publish", {"creation_id": car["id"]}, "POST")
    info = api(pub["id"], {"fields": "id,permalink,timestamp"})
    rec = {"media_id": pub["id"], "permalink": info.get("permalink"), "timestamp": info.get("timestamp"),
           "published_by": "api", "scheduled_at": at.isoformat(timespec="seconds") if at else None, "slides": urls}
    json.dump(rec, open(os.path.join(d, "ig.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sched = os.path.join(d, "schedule.json")
    if os.path.exists(sched):
        os.remove(sched)
    print(f"게시 완료 {info.get('permalink')}  → {ep}/ig.json 기록")


def cmd_publish(a):
    if a.log:
        sys.stdout = Tee(sys.stdout, a.log); sys.stderr = Tee(sys.stderr, a.log)
    d = ep_dir(a.ep)
    at = None
    if a.scheduled:
        sp = os.path.join(d, "schedule.json")
        if not os.path.exists(sp):
            sys.exit(f"{sp} 없음 — 예약이 취소됐다")
        at = parse_iso(json.load(open(sp, encoding="utf-8"))["publish_at"])
        if at - now() > datetime.timedelta(hours=23):
            sys.exit(f"게시 시각까지 {at - now()} — 너무 일찍 깨어났다. 컨테이너가 24h 에 만료되므로 올리지 않는다")
    d, caption, urls = prepare(a.ep, a.caption)
    if a.dry_run:
        print(caption); print(*urls, sep="\n"); return
    do_publish(a.ep, d, caption, urls, at)


# ---- 예약 ----

def now():
    return datetime.datetime.now(KST)


def parse_iso(s):
    dt = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        sys.exit(f"시간대가 없다: {s!r} — 예: 2026-09-24T21:00:00+09:00")
    return dt.astimezone(KST)


def sleep_until(dt, what):
    while (left := (dt - now()).total_seconds()) > 0:
        print(f"  {what} {dt:%m-%d %H:%M} 까지 {left/60:.1f}분 대기", end="\r", flush=True)
        time.sleep(min(left, 30))
    print()


class Tee:
    """스케줄러가 깨웠을 때 화면이 없으므로 로그 파일에도 같이 적는다."""
    def __init__(self, stream, path):
        self.stream, self.f = stream, open(path, "a", encoding="utf-8")
        self.f.write(f"\n=== {now().isoformat(timespec='seconds')} ===\n")
    def write(self, s):
        self.stream.write(s); self.f.write(s.replace("\r", "\n")); self.f.flush()
    def flush(self):
        self.stream.flush(); self.f.flush()


def day_slots(d):
    """날짜 d(KST) 의 슬롯 시각들. 주말은 아침만 10:30."""
    kind = "weekend" if d.weekday() >= 5 else "weekday"
    return [datetime.datetime.combine(d, datetime.time(h, m), tzinfo=KST) for h, m in SLOTS[kind]]


def slot_of(t):
    """게시·예약 시각 t 가 속한 슬롯. 슬롯에서 90분 넘게 떨어진 수동 게시는 슬롯을 차지하지 않는다(None)."""
    t = t.astimezone(KST)
    s = min(day_slots(t.date()), key=lambda s: abs(s - t))
    return s if abs(s - t) <= datetime.timedelta(minutes=90) else None


def taken_slots():
    """게시됐거나 예약된 슬롯(KST) → {datetime: 'ep01 게시'|'ep02 예약'}"""
    out = {}
    for p in glob.glob(os.path.join(ROOT, "episodes", "*", "ig.json")):
        ep = os.path.basename(os.path.dirname(p)); t = json.load(open(p, encoding="utf-8")).get("timestamp")
        if t and slot_of(parse_iso(t)):
            out[slot_of(parse_iso(t))] = f"{ep} 게시"
    for p in glob.glob(os.path.join(ROOT, "episodes", "*", "schedule.json")):
        ep = os.path.basename(os.path.dirname(p))
        out[slot_of(parse_iso(json.load(open(p, encoding="utf-8"))["publish_at"]))] = f"{ep} 예약"
    return out


def next_slot(taken):
    """오늘부터 순서대로, 게시·예약이 없고 아직 오지 않은 첫 슬롯."""
    d = now().date()
    while True:
        for s in day_slots(d):
            if s - now() >= PRE * 2 and s not in taken:
                return s
        d += datetime.timedelta(days=1)


def ps(script):
    enc = base64.b64encode(script.encode("utf-16-le")).decode()
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-EncodedCommand", enc],
                       capture_output=True, text=True, timeout=120)
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def q(s):
    return s.replace("'", "''")


def task_name(ep):
    return TASK_PREFIX + ep


def register_task(ep, at):
    """at − PRE 에 `ig.py publish ep --scheduled --log` 를 깨우는 일회성 작업. 로그인 상태(잠금 화면 가능)여야 돈다."""
    start = (at - PRE).astimezone(); end = (at + datetime.timedelta(days=1)).astimezone()
    log = os.path.join(ep_dir(ep), "ig-log.txt")
    args = f'"{os.path.abspath(__file__)}" publish {ep} --scheduled --log "{log}"'
    code, out, err = ps(f"""$ErrorActionPreference = 'Stop'
$action = New-ScheduledTaskAction -Execute '{q(sys.executable)}' -Argument '{q(args)}' -WorkingDirectory '{q(ROOT)}'
$trigger = New-ScheduledTaskTrigger -Once -At ([datetime]'{start:%Y-%m-%dT%H:%M:%S}')
$trigger.EndBoundary = '{end:%Y-%m-%dT%H:%M:%S}'
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2) -DeleteExpiredTaskAfter (New-TimeSpan -Hours 1) -MultipleInstances IgnoreNew
Unregister-ScheduledTask -TaskName '{q(task_name(ep))}' -Confirm:$false -ErrorAction SilentlyContinue
Register-ScheduledTask -TaskName '{q(task_name(ep))}' -Action $action -Trigger $trigger -Settings $settings | Out-Null
Write-Output OK""")
    if code != 0 or out != "OK":
        sys.exit(f"작업 등록 실패: {err or out}")
    print(f"작업 등록 {task_name(ep)}  {start:%m-%d %H:%M} 시작 → {at:%H:%M} 게시  (로그 {log})")


def task_state(ep):
    code, out, _ = ps(f"""$t = Get-ScheduledTask -TaskName '{q(task_name(ep))}' -ErrorAction SilentlyContinue
if ($t) {{ $i = $t | Get-ScheduledTaskInfo; Write-Output ('{{0}} 다음 {{1}}' -f $t.State, $i.NextRunTime) }} else {{ Write-Output NONE }}""")
    return None if code != 0 or out == "NONE" else out


def cmd_schedule(a):
    taken = taken_slots()
    at = parse_iso(a.at) if a.at else next_slot(taken)
    if at <= now():
        sys.exit(f"{at:%Y-%m-%d %H:%M} 은 지났다")
    if a.at and slot_of(at) and slot_of(at) in taken:
        print(f"경고: {slot_of(at):%m-%d %H:%M} 슬롯에 이미 {taken[slot_of(at)]}")
    d, caption, urls = prepare(a.ep, a.caption)
    print(f"게시 예정 {at:%Y-%m-%d (%a) %H:%M} KST")
    if a.dry_run:
        print(caption); return
    json.dump({"publish_at": at.isoformat(timespec="seconds"), "registered_at": now().isoformat(timespec="seconds"),
               "task": task_name(a.ep)}, open(os.path.join(d, "schedule.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    if at - now() <= WAIT_MAX:
        print("20분 안이라 작업 등록 없이 이 프로세스가 기다린다")
        do_publish(a.ep, d, caption, urls, at); return
    register_task(a.ep, at)
    print(f"→ {a.ep}/schedule.json 커밋. 현황은 `queue`, 취소는 `unschedule {a.ep}`. PC 는 켜져 있고 로그인 상태여야 한다.")


def cmd_unschedule(a):
    ps(f"Unregister-ScheduledTask -TaskName '{q(task_name(a.ep))}' -Confirm:$false -ErrorAction SilentlyContinue")
    sp = os.path.join(ep_dir(a.ep), "schedule.json")
    if os.path.exists(sp):
        os.remove(sp)
    print(f"{a.ep} 예약 취소")


def cmd_queue(a):
    rows = []
    for p in sorted(glob.glob(os.path.join(ROOT, "episodes", "*", "ig.json"))):
        ep = os.path.basename(os.path.dirname(p)); r = json.load(open(p, encoding="utf-8"))
        rows.append((parse_iso(r["timestamp"]), f"{ep}  게시  {r.get('permalink')}"))
    for p in sorted(glob.glob(os.path.join(ROOT, "episodes", "*", "schedule.json"))):
        ep = os.path.basename(os.path.dirname(p)); r = json.load(open(p, encoding="utf-8"))
        rows.append((parse_iso(r["publish_at"]), f"{ep}  예약  작업 {task_state(ep) or '없음 — 스케줄러에서 사라졌다, schedule 다시'}"))
    for t, line in sorted(rows):
        print(f"{t:%Y-%m-%d %a %H:%M}  {line}")
    print(f"다음 빈 슬롯  {next_slot(taken_slots()):%Y-%m-%d %a %H:%M} KST")


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
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--scheduled", action="store_true", help="(작업 스케줄러용)")
    p.add_argument("--log"); p.set_defaults(f=cmd_publish)
    p = sp.add_parser("schedule"); p.add_argument("ep"); p.add_argument("--at"); p.add_argument("--caption", default="caption.txt")
    p.add_argument("--dry-run", action="store_true"); p.set_defaults(f=cmd_schedule)
    p = sp.add_parser("unschedule"); p.add_argument("ep"); p.set_defaults(f=cmd_unschedule)
    sp.add_parser("queue").set_defaults(f=cmd_queue)
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
