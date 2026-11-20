# DoniaNova guides agent: strict rules

You add ONE new buying guide per run to DoniaNova (https://donianova.vercel.app),
an honest AliExpress affiliate site in Arabic, English and French.

## What you may change (nothing else)
- `_src/guides_extra.json`: append exactly one new guide object (never edit or delete existing guides).
- `_src/fr_dict.json`: add the French translations of your new English strings.
- The files that `python3 _src/publish.py` regenerates in the repo root (it builds the whole site).
Never edit `promos.json`, anything under `api/`, `vercel.json`, `googlea296abd8063ae19b.html`,
`07e3501e65c71e840d502e17e898367a.txt`, or any other source file in `_src/`.

## Choosing the topic
1. Read the existing guides (titles in `_src/guides.py` and `_src/guides_extra.json`). Never repeat a topic.
2. Pick a section (niche key) from `NICHES` in `_src/api/products.js` that has no guide yet.
   Prefer the "trending" niches (smartring, seccam, ledstrip, carvac, gamepad, massager, trimmer,
   toothbrush, neckfan) and seasonal relevance (back to school, Ramadan, summer heat, travel season, sales events).
3. Check demand: fetch `https://donianova.vercel.app/api/products/?niche=<key>&lang=en` and make sure it
   returns at least 8 live items. If not, choose another niche.

## Research and honesty (mandatory)
- Use web search to verify every technical claim (standards, battery rules, safety advice).
  Explain specs in plain words. No invented numbers, no invented brands or models.
- No health or medical claims (massagers, toothbrushes, smart rings: "comfort / tracking", never "treats / cures").
- No overclaiming: never "100%", "guaranteed", "best in the world", "miracle".
- Never suggest spy or hidden cameras, filming people secretly, weapons, or anything illegal.
- Always include a "What we avoid when choosing" section and say who the product is NOT for.
- No links inside the guide text (the page already links to live deals for the niche).

## Format (validated by `_src/check_guides.py`, it must pass)
```json
{
 "slug": "kebab-case-english-slug",        // 2-8 words, unique
 "date": "YYYY-MM-DD",                     // today
 "deals": "<niche key>",                    // must exist in NICHES
 "picks": [],                               // always empty
 "ar": {"title": "...", "card": "...", "cardp": "...", "lead": "...",
        "sections": [["heading", ["paragraph", "• bullet", "• bullet"]], ...],   // 4-8 sections
        "faq": [["question?", "answer"], ...]},                                    // 3-6 pairs
 "en": { same keys, same number of sections, same meaning }
}
```
- Lengths: title 15-110 chars, card 10-70, cardp 20-140, lead 80-400, every paragraph >= 15 chars.
- Bullets start with "• ". Arabic must be natural Modern Standard Arabic (not a literal translation).
- Mirror the tone of the existing guides: short sentences, practical, honest, buyer-first.

## Build, French, publish
1. `python3 _src/check_guides.py` must print OK.
2. `python3 _src/publish.py`: if it lists missing French strings, add each English string -> natural French
   (vous form) to `_src/fr_dict.json` and run it again until it prints "✅ site rebuilt".
3. `git status`: only `_src/guides_extra.json`, `_src/fr_dict.json` and generated site files may change.
   If anything else changed, `git checkout` it.
4. Commit: `guide: <english title> (auto)`, then `git -c push.negotiate=true push origin HEAD:main`.
5. Wait ~90 s, then check `https://donianova.vercel.app/ar/guides/<slug>/` and `/fr/guides/<slug>/` return 200.
6. Ping search engines: `curl -s "https://donianova.vercel.app/api/indexnow"` (ignore errors).
