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

function sign(params, secret) {
  const base = Object.keys(params).sort().map(k => k + params[k]).join('');
  return crypto.createHmac('sha256', secret).update(base, 'utf8').digest('hex').toUpperCase();
}

async function call(method, extra) {
  const key = process.env.ALIEXPRESS_APP_KEY, secret = process.env.ALIEXPRESS_APP_SECRET;
  const params = Object.assign({ app_key: key, method, sign_method: 'sha256', timestamp: String(Date.now()) }, extra);
  params.sign = sign(params, secret);
  const r = await fetch('https://api-sg.aliexpress.com/sync', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8' },
    body: new URLSearchParams(params).toString()
  });
  return r.json();
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
    const j = await call('aliexpress.affiliate.product.query', extra);
    const rr = j && j.aliexpress_affiliate_product_query_response && j.aliexpress_affiliate_product_query_response.resp_result;
    if (!rr || Number(rr.resp_code) !== 200) {
      const err = (j && j.error_response) ? { code: j.error_response.code, msg: j.error_response.msg } : { code: rr && rr.resp_code, msg: rr && rr.resp_msg };
      return res.status(502).json({ error: 'upstream', detail: err });
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
    return res.status(200).json({ niche, lang, updated: new Date().toISOString(), items });
  } catch (e) {
    return res.status(502).json({ error: 'fetch_failed' });
  }
};
