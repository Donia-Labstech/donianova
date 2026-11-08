// DoniaNova — AliExpress Affiliates API proxy (runs on Vercel, keeps the secret server-side)
const crypto = require('crypto');

const NICHES = {
  audio:  'wireless earbuds ENC microphone',
  rfid:   'RFID blocking card',
  class:  'usb c hub HDMI',
  board:  'LCD writing tablet',
  travel: 'universal travel adapter',
  tracker:'bluetooth tracker tag',
  car:    'OBD2 scanner'
};

function concat(params) {
  return Object.keys(params).sort().map(k => k + params[k]).join('');
}

function gmt8() {
  const d = new Date(Date.now() + 8 * 3600 * 1000);
  return d.toISOString().replace('T', ' ').slice(0, 19);
}

// Two signing styles AliExpress accepts on /sync: IOP (HMAC-SHA256) and TOP (MD5)
const MODES = {
  sha256: (base, secret) => {
    const p = Object.assign({ sign_method: 'sha256', timestamp: String(Date.now()) }, base);
    p.sign = crypto.createHmac('sha256', secret).update(concat(p), 'utf8').digest('hex').toUpperCase();
    return p;
  },
  md5: (base, secret) => {
    const p = Object.assign({ sign_method: 'md5', timestamp: gmt8(), v: '2.0', format: 'json' }, base);
    p.sign = crypto.createHash('md5').update(secret + concat(p) + secret, 'utf8').digest('hex').toUpperCase();
    return p;
  }
};
let goodMode = null;

async function callMode(mode, method, extra) {
  const key = (process.env.ALIEXPRESS_APP_KEY || '').trim();
  const secret = (process.env.ALIEXPRESS_APP_SECRET || '').trim();
  const params = MODES[mode](Object.assign({ app_key: key, method }, extra), secret);
  const r = await fetch('https://api-sg.aliexpress.com/sync', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
    body: new URLSearchParams(params).toString()
  });
  return r.json();
}

async function call(method, extra, trace) {
  const order = goodMode ? [goodMode] : ['sha256', 'md5'];
  let last;
  for (const m of order) {
    const j = await callMode(m, method, extra);
    const er = j && j.error_response;
    if (trace) trace.push({ mode: m, code: er ? er.code : 'ok' });
    if (!er || !/Signature/i.test(er.code || '')) { if (!er) goodMode = m; return j; }
    last = j;
  }
  return last;
}

module.exports = async (req, res) => {
  if (!process.env.ALIEXPRESS_APP_KEY || !process.env.ALIEXPRESS_APP_SECRET) {
    return res.status(500).json({ error: 'missing_config' });
  }
  const q = req.query || {};
  const niche = NICHES[q.niche] ? q.niche : 'audio';
  const lang = q.lang === 'ar' ? 'AR' : 'EN';
  const extra = {
    keywords: NICHES[niche],
    page_no: '1',
    page_size: '20',
    sort: 'LAST_VOLUME_DESC',
    target_currency: 'USD',
    target_language: lang,
    tracking_id: process.env.ALIEXPRESS_TRACKING_ID || 'default'
  };
  try {
    const trace = q.debug ? [] : null;
    const j = await call('aliexpress.affiliate.product.query', extra, trace);
    const rr = j && j.aliexpress_affiliate_product_query_response && j.aliexpress_affiliate_product_query_response.resp_result;
    if (!rr || Number(rr.resp_code) !== 200) {
      const err = (j && j.error_response) ? { code: j.error_response.code, msg: j.error_response.msg } : { code: rr && rr.resp_code, msg: rr && rr.resp_msg };
      return res.status(502).json({ error: 'upstream', detail: err, trace: trace || undefined });
    }
    const list = (rr.result && rr.result.products && rr.result.products.product) || [];
    const items = list
      .filter(p => p.promotion_link && p.product_main_image_url)
      .slice(0, 12)
      .map(p => ({
        id: String(p.product_id),
        title: p.product_title,
        img: p.product_main_image_url,
        price: p.target_sale_price,
        orig: p.target_original_price,
        discount: p.discount,
        rating: p.evaluate_rate,
        sold: p.lastest_volume,
        link: p.promotion_link
      }));
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
    return res.status(200).json({ niche, lang, updated: new Date().toISOString(), items, mode: goodMode, trace: trace || undefined });
  } catch (e) {
    return res.status(502).json({ error: 'fetch_failed' });
  }
};
