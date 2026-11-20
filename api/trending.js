// 🔥 Most wanted right now: best sellers across the hottest sections, rated 85%+.
// One response per language, cached at the edge for an hour (stale-while-revalidate),
// so AliExpress is called about once an hour per language.
const products = require('./products.js');

const TREND = ['smartring', 'dashcam', 'seccam', 'ledstrip', 'carvac', 'gamepad', 'massager', 'trimmer',
  'audio', 'watch', 'powerbank', 'headphone', 'wcharge', 'projector', 'btspeaker', 'neckfan'];

function score(p) {
  const r = parseFloat(p.rating) || 88, s = Number(p.sold) || 0;
  return Math.log10(s + 10) * r;
}

module.exports = async (req, res) => {
  const q = req.query || {};
  const lang = ['ar', 'en', 'fr'].includes(q.lang) ? q.lang : 'ar';
  try {
    const lists = await Promise.all(TREND.map(n => products.nicheItems(n, lang).then(items => ({ n, items })).catch(() => ({ n, items: [] }))));
    const seen = new Set(), out = [];
    for (const { n, items } of lists) {
      items.filter(p => p.link && p.img && (Number(p.sold) || 0) >= 50)
        .sort((a, b) => score(b) - score(a)).slice(0, 2)
        .forEach(p => { if (!seen.has(p.id)) { seen.add(p.id); out.push(Object.assign({ niche: n }, p)); } });
    }
    out.sort((a, b) => (Number(b.sold) || 0) - (Number(a.sold) || 0));
    if (!out.length) throw new Error('empty');
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
    return res.status(200).json({ lang, updated: new Date().toISOString(), items: out.slice(0, 16) });
  } catch (e) {
    res.setHeader('Cache-Control', 'no-store');
    return res.status(502).json({ error: 'unavailable' });
  }
};
