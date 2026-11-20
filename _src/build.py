#!/usr/bin/env python3
"""DoniaNova static site generator: bilingual, SEO-ready pages from data.json."""
import json, os, re, shutil, html, datetime
from guides import GUIDES

BASE = os.environ.get("DN_BASE", "https://donianova.vercel.app").rstrip("/")
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SRC_IMG = os.path.join(HERE, "img")
OUT = os.environ.get("DN_OUT", "dist")
TODAY = datetime.date.today().isoformat()

D = json.load(open("data.json"))
ICONS, CATS = D["ICONS"], D["CATS"]
CSS = open("style.css").read().replace("<style>", "").replace("</style>", "")
CSS += """
.crumbs{font-size:14px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;padding-block:18px 0}
.crumbs a{color:var(--muted)}
.detail{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:32px;align-items:start;padding-block:24px 48px}
@media (max-width:760px){.detail{grid-template-columns:1fr}}
.detail img{width:100%;max-width:100%;aspect-ratio:1;object-fit:cover;border-radius:var(--r);border:1px solid var(--line);background:var(--chip)}
.detail h1{font-size:clamp(26px,4vw,40px);margin:8px 0 14px}
.detail .lead{font-size:17px;color:var(--ink);margin:0 0 16px;max-width:60ch}
.detail .go{display:inline-flex;margin-top:16px;padding:14px 22px;font-size:16px}
.card h3 a{text-decoration:none}
.card h3 a:hover{text-decoration:underline}
.lang a{color:var(--night-ink);padding:6px 14px;border-radius:999px;font-size:14px;text-decoration:none}
.lang a[aria-current="true"]{background:#E6B95B;color:#101634;font-weight:600}
.sub{padding-block:16px 8px}

/* ---- v2: fixes + motion ---- */
[hidden]{display:none!important}
@view-transition{navigation:auto}
html{scroll-behavior:smooth}
::selection{background:#E6B95B;color:#101634}

/* masthead: drifting aurora under the stars */
.mast::before{content:"";position:absolute;inset:-40%;pointer-events:none;
  background:radial-gradient(40% 35% at 20% 30%,rgba(110,90,255,.22),transparent 70%),
             radial-gradient(35% 30% at 80% 60%,rgba(230,185,91,.16),transparent 70%),
             radial-gradient(30% 30% at 50% 90%,rgba(40,160,220,.14),transparent 70%);
  animation:aurora 22s ease-in-out infinite alternate}
@keyframes aurora{0%{transform:translate3d(-4%,-2%,0) rotate(0deg)}100%{transform:translate3d(4%,3%,0) rotate(8deg)}}
.mast .wrap{position:relative;z-index:1}
.brand svg{animation:twinkle 4s ease-in-out infinite;transform-origin:center}
@keyframes twinkle{0%,100%{transform:scale(1) rotate(0)}50%{transform:scale(1.12) rotate(45deg);filter:drop-shadow(0 0 8px rgba(230,185,91,.8))}}

/* hero entrance */
.hero>*{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}
.hero>*:nth-child(2){animation-delay:.08s}.hero>*:nth-child(3){animation-delay:.16s}
.hero>*:nth-child(4){animation-delay:.24s}.hero>*:nth-child(5){animation-delay:.32s}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.hero h1 .glow{background:linear-gradient(90deg,#F6E3B4,#E6B95B 40%,#FFF4D6 60%,#E6B95B);background-size:200% 100%;
  -webkit-background-clip:text;background-clip:text;color:transparent;animation:sheen 6s linear infinite}
@keyframes sheen{to{background-position:-200% 0}}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:8px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:13px 22px;border-radius:999px;font-weight:600;text-decoration:none;font-size:15px;transition:transform .25s,box-shadow .25s,background .25s}
.btn-gold{background:linear-gradient(135deg,#F2CF7E,#E6B95B 50%,#C9952E);color:#101634;box-shadow:0 8px 28px -8px rgba(230,185,91,.7)}
.btn-gold:hover{transform:translateY(-2px);box-shadow:0 14px 34px -8px rgba(230,185,91,.9)}
.btn-ghost{border:1px solid rgba(238,240,248,.3);color:#EEF0F8}
.btn-ghost:hover{background:rgba(238,240,248,.08);transform:translateY(-2px)}

/* trust strip */
.trust{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin-top:-28px;position:relative;z-index:2}
.trust div{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px;display:flex;gap:12px;align-items:center;box-shadow:0 10px 30px -18px rgba(16,22,52,.35)}
.trust b{display:block;font-size:15px}.trust span{font-size:13px;color:var(--muted)}
.trust i{font-style:normal;width:36px;height:36px;flex:none;border-radius:10px;display:grid;place-items:center;background:var(--gold-soft);color:var(--gold);font-size:18px}

/* cards: lift, spotlight, image zoom */
.card{position:relative;overflow:hidden;transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.card::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .3s;
  background:radial-gradient(320px circle at var(--mx,50%) var(--my,0%),rgba(230,185,91,.16),transparent 60%)}
.card:hover{transform:translateY(-6px);box-shadow:0 22px 44px -22px rgba(16,22,52,.45),0 0 0 1px rgba(230,185,91,.35);border-color:transparent}
.card:hover::before{opacity:1}
.card a:has(.shot){display:block;overflow:hidden;border-radius:10px}
.card .shot{transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.card:hover .shot{transform:scale(1.06)}
.card.enter{animation:pop .45s cubic-bezier(.2,.7,.2,1) both}
@keyframes pop{from{opacity:0;transform:translateY(12px) scale(.97)}to{opacity:1;transform:none}}
.go{position:relative;overflow:hidden;background:linear-gradient(135deg,#D9A647,var(--gold));transition:transform .25s,box-shadow .25s}
.go::after{content:"";position:absolute;inset:0;transform:translateX(-120%);background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.45) 50%,transparent 70%)}
.go:hover{transform:translateY(-1px);box-shadow:0 10px 24px -10px rgba(168,116,28,.8)}
.go:hover::after{transform:translateX(120%);transition:transform .8s}
.filters button{transition:background .25s,color .25s,transform .2s,border-color .25s}
.filters button:hover{transform:translateY(-1px);border-color:var(--gold)}
.count{font-size:14px;color:var(--muted);margin-top:-8px;margin-bottom:14px}

/* reveal on scroll (only when JS is running) */
.js .reveal{opacity:0;transform:translateY(22px);transition:opacity .8s cubic-bezier(.2,.7,.2,1),transform .8s cubic-bezier(.2,.7,.2,1)}
.js .reveal.in{opacity:1;transform:none}
.guide{transition:transform .3s}.guide:hover{transform:translateY(-4px)}

/* footer */
footer{background:var(--night);color:#AEB4CF;border-top:0}
footer a{color:#E6B95B}

.dealbtn{color:#101634;background:#E6B95B;padding:7px 14px;border-radius:999px;font-size:14px;font-weight:600;text-decoration:none;white-space:nowrap}
.dealbtn:hover{filter:brightness(1.08)}
.tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:18px}
.tabs button{border:1px solid var(--line);background:var(--chip);color:var(--ink);padding:9px 16px;border-radius:999px;font-size:14px;transition:background .25s,color .25s}
.tabs button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}
.deal h3{font-size:15px;line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.9em}
.priceRow{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}
.priceRow b{font-size:20px;font-variant-numeric:tabular-nums}
.priceRow s{color:var(--muted);font-size:13px}
.off{background:#E54B4B;color:#fff;font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px}
.meta{font-size:12.5px;color:var(--muted);display:flex;gap:10px;flex-wrap:wrap}
.skel{background:linear-gradient(90deg,var(--chip),var(--surface),var(--chip));background-size:200% 100%;animation:sk 1.2s linear infinite;border-radius:var(--r);min-height:330px}
@keyframes sk{to{background-position:-200% 0}}
.status{color:var(--muted);font-size:14px;margin-bottom:14px}
.card .shot{height:auto;aspect-ratio:1;object-fit:contain;background:#fff}
@media (max-width:520px){.dealbtn{padding:6px 10px;font-size:13px}}
.nova-fab{position:fixed;inset-inline-end:max(18px,env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:50;display:flex;align-items:center;gap:8px;border:0;border-radius:999px;padding:12px 18px;background:linear-gradient(135deg,#1B2350,#101634);color:#EEF0F8;font-weight:600;font-size:15px;box-shadow:0 14px 34px -10px rgba(16,22,52,.6),0 0 0 1px rgba(230,185,91,.4);cursor:pointer}
.nova-fab svg{width:22px;height:22px;animation:twinkle 4s ease-in-out infinite}
.nova-fab:hover{transform:translateY(-2px)}
.nova{padding:0!important;position:fixed;inset-inline-end:max(16px,env(safe-area-inset-right,0px));bottom:calc(82px + env(safe-area-inset-bottom,0px));z-index:51;width:min(380px,calc(100vw - 32px));height:min(560px,calc(100vh - 120px));display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:18px;box-shadow:0 30px 60px -20px rgba(16,22,52,.55);overflow:hidden;animation:pop .3s cubic-bezier(.2,.7,.2,1)}
.nova header{background:var(--night);color:#EEF0F8;padding:14px 16px;display:flex;align-items:center;gap:10px}
.nova header b{font-size:15px}.nova header small{display:block;color:#AEB4CF;font-size:12px;font-weight:400}
.nova header button{margin-inline-start:auto;background:none;border:0;color:#EEF0F8;font-size:22px;line-height:1;cursor:pointer}
.nova .log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}
.nova .m{max-width:88%;padding:10px 13px;border-radius:14px;font-size:14.5px;line-height:1.6;white-space:pre-wrap;overflow-wrap:anywhere}
.nova .m.a{background:var(--chip);color:var(--ink);align-self:flex-start;border-end-start-radius:4px}
.nova .m.u{background:var(--gold);color:#101634;align-self:flex-end;border-end-end-radius:4px}
.nova .m a{color:inherit;font-weight:600;text-decoration:underline}
.nova .chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px}
.nova .chips button{border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 11px;font-size:13px;cursor:pointer}
.nova form{display:flex;gap:8px;padding:10px;border-top:1px solid var(--line)}
.nova input{flex:1;min-width:0;border:1px solid var(--line);border-radius:12px;padding:11px 12px;font:inherit;background:var(--bg);color:var(--ink)}
.nova form button{border:0;border-radius:12px;padding:0 16px;background:var(--ink);color:var(--bg);font-weight:600;cursor:pointer}
.nova .typing{opacity:.7}
.nova .fine{font-size:11.5px;color:var(--muted);text-align:center;padding:0 10px 8px}
.article{max-width:72ch;font-size:17px;line-height:1.85}
.article h2{font-size:clamp(21px,2.6vw,26px);margin:34px 0 10px}
.article p{margin:0 0 14px}.article ul{margin:0 0 16px;padding-inline-start:22px}.article li{margin-bottom:6px}
.article .upd{color:var(--muted);font-size:14px}
.faq details{border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin-bottom:10px;background:var(--surface)}
.faq summary{cursor:pointer;font-weight:600}.faq details p{margin:10px 0 0;color:var(--muted)}
a.guide:hover h3{color:var(--gold)}
/* ---- v3 palette accents ---- */
.mast::before{background:radial-gradient(40% 35% at 20% 30%,rgba(140,100,255,.30),transparent 70%),radial-gradient(35% 30% at 80% 60%,rgba(242,194,102,.20),transparent 70%),radial-gradient(30% 30% at 50% 90%,rgba(59,212,207,.18),transparent 70%)!important}
.head h2,.article h2{position:relative;padding-bottom:10px}
.head h2::after{content:"";position:absolute;inset-inline-start:0;bottom:0;width:64px;height:4px;border-radius:4px;background:linear-gradient(90deg,var(--gold),var(--violet),var(--teal))}
.filters button[aria-pressed="true"],.tabs button[aria-pressed="true"]{background:linear-gradient(135deg,var(--violet),#3B22B8);color:#fff;border-color:transparent;box-shadow:0 8px 20px -10px var(--violet)}
.card .ic{background:var(--violet-soft);color:var(--violet)}
.tag{color:var(--violet);font-weight:600}
.best{background:var(--gold-soft);color:var(--ink)}
.card:hover{box-shadow:0 24px 48px -24px rgba(80,50,200,.45),0 0 0 1px rgba(156,132,255,.45)}
.card::before{background:radial-gradient(320px circle at var(--mx,50%) var(--my,0%),rgba(140,100,255,.14),transparent 60%)}
.trust div:nth-child(1) i{background:var(--violet-soft);color:var(--violet)}
.trust div:nth-child(2) i{background:var(--gold-soft);color:var(--gold)}
.trust div:nth-child(3) i{background:rgba(15,163,163,.12);color:var(--teal)}
.trust div:nth-child(4) i{background:var(--violet-soft);color:var(--violet)}
.guide{border-top:0;background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:18px;box-shadow:inset 0 4px 0 0 var(--gold)}
.guide:nth-child(2){box-shadow:inset 0 4px 0 0 var(--violet)}.guide:nth-child(3){box-shadow:inset 0 4px 0 0 var(--teal)}
.note{background:linear-gradient(135deg,var(--violet-soft),var(--gold-soft));border:1px solid var(--line);padding:24px}
.note h2{font-size:20px!important}
footer{background:linear-gradient(165deg,#1B1155,var(--night) 60%,#07041A);padding-bottom:84px!important}
.nova-fab{background:linear-gradient(135deg,#5B3BE0,#1B1155)!important}
.nova .m.u{background:linear-gradient(135deg,var(--violet),#3B22B8);color:#fff}
.share{display:flex;gap:28px;align-items:center;flex-wrap:wrap;background:linear-gradient(135deg,#1B1155,var(--night) 60%,#07041A);color:#F1EEFF;border-radius:20px;padding:28px;position:relative;overflow:hidden}
.share::after{content:"";position:absolute;inset:auto -60px -80px auto;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(140,100,255,.35),transparent 70%);pointer-events:none}
.share img{width:200px;height:200px;max-width:100%;border-radius:16px;background:#fff;padding:10px;box-shadow:0 0 0 4px rgba(242,194,102,.5),0 18px 40px -16px rgba(0,0,0,.6);flex:none}
.share-t{flex:1;min-width:240px;position:relative;z-index:1}
.share-t h2{font-size:clamp(22px,3vw,28px);color:#F1EEFF}
.share-t p{color:#C9C3EA;margin:8px 0 0}
.share-url{font-family:var(--f-display);color:#F2C266!important;font-weight:700;font-size:18px}
.share-b{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.sb{display:inline-flex;align-items:center;gap:6px;border:0;border-radius:999px;padding:10px 16px;font-size:14px;font-weight:600;text-decoration:none;color:#fff;cursor:pointer;transition:transform .2s,filter .2s}
.sb:hover{transform:translateY(-2px);filter:brightness(1.1)}
.sb-copy{background:linear-gradient(135deg,#F2CF7E,#E6B95B);color:#140D42}
.sb-wa{background:#1FA855}.sb-fb{background:#1877F2}.sb-tg{background:#229ED9}
.sb-dl{background:rgba(255,255,255,.12);box-shadow:inset 0 0 0 1px rgba(255,255,255,.3)}
@media (max-width:560px){.share{justify-content:center;text-align:center}.share-b{justify-content:center}}
@media (prefers-reduced-motion: reduce){.mast::before,.brand svg,.hero h1 .glow{animation:none}.js .reveal{opacity:1;transform:none}}
"""

UI = {
 "en": dict(dir="ltr", other="ar", label="EN", home="Home", view="View on AliExpress", details="Details",
            best="Best for", back="All picks", related="More picks in", disc_short="Affiliate link: we may earn a small commission at no extra cost to you.",
            site_title="DoniaNova — The best of tech: top-rated, best-selling, live prices",
            site_desc="Only the top-rated, best-selling and trending tech from AliExpress, honestly reviewed, with live prices. In Arabic, English and French."),
 "ar": dict(dir="rtl", other="en", label="عربي", home="الرئيسية", view="عرض على علي إكسبريس", details="التفاصيل",
            best="الأنسب لـ", back="كل المختارات", related="مختارات أخرى في", disc_short="رابط عمولة: قد نحصل على عمولة صغيرة دون أي تكلفة إضافية عليك.",
            site_title="دنيا نوفا | أفضل التقنية: الأعلى تقييماً والأكثر مبيعاً بأسعار حيّة",
            site_desc="نعرض لك فقط الأعلى تقييماً والأكثر مبيعاً والأكثر رواجاً من تقنيات علي إكسبريس، بمراجعة صادقة وأسعار حيّة. بالعربية والإنجليزية والفرنسية."),
}

def _L(lang):
    return "en" if lang == "fr" else lang

LANGS = ("en", "ar", "fr")

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-+", "-", s)[:60].strip("-")

PRODUCTS = [p for p in D["PRODUCTS"] if "s.click.aliexpress.com" in p["link"]]
for p in PRODUCTS:
    p["slug"] = slugify(p["en"][0])

e = lambda s: html.escape(s, quote=True)

def icon(p):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[p["ic"]]}</svg>'

def url(lang, path=""):
    return f"/{lang}/{path}"

