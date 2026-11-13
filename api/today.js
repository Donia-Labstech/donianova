// Today's comparison as JSON (for the home page and the Telegram bot).
// Cached at the edge until the next UTC midnight -> one DeepSeek call per day.
const daily = require('./daily.js');
module.exports = async (req, res) => {
  const now = new Date();
  const secsLeft = Math.max(300, Math.floor((Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate() + 1) - now) / 1000));
  try {
    const t = await daily.buildToday();
    if (t.skipped) throw new Error('skipped');
    res.setHeader('Cache-Control', `s-maxage=${secsLeft}`);
    return res.status(200).json({
      day: now.toISOString().slice(0, 10), niche: t.niche, post: t.post, message: t.message,
      winner: { title: t.winner.title, img: t.winner.img, price: t.winner.price, rating: t.winner.rating, sold: t.winner.sold, link: t.winner.link },
      top: (t.top || []).map(p => ({ title: p.title, img: p.img, price: p.price, rating: p.rating, sold: p.sold }))
    });
  } catch (e) {
    res.setHeader('Cache-Control', 's-maxage=300');
    return res.status(502).json({ error: 'unavailable' });
  }
};
