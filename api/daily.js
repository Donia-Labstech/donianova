// DoniaNova daily agent: one category per day -> short honest comparison -> Facebook Page post.
// Runs once a day via Vercel Cron (vercel.json). Cost: one small DeepSeek call (~800 tokens).
// Env: DEEPSEEK_API_KEY, FB_PAGE_ID, FB_PAGE_TOKEN, CRON_SECRET (Vercel sends it automatically to cron calls).
const products = require('./products.js');
const NAMES = require('./_names.js');
const SITE = 'https://donianova.vercel.app';

function pickNiche(date) {
  const keys = Object.keys(products.NICHES);
  const day = Math.floor(date.getTime() / 86400000);   // changes every UTC day
  return keys[day % keys.length];
}

function score(p) {                                     // sold volume weighted by rating
  const r = parseFloat(p.rating) || 90, s = Number(p.sold) || 0;
  return Math.log10(s + 10) * r;
}

// Precise numbers are computed here, not by the model.
function facts(p) {
  const price = Number(p.price) || 0, orig = Number(p.orig) || price;
  let off = orig > price ? Math.round((1 - price / orig) * 100) : 0;
  // Discounts of 60%+ usually come from an inflated "original" price: don't use them as an anchor.
  const trusted = off > 0 && off < 60;
  if (!trusted) off = 0;
  return { price, orig: trusted ? orig : price, off, save: trusted ? +(orig - price).toFixed(2) : 0, rating: parseFloat(p.rating) || 0, sold: Number(p.sold) || 0 };
}
function valueScore(f, minPrice) {          // quality + social proof + price advantage
  return (f.rating || 90) * 0.5 + Math.log10(f.sold + 10) * 12 + (minPrice / (f.price || minPrice)) * 25 + f.off * 0.1;
}