def head(lang, title, desc, path, image=None, jsonld=None):
    u = UI[_L(lang)]
    canon = BASE + url(lang, path)
    alt = BASE + url(u["other"], path)
    img = BASE + (image or "/img/og.jpg")
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    return f"""<!doctype html>
<html lang="{lang}" dir="{u['dir']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
{''.join(f'<link rel="alternate" hreflang="{L_}" href="{BASE}/{L_}/{path}">' for L_ in LANGS)}
<link rel="alternate" hreflang="x-default" href="{BASE}/en/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DoniaNova">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="{dict(ar='ar_AR',en='en_US',fr='fr_FR')[lang]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#101634">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<script defer src="/_vercel/insights/script.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=El+Messiri:wght@500;700&family=Readex+Pro:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="/style.css">
{ld}
</head>
<body>
"""

WORLD_TONE = ["rose","cyan","teal","violet","gold","rose","blue","blue","blue","gold"]
def worlds(lang):
    out = []
    for i,(g,items) in enumerate(DEALS_T[_L(lang)]["tabs"]):
        ic, name = g.split(" ",1)
        out.append(dict(i=i, ic=ic, name=name, items=items, tone=WORLD_TONE[i % len(WORLD_TONE)]))
    return out

def masthead(lang, path, hero=""):
    u = UI[_L(lang)]; ar = lang == "ar"
    L = (lambda a, b: a if ar else b)
    W = worlds(lang)
    mega = "".join(f'<div class="mg-col"><a class="mg-h" href="/{lang}/deals/#{w["items"][0][0]}"><i>{w["ic"]}</i>{e(w["name"])}</a>'
                   + "".join(f'<a href="/{lang}/deals/#{k}">{e(n)}</a>' for k,n in w["items"][:6]) + '</div>' for w in W)
    cur = "home" if path == "" else "deals" if path.startswith("deals") else "guides" if path.startswith("guides") else "page"
    def nl(key, href, label):
        return f'<a href="{href}"{" aria-current=\"page\"" if cur==key else ""}>{label}</a>'
    nav = (nl("home", url(lang), L("الرئيسية","Home")) + f'<a href="/{lang}/deals/" class="nav-hot"{" aria-current=\"page\"" if cur=="deals" else ""}><span class="lamp" aria-hidden="true">💡</span><span class="neon">{L("العروض","Deals")}</span></a>'
           + f'<button type="button" class="mg-btn" aria-expanded="false" aria-controls="mega">{L("الأقسام","Sections")} <span aria-hidden="true">▾</span></button>'
           + nl("guides", url(lang, "guides/"), L("أدلة الشراء","Guides")))
    tg = (f'<div class="tgdd"><button type="button" class="tg-pill" aria-expanded="false"><svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path fill="currentColor" d="M21.9 4.3 18.7 19.4c-.2 1.1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.2 13 1.4 11.5c-1-.3-1.1-1 .2-1.5L20.5 2.8c.9-.3 1.7.2 1.4 1.5z"/></svg><span>{L("تيلغرام","Telegram")}</span></button>'
          f'<div class="tgmenu" hidden><a href="/api/telegram?go=1" target="_blank" rel="noopener"><img src="/img/tg-bot.jpg" alt="" width="40" height="40"><span><b>{L("بوت DoniaNova","DoniaNova bot")}</b><small>{L("اسأله عن أي منتج","Ask about any product")}</small></span></a>'
          f'<a href="https://t.me/donianova_deals" target="_blank" rel="noopener"><img src="/img/tg-channel.jpg" alt="" width="40" height="40"><span><b>{L("قناة العروض","Deals channel")}</b><small>{L("مقارنة جديدة كل صباح","A new comparison every morning")}</small></span></a></div></div>')
    back = ""
    if path:
        here = L("العروض","Deals") if cur == "deals" else L("أدلة الشراء","Guides") if cur == "guides" else L("المنتج","Product") if path.startswith("p/") else L("الصفحة","Page")
        back = (f'<div class="crumbs"><button type="button" class="backbtn" data-home="{url(lang)}">{L("→ رجوع","← Back")}</button>'
                + ('' if path.startswith("p/") else f'<nav aria-label="breadcrumb"><a href="{url(lang)}">{L("الرئيسية","Home")}</a><span aria-hidden="true">{L("‹","›")}</span><b>{e(here)}</b></nav>') + '</div>')
    return f"""  <div class="topbar" id="topbar"><div class="wrap top">
      <a class="brand" href="{url(lang)}" aria-label="DoniaNova">
        <svg width="28" height="28" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 1 L19 13 L31 16 L19 19 L16 31 L13 19 L1 16 L13 13 Z" fill="#E6B95B"/></svg>
        <b>Donia<span>Nova</span></b>
      </a>
      <nav class="mainnav" aria-label="{L('القائمة','Menu')}">{nav}</nav>
      <div class="tright">
      <form class="msearch" action="/{lang}/deals/" role="search"><input type="search" name="q" id="mq" aria-label="{L('ابحث عن منتج','Search products')}" placeholder="{L('ابحث عن منتج…','Search products…')}" autocomplete="off">{imgbtn(lang)}<button type="submit" aria-label="{L('بحث','Search')}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M20 20l-4.2-4.2" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg></button></form>
      {tg}
      <nav class="lang" aria-label="Language">
        <a href="/ar/{path}" hreflang="ar" lang="ar" aria-current="{str(lang=='ar').lower()}">عربي</a>
        <a href="/en/{path}" hreflang="en" lang="en" aria-current="{str(lang=='en').lower()}">EN</a>
        <a href="/fr/{path}" hreflang="fr" lang="fr" aria-current="{str(lang=='fr').lower()}">FR</a>
      </nav>
      </div>
  </div>
  <div class="mega" id="mega" hidden><div class="wrap"><div class="mg-grid">{mega}</div></div></div></div>
<header class="mast">
  <canvas id="sky" aria-hidden="true"></canvas>
  <div class="wrap">
    {back}
    {hero}
  </div>
</header>
<nav class="bbar" aria-label="{L('تنقل سريع','Quick nav')}">
  <a href="{url(lang)}"{' aria-current="page"' if cur=="home" else ''}><i>🏠</i><span>{L('الرئيسية','Home')}</span></a>
  <a href="/{lang}/deals/"{' aria-current="page"' if cur=="deals" else ''}><i>🔥</i><span>{L('العروض','Deals')}</span></a>
  <button type="button" class="bb-sec"><i>🧭</i><span>{L('الأقسام','Sections')}</span></button>
  <button type="button" class="bb-nova"><i>✨</i><span>{L('نوفا','Nova')}</span></button>
  <button type="button" class="bb-tg"><i>✈️</i><span>{L('تيلغرام','Telegram')}</span></button>
</nav>
"""

def fcols(lang):
    ar = lang == "ar"
    secs = [("barcode","قارئ الباركود","Barcode scanners"),("ssd","أقراص SSD","Portable SSDs"),("projector","داتاشو","Projectors"),("translator","أجهزة الترجمة","AI translators"),("powerbank","بطاريات محمولة","Power banks"),("board","ألواح الكتابة","Writing tablets")]
    c1 = "".join(f'<a href="/{lang}/deals/#{k}">{e(a if ar else b)}</a>' for k,a,b in secs)
    c2 = "".join(f'<a href="{url(lang, "guides/"+g["slug"]+"/")}">{e(g[_L(lang)]["card"])}</a>' for g in GUIDES)
    about = "مختارات تقنية صادقة للعمل والتعليم والسفر، بأسعار حيّة من علي إكسبريس." if ar else "Honest tech picks for work, teaching and travel, with live AliExpress prices."
    H = ("أقسام شائعة","أدلة الشراء","تابعنا") if ar else ("Popular sections","Buying guides","Follow us")
    follow = (f'<a href="https://www.facebook.com/305535802642278" target="_blank" rel="noopener">Facebook</a>'
              f'<a href="/api/telegram?go=1" target="_blank" rel="noopener">{"بوت تيلغرام" if ar else "Telegram bot"}</a>'
              f'<a href="https://t.me/donianova_deals" target="_blank" rel="noopener">{"قناة تيلغرام" if ar else "Telegram channel"}</a>'
              f'<a href="/daily.xml">{"مقارنة اليوم (RSS)" if ar else "Daily comparison (RSS)"}</a>'
              f'<a href="/privacy/">{"سياسة الخصوصية" if ar else "Privacy policy"}</a>')
    return (f'<div class="fgrid"><div class="fabout"><b class="flogo">Donia<i>Nova</i></b><p>{e(about)}</p></div>'
            f'<nav><h4>{H[0]}</h4>{c1}</nav><nav><h4>{H[1]}</h4>{c2}</nav><nav><h4>{H[2]}</h4>{follow}</nav></div>')

def footer(lang):
    t = D["T"][_L(lang)]
    S = {"ar": dict(h="شارك DoniaNova 📲", p="امسح الرمز بكاميرا الهاتف لفتح الموقع، أو شارك الصفحة مباشرة مع أصدقائك.", copy="نسخ الرابط", copied="تم النسخ ✓", dl="تحميل رمز QR", alt="رمز QR لموقع DoniaNova"),
         "en": dict(h="Share DoniaNova 📲", p="Scan the code with your phone camera to open the site, or share this page with your friends.", copy="Copy link", copied="Copied ✓", dl="Download QR code", alt="DoniaNova QR code")}[_L(lang)]
    share = f"""<section id="share"><div class="wrap"><div class="share">
  <img src="/img/qr-400.png" alt="{e(S['alt'])}" width="200" height="200" loading="lazy">
  <div class="share-t"><h2>{e(S['h'])}</h2><p>{e(S['p'])}</p>
  <p class="share-url" dir="ltr">donianova.vercel.app</p>
  <div class="share-b">
    <button type="button" class="sb sb-copy" data-copied="{e(S['copied'])}">🔗 <span>{e(S['copy'])}</span></button>
    <a class="sb sb-wa" data-net="wa" href="https://wa.me/?text=https%3A%2F%2Fdonianova.vercel.app%2F" target="_blank" rel="noopener">WhatsApp</a>
    <a class="sb sb-fb" data-net="fb" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdonianova.vercel.app%2F" target="_blank" rel="noopener">Facebook</a>
    <a class="sb sb-tg" data-net="tg" href="https://t.me/share/url?url=https%3A%2F%2Fdonianova.vercel.app%2F" target="_blank" rel="noopener">Telegram</a>
    <a class="sb sb-dl" href="/img/qr.png" download="DoniaNova-QR.png">⬇ {e(S['dl'])}</a>
  </div></div></div></div></section>"""
    return share + f"""<section><div class="wrap"><div class="note"><h2 style="font-size:17px">{e(t['discT'])}</h2><p>{e(t['discD'])}</p></div></div></section>
</main>
{overlays(lang)}
<footer class="fx"><div class="wrap">{fcols(lang)}<div class="fbot"><span>© {datetime.date.today().year} DoniaNova · {e(t['by'])}</span><span>{e(t['tag'])}</span></div></div></footer>
<script src="/site.js" defer></script>
</body></html>
"""

def card(p, lang):
    u = UI[_L(lang)]; name, why, best = p[_L(lang)]
    img = f'<a href="{url(lang, "p/"+p["slug"]+"/")}" tabindex="-1"><img class="shot" src="/{p["img"]}" alt="{e(name)}" loading="lazy" width="560" height="560"></a>' if p.get("img") else ""
    return f"""<article class="card" data-cat="{p['cat']}">
  {img}
  <div style="display:flex;align-items:center;gap:12px"><div class="ic">{icon(p)}</div><span class="tag">{e(CATS[p['cat']][_L(lang)])}</span></div>
  <h3><a href="{url(lang, 'p/'+p['slug']+'/')}">{e(name)}</a></h3>
  <p>{e(why)}</p>
  <div style="display:grid;gap:12px">
    <span class="best">{e(u['best'])}: {e(best)}</span>
    <a class="go" href="{p['link']}" target="_blank" rel="sponsored nofollow noopener">{e(u['view'])}</a>
  </div>
</article>"""

from v10 import hot_section, promise_band, overlays, imgbtn, V10_JS, CSS_V10, promo_bar, PROMO_JS, CSS_PROMO, CSS_GLOW
from catcards import CARD

HOME_CATS = {
 "ar": ("كل أقسام التقنية 🧭","عروض حيّة من علي إكسبريس، تتحدّث تلقائياً كل ساعة.",[("📶","قارئ QR لاسلكي","qrscan"),("⚡","شاحن لاسلكي","wcharge"),("🎧","سماعات رأس لاسلكية","headphone"),("🔊","مكبر صوت بلوتوث","btspeaker"),("🖱️","فأرة لاسلكية","wmouse"),("🚗","CarPlay لاسلكي","carplay"),("📡","مقوّي واي فاي","extender"),("💍","ماسح الخاتم","ringscan"),("🏷️","قارئ الباركود","barcode"),("💾","أقراص SSD محمولة","ssd"),("🗄️","أقراص صلبة خارجية","hdd"),("🔌","شواحن سريعة","charger"),("🔋","بطاريات محمولة","powerbank"),("📱","حوامل الهاتف","phone"),("⌚","ساعات ذكية","watch"),("🎧","سماعات","audio"),("⌨️","لوحات مفاتيح","keyboard"),("✍️","ألواح الكتابة","board"),("🎥","كاميرات ويب","webcam"),("🎙️","ميكروفونات","mic"),("📽️","بروجكتور داتاشو","projector"),("🖥️","شاشات محمولة","monitor"),("🌐","أجهزة الترجمة","translator"),("🖊️","قلم الترجمة","scanpen"),("🎙️","مسجّل صوت","recorder"),("💡","إضاءة وحامل","ringlight"),("🎬","كاميرا أكشن","actioncam"),("💳","بطاقات الذاكرة","microsd"),("🧾","طابعات الفواتير","receiptprn"),("📄","كاميرا المستندات","doccam"),("✈️","محوّلات السفر","travel"),("🧳","ميزان الحقائب","luggage"),("🛡️","حماية RFID","rfid")],
        "لا تعرف ماذا تختار؟","اسأل نوفا: يبحث ويقارن لك بين المنتجات بأسعارها الحالية.","🤖 اسأل نوفا"),
 "en": ("All tech sections 🧭","Live AliExpress deals, refreshed automatically every hour.",[("📶","Wireless QR scanners","qrscan"),("⚡","Wireless chargers","wcharge"),("🎧","Wireless headphones","headphone"),("🔊","Bluetooth speakers","btspeaker"),("🖱️","Wireless mice","wmouse"),("🚗","Wireless CarPlay","carplay"),("📡","Wi-Fi extenders","extender"),("💍","Ring scanners","ringscan"),("🏷️","Barcode scanners","barcode"),("💾","Portable SSDs","ssd"),("🗄️","External hard drives","hdd"),("🔌","Fast chargers","charger"),("🔋","Power banks","powerbank"),("📱","Phone holders","phone"),("⌚","Smart watches","watch"),("🎧","Earbuds","audio"),("⌨️","Keyboards","keyboard"),("✍️","Writing tablets","board"),("🎥","Webcams","webcam"),("🎙️","Microphones","mic"),("📽️","Projectors","projector"),("🖥️","Portable monitors","monitor"),("🌐","AI translators","translator"),("🖊️","Translation pens","scanpen"),("🎙️","Voice recorders","recorder"),("💡","Ring lights","ringlight"),("🎬","Action cameras","actioncam"),("💳","Memory cards","microsd"),("🧾","Receipt printers","receiptprn"),("📄","Document cameras","doccam"),("✈️","Travel adapters","travel"),("🧳","Luggage scales","luggage"),("🛡️","RFID protection","rfid")],
        "Not sure what to pick?","Ask Nova: it searches and compares products at their current prices.","🤖 Ask Nova"),
}

def hsearch(lang):
    ar = lang == "ar"
    pop = [("qrscan","قارئ QR لاسلكي","Wireless QR scanner"),("wcharge","شاحن لاسلكي","Wireless charger"),("barcode","قارئ باركود","Barcode scanner"),("ssd","SSD محمول","Portable SSD"),("projector","داتاشو","Projector"),("translator","جهاز ترجمة","AI translator"),("powerbank","بطارية محمولة","Power bank")]
    chips = "".join(f'<a href="/{lang}/deals/#{k}">{e(a if ar else b)}</a>' for k,a,b in pop)
    return (f'<form class="hsearch" action="/{lang}/deals/" role="search">'
            f'<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M20 20l-4.2-4.2" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
            f'<input type="search" name="q" id="hq" autocomplete="off" aria-label="{"ابحث عن منتج" if ar else "Search products"}" placeholder="{"ابحث عن أي منتج تقني: سماعة، SSD، داتاشو…" if ar else "Search any tech product: earbuds, SSD, projector…"}">'
            + imgbtn(lang) + f'<button type="submit">{"ابحث" if ar else "Search"}</button></form>'
            f'<div class="hpop"><span>{"الأكثر بحثاً:" if ar else "Popular:"}</span>{chips}</div>')

