#!/usr/bin/env python3
"""Strict validator for guides_extra.json (run by publish.py). Exit 1 on any problem."""
import json, re, sys, os, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
errs = []
extra = json.load(open(os.path.join(HERE, "guides_extra.json"), encoding="utf-8"))
import importlib.util
spec = importlib.util.spec_from_file_location("g0", os.path.join(HERE, "guides.py"))
# base guides only (without extra): read slugs textually
base_slugs = re.findall(r'"slug": "([a-z0-9-]+)"', open(os.path.join(HERE, "guides.py"), encoding="utf-8").read())
import subprocess
niches = set(json.loads(subprocess.run(["node", "-e", "console.log(JSON.stringify(Object.keys(require(process.argv[1]).NICHES)))", os.path.join(HERE, "api", "products.js")], capture_output=True, text=True).stdout or "[]"))
if not niches: errs.append("could not read NICHES from api/products.js (is node installed?)")
BANNED = re.compile(r"100\s?%\s*(guarantee|protection|حماية|مضمون)|guaranteed|الأفضل في العالم|best in the world|لا مثيل له|miracle|معجزة|\bspy\b|تجسس|hidden camera|كاميرا مخفية|cure|يعالج", re.I)
seen = set(base_slugs)
for i, g in enumerate(extra):
    w = f"guide[{i}] {g.get('slug')}"
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+){1,7}", g.get("slug", "")): errs.append(f"{w}: bad slug")
    if g.get("slug") in seen: errs.append(f"{w}: duplicate slug")
    seen.add(g.get("slug"))
    if g.get("deals") not in niches: errs.append(f"{w}: deals '{g.get('deals')}' is not a niche in api/products.js")
    try: datetime.date.fromisoformat(g.get("date", ""))
    except Exception: errs.append(f"{w}: missing/invalid date YYYY-MM-DD")
    if g.get("picks"): errs.append(f"{w}: picks must be [] (agent guides link to live deals instead)")
    for L in ("ar", "en"):
        G = g.get(L) or {}
        for k, lo, hi in (("title", 15, 110), ("card", 10, 70), ("cardp", 20, 140), ("lead", 80, 400)):
            v = G.get(k, "")
            if not (lo <= len(v) <= hi): errs.append(f"{w}.{L}.{k}: length {len(v)} not in {lo}-{hi}")
        secs = G.get("sections", [])
        if not (4 <= len(secs) <= 8): errs.append(f"{w}.{L}: needs 4-8 sections, has {len(secs)}")
        for s in secs:
            if len(s) != 2 or not s[0] or not isinstance(s[1], list) or not (1 <= len(s[1]) <= 8) or any(not isinstance(x, str) or len(x) < 15 for x in s[1]):
                errs.append(f"{w}.{L}: malformed section {str(s)[:60]}")
        faq = G.get("faq", [])
        if not (3 <= len(faq) <= 6) or any(len(f) != 2 or len(f[0]) < 8 or len(f[1]) < 15 for f in faq): errs.append(f"{w}.{L}: needs 3-6 FAQ pairs")
        blob = json.dumps(G, ensure_ascii=False)
        m = BANNED.search(blob)
        if m: errs.append(f"{w}.{L}: banned/overclaiming phrase '{m.group(0)}'")
        if "http" in blob: errs.append(f"{w}.{L}: no links allowed inside guide text")
    if len(g.get("ar", {}).get("sections", [])) != len(g.get("en", {}).get("sections", [])): errs.append(f"{w}: ar/en section count differs")
if errs:
    print("GUIDES CHECK FAILED:"); [print(" -", x) for x in errs]; sys.exit(1)
print(f"guides_extra.json OK ({len(extra)} extra guides)")
