// DoniaNova shopping assistant — DeepSeek (OpenAI-compatible). Key stays on the server.
const CATALOG = require('./_catalog.js');

const hits = new Map(); // best-effort per-IP rate limit (per warm instance)
function limited(ip) {
  const now = Date.now(), w = 10 * 60 * 1000, max = 20;
  const arr = (hits.get(ip) || []).filter(t => now - t < w);
  arr.push(now); hits.set(ip, arr);
  return arr.length > max;
}

function system(lang) {
  const list = CATALOG.map(p => `- ${p[lang].name} | ${lang === 'ar' ? 'الأنسب لـ' : 'best for'}: ${p[lang].best} | ${lang === 'ar' ? 'ملاحظات' : 'notes'}: ${p[lang].why} | page: /${lang}/p/${p.slug}/`).join('\n');
  return [
    lang === 'ar'
      ? 'أنت «نوفا»، المساعد الذكي لموقع DoniaNova الذي يوصي بأجهزة تقنية من علي إكسبريس. أجب بالعربية الفصحى المبسّطة دائماً، إلا إذا كتب الزائر بلغة أخرى فأجب بلغته.'
      : 'You are "Nova", the shopping assistant of DoniaNova, a site that recommends tech gear from AliExpress. Reply in English unless the visitor writes in another language.',
    'Rules:',
    '1. Recommend only products from the catalog below. Link each one with its page path exactly as given (e.g. /ar/p/slug/). Recommend at most 3.',
    '2. If nothing in the catalog fits, say so honestly and suggest the live deals page: /' + lang + '/deals/',
    '3. Be honest: mention the main limitation from the notes. Never invent specs, prices, discounts, stock or shipping times. Prices change; say the final price is on AliExpress.',
    '4. Keep answers short: 2 to 6 sentences or a short list. No markdown tables.',
    '5. Stay on topic (choosing tech products, using them, the site). Politely decline anything else in one sentence.',
    '6. If asked, say links are affiliate links that cost the buyer nothing extra.',
    'Catalog:',
    list
  ].join('\n');
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ error: 'method' });
  const key = (process.env.DEEPSEEK_API_KEY || '').trim();
  if (!key) return res.status(500).json({ error: 'missing_config' });
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0] || 'x';
  if (limited(ip)) return res.status(429).json({ error: 'rate' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  const lang = body && body.lang === 'en' ? 'en' : 'ar';
  const msgs = Array.isArray(body && body.messages) ? body.messages : [];
  const clean = msgs.slice(-8)
    .filter(m => m && (m.role === 'user' || m.role === 'assistant') && typeof m.content === 'string')
    .map(m => ({ role: m.role, content: m.content.slice(0, 600) }));
  if (!clean.length || clean[clean.length - 1].role !== 'user') return res.status(400).json({ error: 'empty' });

  try {
    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key },
      body: JSON.stringify({
        model: process.env.DEEPSEEK_MODEL || 'deepseek-chat',
        messages: [{ role: 'system', content: system(lang) }].concat(clean),
        max_tokens: 450,
        temperature: 0.4
      })
    });
    const j = await r.json();
    if (!r.ok) return res.status(502).json({ error: 'upstream', code: j && j.error && (j.error.code || j.error.type) });
    const text = j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content;
    return res.status(200).json({ reply: (text || '').trim() });
  } catch (e) {
    return res.status(502).json({ error: 'fetch_failed' });
  }
};