def catcard(ic, n, k, lang):
    tone, bar, ben, har, hen = CARD.get(k, ("violet","","","",""))
    badge = bar if lang == "ar" else ben
    hook = har if lang == "ar" else hen
    cta = "تسوّق الآن" if lang == "ar" else "Shop now"
    arrow = "←" if lang == "ar" else "→"
    b = f'<span class="cc-badge">{e(badge)}</span>' if badge else ''
    return (f'<a class="cc tone-{tone}" href="/{lang}/deals/#{k}">{b}'
            f'<span class="cc-orb" aria-hidden="true"><i>{ic}</i></span>'
            f'<b class="cc-name">{e(n)}</b><span class="cc-hook">{e(hook)}</span>'
            f'<span class="cc-cta">{e(cta)} <em>{arrow}</em></span></a>')

def stats_band(lang):
    ar = lang == "ar"
    S = [(str(sum(len(i) for _, i in DEALS_T["en"]["tabs"])),"قسماً حيّاً","live sections"),("600+","عرض تتحدث أسعاره كل ساعة","deals refreshed hourly"),("85%+","أدنى تقييم نقبل عرضه","minimum rating we list"),("1","مقارنة جديدة صادقة كل يوم","honest comparison every day")]
    cells = "".join(f'<div><b>{n}</b><span>{e(a if ar else b)}</span></div>' for n,a,b in S)
    return f'<div class="wrap"><div class="stats">{cells}</div></div>'

def brands_band(lang):
    ar = lang == "ar"
    B = ["DJI","Lenovo","SanDisk","Kodak","ORICO","NETUM","Baseus","UGREEN","Xiaomi","Anker","QCY","Eyoyo"]
    row = "".join(f'<span>{b}</span>' for b in B)
    t = "علامات تظهر باستمرار في عروضنا" if ar else "Brands you will often find in our deals"
    return f'<section class="brands" aria-label="{e(t)}"><div class="wrap"><p>{e(t)}</p></div><div class="marq" dir="ltr"><div class="mtrack">{row}{row}</div></div></section>'

def today_section(lang):
    ar = lang == "ar"
    T = dict(h="🏆 مقارنة اليوم" if ar else "🏆 Today's comparison",
             p="كل يوم يقارن وكيلنا الذكي أفضل 3 منتجات في قسم واحد بالأرقام الحقيقية، ويختار الأفضل قيمة." if ar else "Every day our AI agent compares the top 3 products in one section with real numbers and picks the best value.",
             win="اختيار اليوم" if ar else "Today's pick", buy="🛒 اطلبه الآن" if ar else "🛒 Get it now",
             more="قارن القسم كاملاً" if ar else "Compare the full section", sold="مبيع" if ar else "sold")
    cfg = json.dumps(T, ensure_ascii=False).replace("</", "<\\/")
    return f"""<section id="today" hidden><div class="wrap"><div class="head"><div><h2>{e(T['h'])}</h2><p>{e(T['p'])}</p></div></div>
<div class="today" id="todayBox"></div></div></section>
<script>(function(){{var T={cfg},L='{lang}';function x(s){{return String(s==null?'':s).replace(/[&<>"]/g,function(c){{return{{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]}})}}
fetch('/api/today').then(function(r){{return r.json()}}).then(function(t){{if(!t||t.error||!t.winner)return;var top=(t.top||[]).slice(0,3),w=t.winner;
var others=top.filter(function(p){{return p.title!==w.title}}).slice(0,2);
var lines=String((t.posts&&t.posts[L])||t.post||'').split('\\n').filter(Boolean);
var box=document.getElementById('todayBox');
box.innerHTML='<article class="tw card"><span class="tw-badge">'+x(T.win)+'</span><img src="'+x(w.img)+'" alt="" loading="lazy"><div class="tw-b"><h3>'+x(((t.names&&t.names[L]&&t.names[L][t.wi])||w.title).slice(0,90))+'</h3><div class="tw-m"><b>$'+x(w.price)+'</b><span>⭐ '+x(w.rating||'—')+'</span><span>🛒 '+x(w.sold)+' '+x(T.sold)+'</span></div><a class="go buy" href="'+x(w.link)+'" target="_blank" rel="sponsored nofollow noopener">'+x(T.buy)+'</a></div></article>'
+'<div class="tl"><div class="tpost">'+lines.slice(0,6).map(function(l){{return '<p>'+x(l)+'</p>'}}).join('')+'</div>'
+'<div class="tmini">'+others.map(function(p){{return '<div class="card"><img src="'+x(p.img)+'" alt="" loading="lazy"><span>$'+x(p.price)+' · ⭐ '+x(p.rating||'—')+'</span></div>'}}).join('')+'</div>'
+'<a class="btn btn-ghost tmore" href="/'+L+'/deals/#'+x(t.niche)+'">'+x(T.more)+' →</a></div>';
document.getElementById('today').hidden=false;}}).catch(function(){{}});}})();</script>"""

def tg_band(lang):
    ar = lang == "ar"
    L = (lambda a, b: a if ar else b)
    return f"""<section class="tgx-s reveal"><div class="wrap"><div class="tgx">
<div class="tgx-head"><span class="tgx-pill">Telegram</span><h2>{L("DoniaNova في جيبك ✈️","DoniaNova in your pocket ✈️")}</h2><p>{L("بوت يجيبك عن أي منتج في ثوانٍ، وقناة تصلك فيها مقارنة جديدة كل صباح. مجاناً.","A bot that answers about any product in seconds, and a channel with a fresh comparison every morning. Free.")}</p></div>
<a class="tgx-card" href="/api/telegram?go=1" target="_blank" rel="noopener"><img src="/img/tg-bot.jpg" alt="" width="72" height="72" loading="lazy">
 <div><b>{L("بوت DoniaNova","DoniaNova bot")}</b><span>{L("اكتب «قارئ باركود» أو «SSD 1TB» ويرسل لك أفضل العروض بصورها وأسعارها.","Type “barcode scanner” or “1TB SSD” and get the best deals with photos and prices.")}</span><em>@DoniaNovaBot</em></div>
 <i class="tgx-go">{L("افتح البوت ↗","Open bot ↗")}</i></a>
<a class="tgx-card ch" href="https://t.me/donianova_deals" target="_blank" rel="noopener"><img src="/img/tg-channel.jpg" alt="" width="72" height="72" loading="lazy">
 <div><b>{L("قناة العروض اليومية","Daily deals channel")}</b><span>{L("كل صباح: أفضل 3 منتجات في قسم، بالأرقام الحقيقية، واختيارنا الأوفر.","Every morning: top 3 products in one section, real numbers, our best-value pick.")}</span><em>@donianova_deals</em></div>
 <i class="tgx-go">{L("انضم للقناة ↗","Join channel ↗")}</i></a>
</div></div></section>"""

def worlds_section(lang):
    ar = lang == "ar"
    tiles = ""
    for w in worlds(lang):
        sub = " · ".join(n for _,n in w["items"][:3])
        cnt = (f'{len(w["items"])} أقسام' if len(w["items"])>2 else f'{len(w["items"])} قسم') if ar else f'{len(w["items"])} sections'
        tiles += (f'<a class="wt tone-{w["tone"]}" href="/{lang}/deals/#{w["items"][0][0]}"><span class="wt-ic" aria-hidden="true">{w["ic"]}</span>'
                  f'<b>{e(w["name"])}</b><small>{e(sub)}</small><span class="wt-f"><em>{e(cnt)}</em><i aria-hidden="true">{"←" if ar else "→"}</i></span></a>')
    h = "تسوّق حسب العالم 🧭" if ar else "Shop by world 🧭"
    W_ = worlds(lang); NS_ = sum(len(w["items"]) for w in W_)
    p = f"{len(W_)} عوالم تقنية و{NS_} قسماً بأسعار حيّة. اختر عالمك وابدأ." if ar else f"{len(W_)} tech worlds, {NS_} sections, live prices. Pick yours."
    nova = ("لا تعرف ماذا تختار؟","اسأل نوفا: يبحث ويقارن لك بين المنتجات بأسعارها الحالية.","✨ اسأل نوفا") if ar else ("Not sure what to pick?","Ask Nova: it searches and compares products at their current prices.","✨ Ask Nova")
    return f"""<section id="cats" class="reveal"><div class="wrap"><div class="head"><div><h2>{e(h)}</h2><p>{e(p)}</p></div></div>
<div class="wgrid">{tiles}</div>
<div class="ask-nova"><div><b>{e(nova[0])}</b><p>{e(nova[1])}</p></div><button type="button" class="btn btn-gold" onclick="var f=document.querySelector('.nova-fab');if(f)f.click()">{e(nova[2])}</button></div></div></section>"""

def wireless_band(lang):
    ar = lang == "ar"
    h = "عالم اللاسلكي" if ar else "The wireless world"
    p = "بلا أسلاك، بلا فوضى. أجهزة لاسلكية مختارة بتقييم 85% فأكثر، وأسعار حيّة من علي إكسبريس." if ar else "No cables, no clutter. Wireless gear rated 85%+ only, with live AliExpress prices."
    items = [("qrscan","📶","قارئ QR لاسلكي","Wireless QR scanner","امسح بحرية بعيداً عن الحاسوب","Scan freely away from the PC"),
             ("wcharge","⚡","شاحن لاسلكي 3 في 1","3-in-1 wireless charger","الهاتف والساعة والسماعة معاً","Phone, watch and buds together"),
             ("headphone","🎧","سماعات رأس لاسلكية","Wireless headphones","عزل ضجيج لتركيز أعمق","Noise cancelling for deep focus"),
             ("carplay","🚗","CarPlay لاسلكي","Wireless CarPlay","يتصل تلقائياً عند ركوبك","Connects as soon as you get in"),
             ("btspeaker","🔊","مكبر صوت بلوتوث","Bluetooth speaker","مقاوم للماء وصوت قوي","Waterproof, big sound"),
             ("ringscan","💍","ماسح الخاتم","Ring scanner","ماسح في إصبعك ويداك حرّتان","On your finger, hands free")]
    tiles = "".join(f'<a class="wl-tile" href="/{lang}/deals/#{k}"><span class="wl-ic" aria-hidden="true">{ic}</span><b>{e(na if ar else ne)}</b><small>{e(ha if ar else he)}</small><em>{"تسوّق ←" if ar else "Shop →"}</em></a>' for k,ic,na,ne,ha,he in items)
    btn = "كل الأجهزة اللاسلكية" if ar else "All wireless gear"
    return f"""<section class="wl-s reveal"><div class="wrap"><div class="wl">
<div class="wl-waves" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
<div class="wl-head"><span class="wl-pill">{"جديد" if ar else "New"}</span><h2><span class="wl-gt">{e(h)}</span> <span aria-hidden="true">📶</span></h2><p>{e(p)}</p><a class="btn btn-gold" href="/{lang}/deals/#qrscan">{e(btn)} {"←" if ar else "→"}</a></div>
<div class="wl-grid">{tiles}</div></div></div></section>"""

def home(lang):
    t = D["T"][_L(lang)]; u = UI[_L(lang)]
    cats_used = [k for k in CATS if k == "all" or any(p["cat"] == k for p in PRODUCTS)]
    filters = "".join(f'<button type="button" id="f-{k}" data-cat="{k}" aria-pressed="{str(k=="all").lower()}">{e(CATS[k][_L(lang)])}</button>' for k in cats_used)
    cta = ("تصفّح المختارات", "🔥 عروض اليوم") if lang == "ar" else ("Browse the picks", "🔥 Today's deals")
    art_items = [p for p in PRODUCTS if p.get("img")][:3]
    live = "أسعار حيّة · تتحدث كل ساعة" if lang == "ar" else "Live prices · updated hourly"
    art = '<div class="h-art" aria-hidden="true"><span class="h-live">⚡ ' + e(live) + '</span>' + "".join(
        f'<div class="fc fc{i+1}"><img src="/{p["img"]}" alt="" width="220" height="220"><b>{e(p[_L(lang)][0][:34])}</b><span>{e(CATS[p["cat"]][_L(lang)])}</span></div>'
        for i, p in enumerate(art_items)) + '<div class="h-orb"></div></div>'
    hero = f"""<div class="hero hero2"><div class="h-txt"><div class="eyebrow">{e(t['eyebrow'])}</div><h1><span class="glow">{e(t['title'])}</span></h1><p>{e(t['lead'])}</p>
    <div class="pillars"><span>{e(t['p1'])}</span><span>{e(t['p2'])}</span><span>{e(t['p3'])}</span><span>{e(t['p4'])}</span></div>
    {hsearch(lang)}
    <div class="cta-row"><a class="btn btn-gold" href="#picks">{e(cta[0])} ↓</a><a class="btn btn-ghost" href="/{lang}/deals/">{e(cta[1])}</a></div></div>{art}</div>"""
    TR = {"ar":[("✓","مختارة يدوياً","كل منتج نراجع مواصفاته"),("⚠","عيوب بصراحة","نذكر ما لا يناسبك أيضاً"),("🌍","3 لغات","عربي، إنجليزي، فرنسي"),("↻","تحديث أسبوعي","عروض وحملات جديدة")],
          "en":[("✓","Hand-picked","Every spec checked"),("⚠","Honest downsides","We say who it is not for"),("🌍","3 languages","Arabic, English, French"),("↻","Updated weekly","New deals and campaigns")]}[_L(lang)]
    trust = "".join(f'<div><i aria-hidden="true">{a}</i><p style="margin:0"><b>{e(b)}</b><span>{e(c)}</span></p></div>' for a,b,c in TR)
    count_tpl = ("المعروض: {n}" if lang == "ar" else "Showing: {n}")
    readl = "اقرأ الدليل ←" if lang == "ar" else "Read the guide →"
    guides = "".join(f'<a class="guide" href="{url(lang, "guides/"+g["slug"]+"/")}" style="text-decoration:none;color:inherit"><span class="soon">{e(readl)}</span>{new_badge(g, lang)}<h3>{e(g[_L(lang)]["card"])}</h3><p>{e(g[_L(lang)]["cardp"])}</p></a>' for g in GUIDES)
    ld = [
      {"@context":"https://schema.org","@type":"WebSite","name":"DoniaNova","url":BASE+url(lang),"inLanguage":lang,
       "publisher":{"@type":"Organization","name":"DONIA LABS TECH","url":"https://donialabstech.online"}},
      {"@context":"https://schema.org","@type":"ItemList","name":t["picksT"],"itemListElement":[
        {"@type":"ListItem","position":i+1,"url":BASE+url(lang,"p/"+p["slug"]+"/"),"name":p[_L(lang)][0]} for i,p in enumerate(PRODUCTS)]}
    ]
    return (head(lang, u["site_title"], u["site_desc"], "", jsonld=ld) + masthead(lang, "", hero) + f"""<main>
<div class="wrap"><div class="trust">{trust}</div></div>
{promo_bar(lang)}
{hot_section(lang)}
{promise_band(lang)}
{stats_band(lang)}
{wireless_band(lang)}
{tg_band(lang)}
{today_section(lang)}
<section id="picks"><div class="wrap">
  <div class="head"><div><h2>{e(t['picksT'])}</h2><p>{e(t['picksD'])}</p></div>
  <div class="filters" id="filters" role="group">{filters}</div></div>
  <p class="count" id="count" data-tpl="{e(count_tpl)}" aria-live="polite">{e(count_tpl.replace('{n}', str(len(PRODUCTS))))}</p>
  <div class="grid" id="grid">{''.join(card(p, lang) for p in PRODUCTS)}</div>
</div></section>
{worlds_section(lang)}
{brands_band(lang)}
<section id="how" class="reveal" style="padding-top:8px"><div class="wrap"><div class="head"><div><h2>{e(t['guidesT'])}</h2><p>{e(t['guidesD'])}</p></div></div>
<div class="guides">{guides}</div></div></section>
""" + footer(lang))

def product(p, lang):
    u = UI[_L(lang)]; name, why, best = p[_L(lang)]
    path = "p/" + p["slug"] + "/"
    cat = CATS[p["cat"]][_L(lang)]
    title = f"{name} | DoniaNova"
    desc = why[:155]
    related = [q for q in PRODUCTS if q is not p and q["cat"] == p["cat"]][:3] or [q for q in PRODUCTS if q is not p][:3]
    ld = [{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":u["home"],"item":BASE+url(lang)},
        {"@type":"ListItem","position":2,"name":name,"item":BASE+url(lang,path)}]}]
    img = f'<img src="/{p["img"]}" alt="{e(name)}" width="560" height="560">' if p.get("img") else f'<div class="ic" style="width:100%;height:auto;aspect-ratio:1;border-radius:14px">{icon(p)}</div>'
    return (head(lang, title, desc, path, image="/"+p["img"] if p.get("img") else None, jsonld=ld) + masthead(lang, path) + f"""<main>
<div class="wrap">
  <nav class="crumbs" aria-label="breadcrumb"><a href="{url(lang)}">{e(u['home'])}</a><span>/</span><span>{e(cat)}</span></nav>
  <article class="detail">
    <div>{img}</div>
    <div>
      <span class="tag">{e(cat)}</span>
      <h1>{e(name)}</h1>
      <p class="lead">{e(why)}</p>
      <span class="best">{e(u['best'])}: {e(best)}</span><br>
      <a class="go" href="{p['link']}" target="_blank" rel="sponsored nofollow noopener">{e(u['view'])}</a>
      <p style="color:var(--muted);font-size:13px;margin-top:12px">{e(u['disc_short'])}</p>
    </div>
  </article>
</div>
<section class="sub"><div class="wrap"><div class="head"><div><h2>{e(u['related'])} {e(cat)}</h2></div></div>
<div class="grid">{''.join(card(q, lang) for q in related)}</div></div></section>
""" + footer(lang))

