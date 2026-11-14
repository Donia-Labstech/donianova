// IndexNow: tells Bing/Yandex (and others) about all site URLs from the sitemap.
// GET /api/indexnow/  — safe to call: it only submits this site's own sitemap URLs.
const SITE = 'https://donianova.vercel.app';
const KEY = '07e3501e65c71e840d502e17e898367a';
module.exports = async (req, res) => {
  try {
    const xml = await (await fetch(SITE + '/sitemap.xml')).text();
    const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);
    const r = await fetch('https://api.indexnow.org/indexnow', {
      method: 'POST', headers: { 'Content-Type': 'application/json; charset=utf-8' },
      body: JSON.stringify({ host: 'donianova.vercel.app', key: KEY, keyLocation: SITE + '/' + KEY + '.txt', urlList: urls })
    });
    res.setHeader('Cache-Control', 'no-store');
    res.status(200).json({ submitted: urls.length, indexnow_status: r.status });
  } catch (e) { res.status(500).json({ error: String(e.message || e) }); }
};
