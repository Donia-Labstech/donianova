// Image search: identify the product in a photo and return search keywords.
// Uses Google Gemini (vision) when GEMINI_API_KEY is set; otherwise answers 503 and the
// browser falls back to on-device recognition. The photo is never stored.
const MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') return res.status(405).json({ error: 'method' });
  const key = process.env.GEMINI_API_KEY;
  if (!key) return res.status(503).json({ error: 'no_vision' });
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch (e) { body = {}; } }
  body = body || {};
  const lang = ['ar', 'en', 'fr'].includes(body.lang) ? body.lang : 'ar';
  const m = String(body.img || '').match(/^data:(image\/(?:jpeg|png|webp));base64,([A-Za-z0-9+/=]+)$/);
  if (!m || m[2].length > 1400000) return res.status(400).json({ error: 'bad_image' });

  const prompt = [
    'You help shoppers find a product on AliExpress from a photo.',
    'Identify the main product in the photo (type, key feature, brand only if clearly visible).',
    'Return JSON only: {"ok":true,"q":"<2-6 English AliExpress search keywords>","name":"<short product name in ' +
      ({ ar: 'Arabic', en: 'English', fr: 'French' })[lang] + '>","alts":[{"q":"...","name":"..."}, {"q":"...","name":"..."}]}',
    'alts = two other plausible matches (more generic or a close variant).',
    'If there is no recognisable product (person, landscape, document, unsafe content), return {"ok":false}.',
    'Never identify people. Never suggest weapons, drugs, spy or covert-surveillance devices.'
  ].join('\n');

  try {
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${encodeURIComponent(key)}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: prompt }, { inline_data: { mime_type: m[1], data: m[2] } }] }],
        generationConfig: { temperature: 0.2, maxOutputTokens: 300, responseMimeType: 'application/json' }
      })
    });
    const j = await r.json();
    const txt = (((j.candidates || [])[0] || {}).content || {}).parts ? j.candidates[0].content.parts.map(p => p.text || '').join('') : '';
    const out = JSON.parse((txt.match(/\{[\s\S]*\}/) || ['{}'])[0]);
    if (!out.ok || !out.q) return res.status(200).json({ ok: false });
    const clean = s => String(s || '').replace(/[<>]/g, '').slice(0, 80).trim();
    const BAN = /\bspy\b|hidden camera|covert|weapon|gun\b|knife|drug/i;
    const list = [{ q: clean(out.q), name: clean(out.name || out.q) }]
      .concat((out.alts || []).map(a => ({ q: clean(a.q), name: clean(a.name || a.q) })))
      .filter(x => x.q.length > 1 && !BAN.test(x.q)).slice(0, 3);
    if (!list.length) return res.status(200).json({ ok: false });
    return res.status(200).json({ ok: true, items: list });
  } catch (e) {
    return res.status(502).json({ error: 'upstream' });
  }
};