async function writePost(niche, top) {
  const F = top.map(facts);
  const minPrice = Math.min(...F.map(f => f.price || Infinity));
  const scores = F.map(f => valueScore(f, minPrice));
  const wi = scores.indexOf(Math.max(...scores));
  const cheapest = F.findIndex(f => f.price === minPrice);
  const topRated = F.reduce((b, f, i) => f.rating > F[b].rating ? i : b, 0);
  const bestSeller = F.reduce((b, f, i) => f.sold > F[b].sold ? i : b, 0);
  const lines = top.map((p, i) => {
    const f = F[i];
    return `${i + 1}) title: ${p.title.slice(0, 110)}\n   price $${f.price}${f.off ? ` (was $${f.orig}, -${f.off}%, saves $${f.save})` : ''} | rating ${f.rating ? f.rating + '%' : 'new'} | sold ${f.sold}`;
  }).join('\n');
  const tags = `cheapest=${cheapest + 1}; top_rated=${topRated + 1}; best_seller=${bestSeller + 1}; best_value(winner)=${wi + 1}`;
  const sys = [
    'You write Arabic Facebook posts for DoniaNova, a tech deals page. Be precise and honest, persuasive through facts.',
    'Use ONLY the given data. Specs may come only from the product title (capacity, Bluetooth version, size...). Never invent specs, stock levels or deadlines.',
    'Honest marketing psychology: social proof (units sold, rating), price anchoring (old price -> new price, exact saving), loss aversion stated truthfully ("prices on AliExpress change daily"), clarity of choice (one clear winner).',
    'Use strong Arabic action keywords naturally: اطلبه الآن، احصل عليه، وفّر، اكتشف، لا تفوّت.',
    'Format exactly:',
    'line 1: hook with emoji about the WINNER (its real saving, rating or sales) or the category benefit (max 12 words). Never sum or exaggerate savings.',
    'then one line per product: "1️⃣ <short name with 1 key spec from title> — $<price> بدل $<old> (‑<off>%) — ⭐<rating> — 🛒<sold> مبيع — <one precise pro or con>". Omit the "بدل" part if there is no discount.',
    'then: "🏆 اختيارنا: <winner short name> — <reason with numbers>" (the winner is given; do not change it).',
    'then: "👇 <one action sentence>"',
    'Max 120 words. No links, no hashtags.',
    'Output JSON only: {"post":"...","hashtags":["3 short Arabic hashtags for this category, without #"]}'
  ].join('\n');
  const r = await fetch('https://api.deepseek.com/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + process.env.DEEPSEEK_API_KEY },
    body: JSON.stringify({ model: 'deepseek-chat', temperature: 0.35, max_tokens: 520, response_format: { type: 'json_object' }, messages: [
      { role: 'system', content: sys },
      { role: 'user', content: `Category: ${NAMES.ar[niche] || niche}\n${lines}\nFacts: ${tags}` } ] })
  });
  const j = await r.json();
  const txt = j.choices && j.choices[0] && j.choices[0].message.content || '';
  const m = txt.match(/\{[\s\S]*\}/);
  const out = JSON.parse(m ? m[0] : txt);
  const raw = out.hashtags || out.tags || out.hashtag || [];
  const list = (Array.isArray(raw) ? raw : String(raw).split(/[\s,،]+/)).concat([NAMES.ar[niche] || '']);
  const hashtags = [...new Set(list.map(h => String(h).replace(/^#/, '').trim()).filter(Boolean))].slice(0, 3)
    .map(h => '#' + String(h).replace(/^#/, '').trim().replace(/\s+/g, '_')).filter(h => h.length > 2);
  return { post: String(out.post || '').trim(), winner: top[wi], hashtags, usage: j.usage };
}

async function postToFacebook(message, link) {
  const body = new URLSearchParams({ message, link, access_token: process.env.FB_PAGE_TOKEN });
  const r = await fetch(`https://graph.facebook.com/v21.0/${process.env.FB_PAGE_ID}/feed`, { method: 'POST', body });
  return r.json();
}

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// Build today's comparison (used by the cron endpoint and by the RSS feed).
async function buildToday(forced) {
  const niche = products.NICHES[forced] ? forced : pickNiche(new Date());
  const items = await products.nicheItems(niche, 'ar');
  const top = items.filter(p => p.link).sort((a, b) => score(b) - score(a)).slice(0, 3);
  if (top.length < 2) return { niche, skipped: 'not_enough_items' };
  const { post, winner, hashtags, usage } = await writePost(niche, top);
  // Facebook needs a short link: ask AliExpress for one, else fall back to our own category page.
  const short = await require('./_ali.js').shortLink(winner.id);
  winner.link = short || `${SITE}/ar/deals/#${niche}`;
  const message = post +
    `\n\n🛒 اطلبه الآن بأفضل سعر:\n${winner.link}` +
    `\n\n🔎 قارن كل عروض ${NAMES.ar[niche] || ''}:\n${SITE}/ar/deals/#${niche}` +
    '\n\n' + [...hashtags, '#عروض_اليوم', '#تخفيضات', '#علي_إكسبريس', '#DoniaNova', '#رابط_شراكة'].join(' ');
  return { niche, post, message, winner, tokens: usage && usage.total_tokens };
}

module.exports = async (req, res) => {
  const secret = process.env.CRON_SECRET;
  const auth = req.headers.authorization || '';
  const q = req.query || {};
  if (!secret || (auth !== 'Bearer ' + secret && q.key !== secret)) return res.status(401).json({ error: 'unauthorized' });
  if (!process.env.DEEPSEEK_API_KEY) return res.status(500).json({ error: 'missing_deepseek' });

  try {
    const t = await buildToday(q.niche);
    if (t.skipped) return res.status(200).json(t);
    const { niche, message, winner } = t;
    const dry = q.dry === '1' || !process.env.FB_PAGE_ID || !process.env.FB_PAGE_TOKEN;
    const fb = dry ? { dry: true } : await postToFacebook(message, winner.link);
    return res.status(200).json({ niche, message, fb, tokens: t.tokens });
  } catch (e) {
    return res.status(502).json({ error: String(e.message || e) });
  }
};
module.exports.buildToday = buildToday;
module.exports.esc = esc;
