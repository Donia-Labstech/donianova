// RSS feed with today's comparison, for Zapier "RSS by Zapier -> Facebook Pages".
// One item per day (guid = date + category), cached at the edge until the next UTC midnight,
// so DeepSeek is called about once a day.
const daily = require('./daily.js');
const SITE = 'https://donianova.vercel.app';

module.exports = async (req, res) => {
  const now = new Date();
  const day = now.toISOString().slice(0, 10);
  const secsLeft = Math.max(300, Math.floor((Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1) - now) / 1000));
  let item = '';
  try {
    const t = await daily.buildToday();
    if (!t.skipped) {
      const title = (t.post.split('\n')[0] || 'مقارنة اليوم').replace(/[#*]/g, '').trim();
      item = `<item><title>${daily.esc(title)}</title><link>${daily.esc(t.winner.link)}</link>` +
        `<guid isPermaLink="false">donianova-${day}-${t.niche}</guid><pubDate>${now.toUTCString()}</pubDate>` +
        `<description>${daily.esc(t.message)}</description>` +
        (t.winner.img ? `<enclosure url="${daily.esc(t.winner.img)}" type="image/jpeg" length="0"/>` : '') +
        `</item>`;
    }
  } catch (e) { /* empty feed on failure: Zapier simply posts nothing that day */ }
  res.setHeader('Content-Type', 'application/rss+xml; charset=utf-8');
  res.setHeader('Cache-Control', item ? `s-maxage=${secsLeft}` : 's-maxage=300');
  res.status(200).send(`<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>DoniaNova · مقارنة اليوم</title><link>${SITE}/ar/deals/</link>
<description>مقارنة يومية صادقة لمنتجات التقنية من علي إكسبريس</description><language>ar</language>${item}</channel></rss>`);
};