def guide_page(g, lang):
    G = g[_L(lang)]; u = UI[_L(lang)]; path = "guides/" + g["slug"] + "/"
    bysl = {p["slug"]: p for p in PRODUCTS}
    picks = [bysl[x] for x in g["picks"] if x in bysl]
    body = ""
    for h, paras in G["sections"]:
        body += f'<h2>{e(h)}</h2>'; inl = False
        for x in paras:
            isl = x[:1] in "•123456789"
            if isl and not inl: body += "<ul>"; inl = True
            if not isl and inl: body += "</ul>"; inl = False
            body += f"<li>{e(x.lstrip('• '))}</li>" if isl else f"<p>{e(x)}</p>"
        if inl: body += "</ul>"
    faq_h = "أسئلة شائعة" if lang == "ar" else "Frequently asked questions"
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in G["faq"])
    picks_h = "منتجات راجعناها لهذا الدليل" if lang == "ar" else "Products we reviewed for this guide"
    deals_l = "🔥 شاهد عروض اليوم في هذا القسم" if lang == "ar" else "🔥 See today's deals in this category"
    upd = ("آخر تحديث: " if lang == "ar" else "Last updated: ") + g.get("date", TODAY)
    ld = [{"@context":"https://schema.org","@type":"Article","headline":G["title"],"description":G["lead"],"inLanguage":lang,"dateModified":TODAY,
           "author":{"@type":"Organization","name":"DoniaNova"},"publisher":{"@type":"Organization","name":"DONIA LABS TECH"},"mainEntityOfPage":BASE+url(lang,path)},
          {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in G["faq"]]}]
    hero = f'<div class="hero" style="padding-block:28px 56px"><div class="eyebrow">{e("دليل شراء" if lang=="ar" else "Buying guide")}</div><h1><span class="glow">{e(G["title"])}</span></h1><p>{e(G["lead"])}</p></div>'
    return (head(lang, G["title"] + " | DoniaNova", G["lead"][:155], path, jsonld=ld) + masthead(lang, path, hero) + f"""<main>
<div class="wrap"><nav class="crumbs" aria-label="breadcrumb"><a href="{url(lang)}">{e(u['home'])}</a><span>/</span><span>{e(G['card'])}</span></nav></div>
<section style="padding-top:20px"><div class="wrap"><article class="article">
<p class="upd">{e(upd)}</p>{body}
<p><a class="btn btn-gold" href="{url(lang,'deals/')}#{g.get('deals','')}">{e(deals_l)}</a></p>
<h2>{e(faq_h)}</h2><div class="faq">{faq}</div>
</article></div></section>
""" + (f'''<section class="sub"><div class="wrap"><div class="head"><div><h2>{e(picks_h)}</h2></div></div>
<div class="grid">{''.join(card(q, lang) for q in picks)}</div></div></section>''' if picks else "") + footer(lang))

def new_badge(g, lang):
    try: fresh = (datetime.date.today() - datetime.date.fromisoformat(g.get("date", "2000-01-01"))).days <= 14
    except Exception: fresh = False
    return f'<span class="g-new">{"🆕 جديد" if lang == "ar" else "🆕 New"}</span>' if fresh else ""

def guides_index(lang):
    ar = lang == "ar"; path = "guides/"
    t = "أدلة الشراء" if ar else "Buying guides"
    lead = ("أدلة قصيرة وصادقة تساعدك على الاختيار قبل الشراء: ما المواصفات التي تهم فعلاً، وما الذي نتجنّبه، ولمن يناسب كل منتج. نضيف دليلاً جديداً كل أسبوع."
            if ar else "Short, honest guides to help you choose before you buy: which specs really matter, what we avoid, and who each product suits. A new guide every week.")
    readl = "اقرأ الدليل ←" if ar else "Read the guide →"
    gs = sorted(GUIDES, key=lambda g: g.get("date", "2026-11-01"), reverse=True)
    cards = "".join(f'<a class="guide" href="{url(lang, "guides/"+g["slug"]+"/")}" style="text-decoration:none;color:inherit"><span class="soon">{e(readl)}</span>{new_badge(g, lang)}<h3>{e(g[_L(lang)]["card"])}</h3><p>{e(g[_L(lang)]["cardp"])}</p></a>' for g in gs)
    hero = f'<div class="hero" style="padding-block:28px 56px"><div class="eyebrow">{e("📚 " + t)}</div><h1><span class="glow">{e(t)}</span></h1><p>{e(lead)}</p></div>'
    return (head(lang, t + " | DoniaNova", lead[:155], path) + masthead(lang, path, hero) + f"""<main>
<section style="padding-top:20px"><div class="wrap"><div class="guides">{cards}</div></div></section>
""" + footer(lang))

DEALS_T = {
 "ar": dict(title="عروض اليوم | DoniaNova", h="عروض اليوم 🔥", lead="منتجات رائجة في مجالاتنا، بأسعار محدّثة تلقائياً من علي إكسبريس. السعر النهائي قد يتغيّر، فتأكّد منه على صفحة المنتج.",
   tabs=[("🔥 الأكثر رواجاً",[("smartring","خاتم ذكي"),("dashcam","كاميرا السيارة"),("seccam","كاميرا مراقبة واي فاي"),("ledstrip","إضاءة LED ذكية"),("carvac","مكنسة السيارة"),("gamepad","يد تحكم للألعاب"),("massager","مسدس التدليك"),("trimmer","ماكينة الحلاقة"),("toothbrush","فرشاة أسنان كهربائية"),("neckfan","مروحة الرقبة")]),
         ("📶 عالم اللاسلكي",[("qrscan","قارئ QR لاسلكي"),("ringscan","ماسح الخاتم"),("wmouse","فأرة لاسلكية"),("wcombo","لوحة وفأرة لاسلكية"),("wcharge","شاحن لاسلكي"),("headphone","سماعات رأس لاسلكية"),("btspeaker","مكبر صوت بلوتوث"),("btreceiver","مستقبل بلوتوث"),("carplay","CarPlay لاسلكي"),("wifi","محوّل واي فاي"),("extender","مقوّي واي فاي")]),
         ("📱 الهاتف والصوت",[("audio","سماعات"),("phone","حوامل الهاتف"),("charger","شواحن سريعة"),("powerbank","بطاريات محمولة"),("cable","كوابل الشحن"),("watch","ساعات ذكية")]),
         ("💾 التخزين والحاسوب",[("ssd","أقراص SSD محمولة"),("hdd","أقراص صلبة خارجية"),("microsd","بطاقات الذاكرة"),("cardreader","قارئ البطاقات"),("flash","فلاش USB"),("class","موزّعات USB"),("keyboard","لوحات مفاتيح")]),
         ("🏷️ الأعمال والأمان",[("barcode","قارئ الباركود"),("labelprn","طابعات الملصقات"),("receiptprn","طابعات الفواتير"),("rfid","حماية RFID"),("tracker","أجهزة التتبّع"),("car","تشخيص السيارة")]),
         ("🎓 التعليم",[("board","ألواح الكتابة"),("presenter","مؤشر العرض"),("webcam","كاميرات ويب"),("mic","ميكروفونات")]),
         ("📽️ العرض (داتاشو)",[("projector","بروجكتور داتاشو"),("projscreen","شاشات العرض"),("hdmiwifi","HDMI لاسلكي"),("monitor","شاشات محمولة"),("doccam","كاميرا المستندات")]),
         ("🎙️ التسجيل والتصوير",[("recorder","مسجّل صوت"),("ringlight","إضاءة وحامل"),("gimbal","مثبّت الهاتف"),("actioncam","كاميرا أكشن")]),
         ("🌐 الترجمة",[("translator","جهاز ترجمة فورية"),("transbuds","سماعات الترجمة"),("scanpen","قلم الترجمة الماسح")]),
         ("✈️ السفر",[("travel","محوّلات السفر"),("luggage","ميزان الحقائب"),("organizer","منظّم الإلكترونيات")])],
   loading="جارٍ تحميل العروض…", fail="تعذّر تحميل العروض الآن. جرّب بعد قليل، أو تصفّح مختاراتنا.", empty="لا توجد عروض في هذا القسم حالياً.",
   go="🛒 اشترِ الآن", sold="بيع", updated="آخر تحديث", back="← مختاراتنا المراجَعة",
   sph="ابحث عن أي منتج: قارئ باركود، SSD 1TB، داتاشو…", sbtn="ابحث",
   S={"res":"نتائج البحث","for":"عن","hook":"نتائج حيّة من علي إكسبريس، مرتّبة حسب الأكثر مبيعاً، وأخفينا ما تقييمه ضعيف.","cats":"أقسام مطابقة:","none":"لم نجد نتائج. جرّب كلمة أبسط، أو اختر قسماً من الأقسام.","short":"اكتب حرفين على الأقل."}),
 "en": dict(title="Today's Deals | DoniaNova", h="Today's deals 🔥", lead="Trending products in our niches, with prices pulled live from AliExpress. Final prices can change, so check them on the product page.",
   tabs=[("🔥 Trending now",[("smartring","Smart rings"),("dashcam","Dash cams"),("seccam","Wi-Fi security cameras"),("ledstrip","Smart LED lights"),("carvac","Car vacuums"),("gamepad","Game controllers"),("massager","Massage guns"),("trimmer","Hair trimmers"),("toothbrush","Electric toothbrushes"),("neckfan","Neck fans")]),
         ("📶 Wireless world",[("qrscan","Wireless QR scanners"),("ringscan","Ring scanners"),("wmouse","Wireless mice"),("wcombo","Keyboard + mouse sets"),("wcharge","Wireless chargers"),("headphone","Wireless headphones"),("btspeaker","Bluetooth speakers"),("btreceiver","Bluetooth receivers"),("carplay","Wireless CarPlay"),("wifi","Wi-Fi adapters"),("extender","Wi-Fi extenders")]),
         ("📱 Phone & audio",[("audio","Earbuds"),("phone","Phone holders"),("charger","Fast chargers"),("powerbank","Power banks"),("cable","Charging cables"),("watch","Smart watches")]),
         ("💾 Storage & computer",[("ssd","Portable SSDs"),("hdd","External hard drives"),("microsd","Memory cards"),("cardreader","Card readers"),("flash","USB flash drives"),("class","USB hubs"),("keyboard","Keyboards")]),
         ("🏷️ Business & security",[("barcode","Barcode scanners"),("labelprn","Label printers"),("receiptprn","Receipt printers"),("rfid","RFID protection"),("tracker","Trackers"),("car","Car scanners")]),
         ("🎓 Teaching",[("board","Writing tablets"),("presenter","Presenters"),("webcam","Webcams"),("mic","Microphones")]),
         ("📽️ Display & projection",[("projector","Projectors"),("projscreen","Projector screens"),("hdmiwifi","Wireless HDMI"),("monitor","Portable monitors"),("doccam","Document cameras")]),
         ("🎙️ Recording & camera",[("recorder","Voice recorders"),("ringlight","Ring lights"),("gimbal","Phone gimbals"),("actioncam","Action cameras")]),
         ("🌐 Translation",[("translator","AI translators"),("transbuds","Translation earbuds"),("scanpen","Translation pens")]),
         ("✈️ Travel",[("travel","Travel adapters"),("luggage","Luggage scales"),("organizer","Tech organizers")])],
   loading="Loading deals…", fail="Deals could not load right now. Try again shortly, or browse our picks.", empty="No deals in this section right now.",
   go="🛒 Buy now", sold="sold", updated="Updated", back="← Our reviewed picks",
   sph="Search any product: barcode scanner, 1TB SSD, projector…", sbtn="Search",
   S={"res":"Search results","for":"for","hook":"Live AliExpress results, best sellers first, poorly rated items hidden.","cats":"Matching sections:","none":"No results. Try a simpler word, or pick a section.","short":"Type at least 2 characters."}),
}

def deals(lang):
    d = DEALS_T[_L(lang)]; path = "deals/"
    W = worlds(lang)
    wrow = "".join(f'<button type="button" class="wbtn tone-{w["tone"]}" data-w="{w["i"]}" aria-pressed="{str(w["i"]==0).lower()}"><i aria-hidden="true">{w["ic"]}</i>{e(w["name"])}</button>' for w in W)
    tabs = "".join(f'<div class="tgroup" data-w="{gi}"' + ('' if gi==0 else ' hidden') + '>' + "".join(f'<button type="button" id="t-{k}" data-n="{k}" aria-pressed="{str(gi==0 and i==0).lower()}">{e(v)}</button>' for i,(k,v) in enumerate(items)) + '</div>' for gi,(g,items) in enumerate(d["tabs"]))
    hero = f'<div class="hero" style="padding-block:28px 56px"><h1><span class="glow">{e(d["h"])}</span></h1><p>{e(d["lead"])}</p></div>'
    hooks = {k:v[3 if lang=="ar" else 4] for k,v in CARD.items()}
    tones = {k:v[0] for k,v in CARD.items()}
    names = {k:n for _,items in d["tabs"] for k,n in items}
    icons = {k:ic for ic,_,k in HOME_CATS[_L(lang)][2]}
    icons.update({"wcombo":"⌨️","btreceiver":"📻","wifi":"📶","smartring":"💍","dashcam":"📹","seccam":"🛡️","ledstrip":"🌈","carvac":"🧹","gamepad":"🎮","massager":"💆","trimmer":"✂️","toothbrush":"🪥","neckfan":"🌀"})
    B = {"ar":{"off":"خصم","best":"⭐ الأكثر مبيعاً","top":"👍 تقييم","save":"وفّر","cdT":"تخفيضات 11.11 تبدأ خلال","cdS":"جهّز سلّتك الآن، الأسعار تنخفض في موعدها","liveT":"تخفيضات 11.11 جارية الآن 🎉","liveS":"حتى 18 نوفمبر، اغتنم الفرصة قبل انتهائها","d":"ي","h":"س","m":"د","s":"ث"},
         "en":{"off":"off","best":"⭐ Best seller","top":"👍 Rated","save":"Save","cdT":"11.11 sale starts in","cdS":"Fill your cart now, prices drop on time","liveT":"11.11 sale is live 🎉","liveS":"Until Nov 18, grab it before it ends","d":"d","h":"h","m":"m","s":"s"}}[_L(lang)]
    cfg = json.dumps({"lang":lang,"go":d["go"],"hooks":hooks,"tones":tones,"names":names,"icons":icons,"B":B,"sold":d["sold"],"fail":d["fail"],"empty":d["empty"],"loading":d["loading"],"updated":d["updated"],"home":url(lang),"S":d["S"]}, ensure_ascii=False)
    return (head(lang, d["title"], d["lead"][:155], path) + masthead(lang, path, hero) + f"""<main>
{promo_bar(lang)}
<section><div class="wrap">
  <div class="cd" id="cd" hidden><span class="cd-fire" aria-hidden="true">🔥</span><div><b id="cd-t"></b><small id="cd-s"></small></div><div class="cd-clock" id="cd-c" dir="ltr"></div></div>
  <form class="dsearch" id="sform" role="search"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M20 20l-4.2-4.2" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg><input type="search" id="q" name="q" autocomplete="off" aria-label="{e(d['sph'])}" placeholder="{e(d['sph'])}">{imgbtn(lang)}<button type="submit">{e(d['sbtn'])}</button></form>
  <div class="sugg" id="sugg" aria-live="polite"></div>
  <div class="dnav"><div class="worlds" id="worlds" role="group">{wrow}</div>
  <div class="tabs" id="tabs" role="group">{tabs}</div></div>
  <div class="cathero" id="cathero" aria-live="polite"><span class="ch-orb" id="ch-i"></span><div><h2 id="ch-n"></h2><p id="ch-h"></p></div></div>
  <p class="status" id="status" aria-live="polite">{e(d['loading'])}</p>
  <div class="grid" id="deals">{''.join('<div class="skel"></div>' for _ in range(8))}</div>
  <p style="margin-top:22px"><a href="{url(lang)}">{e(d['back'])}</a></p>
</div></section>
<script>window.DEALS={cfg};</script>
<script src="/deals.js" defer></script>
""" + footer(lang))

