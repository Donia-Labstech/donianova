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

async function writePost(niche, top) {
  const facts = top.map((p, i) => `${i + 1}) ${p.title.slice(0, 90)} | $${p.price} (was $${p.orig}) | rating ${p.rating || 'new'} | sold ${p.sold}`).join('\n');
  const r = await fetch('https://api.deepseek.com/chat/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + process.env.DEEPSEEK_API_KEY },
    body: JSON.stringify({ model: 'deepseek-chat', temperature: 0.4, max_tokens: 380, messages: [
      { role: 'system', content: 'You write short, honest Arabic Facebook posts for DoniaNova, a tech deals page. Use ONLY the given facts; never invent specs, never fake urgency. Format: a catchy first line with an emoji; then 3 lines, one per product: short name — price — rating — one honest pro or con; then a line starting with "🏆 اختيارنا:" naming the best value and why in one sentence. Max 90 words. No hashtags, no links (they are added later). Output JSON only: {"post":"...","winner":1|2|3}' },
      { role: 'user', content: `Category: ${NAMES.ar[niche] || niche}\n${facts}` } ] })
  });
  const j = await r.json();
  const txt = j.choices && j.choices[0] && j.choices[0].message.content || '';
  const m = txt.match(/\{[\s\S]*\}/);
  const out = JSON.parse(m ? m[0] : txt);
  const w = Math.min(Math.max(parseInt(out.winner, 10) || 1, 1), top.length);
  return { post: String(out.post || '').trim(), winner: top[w - 1], usage: j.usage };
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
  const { post, winner, usage } = await writePost(niche, top);
  // Facebook needs a short link: ask AliExpress for one, else fall back to our own category page.
  const short = await require('./_ali.js').shortLink(winner.id);
  winner.link = short || `${SITE}/ar/deals/#${niche}`;
  const message = post +
    `\n\n🛒 رابط المنتج (رابط عمولة، لا يكلّفك شيئاً إضافياً):\n${winner.link}` +
    `\n\n🔎 قارن المزيد من ${NAMES.ar[niche] || ''}:\n${SITE}/ar/deals/#${niche}` +
    `\n\n#DoniaNova #مقارنة_اليوم`;
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
