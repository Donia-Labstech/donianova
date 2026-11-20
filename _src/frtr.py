"""EN -> FR translation layer for DoniaNova: pages are rendered in English, then every
visible string (text nodes, UI attributes, JSON-LD, inline JSON configs) is mapped
through fr_dict.json. Unknown strings stay English and are listed in fr_missing.json."""
import json, os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
DICT_PATH = os.path.join(HERE, "fr_dict.json")
FR = json.load(open(DICT_PATH, encoding="utf-8")) if os.path.exists(DICT_PATH) else {}
MISSING = {}
LETTERS = re.compile(r"[A-Za-z]{2,}|^[A-Za-z]$")
SKIP_KEYS = {"lang", "home", "tones", "icons", "url", "image", "img", "link", "@type", "@context", "@id", "sameAs", "logo",
             "item", "priceCurrency", "availability", "inLanguage", "datePublished", "dateModified", "slug", "ic"}

def tr_text(s):
    if not s or not LETTERS.search(s): return s
    k = s.strip()
    if not k or k.startswith(("/", "http", "#", "{")): return s
    if k in FR:
        v = FR[k]
        lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
        return lead + v + trail
    v = _compose(k)
    if v is not None:
        lead = s[:len(s) - len(s.lstrip())]; trail = s[len(s.rstrip()):]
        return lead + v + trail
    MISSING[k] = MISSING.get(k, 0) + 1
    return s

PATTERNS = [(re.compile(r"^Last updated: (.+)$"), "Dernière mise à jour : {}"), (re.compile(r"^Showing: (.+)$"), "Affichés : {}")]

def _compose(k):
    for rx, tpl in PATTERNS:
        m = rx.match(k)
        if m: return tpl.format(m.group(1))
    for sep in (" | ", " · ", " — "):
        if sep in k:
            parts = k.split(sep)
            if all((not LETTERS.search(x)) or x.strip() in FR or x.strip() in BRANDS for x in parts):
                return sep.join(FR.get(x.strip(), x) for x in parts)
    if len(k) >= 80:  # truncated meta description: translate the full text, cut again
        full = next((f for f in FR if f.startswith(k) and len(f) > len(k)), None)
        if full:
            v = FR[full]; n = len(k)
            return v if len(v) <= n + 15 else v[:n].rsplit(" ", 1)[0] + "…"
    return None

BRANDS = {"DoniaNova", "AliExpress", "Anker", "Baseus", "DJI", "Eyoyo", "UGREEN", "Xiaomi", "Netum", "Lenovo", "EN", "FR", "DONIA LABS TECH"}

def tr_json(o, key=None):
    if key in SKIP_KEYS: return o
    if isinstance(o, str): return tr_text(o)
    if isinstance(o, list): return [tr_json(x, key) for x in o]
    if isinstance(o, dict): return {k: (k_names(v) if k == "names" else tr_json(v, k)) for k, v in o.items()}
    return o

def k_names(d):
    return {k: tr_text(v) for k, v in d.items()} if isinstance(d, dict) else d

ATTRS = ("alt", "title", "placeholder", "aria-label")
TOKEN = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<!--.*?-->|<[^>]+>)", re.S | re.I)
ATTR_RE = re.compile(r'(\s(?:alt|title|placeholder|aria-label)=")([^"]*)(")')
META_RE = re.compile(r'(<meta\s+(?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description)"\s+content=")([^"]*)(")')
JSCFG = re.compile(r"((?:window\.DEALS|var T)=)(\{.*?\})((?:,L=|;</script>|;\s*</script>))", re.S)

def _attr(m):
    return m.group(1) + html.escape(tr_text(html.unescape(m.group(2))), quote=True) + m.group(3)

def _script(tok):
    if 'application/ld+json' in tok[:80]:
        i = tok.index(">") + 1; j = tok.rindex("</script>")
        try:
            data = json.loads(tok[i:j])
            return tok[:i] + json.dumps(tr_json(data), ensure_ascii=False).replace("</", "<\\/") + tok[j:]
        except Exception:
            return tok
    def rep(m):
        try:
            data = json.loads(m.group(2).replace("<\\/", "</"))
        except Exception:
            return m.group(0)
        return m.group(1) + json.dumps(tr_json(data), ensure_ascii=False).replace("</", "<\\/") + m.group(3)
    return JSCFG.sub(rep, tok)

def tr_html(s):
    out = []
    for part in TOKEN.split(s):
        if not part: continue
        if part.startswith("<"):
            low = part[:7].lower()
            if low.startswith("<script"): out.append(_script(part))
            elif low.startswith("<style") or part.startswith("<!--"): out.append(part)
            else:
                part = ATTR_RE.sub(_attr, part)
                part = META_RE.sub(_attr, part)
                out.append(part)
        else:
            out.append(html.escape(tr_text(html.unescape(part)), quote=False))
    return "".join(out)

def dump_missing():
    p = os.path.join(HERE, "fr_missing.json")
    json.dump(sorted(MISSING), open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"FR: {len(FR)} entries, {len(MISSING)} missing -> fr_missing.json")