PRIVACY = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>سياسة الخصوصية · DoniaNova</title><link rel="stylesheet" href="/style.css"><link rel="icon" href="/favicon.svg"><script defer src="/_vercel/insights/script.js"></script></head>
<body><main class="wrap" style="max-width:760px;padding-block:48px;line-height:1.9">
<h1>سياسة الخصوصية</h1>
<p>موقع DoniaNova من DONIA LABS TECH يعرض منتجات تقنية من علي إكسبريس بروابط عمولة. لا نطلب منك إنشاء حساب، ولا نجمع اسمك أو بريدك أو أي بيانات شخصية.</p>
<h2>ما الذي نستعمله</h2>
<ul><li>عند الضغط على رابط منتج، تنتقل إلى علي إكسبريس، وتخضع هناك لسياسة خصوصيتهم.</li>
<li>أسئلتك للمساعد «نوفا» تُرسل إلى خدمة الذكاء الاصطناعي DeepSeek للإجابة فقط، ولا نحفظها.</li>
<li>نحفظ في متصفحك اختيار اللغة فقط.</li>
<li>تطبيقنا على فيسبوك يُستعمل فقط لنشر مقارنات المنتجات على صفحتنا، ولا يقرأ بيانات الزوار.</li></ul>
<h2>Privacy policy (English)</h2>
<p>DoniaNova by DONIA LABS TECH lists AliExpress tech products with affiliate links. We collect no personal data and require no account. Questions to the Nova assistant are sent to DeepSeek only to generate an answer and are not stored. Our Facebook app is used only to publish product comparisons on our own Page.</p>
<p>تواصل · Contact: DONIA LABS TECH — donialabstech.online</p>
<p><a href="/ar/">← العودة إلى الموقع</a></p></main></body></html>"""

CSS_V9 = r"""
/* ===== v9: world-class navigation ===== */
.mast{padding-top:74px}
.topbar{position:fixed;inset-inline:0;top:0;z-index:60;transition:background .35s,box-shadow .35s,backdrop-filter .35s}
.topbar .top{padding-block:12px;gap:18px}
.topbar.stuck{background:rgba(14,10,46,.78);backdrop-filter:blur(16px) saturate(1.4);-webkit-backdrop-filter:blur(16px) saturate(1.4);box-shadow:0 10px 30px -12px rgba(0,0,0,.6),inset 0 -1px 0 rgba(255,255,255,.08)}
.mainnav{display:flex;align-items:center;gap:4px;margin-inline:auto}
.mainnav a,.mg-btn{color:rgba(255,255,255,.82);text-decoration:none;font:inherit;font-size:15px;font-weight:500;padding:8px 14px;border-radius:999px;background:none;border:0;cursor:pointer;transition:background .25s,color .25s}
.mainnav a:hover,.mg-btn:hover,.mg-btn[aria-expanded="true"]{background:rgba(255,255,255,.1);color:#fff}
.mainnav a[aria-current="page"]{color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266);font-weight:700}
.tright{display:flex;align-items:center;gap:10px}
.tgdd{position:relative}
.tg-pill{display:flex;align-items:center;gap:7px;border:0;cursor:pointer;font:inherit;font-size:14px;font-weight:600;color:#fff;padding:8px 14px;border-radius:999px;background:linear-gradient(135deg,#2AABEE,#1E88D1);box-shadow:0 6px 18px -6px rgba(42,171,238,.7)}
.tg-pill:hover{filter:brightness(1.08)}
.tgmenu{position:absolute;top:calc(100% + 10px);inset-inline-end:0;width:300px;display:grid;gap:6px;padding:8px;border-radius:18px;background:#151041;border:1px solid rgba(255,255,255,.12);box-shadow:0 24px 60px -18px rgba(0,0,0,.7);z-index:70}
.tgmenu a{display:flex;align-items:center;gap:12px;padding:10px;border-radius:14px;color:#fff;text-decoration:none;transition:background .2s}
.tgmenu a:hover{background:rgba(255,255,255,.08)}
.tgmenu img{border-radius:12px;flex:none}
.tgmenu b{display:block;font-size:15px}.tgmenu small{opacity:.7;font-size:12.5px}
.mega{background:rgba(14,10,46,.97);backdrop-filter:blur(18px);border-top:1px solid rgba(255,255,255,.08);box-shadow:0 30px 60px -20px rgba(0,0,0,.7);max-height:calc(100vh - 70px);overflow:auto}
.mg-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:22px 18px;padding-block:22px 26px}
.mg-col{display:grid;gap:4px;align-content:start}
.mg-col a{color:rgba(255,255,255,.72);text-decoration:none;font-size:14px;padding:4px 0}
.mg-col a:hover{color:#F2C266}
.mg-col .mg-h{color:#fff;font-weight:700;font-size:15px;display:flex;align-items:center;gap:8px;margin-bottom:4px}
.mg-h i{font-style:normal;width:30px;height:30px;display:grid;place-items:center;border-radius:10px;background:rgba(255,255,255,.08)}
.crumbs{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding-top:8px;position:relative;z-index:2}
.backbtn{font:inherit;font-size:14px;font-weight:600;color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266);border:0;border-radius:999px;padding:7px 16px;cursor:pointer;box-shadow:0 6px 18px -8px rgba(242,194,102,.8)}
.crumbs nav{display:flex;gap:8px;align-items:center;font-size:14px;color:rgba(255,255,255,.7)}
.crumbs nav a{color:rgba(255,255,255,.85)}.crumbs nav b{color:#fff;font-weight:600}
.bbar{display:none}
.topbar .brand{color:#fff;text-decoration:none}.topbar .brand b{color:#fff}.topbar .brand b span{color:#F2C266}
body.sheet-mega .topbar,body.sheet-tg .topbar{backdrop-filter:none!important;-webkit-backdrop-filter:none!important}
.veil{position:fixed;inset:0;background:rgba(5,3,20,.55);backdrop-filter:blur(2px);z-index:58}
/* Telegram band v2 */
.tgx-s{padding-block:14px}
.tgx{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:16px;align-items:stretch;padding:28px;border-radius:28px;background:radial-gradient(90% 140% at 100% 0%,rgba(42,171,238,.28),transparent 55%),linear-gradient(160deg,#101a4f,#0b0a2b);border:1px solid rgba(42,171,238,.3);box-shadow:0 30px 70px -30px rgba(30,136,209,.65);color:#fff}
.tgx-head h2{font-size:clamp(1.5rem,3vw,2.1rem);margin:.4em 0 .3em}.tgx-head p{opacity:.82;line-height:1.8;margin:0}
.tgx-pill{display:inline-block;font-size:12px;font-weight:700;padding:5px 12px;border-radius:999px;background:rgba(42,171,238,.2);color:#8fd6ff;border:1px solid rgba(42,171,238,.45)}
.tgx-card{display:grid;grid-template-columns:72px 1fr;grid-template-rows:1fr auto;gap:10px 14px;padding:18px;border-radius:22px;text-decoration:none;color:#fff;background:linear-gradient(160deg,rgba(255,255,255,.09),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.14);transition:transform .35s cubic-bezier(.2,.8,.2,1),border-color .35s,box-shadow .35s}
.tgx-card:hover{transform:translateY(-6px);border-color:rgba(42,171,238,.7);box-shadow:0 20px 44px -18px rgba(42,171,238,.7)}
.tgx-card img{border-radius:18px;grid-row:1}
.tgx-card b{display:block;font-size:17px;margin-bottom:4px}.tgx-card span{display:block;font-size:13.5px;opacity:.8;line-height:1.7}
.tgx-card em{display:inline-block;margin-top:6px;font-style:normal;font-size:13px;color:#8fd6ff;direction:ltr}
.tgx-go{grid-column:1/-1;font-style:normal;text-align:center;font-weight:700;padding:10px;border-radius:14px;background:linear-gradient(135deg,#2AABEE,#1E88D1)}
.tgx-card.ch .tgx-go{background:linear-gradient(135deg,#FFE3A0,#F2C266);color:#1A1250}
/* worlds tiles */
.wgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.wt{position:relative;overflow:hidden;display:grid;gap:6px;padding:22px 20px;border-radius:24px;text-decoration:none;color:#fff;min-height:150px;
 background:radial-gradient(120% 120% at 100% 0%,color-mix(in srgb,var(--t1) 38%,transparent),transparent 60%),linear-gradient(160deg,#1a1452,#0d0a2c);border:1px solid color-mix(in srgb,var(--t1) 35%,transparent);transition:transform .4s cubic-bezier(.2,.8,.2,1),box-shadow .4s}
.wt::after{content:"";position:absolute;inset-inline-end:-40px;bottom:-40px;width:140px;height:140px;border-radius:50%;background:radial-gradient(circle,color-mix(in srgb,var(--t1) 45%,transparent),transparent 70%);opacity:.6;transition:transform .5s}
.wt:hover{transform:translateY(-6px);box-shadow:0 24px 50px -20px color-mix(in srgb,var(--t1) 70%,transparent)}
.wt:hover::after{transform:scale(1.4)}
.wt-ic{font-size:30px;width:56px;height:56px;display:grid;place-items:center;border-radius:18px;background:color-mix(in srgb,var(--t1) 22%,transparent);box-shadow:0 0 30px color-mix(in srgb,var(--t1) 40%,transparent)}
.wt b{font-size:18px;margin-top:4px}.wt small{opacity:.72;font-size:13.5px;line-height:1.6}
.wt-f{display:flex;justify-content:space-between;align-items:center;margin-top:auto;padding-top:8px;position:relative;z-index:1}
.wt-f em{font-style:normal;font-size:12.5px;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,.1)}
.wt-f i{font-style:normal;font-weight:700;color:var(--t1)}
/* deals navigator */
.dnav{position:sticky;top:64px;z-index:20;margin:8px 0 14px;padding:10px;border-radius:22px;background:color-mix(in srgb,var(--paper,#fff) 88%,transparent);backdrop-filter:blur(14px);border:1px solid var(--line,rgba(0,0,0,.08));box-shadow:0 14px 34px -22px rgba(20,10,80,.45)}
.worlds{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:2px}
.worlds::-webkit-scrollbar{display:none}
.wbtn{flex:none;display:flex;align-items:center;gap:8px;font:inherit;font-size:14.5px;font-weight:600;padding:9px 16px;border-radius:999px;cursor:pointer;border:1px solid var(--line,rgba(0,0,0,.1));background:var(--chip,#f3f0ff);color:inherit;transition:all .25s}
.wbtn i{font-style:normal}
.wbtn[aria-pressed="true"]{color:#fff;border-color:transparent;background:linear-gradient(135deg,var(--t1),var(--t2));box-shadow:0 8px 20px -8px var(--t2)}
.dnav .tabs{margin-top:10px;padding-top:10px;border-top:1px dashed var(--line,rgba(0,0,0,.1))}
.dnav .tgroup{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:8px;scrollbar-width:none}
.dnav .tgroup::-webkit-scrollbar{display:none}
.dnav .tgroup[hidden]{display:none}
.dnav .tgroup button{flex:none}
/* ===== mobile app-like ===== */
@media (max-width:980px){.mainnav{display:none}.mg-grid{grid-template-columns:repeat(3,1fr)}}
@media (max-width:860px){.tgx{grid-template-columns:1fr}.wgrid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:760px){
 .mast{padding-top:64px}
 .tg-pill span{display:none}.tg-pill{padding:9px}
 .bbar{display:grid;grid-template-columns:repeat(5,1fr);position:fixed;inset-inline:10px;bottom:calc(10px + env(safe-area-inset-bottom));z-index:65;padding:6px;border-radius:22px;background:rgba(18,13,58,.92);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.12);box-shadow:0 18px 40px -12px rgba(0,0,0,.7)}
 .bbar a,.bbar button{display:grid;justify-items:center;gap:2px;padding:6px 2px;border-radius:16px;color:rgba(255,255,255,.75);text-decoration:none;font:inherit;font-size:11px;background:none;border:0;cursor:pointer}
 .bbar i{font-style:normal;font-size:20px;line-height:1}
 .bbar [aria-current="page"]{color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266);font-weight:700}
 body{padding-bottom:86px}
 .nova-fab{display:none!important}
 .nova{bottom:96px!important}
 body.sheet-mega .mega{position:fixed;inset-inline:0;bottom:0;top:auto;z-index:66;border-radius:26px 26px 0 0;max-height:78vh;padding-bottom:calc(20px + env(safe-area-inset-bottom))}
 body.sheet-mega .mega::before{content:"";display:block;width:44px;height:5px;border-radius:5px;background:rgba(255,255,255,.3);margin:10px auto 0}
 .mg-grid{grid-template-columns:repeat(2,1fr);gap:18px 14px}
 body.sheet-tg .tgmenu{position:fixed;inset-inline:10px;top:auto;bottom:calc(96px + env(safe-area-inset-bottom));width:auto;z-index:66}
 .dnav{top:58px;border-radius:18px;padding:8px}
 .wgrid{gap:12px}.wt{padding:16px 14px;min-height:0}.wt b{font-size:16px}.wt-ic{width:46px;height:46px;font-size:24px}
}
@media (max-width:420px){.wgrid{grid-template-columns:1fr 1fr}.wt small{display:none}}
"""

CSS_V8 = r"""
.tone-cyan{--t1:#5CF2FF;--t2:#0A84C6}
/* wireless world band */
.wl-s{padding-block:18px 8px}
.wl{position:relative;overflow:hidden;border-radius:28px;padding:38px 34px;background:radial-gradient(120% 140% at 85% 0%,rgba(92,242,255,.18),transparent 55%),radial-gradient(90% 120% at 0% 100%,rgba(139,108,255,.28),transparent 60%),linear-gradient(160deg,#16124a,#0c0a2b);border:1px solid rgba(92,242,255,.22);box-shadow:0 30px 80px -30px rgba(10,132,198,.55),inset 0 1px 0 rgba(255,255,255,.08);display:grid;grid-template-columns:minmax(240px,.9fr) 2fr;gap:30px;align-items:center;color:#fff}
.wl-waves{position:absolute;inset-inline-end:-120px;top:-120px;width:420px;height:420px;pointer-events:none}
.wl-waves i{position:absolute;inset:0;border-radius:50%;border:2px solid rgba(92,242,255,.35);animation:wlw 4.8s cubic-bezier(.2,.6,.3,1) infinite;opacity:0}
.wl-waves i:nth-child(2){animation-delay:1.2s}.wl-waves i:nth-child(3){animation-delay:2.4s}.wl-waves i:nth-child(4){animation-delay:3.6s}
@keyframes wlw{0%{transform:scale(.15);opacity:.9}100%{transform:scale(1);opacity:0}}
.wl-head{position:relative;z-index:1}
.wl-head h2{font-size:clamp(1.7rem,3.4vw,2.4rem);margin:.35em 0 .3em}.wl-gt{background:linear-gradient(90deg,#fff,#9ff7ff 60%,#ffe29a);-webkit-background-clip:text;background-clip:text;color:transparent}
.wl-head p{opacity:.85;line-height:1.8;margin:0 0 18px}
.wl-pill{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.04em;padding:5px 12px;border-radius:999px;background:rgba(92,242,255,.15);color:#9ff7ff;border:1px solid rgba(92,242,255,.35)}
.wl-grid{position:relative;z-index:1;display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.wl-tile{position:relative;display:grid;gap:6px;padding:18px 16px;border-radius:20px;text-decoration:none;color:#fff;background:linear-gradient(160deg,rgba(255,255,255,.09),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.12);backdrop-filter:blur(8px);transition:transform .35s cubic-bezier(.2,.8,.2,1),border-color .35s,box-shadow .35s}
.wl-tile:hover,.wl-tile:focus-visible{transform:translateY(-6px);border-color:rgba(92,242,255,.6);box-shadow:0 18px 40px -16px rgba(92,242,255,.55)}
.wl-ic{width:48px;height:48px;display:grid;place-items:center;font-size:1.5rem;border-radius:16px;background:radial-gradient(circle at 30% 30%,rgba(159,247,255,.45),rgba(10,132,198,.25));box-shadow:0 0 24px rgba(92,242,255,.35)}
.wl-tile b{font-size:1.02rem}.wl-tile small{opacity:.75;line-height:1.6}
.wl-tile em{font-style:normal;font-weight:700;color:#ffe29a;font-size:.88rem;margin-top:4px}
@media (max-width:900px){.wl{grid-template-columns:1fr;padding:28px 20px}.wl-grid{grid-template-columns:repeat(2,1fr)}}
@media (max-width:420px){.wl-grid{grid-template-columns:1fr 1fr;gap:10px}.wl-tile{padding:14px 12px}}
@media (prefers-reduced-motion:reduce){.wl-waves i{animation:none;opacity:.25}}
/* polish: section headings + smoother cards */
.head h2{position:relative;padding-bottom:10px}
.head h2::after{content:"";position:absolute;inset-inline-start:0;bottom:0;width:56px;height:3px;border-radius:3px;background:linear-gradient(90deg,#FFD27A,#5CF2FF)}
.cc,.card{transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
.tgroup:first-child .tlabel{color:#0A84C6}
"""

CSS_V7 = r"""
/* ---- v7: global polish ---- */
.js .reveal{opacity:1!important;transform:none!important}
.hero2{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:40px;align-items:center}
.h-txt{min-width:0}
.h-art{position:relative;height:500px;max-width:470px;width:100%;justify-self:center}
.hero2 h1{font-size:clamp(34px,3.9vw,54px)!important;line-height:1.25!important}
.h-orb{position:absolute;inset:12% 10%;border-radius:50%;background:radial-gradient(circle,#8B6CFF66,#0FA3A333 45%,transparent 70%);filter:blur(30px);z-index:0}
.fc{position:absolute;z-index:1;width:210px;padding:12px 12px 14px;border-radius:22px;background:rgba(255,255,255,.96);color:#18123D;box-shadow:0 30px 60px -24px rgba(0,0,0,.6),0 0 0 1px rgba(255,255,255,.5);display:flex;flex-direction:column;gap:4px;animation:floaty 6s ease-in-out infinite}
.fc img{width:100%;aspect-ratio:1;object-fit:contain;border-radius:14px;background:#fff}
.fc b{font-size:13.5px;line-height:1.35}.fc span{font-size:12px;color:#6D4AF0;font-weight:600}
.fc1{top:40px;left:0;transform:rotate(-7deg);animation-delay:0s}
.fc2{top:0;right:0;transform:rotate(6deg);animation-delay:-2s;z-index:2}
.fc3{top:200px;left:50%;margin-left:-105px;transform:rotate(-1deg);animation-delay:-4s;z-index:3}
@keyframes floaty{0%,100%{translate:0 0}50%{translate:0 -14px}}
.h-live{position:absolute;top:-6px;inset-inline-end:6%;z-index:3;font-size:13px;font-weight:700;padding:7px 14px;border-radius:999px;color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266);box-shadow:0 0 24px -4px #F2C266}
@media(max-width:900px){.hero2{grid-template-columns:1fr}.h-art{display:none}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:22px;border-radius:22px;overflow:hidden;background:var(--line);border:1px solid var(--line)}
.stats div{background:var(--surface);padding:22px 18px;text-align:center;display:flex;flex-direction:column;gap:4px}
.stats b{direction:ltr;unicode-bidi:isolate;font-family:'Bricolage Grotesque',inherit;font-size:34px;line-height:1;background:linear-gradient(120deg,var(--violet),var(--teal));-webkit-background-clip:text;color:transparent}
.stats span{font-size:13.5px;color:var(--muted)}
@media(max-width:700px){.stats{grid-template-columns:1fr 1fr}.stats b{font-size:28px}}
.card>p{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.grid{align-items:stretch}
#today .today{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:22px;align-items:stretch}
.tw{position:relative;display:flex;flex-direction:column;gap:12px}
.tw img{width:100%;aspect-ratio:4/3;object-fit:contain;background:#fff;border-radius:16px}
.tw-badge{position:absolute;top:16px;inset-inline-start:16px;z-index:2;font-weight:700;font-size:13px;padding:6px 14px;border-radius:999px;color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266);box-shadow:0 0 22px -4px #F2C266}
.tw h3{margin:0;font-size:17px;line-height:1.45}
.tw-m{display:flex;flex-wrap:wrap;gap:12px;align-items:center;font-size:14px;color:var(--muted)}.tw-m b{font-size:24px;color:var(--ink)}
.tl{display:flex;flex-direction:column;gap:14px;min-width:0}
.tpost{padding:18px 20px;border-radius:20px;background:linear-gradient(135deg,var(--violet-soft),var(--gold-soft));border:1px solid var(--line);font-size:14.5px;line-height:1.75}
.tpost p{margin:0}.tpost p:first-child{font-weight:700;font-size:16px;margin-bottom:4px}
.tmini{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tmini .card{padding:10px;display:flex;flex-direction:column;gap:6px;font-size:13px;color:var(--muted)}
.tmini img{width:100%;aspect-ratio:1;object-fit:contain;background:#fff;border-radius:12px}
.tmore{align-self:flex-start}
@media(max-width:820px){#today .today{grid-template-columns:1fr}}
.tgband{display:flex;align-items:center;gap:22px;flex-wrap:wrap;padding:26px 28px;border-radius:26px;color:#fff;background:radial-gradient(120% 140% at 0% 0%,#2AABEE,#1A6FD0 45%,#1A1250);box-shadow:0 26px 60px -28px #229ED9}
.tg-ic{flex:none;width:74px;height:74px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.16);box-shadow:inset 0 0 0 1px rgba(255,255,255,.3)}
.tg-t{flex:1;min-width:220px}.tg-t h2{margin:0 0 4px;color:#fff;font-size:22px}.tg-t p{margin:0;opacity:.9;font-size:14.5px}
.tg-btn{background:#fff!important;color:#1A6FD0!important;font-weight:700}
.tg-bs{display:flex;flex-wrap:wrap;gap:10px}.tg-btn2{background:rgba(255,255,255,.14)!important;color:#fff!important;border:1px solid rgba(255,255,255,.4)!important;font-weight:700}
.brands{padding-block:30px 40px!important;overflow:hidden}
.brands p{text-align:center;color:var(--muted);font-size:13.5px;letter-spacing:.04em;margin:0 0 12px}
.marq{overflow:hidden;-webkit-mask:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);mask:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.mtrack{display:flex;gap:46px;width:max-content;animation:marq 32s linear infinite}
.mtrack span{font-family:'Bricolage Grotesque',inherit;font-weight:800;font-size:26px;letter-spacing:-.02em;color:var(--ink);opacity:.38;white-space:nowrap;transition:opacity .3s}
.mtrack span:hover{opacity:.9}
@keyframes marq{to{transform:translateX(-50%)}}
footer.fx{padding-block:44px 22px}
.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:28px;margin-bottom:26px}
.fgrid nav{display:flex;flex-direction:column;gap:9px}
.fgrid h4{margin:0 0 4px;font-size:14px;color:#F2C266;letter-spacing:.02em}
.fgrid a{color:rgba(255,255,255,.78);text-decoration:none;font-size:14px}.fgrid a:hover{color:#fff}
.flogo{font-family:'Bricolage Grotesque',inherit;font-size:26px;color:#fff}.flogo i{font-style:normal;color:#F2C266}
.fabout p{color:rgba(255,255,255,.7);font-size:14px;line-height:1.7;max-width:34ch}
.fbot{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;padding-top:18px;border-top:1px solid rgba(255,255,255,.12);font-size:13px;color:rgba(255,255,255,.6)}
@media(max-width:820px){.fgrid{grid-template-columns:1fr 1fr}.fabout{grid-column:1/-1}}
@media (prefers-reduced-motion:reduce){.fc,.mtrack{animation:none}}
"""
CSS_V6 = r"""
/* ---- v6: search + 3D cards ---- */
@property --ang{syntax:'<angle>';initial-value:0deg;inherits:false}
.tilt{transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(var(--ty,0px));transform-style:preserve-3d;
  transition:transform .6s cubic-bezier(.2,.7,.2,1),box-shadow .4s,border-color .4s;will-change:transform}
.tilt.tilting{--ty:-8px;transition:transform .1s linear,box-shadow .4s,border-color .4s}
.card.tilt{box-shadow:0 1px 0 rgba(255,255,255,.7) inset,0 2px 0 var(--line),0 18px 34px -22px rgba(24,18,61,.45)}
.card.tilt.tilting{box-shadow:0 1px 0 rgba(255,255,255,.7) inset,0 30px 60px -24px rgba(109,74,240,.55),0 0 34px -10px rgba(242,194,102,.55);border-color:transparent}
.card.tilt:hover{transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(var(--ty,0px))}
.cc.tilt:hover,.cc.tilt:focus-visible{transform:perspective(900px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg)) translateY(var(--ty,0px)) scale(1.02)}
.glare{position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:3;opacity:0;transition:opacity .35s;
  background:radial-gradient(circle at var(--gx,50%) var(--gy,0%),rgba(255,255,255,.55),rgba(255,255,255,.12) 22%,transparent 50%);mix-blend-mode:soft-light}
.tilting .glare{opacity:1}
.rim{position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:4;padding:2px;opacity:0;transition:opacity .4s;
  background:conic-gradient(from var(--ang),#F2C266,#8B6CFF,#2FD6C8,#FF7FB0,#F2C266);
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box exclude,linear-gradient(#000 0 0);
  animation:rimspin 3.2s linear infinite;filter:drop-shadow(0 0 6px rgba(242,194,102,.7))}
@keyframes rimspin{to{--ang:360deg}}
.tilting .rim{opacity:1}
.card.tilting .shot{transform:scale(1.06) translateZ(30px)}
.card.tilting .bds{transform:translateZ(40px)}
.card.tilting .go.buy{transform:translateZ(24px)}
.cc.tilting .cc-orb{transform:translateZ(36px) scale(1.06)}
.bds,.go.buy,.cc-orb{transition:transform .4s cubic-bezier(.2,.7,.2,1)}
/* header search */
.msearch{display:flex;align-items:center;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:3px;backdrop-filter:blur(6px);transition:border-color .3s,box-shadow .3s}
.msearch:focus-within{border-color:#F2C266;box-shadow:0 0 0 3px rgba(242,194,102,.25),0 0 24px -6px #F2C266}
.msearch input{width:190px;background:transparent;border:0;outline:0;color:#fff;font:inherit;font-size:14px;padding:6px 12px}
.msearch input::placeholder{color:rgba(255,255,255,.65)}
.msearch button{width:34px;height:34px;border-radius:50%;border:0;display:grid;place-items:center;cursor:pointer;color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266)}
@media(max-width:480px){.dl-t{display:none}.mast .top>div{gap:6px!important}}
@media(max-width:760px){.msearch input{display:none}.msearch{padding:2px;background:transparent;border-color:transparent}}
/* hero + deals search */
.hsearch,.dsearch{display:flex;align-items:center;gap:10px;max-width:640px;padding:7px 7px 7px 7px;padding-inline-start:16px;border-radius:999px;
  background:rgba(255,255,255,.97);border:1px solid var(--line);box-shadow:0 20px 50px -24px rgba(109,74,240,.7),0 0 0 1px rgba(255,255,255,.4) inset;transition:box-shadow .3s}
.hsearch{margin-top:22px}
.hsearch:focus-within,.dsearch:focus-within{box-shadow:0 0 0 3px rgba(139,108,255,.35),0 24px 60px -20px rgba(109,74,240,.8),0 0 40px -10px rgba(242,194,102,.6)}
.hsearch svg,.dsearch svg{color:#6D4AF0;flex:none}
.hsearch input,.dsearch input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:inherit;font-size:16px;color:#18123D;padding:8px 0}
.hsearch input::placeholder,.dsearch input::placeholder{color:#8A85A8}
.hsearch button,.dsearch button{flex:none;border:0;cursor:pointer;font:inherit;font-weight:700;font-size:15px;padding:11px 22px;border-radius:999px;color:#fff;
  background:linear-gradient(135deg,#8B6CFF,#4B2FD0);box-shadow:0 10px 22px -10px #4B2FD0;transition:transform .2s,box-shadow .2s}
.hsearch button:hover,.dsearch button:hover{transform:translateY(-1px);box-shadow:0 14px 28px -10px #4B2FD0,0 0 18px -4px #8B6CFF}
.hpop{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px;font-size:13.5px}
.hpop span{color:rgba(255,255,255,.75)}
.hpop a{color:#fff;text-decoration:none;padding:5px 12px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.2);transition:background .2s,border-color .2s}
.hpop a:hover{background:rgba(242,194,102,.22);border-color:#F2C266}
.dsearch{max-width:none;margin-bottom:10px}
.sugg{display:flex;flex-wrap:wrap;gap:8px;align-items:center;min-height:0;margin-bottom:14px;font-size:13.5px}
.sugg:empty{display:none}
.sugg span{color:var(--muted);font-weight:600}
.sugg button{font:inherit;cursor:pointer;padding:6px 13px;border-radius:999px;border:1px solid var(--violet);background:var(--violet-soft);color:var(--ink)}
.tone-blue{--t1:#6FB8FF;--t2:#2457D6}
@media(max-width:640px){.hsearch,.dsearch{padding:5px;padding-inline-start:12px}.hsearch input,.dsearch input{font-size:15px}.hsearch button,.dsearch button{padding:10px 16px}}
"""
TILT_JS = r"""
/* 3D tilt + glare + glowing rim for product and category cards */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce)return;
  var SEL='.card,.cc', MAX=9;
  function prep(el){if(el._t)return;el._t=1;el.classList.add('tilt');
    var g=document.createElement('span');g.className='glare';g.setAttribute('aria-hidden','true');el.appendChild(g);
    var r=document.createElement('span');r.className='rim';r.setAttribute('aria-hidden','true');el.appendChild(r);}
  function move(el,x,y){var b=el.getBoundingClientRect(),px=(x-b.left)/b.width,py=(y-b.top)/b.height;
    if(px<0||px>1||py<0||py>1)return;
    el.style.setProperty('--ry',((px-.5)*2*MAX).toFixed(2)+'deg');
    el.style.setProperty('--rx',((.5-py)*2*MAX).toFixed(2)+'deg');
    el.style.setProperty('--gx',(px*100).toFixed(1)+'%');el.style.setProperty('--gy',(py*100).toFixed(1)+'%');
    el.style.setProperty('--mx',(x-b.left)+'px');el.style.setProperty('--my',(y-b.top)+'px');}
  function on(el){prep(el);el.classList.remove('enter');el.classList.add('tilting');}
  function off(el){el.classList.remove('tilting');el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg');}
  var cur=null;
  document.addEventListener('pointerover',function(ev){var el=ev.target.closest&&ev.target.closest(SEL);if(!el||el===cur)return;if(cur)off(cur);cur=el;on(el);},{passive:true});
  document.addEventListener('pointermove',function(ev){if(cur)move(cur,ev.clientX,ev.clientY);},{passive:true});
  document.addEventListener('pointerout',function(ev){if(!cur)return;var to=ev.relatedTarget;if(to&&cur.contains(to))return;off(cur);cur=null;},{passive:true});
  document.addEventListener('touchend',function(){if(cur){off(cur);cur=null;}},{passive:true});
  document.addEventListener('animationend',function(ev){var t=ev.target;if(t.classList&&t.classList.contains('enter')&&t.matches(SEL))t.classList.remove('enter');});
  function all(){document.querySelectorAll(SEL).forEach(prep);}
  all(); if('MutationObserver' in window){new MutationObserver(function(){all()}).observe(document.body,{childList:true,subtree:true});}
})();
"""
CSS_V5 = r"""
/* ---- v5 ---- */
@keyframes spin{to{transform:rotate(360deg)}}
.tone-violet{--t1:#8B6CFF;--t2:#4B2FD0}
.tone-teal{--t1:#2FD6C8;--t2:#0B7F86}
.tone-gold{--t1:#FFD27A;--t2:#C98A1E}
.tone-rose{--t1:#FF7FB0;--t2:#C2336F}
.tone-blue{--t1:#6FB8FF;--t2:#2457D6}
.ccards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px;margin-top:16px}
.cc{position:relative;overflow:hidden;isolation:isolate;display:flex;flex-direction:column;gap:6px;padding:20px 18px 16px;border-radius:22px;text-decoration:none;color:#F4F1FF;
  background:radial-gradient(120% 90% at 85% 0%,color-mix(in srgb,var(--t1) 38%,transparent),transparent 60%),linear-gradient(160deg,#1A1250,#0D0930);
  border:1px solid color-mix(in srgb,var(--t1) 45%,transparent);box-shadow:0 18px 40px -24px var(--t2),inset 0 1px 0 rgba(255,255,255,.08);
  transition:transform .35s cubic-bezier(.2,.7,.2,1),box-shadow .35s,border-color .35s}
.cc::before{content:"";position:absolute;inset:-40%;z-index:-1;background:conic-gradient(from 0deg,transparent 0 70%,color-mix(in srgb,var(--t1) 55%,transparent) 80%,transparent 90%);animation:spin 7s linear infinite;opacity:.0;transition:opacity .4s}
.cc::after{content:"";position:absolute;inset:1px;z-index:-1;border-radius:21px;background:inherit}
.cc:hover,.cc:focus-visible{transform:translateY(-6px) scale(1.015);border-color:var(--t1);box-shadow:0 26px 60px -20px var(--t1),0 0 0 1px var(--t1),0 0 34px -6px var(--t1)}
.cc:hover::before{opacity:1}
.cc-orb{width:62px;height:62px;border-radius:50%;display:grid;place-items:center;margin-bottom:6px;
  background:radial-gradient(circle at 35% 30%,#fff8,transparent 45%),radial-gradient(circle,var(--t1),var(--t2));box-shadow:0 0 26px -2px var(--t1),0 0 60px -10px var(--t1);animation:breathe 3.6s ease-in-out infinite}
.cc-orb i{font-style:normal;font-size:30px;filter:drop-shadow(0 2px 4px rgba(0,0,0,.35))}
@keyframes breathe{50%{box-shadow:0 0 38px 2px var(--t1),0 0 80px -6px var(--t1)}}
.cc-name{font-size:17px;font-family:'El Messiri',inherit;line-height:1.3}
.cc-hook{font-size:13.5px;color:#C9C2EE;line-height:1.5;flex:1}
.cc-cta{margin-top:8px;font-weight:700;font-size:14px;color:var(--t1)}
.cc-cta em{font-style:normal;display:inline-block;transition:transform .3s}
.cc:hover .cc-cta em{transform:translateX(-5px)}
html[dir="ltr"] .cc:hover .cc-cta em{transform:translateX(5px)}
.cc-badge{position:absolute;top:12px;inset-inline-end:12px;font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:999px;color:#1A1250;background:linear-gradient(135deg,#FFE3A0,#F2C266);box-shadow:0 0 18px -4px #F2C266}
/* deals: countdown */
.cd{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:18px;padding:14px 18px;border-radius:18px;color:#fff;
  background:linear-gradient(120deg,#E8452C,#C2336F 45%,#6D4AF0);box-shadow:0 18px 40px -20px #E8452C;position:relative;overflow:hidden}
.cd::after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.25) 50%,transparent 70%);transform:translateX(-100%);animation:shine 3.5s ease-in-out infinite}
@keyframes shine{60%,100%{transform:translateX(100%)}}
.cd-fire{font-size:30px;animation:breathe2 1.6s ease-in-out infinite}@keyframes breathe2{50%{transform:scale(1.18)}}
.cd b{font-size:17px;display:block}.cd small{opacity:.9;font-size:13px}
.cd-clock{display:flex;gap:6px;margin-inline-start:auto}
.cd-clock span{min-width:52px;text-align:center;padding:6px 4px;border-radius:12px;background:rgba(0,0,0,.25);backdrop-filter:blur(4px)}
.cd-clock b{font-family:'Bricolage Grotesque',inherit;font-size:22px;line-height:1}.cd-clock i{font-style:normal;font-size:11px;opacity:.85}
/* deals: category hero */
.cathero{display:flex;align-items:center;gap:16px;margin:4px 0 14px;padding:16px 18px;border-radius:20px;color:#F4F1FF;
  background:radial-gradient(90% 120% at 90% 0%,color-mix(in srgb,var(--t1,#8B6CFF) 40%,transparent),transparent 60%),linear-gradient(160deg,#1A1250,#0D0930);border:1px solid color-mix(in srgb,var(--t1,#8B6CFF) 50%,transparent)}
.cathero h2{margin:0;font-size:22px;color:#fff}.cathero p{margin:2px 0 0;color:#C9C2EE;font-size:14px}
.ch-orb{flex:none;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;font-size:26px;background:radial-gradient(circle at 35% 30%,#fff8,transparent 45%),radial-gradient(circle,var(--t1,#8B6CFF),var(--t2,#4B2FD0));box-shadow:0 0 28px -2px var(--t1,#8B6CFF)}
.cathero.pulse{animation:pop .5s cubic-bezier(.2,.7,.2,1)}
/* deals: glowing product cards + badges */
.glowcard{position:relative;transition:transform .3s,box-shadow .3s,border-color .3s}
.glowcard:hover{transform:translateY(-5px);border-color:var(--violet);box-shadow:0 22px 50px -22px var(--violet),0 0 0 1px color-mix(in srgb,var(--violet) 50%,transparent)}
.bds{position:absolute;top:12px;inset-inline-start:12px;z-index:2;display:flex;flex-direction:column;gap:6px;align-items:flex-start}
.bd{font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:999px;color:#fff;box-shadow:0 6px 16px -6px rgba(0,0,0,.4)}
.bd-hot{background:linear-gradient(135deg,#FF6A3D,#E8252C);animation:breathe2 2.2s ease-in-out infinite}
.bd-best{background:linear-gradient(135deg,#F2C266,#C98A1E);color:#1A1250}
.bd-top{background:linear-gradient(135deg,#2FD6C8,#0B7F86)}
.save{display:inline-block;align-self:flex-start;margin-top:4px;font-size:12.5px;font-weight:700;color:#0B7F86;background:color-mix(in srgb,#2FD6C8 18%,transparent);padding:2px 9px;border-radius:999px}
.go.buy{display:block;text-align:center;padding:11px 14px;border-radius:12px;font-weight:700;color:#1A1250!important;text-decoration:none;
  background:linear-gradient(135deg,#FFE3A0,#F2C266 50%,#E0A53A);box-shadow:0 10px 24px -12px #C98A1E;transition:transform .2s,box-shadow .2s}
.go.buy:hover{transform:translateY(-2px);box-shadow:0 14px 30px -10px #C98A1E,0 0 20px -6px #F2C266}
@media (prefers-reduced-motion:reduce){.cc,.cc-orb,.cd::after,.cd-fire,.bd-hot,.cc::before{animation:none!important}}
@media(max-width:640px){.ccards{grid-template-columns:1fr 1fr;gap:10px}.cc{padding:16px 13px 13px}.cc-orb{width:50px;height:50px}.cc-orb i{font-size:24px}.cc-hook{font-size:12.5px}.cc-badge{font-size:10px;padding:3px 8px}.cd-clock{margin-inline-start:0;width:100%;justify-content:center}}
"""
CSS_V4 = r"""
.nova{width:min(420px,calc(100vw - 32px))!important;height:min(640px,calc(100vh - 110px))!important}
.nova .m.a{white-space:normal;max-width:96%}
.nova .m p{margin:0 0 6px}.nova .m p:last-child{margin:0}
.nova .m ul{margin:4px 0 6px;padding-inline-start:18px}
.nova .tbl{overflow-x:auto;margin:6px 0;border-radius:10px;border:1px solid var(--line);background:var(--surface)}
.nova table{border-collapse:collapse;width:100%;font-size:12.5px;line-height:1.4}
.nova th{background:linear-gradient(135deg,var(--violet),#3B22B8);color:#fff;font-weight:600;padding:7px 8px;text-align:start;white-space:nowrap}
.nova td{padding:7px 8px;border-top:1px solid var(--line);vertical-align:top}
.nova tr:nth-child(odd) td{background:var(--violet-soft)}
.tabs{flex-direction:column;gap:12px}
.tgroup{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.tlabel{font-weight:700;font-size:13.5px;color:var(--muted);min-width:150px}
@media(max-width:640px){.tlabel{min-width:100%}.tabs{max-width:100%;overflow:hidden}.tgroup{max-width:100%;min-width:0;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}.tgroup .tlabel{position:sticky;inset-inline-start:0;min-width:auto;background:var(--bg);padding-inline-end:6px}.tgroup button{flex:none}}
.cats{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:14px}
.cats a{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:14px;background:var(--surface);border:1px solid var(--line);color:var(--ink);text-decoration:none;font-weight:600;font-size:14px;transition:transform .2s,border-color .2s,box-shadow .2s}
.cats a:hover{transform:translateY(-2px);border-color:var(--violet);box-shadow:0 10px 24px -14px var(--violet)}
.cats a i{font-style:normal;font-size:20px}
.ask-nova{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;margin-top:18px;padding:16px 18px;border-radius:16px;background:linear-gradient(135deg,var(--violet-soft),var(--gold-soft));border:1px solid var(--line)}
.ask-nova b{font-size:16px}.ask-nova p{margin:2px 0 0;color:var(--muted);font-size:14px}
"""

DEALS_JS = r"""
(function(){
  var C=window.DEALS||{}, grid=document.getElementById('deals'), st=document.getElementById('status'), tabs=document.getElementById('tabs');
  if(!grid)return;
  var cache={};
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function skel(){grid.innerHTML=new Array(9).join('<div class="skel"></div>');st.textContent=C.loading;}
  function render(data){
    var items=(data&&data.items)||[];
    if(!items.length){grid.innerHTML='';st.innerHTML=esc(C.empty);return;}
    var t=new Date(data.updated);
    st.textContent=C.updated+': '+t.toLocaleString(C.lang==='ar'?'ar':C.lang==='fr'?'fr-FR':'en',{dateStyle:'medium',timeStyle:'short'});
    var B=C.B||{};
    grid.innerHTML=items.map(function(p,i){
      var d=parseInt(String(p.discount||'0').replace(/[^0-9]/g,''))||0, r=parseFloat(String(p.rating||'0'))||0, sold=+p.sold||0;
      var badges=[];
      if(d>=50)badges.push('<span class="bd bd-hot">🔥 '+(C.lang==='ar'?B.off+' '+d+'%':'-'+d+'% '+B.off)+'</span>');
      if(sold>=1000)badges.push('<span class="bd bd-best">'+esc(B.best)+'</span>');
      else if(r>=97)badges.push('<span class="bd bd-top">'+esc(B.top)+' '+r.toFixed(0)+'%</span>');
      var off=d&&d<50?'<span class="off">-'+d+'%</span>':'';
      var orig=p.orig&&p.orig!==p.price?'<s>$'+esc(p.orig)+'</s>':'';
      var sv=(+p.orig-+p.price);var save=sv>=2?'<div class="save">'+esc(B.save)+' $'+sv.toFixed(2)+'</div>':'';
      var meta=[];if(sold)meta.push(esc(sold)+' '+esc(C.sold));if(r)meta.push('★ '+esc(p.rating));
      return '<article class="card deal glowcard enter" style="animation-delay:'+(i*40)+'ms">'
        +'<div class="bds">'+badges.slice(0,2).join('')+'</div>'
        +'<a href="'+esc(p.link)+'" target="_blank" rel="sponsored nofollow noopener"><img class="shot" src="'+esc(p.img)+'" alt="" loading="lazy" width="350" height="350"></a>'
        +'<h3>'+esc(p.title)+'</h3>'
        +'<div class="priceRow"><b>$'+esc(p.price)+'</b>'+orig+off+'</div>'+save
        +'<div class="meta">'+meta.join(' · ')+'</div>'
        +'<div style="margin-top:auto"><a class="go buy" href="'+esc(p.link)+'" target="_blank" rel="sponsored nofollow noopener">'+esc(C.go)+'</a></div></article>';
    }).join('');
  }
  function hero(n){var h=document.getElementById('cathero');if(!h)return;
    h.className='cathero tone-'+((C.tones||{})[n]||'violet');
    document.getElementById('ch-i').textContent=(C.icons||{})[n]||'✦';
    document.getElementById('ch-n').textContent=(C.names||{})[n]||'';
    document.getElementById('ch-h').textContent=(C.hooks||{})[n]||'';
    h.classList.remove('pulse');void h.offsetWidth;h.classList.add('pulse');}
  (function(){var cd=document.getElementById('cd');if(!cd)return;var B=C.B,start=new Date(2026,10,11,0,0,0),end=new Date(2026,10,19,0,0,0);
    function pad(x){return (x<10?'0':'')+x}
    function tick(){var now=new Date();if(now>=end){cd.hidden=true;return;}cd.hidden=false;
      if(now<start){var t=Math.floor((start-now)/1000),D=Math.floor(t/86400),H=Math.floor(t%86400/3600),M=Math.floor(t%3600/60),S=t%60;
        document.getElementById('cd-t').textContent=B.cdT;document.getElementById('cd-s').textContent=B.cdS;
        document.getElementById('cd-c').innerHTML=[[D,B.d],[H,B.h],[M,B.m],[S,B.s]].map(function(x){return '<span><b>'+pad(x[0])+'</b><i>'+x[1]+'</i></span>'}).join('');}
      else{cd.classList.add('live');document.getElementById('cd-t').textContent=B.liveT;document.getElementById('cd-s').textContent=B.liveS;document.getElementById('cd-c').innerHTML='';}}
    tick();setInterval(tick,1000);})();
  var S=C.S||{}, qi=document.getElementById('q'), sugg=document.getElementById('sugg'), sform=document.getElementById('sform');
  function norm(x){return String(x||'').toLowerCase().replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').trim()}
  function suggest(v){if(!sugg)return;var n=norm(v);if(n.length<2){sugg.innerHTML='';return;}
    var hits=Object.keys(C.names||{}).filter(function(k){return norm(C.names[k]).indexOf(n)>-1||norm((C.hooks||{})[k]).indexOf(n)>-1||k.indexOf(n)>-1}).slice(0,6);
    sugg.innerHTML=hits.length?'<span>'+esc(S.cats)+'</span>'+hits.map(function(k){return '<button type="button" data-n="'+k+'">'+esc((C.icons||{})[k]||'✦')+' '+esc(C.names[k])+'</button>'}).join(''):'';}
  function search(v){v=String(v||'').trim();if(v.length<2){st.textContent=S.short;return;}
    var h=document.getElementById('cathero');h.className='cathero tone-blue';
    document.getElementById('ch-i').textContent='🔍';document.getElementById('ch-n').textContent=S.res+' '+S.for+' «'+v+'»';document.getElementById('ch-h').textContent=S.hook;
    h.classList.remove('pulse');void h.offsetWidth;h.classList.add('pulse');
    tabs.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed','false')});
    try{history.replaceState(null,'','?q='+encodeURIComponent(v))}catch(e){}
    var key='q:'+v.toLowerCase();if(cache[key]){render(cache[key]);return;}
    skel();
    fetch('/api/products?q='+encodeURIComponent(v)+'&lang='+C.lang).then(function(r){return r.json()}).then(function(j){
      if(j.error)throw j; cache[key]=j; if(!(j.items||[]).length){grid.innerHTML='';st.textContent=S.none;return;} render(j);
    }).catch(function(){grid.innerHTML='';st.innerHTML=esc(C.fail);});
    if(innerWidth<760)h.scrollIntoView({behavior:'smooth',block:'start'});}
  if(sform){sform.addEventListener('submit',function(ev){ev.preventDefault();qi.blur();search(qi.value);});
    qi.addEventListener('input',function(){suggest(qi.value)});
    sugg.addEventListener('click',function(ev){var b=ev.target.closest('button[data-n]');if(!b)return;sugg.innerHTML='';qi.value='';nav(b.dataset.n);});}
  var wr=document.getElementById('worlds');
  function setWorld(wi){if(!wr)return;wr.querySelectorAll('.wbtn').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.w===String(wi))});
    tabs.querySelectorAll('.tgroup').forEach(function(g){g.hidden=g.dataset.w!==String(wi)});
    var a=wr.querySelector('.wbtn[data-w="'+wi+'"]');if(a&&a.scrollIntoView)try{a.scrollIntoView({block:'nearest',inline:'center',behavior:'smooth'})}catch(e){}}
  function nav(n){try{if(location.hash.slice(1)!==n)history.pushState({n:n},'',location.pathname+'#'+n)}catch(e){}load(n);}
  if(wr)wr.addEventListener('click',function(ev){var b=ev.target.closest('.wbtn');if(!b)return;var g=tabs.querySelector('.tgroup[data-w="'+b.dataset.w+'"] button');if(g)nav(g.dataset.n);});
  addEventListener('popstate',function(){var n=(location.hash||'').slice(1);if(n&&tabs.querySelector('button[data-n="'+n+'"]'))load(n);});
  addEventListener('hashchange',function(){var n=(location.hash||'').slice(1);if(n&&tabs.querySelector('button[data-n="'+n+'"]'))load(n);});
  function load(n){
    hero(n);
    var tb=tabs.querySelector('button[data-n="'+n+'"]');if(tb)setWorld(tb.parentNode.dataset.w);
    tabs.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.n===n)});
    if(cache[n]){render(cache[n]);return;}
    skel();
    fetch('/api/products?niche='+encodeURIComponent(n)+'&lang='+C.lang).then(function(r){return r.json()}).then(function(j){
      if(j.error)throw j; cache[n]=j; render(j);
    }).catch(function(){grid.innerHTML='';st.innerHTML=esc(C.fail)+' <a href="'+C.home+'">DoniaNova</a>';});
  }
  tabs.addEventListener('click',function(ev){var b=ev.target.closest('button[data-n]');if(!b)return;nav(b.dataset.n);
    if(innerWidth<760)st.scrollIntoView({behavior:'smooth',block:'start'});});
  var h=(location.hash||'').slice(1), sp=null;try{sp=new URLSearchParams(location.search)}catch(e){}
  var q0=sp&&sp.get('q');
  if(q0&&q0.trim().length>=2){qi.value=q0;suggest(q0);search(q0);}
  else{load(tabs.querySelector('button[data-n="'+h+'"]')?h:tabs.querySelector('button').dataset.n);
    if(sp&&sp.has('q')&&qi){qi.focus();}}
})();
"""

NOVA_JS = r"""
(function(){
  var LG=document.documentElement.lang||'ar',ar=LG==='ar';
  var NOVA_FR={fab:'Demander à Nova',title:'Nova, votre assistant intelligent',sub:'Il cherche, compare et vous conseille',hi:'Bonjour 👋 Je suis Nova. Je cherche sur AliExpress et compare les produits à leur prix actuel : lecteurs de codes-barres, disques, accessoires de téléphone, matériel pour enseigner et voyager… Dites-moi ce dont vous avez besoin et votre budget.',ph:'Écrivez votre question…',send:'Envoyer',chips:['Compare les meilleurs SSD portables','Lecteur de codes-barres sans fil pour une petite boutique','De bons écouteurs pour les cours en ligne','Chargeur rapide et batterie externe pour voyager'],err:'Pas de réponse pour le moment. Réessayez dans un instant.',rate:'Limite de questions atteinte pour le moment. Réessayez dans quelques minutes.',fine:"L'assistant peut se tromper. Le prix final est sur AliExpress."};
  var T=LG==='fr'?NOVA_FR:ar?{fab:'اسأل نوفا',title:'نوفا، مساعدك الذكي',sub:'يبحث، يقارن ويقترح لك الأنسب',hi:'أهلاً 👋 أنا نوفا. أبحث لك في علي إكسبريس وأقارن بين المنتجات بأسعارها الحالية: قارئ باركود، أقراص صلبة، لواحق الهاتف، أدوات التعليم والسفر… أخبرني ماذا تحتاج وميزانيتك.',ph:'اكتب سؤالك…',send:'إرسال',chips:['قارن لي بين أفضل أقراص SSD المحمولة','قارئ باركود لاسلكي لمحل صغير','سماعة جيدة للحصص عن بعد','شاحن سريع وبطارية للسفر'],err:'تعذّر الرد الآن. جرّب بعد قليل.',rate:'وصلت إلى الحد المؤقت للأسئلة، جرّب بعد دقائق.',fine:'قد يخطئ المساعد. السعر النهائي على علي إكسبريس.'}
          :{fab:'Ask Nova',title:'Nova, your smart assistant',sub:'Searches, compares and suggests',hi:'Hi 👋 I am Nova. I search AliExpress and compare products at their current prices: barcode scanners, drives, phone accessories, teaching and travel gear… Tell me what you need and your budget.',ph:'Type your question…',send:'Send',chips:['Compare the best portable SSDs','Wireless barcode scanner for a small shop','Good earbuds for online classes','Fast charger and power bank for travel'],err:'No reply right now. Please try again shortly.',rate:'Question limit reached for now. Try again in a few minutes.',fine:'The assistant can make mistakes. Final price is on AliExpress.'};
  var hist=[];try{hist=JSON.parse(sessionStorage.getItem('nova')||'[]')}catch(e){}
  var star='<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 1 L19 13 L31 16 L19 19 L16 31 L13 19 L1 16 L13 13 Z" fill="#E6B95B"/></svg>';
  var fab=document.createElement('button');fab.className='nova-fab';fab.type='button';fab.innerHTML=star+'<span>'+T.fab+'</span>';fab.setAttribute('aria-expanded','false');
  document.body.appendChild(fab);
  var box=null,log,inp,busy=false;
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function inl(s){s=esc(s).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
    return s.replace(/(https?:\/\/[^\s)<]+|\/(?:ar|en|fr)\/(?:p\/[a-z0-9-]+\/|deals\/))/g,function(u){var ext=u.indexOf('http')===0;return '<a href="'+u+'"'+(ext?' target="_blank" rel="sponsored nofollow noopener"':'')+'>'+(ext?(ar?'عرض المنتج ↗':LG==='fr'?'Voir le produit ↗':'View product ↗'):(ar?'افتح الصفحة':LG==='fr'?'Ouvrir la page':'Open page'))+'</a>'});}
  function fmt(s){var L=s.split('\n'),o='',i=0;
    while(i<L.length){var l=L[i].trim();
      if(/^\|.*\|$/.test(l)){var rows=[];while(i<L.length&&/^\|.*\|$/.test(L[i].trim())){rows.push(L[i].trim());i++;}
        rows=rows.filter(function(r){return !/^\|[\s:\-|]+\|$/.test(r)});
        o+='<div class="tbl"><table>'+rows.map(function(r,ri){var c=r.slice(1,-1).split('|');return '<tr>'+c.map(function(x){return ri?'<td>'+inl(x.trim())+'</td>':'<th>'+inl(x.trim())+'</th>'}).join('')+'</tr>'}).join('')+'</table></div>';continue;}
      if(/^[-•*]\s+/.test(l)){o+='<ul>';while(i<L.length&&/^[-•*]\s+/.test(L[i].trim())){o+='<li>'+inl(L[i].trim().replace(/^[-•*]\s+/,''))+'</li>';i++;}o+='</ul>';continue;}
      if(/^#{1,4}\s/.test(l)){o+='<p><b>'+inl(l.replace(/^#+\s/,''))+'</b></p>';i++;continue;}
      if(l)o+='<p>'+inl(l)+'</p>';i++;}
    return o;}
  function add(role,text,cls){var d=document.createElement('div');d.className='m '+(role==='user'?'u':'a')+(cls?' '+cls:'');d.innerHTML=role==='user'?esc(text):fmt(text);log.appendChild(d);log.scrollTop=log.scrollHeight;return d;}
  function save(){try{sessionStorage.setItem('nova',JSON.stringify(hist.slice(-12)))}catch(e){}}
  function send(q){q=(q||'').trim();if(!q||busy)return;busy=true;inp.value='';add('user',q);hist.push({role:'user',content:q});save();
    var t=add('assistant','…','typing');
    fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:LG,messages:hist})})
      .then(function(r){return r.json().then(function(j){return{s:r.status,j:j}})})
      .then(function(x){t.remove();if(x.j.reply){add('assistant',x.j.reply);hist.push({role:'assistant',content:x.j.reply});save();}else add('assistant',x.s===429?T.rate:T.err);})
      .catch(function(){t.remove();add('assistant',T.err);}).then(function(){busy=false;inp.focus();});}
  function open(){
    if(box){box.hidden=!box.hidden;fab.setAttribute('aria-expanded',String(!box.hidden));if(!box.hidden)inp.focus();return;}
    box=document.createElement('section');box.className='nova';box.setAttribute('aria-label',T.title);
    box.innerHTML='<header>'+star.replace('<svg','<svg width="26" height="26"')+'<div><b>'+T.title+'</b><small>'+T.sub+'</small></div><button type="button" aria-label="close">×</button></header><div class="log" aria-live="polite"></div><div class="chips"></div><form><input id="nova-q" maxlength="600" autocomplete="off" placeholder="'+T.ph+'"><button type="submit">'+T.send+'</button></form><div class="fine">'+T.fine+'</div>';
    document.body.appendChild(box);log=box.querySelector('.log');inp=box.querySelector('input');
    add('assistant',T.hi);hist.forEach(function(m){add(m.role,m.content)});
    var ch=box.querySelector('.chips');if(!hist.length)T.chips.forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c;b.onclick=function(){ch.remove();send(c)};ch.appendChild(b)});
    box.querySelector('header button').onclick=function(){box.hidden=true;fab.setAttribute('aria-expanded','false')};
    box.querySelector('form').onsubmit=function(ev){ev.preventDefault();var c=box.querySelector('.chips');if(c)c.remove();send(inp.value)};
    fab.setAttribute('aria-expanded','true');inp.focus();}
  fab.addEventListener('click',open);
})();
"""

NAV_JS = r"""
(function(){
  var tb=document.getElementById('topbar'),mega=document.getElementById('mega'),mb=document.querySelector('.mg-btn'),dd=document.querySelector('.tgdd'),tp=dd&&dd.querySelector('.tg-pill'),tm=dd&&dd.querySelector('.tgmenu');
  var veil=document.createElement('div');veil.className='veil';veil.hidden=true;document.body.appendChild(veil);
  function onS(){if(tb)tb.classList.toggle('stuck',scrollY>40)}onS();addEventListener('scroll',onS,{passive:true});
  function closeAll(){if(mega){mega.hidden=true;if(mb)mb.setAttribute('aria-expanded','false');}if(tm){tm.hidden=true;tp.setAttribute('aria-expanded','false');}document.body.classList.remove('sheet-mega','sheet-tg');veil.hidden=true;}
  function openMega(sheet){var o=mega.hidden;closeAll();if(!o)return;mega.hidden=false;if(mb)mb.setAttribute('aria-expanded','true');if(sheet){document.body.classList.add('sheet-mega');veil.hidden=false;}if(tb)tb.classList.add('stuck');}
  function openTg(sheet){var o=tm.hidden;closeAll();if(!o)return;tm.hidden=false;tp.setAttribute('aria-expanded','true');if(sheet){document.body.classList.add('sheet-tg');veil.hidden=false;}}
  if(mb&&mega)mb.addEventListener('click',function(ev){ev.stopPropagation();openMega(false)});
  if(tp&&tm)tp.addEventListener('click',function(ev){ev.stopPropagation();openTg(false)});
  document.addEventListener('click',function(ev){if(ev.target.closest('.mega .mg-grid,.tgmenu,.bbar'))return;if((mega&&!mega.hidden)||(tm&&!tm.hidden))closeAll();});
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape')closeAll()});
  if(mega)mega.addEventListener('click',function(ev){if(ev.target.closest('a'))closeAll()});
  var bs=document.querySelector('.bb-sec'),bn=document.querySelector('.bb-nova'),bt=document.querySelector('.bb-tg');
  if(bs)bs.addEventListener('click',function(ev){ev.stopPropagation();openMega(true)});
  if(bt)bt.addEventListener('click',function(ev){ev.stopPropagation();openTg(true)});
  if(bn)bn.addEventListener('click',function(){closeAll();var f=document.querySelector('.nova-fab');if(f)f.click()});
  veil.addEventListener('click',closeAll);
  document.querySelectorAll('.backbtn').forEach(function(b){b.addEventListener('click',function(){
    var same=document.referrer&&document.referrer.indexOf(location.origin)===0;
    if(same&&history.length>1)history.back();else location.href=b.dataset.home;});});
})();
"""

JS = """
(function(){
  var f=document.getElementById('filters');
  document.documentElement.classList.add('js');
  (function(){var u=location.href.split('#')[0],en=encodeURIComponent(u);
    document.querySelectorAll('.sb[data-net]').forEach(function(a){var n=a.dataset.net;
      a.href=n==='wa'?'https://wa.me/?text='+encodeURIComponent(document.title+' '+u):n==='fb'?'https://www.facebook.com/sharer/sharer.php?u='+en:'https://t.me/share/url?url='+en+'&text='+encodeURIComponent(document.title);});
    var c=document.querySelector('.sb-copy');if(c)c.addEventListener('click',function(){var sp=c.querySelector('span'),o=sp.textContent;
      var done=function(){sp.textContent=c.dataset.copied;setTimeout(function(){sp.textContent=o},1800)};
      if(navigator.clipboard)navigator.clipboard.writeText(u).then(done,function(){prompt('',u)});else prompt('',u);});})();
  var still0=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(f){f.addEventListener('click',function(ev){var b=ev.target.closest('button[data-cat]');if(!b)return;var c=b.dataset.cat;
    f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    var n=0,i=0;
    document.querySelectorAll('#grid .card').forEach(function(k){var show=(c==='all'||k.dataset.cat===c);k.hidden=!show;k.classList.remove('enter');
      if(show){n++;if(!still0){void k.offsetWidth;k.style.animationDelay=(i++*45)+'ms';k.classList.add('enter');}}});
    var ct=document.getElementById('count');if(ct)ct.textContent=ct.dataset.tpl.replace('{n}',n);
    var g=document.getElementById('picks');if(g&&g.getBoundingClientRect().top<0)g.scrollIntoView({behavior:still0?'auto':'smooth'});});}
  document.querySelectorAll('.card').forEach(function(k){k.addEventListener('pointermove',function(ev){var r=k.getBoundingClientRect();
    k.style.setProperty('--mx',(ev.clientX-r.left)+'px');k.style.setProperty('--my',(ev.clientY-r.top)+'px');});});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});}
  else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});}
  try{document.querySelectorAll('.lang a').forEach(function(a){a.addEventListener('click',function(){localStorage.setItem('dn-lang',a.getAttribute('hreflang'))})})}catch(e){}
  var c=document.getElementById('sky');if(!c)return;var x=c.getContext('2d');
  var still=matchMedia('(prefers-reduced-motion: reduce)').matches,stars=[],w,h;
  function size(){var r=c.getBoundingClientRect(),d=devicePixelRatio||1;w=r.width;h=r.height;c.width=w*d;c.height=h*d;x.setTransform(d,0,0,d,0,0);
    stars=Array.from({length:Math.round(w*h/5000)},function(){return{x:Math.random()*w,y:Math.random()*h,r:Math.random()*1.2+.2,p:Math.random()*6.28}})}
  function draw(t){x.clearRect(0,0,w,h);var nx=document.documentElement.dir==='rtl'?w*.16:w*.84,ny=h*.42;
    var g=x.createRadialGradient(nx,ny,0,nx,ny,Math.min(w,h)*.55);g.addColorStop(0,'rgba(230,185,91,.35)');g.addColorStop(.35,'rgba(230,185,91,.08)');g.addColorStop(1,'rgba(230,185,91,0)');
    x.fillStyle=g;x.fillRect(0,0,w,h);stars.forEach(function(s){x.fillStyle='rgba(238,240,248,'+(.35+.45*Math.sin(s.p+(t||0)/1400))+')';x.beginPath();x.arc(s.x,s.y,s.r,0,6.28);x.fill()});
    if(!still)requestAnimationFrame(draw)}
  size();addEventListener('resize',size);draw(0);
})();
"""

ROOT = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>DoniaNova — The best of tech: top-rated, best-selling, live prices</title>
<meta name="description" content="{e(UI['en']['site_desc'])}">
<link rel="canonical" href="{BASE}/en/">
<link rel="alternate" hreflang="en" href="{BASE}/en/"><link rel="alternate" hreflang="ar" href="{BASE}/ar/"><link rel="alternate" hreflang="fr" href="{BASE}/fr/"><link rel="alternate" hreflang="x-default" href="{BASE}/en/">
<meta http-equiv="refresh" content="0; url=/en/">
<script>try{{var l=localStorage.getItem('dn-lang')||(function(n){{return n==='ar'||n==='fr'?n:'en'}})((navigator.language||'').slice(0,2));location.replace('/'+l+'/')}}catch(e){{location.replace('/en/')}}</script>
</head><body><p><a href="/en/">DoniaNova (English)</a> · <a href="/ar/">دنيا نوفا (العربية)</a> · <a href="/fr/">DoniaNova (Français)</a></p></body></html>"""

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#101634"/><path d="M16 4 L18.4 13.6 L28 16 L18.4 18.4 L16 28 L13.6 18.4 L4 16 L13.6 13.6 Z" fill="#E6B95B"/></svg>'

def write(path, s):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full) or OUT, exist_ok=True)
    open(full, "w", encoding="utf-8").write(s)

def main():
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    shutil.copytree(SRC_IMG, os.path.join(OUT, "img"))
    if os.path.exists("og.jpg"): shutil.copy("og.jpg", os.path.join(OUT, "img", "og.jpg"))
    write("deals.js", DEALS_JS); shutil.copytree("api", os.path.join(OUT, "api"))
    cat = [{"slug":p["slug"],"cat":p["cat"],"ar":{"name":p["ar"][0],"why":p["ar"][1],"best":p["ar"][2]},"en":{"name":p["en"][0],"why":p["en"][1],"best":p["en"][2]}} for p in PRODUCTS]
    write("api/_catalog.js", "module.exports = " + json.dumps(cat, ensure_ascii=False, indent=1) + ";\n")
    write("style.css", CSS + CSS_V4 + CSS_V5 + CSS_V6 + CSS_V7 + CSS_V8 + CSS_V9 + CSS_V10 + CSS_PROMO + CSS_GLOW + "\n@media (max-width:560px){.lang a{padding:4px 7px;font-size:12px}.lang{gap:0;padding:2px}.tright{gap:6px}}\n@media (max-width:380px){.lang a{padding:4px 6px}}\n"); write("site.js", JS + NOVA_JS + TILT_JS + NAV_JS + V10_JS + PROMO_JS); shutil.copy("promos.json", os.path.join(OUT, "promos.json")); shutil.copy("labels.json", os.path.join(OUT, "img", "labels.json")); write("favicon.svg", FAVICON); write("index.html", ROOT)
    for g in os.listdir("."):
        if g.startswith("google") and g.endswith(".html"): shutil.copy(g, os.path.join(OUT, g))
    urls = []
    from frtr import tr_html, tr_text, dump_missing
    for lang in LANGS:
        W = (lambda p_, s_: write(p_, tr_html(s_))) if lang == "fr" else write
        W(f"{lang}/index.html", home(lang)); urls.append(url(lang))
        W(f"{lang}/deals/index.html", deals(lang)); urls.append(url(lang, "deals/"))
        W(f"{lang}/guides/index.html", guides_index(lang)); urls.append(url(lang, "guides/"))
        for g in GUIDES:
            W(f"{lang}/guides/{g['slug']}/index.html", guide_page(g, lang)); urls.append(url(lang, "guides/"+g["slug"]+"/"))
        for p in PRODUCTS:
            W(f"{lang}/p/{p['slug']}/index.html", product(p, lang)); urls.append(url(lang, "p/"+p["slug"]+"/"))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for u_ in urls:
        lang = u_.split("/")[1]; rest = u_[len(lang)+2:]
        sm.append(f'<url><loc>{BASE}{u_}</loc><lastmod>{TODAY}</lastmod>'
                  + "".join(f'<xhtml:link rel="alternate" hreflang="{L_}" href="{BASE}/{L_}/{rest}"/>' for L_ in LANGS) + '</url>')
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    _k=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),".indexnow_key")).read().strip(); write(_k+".txt", _k)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    os.makedirs(os.path.join(OUT,"privacy"),exist_ok=True); write("privacy/index.html", PRIVACY)
    names = {L:{k:n for _,items in DEALS_T[L]["tabs"] for k,n in items} for L in ("ar","en")}
    names["fr"] = {k: tr_text(v) for k, v in names["en"].items()}
    dump_missing()
    with open(os.path.join(OUT,"api","_names.js"),"w",encoding="utf-8") as f: f.write("module.exports = "+json.dumps(names,ensure_ascii=False)+";\n")
    write("vercel.json", json.dumps({"cleanUrls": False, "trailingSlash": True,
        "rewrites":[{"source":"/daily.xml","destination":"/api/feed"}],
        "crons":[{"path":"/api/telegram?daily=1","schedule":"30 7 * * *"},{"path":"/api/indexnow","schedule":"0 6 * * 1"}],
        "headers":[{"source":"/img/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=604800"}]}]}, indent=1))
    print(f"{len(PRODUCTS)} products, {len(urls)} pages -> {OUT}/ (base {BASE})")

main()
