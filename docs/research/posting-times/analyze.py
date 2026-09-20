"""raw/<계정>.json (프로필 그리드에서 모은 shortcode) → posts.json + 시간대 통계.
shortcode 는 미디어 id 의 base64 — 상위 비트가 게시 시각(ms, epoch 1314220021721)이라 API 없이 시각을 복원한다 (EP.01 실측 오차 10초).
"""
import collections, datetime, glob, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
KST = datetime.timezone(datetime.timedelta(hours=9))
DOW = "월화수목금토일"
SINCE = datetime.datetime.now(KST) - datetime.timedelta(days=365)


def decode(code):
    n = 0
    for c in code:
        n = n * 64 + A.index(c)
    return datetime.datetime.fromtimestamp(((n >> 23) + 1314220021721) / 1000, KST)


rows = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "raw", "*.json"))):
    acc = os.path.basename(f)[:-5]
    for c in json.load(open(f, encoding="utf-8"))["codes"]:
        kind, code = c.split(":", 1)
        t = decode(code)
        rows.append({"account": acc, "kind": kind, "code": code, "ts": t.isoformat(timespec="seconds"),
                     "dow": t.weekday(), "hour": t.hour, "minute": t.minute})
json.dump(rows, open(os.path.join(os.path.dirname(__file__), "posts.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)

recent = [r for r in rows if datetime.datetime.fromisoformat(r["ts"]) >= SINCE]
print(f"전체 {len(rows)}건 / 최근 1년 {len(recent)}건 ({len(set(r['account'] for r in recent))}계정)\n")


def hist(rs, key, labels):
    c = collections.Counter(r[key] for r in rs)
    n = len(rs) or 1
    for k, lab in labels:
        v = c.get(k, 0)
        print(f"  {lab:>4} {v:4} {100*v/n:5.1f}%  {'█'*int(round(50*v/n))}")


print("■ 시간대 (KST, 최근 1년)")
hist(recent, "hour", [(h, f"{h:02}시") for h in range(24)])
print("\n■ 요일 (최근 1년)")
hist(recent, "dow", [(d, DOW[d]) for d in range(7)])

wk = [r for r in recent if r["dow"] < 5]
we = [r for r in recent if r["dow"] >= 5]
print(f"\n■ 평일({len(wk)}) vs 주말({len(we)}) 시간대 상위")
for name, rs in (("평일", wk), ("주말", we)):
    c = collections.Counter(r["hour"] for r in rs).most_common(6)
    print(f"  {name}: " + ", ".join(f"{h:02}시 {100*v/len(rs):.0f}%" for h, v in c))

print("\n■ 분 단위 — 정각·30분 게시 비율 (예약 도구 사용 흔적)")
m = collections.Counter(r["minute"] for r in recent)
print(f"  :00 {100*m[0]/len(recent):.0f}%  :30 {100*m[30]/len(recent):.0f}%  그 외 {100*(1-(m[0]+m[30])/len(recent)):.0f}%")

print("\n■ 계정별 (최근 1년 · 건수 · 주 평균 · 최빈 시간대 3개 · 최빈 요일)")
for acc in sorted(set(r["account"] for r in rows)):
    rs = [r for r in recent if r["account"] == acc]
    if not rs:
        print(f"  {acc:17} (최근 1년 게시 없음)"); continue
    ts = sorted(datetime.datetime.fromisoformat(r["ts"]) for r in rs)
    weeks = max((ts[-1] - ts[0]).days, 7) / 7
    hc = collections.Counter(r["hour"] for r in rs).most_common(3)
    dc = collections.Counter(r["dow"] for r in rs).most_common(2)
    print(f"  {acc:17} {len(rs):3}건  주 {len(rs)/weeks:3.1f}회  "
          + " ".join(f"{h:02}시({100*v/len(rs):.0f}%)" for h, v in hc)
          + "  " + " ".join(f"{DOW[d]}({100*v/len(rs):.0f}%)" for d, v in dc))

print("\n■ 계정 가중 평균 (계정마다 분포를 100% 로 정규화 — 일 1회 이상 올리는 사연툰이 표본을 지배하지 않도록)")
accs = sorted(set(r["account"] for r in recent))
w = collections.Counter()
for acc in accs:
    rs = [r for r in recent if r["account"] == acc]
    for r in rs:
        w[r["hour"]] += 1 / len(rs) / len(accs)
for h in range(24):
    v = w.get(h, 0)
    print(f"  {h:02}시 {100*v:5.1f}%  {'█'*int(round(50*v))}")
blocks = [("07~09", range(7, 10)), ("10~12", range(10, 13)), ("13~15", range(13, 16)), ("16~18", range(16, 19)),
          ("19~20", range(19, 21)), ("21~23", range(21, 24)), ("00~06", list(range(0, 7)))]
print("  블록: " + ", ".join(f"{n} {100*sum(w.get(h,0) for h in hs):.0f}%" for n, hs in blocks))
