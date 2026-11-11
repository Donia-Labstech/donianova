// DoniaNova shopping assistant — DeepSeek (OpenAI-compatible). Key stays on the server.
const CATALOG = require('./_catalog.js');
const ali = require('./_ali.js');

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
    '1. First check the reviewed catalog below. Link catalog products with their page path exactly as given (e.g. /' + lang + '/p/slug/).',
    '2. For any tech, phone-accessory, storage, teaching or travel product NOT in the catalog (barcode scanners, SSDs, hard drives, memory cards, chargers, power banks, webcams, projectors/data show, portable monitors, voice recorders, gimbals, AI translators, translation pens, label/receipt printers, etc.), or when the visitor asks to COMPARE products, call the tool search_aliexpress with short English keywords. Use only the returned data. Ignore results that are accessories or a different product than requested (e.g. an SSD enclosure when the visitor wants an SSD); if needed search again with more precise keywords.',
    '3. Comparisons: compare 2 to 4 products in a compact markdown table (columns: product, price, rating, sold) using only tool data, then 2-3 lines on who each one suits, then a clear honest verdict. After the table, give each product link on its own line as: 🛒 short name: link',
    '4. Never invent specs, prices, ratings, stock or shipping times. If a value is missing write "—". Say prices are live from AliExpress and may change.',
    'Never recommend spy, hidden or covert recording/surveillance devices; politely refuse such requests.',
    '5. Keep answers concise. Stay on topic (choosing tech/teaching/travel products, using them, the site). Politely decline anything else in one sentence.',
    '6. If asked, say links are affiliate links that cost the buyer nothing extra.',
    '7. If nothing fits, say so honestly and suggest the live deals page: /' + lang + '/deals/',
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

  const TOOLS = [{
    type: 'function',
    function: {
      name: 'search_aliexpress',
      description: 'Search live AliExpress products (price in USD, rating %, units sold, affiliate link). Use for products not in the catalog and for comparisons.',
      parameters: { type: 'object', properties: {
        keywords: { type: 'string', description: 'Short English product keywords, e.g. "portable SSD 1TB USB C"' }
      }, required: ['keywords'] }
    }
  }];

  async function ds(messages, withTools) {
    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key },
      body: JSON.stringify(Object.assign({
        model: process.env.DEEPSEEK_MODEL || 'deepseek-chat',
        messages, max_tokens: 900, temperature: 0.3
      }, withTools ? { tools: TOOLS } : {}))
    });
    const j = await r.json();
    if (!r.ok) { const e = new Error('upstream'); e.code = j && j.error && (j.error.code || j.error.type); throw e; }
    return j.choices && j.choices[0] && j.choices[0].message;
  }

  async function runTool(call) {
    let args = {};
    try { args = JSON.parse(call.function.arguments || '{}'); } catch (e) {}
    const kw = String(args.keywords || '').replace(/[^\w\s\-+.]/g, ' ').trim().slice(0, 60);
    if (!kw || !process.env.ALIEXPRESS_APP_KEY) return { error: 'unavailable' };
    try {
      const items = (await ali.search(kw, { lang, size: 20 })).slice(0, 6);
      return { keywords: kw, items: items.map(p => ({ title: p.title.slice(0, 110), price_usd: p.price, original_usd: p.orig, discount: p.discount, rating: p.rating, sold: p.sold, link: p.link })) };
    } catch (e) { return { error: 'search_failed' }; }
  }

  try {
    const convo = [{ role: 'system', content: system(lang) }].concat(clean);
    let msg = await ds(convo, true);
    for (let round = 0; round < 2 && msg && msg.tool_calls && msg.tool_calls.length; round++) {
      convo.push({ role: 'assistant', content: msg.content || '', tool_calls: msg.tool_calls });
      const calls = msg.tool_calls.slice(0, 3);
      const results = await Promise.all(calls.map(runTool));
      calls.forEach((c, i) => convo.push({ role: 'tool', tool_call_id: c.id, content: JSON.stringify(results[i]) }));
      msg = await ds(convo, round === 0);
    }
    const text = msg && msg.content;
    return res.status(200).json({ reply: (text || '').trim() });
  } catch (e) {
    return res.status(502).json({ error: e.message === 'upstream' ? 'upstream' : 'fetch_failed', code: e.code });
  }
};
