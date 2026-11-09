// DoniaNova — live deals endpoint: /api/products?niche=ssd&lang=ar
const ali = require('./_ali.js');

const NICHES = {
  // audio & phone
  audio:     'wireless earbuds ENC microphone',
  phone:     'magnetic phone holder stand',
  charger:   'GaN fast charger USB C 65W',
  powerbank: 'power bank 20000mAh fast charging',
  cable:     'USB C cable 100W fast charging',
  watch:     'smart watch bluetooth call',
  // storage & computer
  ssd:       'portable SSD external USB C',
  hdd:       'external hard drive portable 1TB',
  flash:     'USB flash drive 128GB metal',
  class:     'usb c hub HDMI',
  keyboard:  'foldable bluetooth keyboard',
  // business & security
  barcode:   'wireless barcode scanner 2D',
  rfid:      'RFID blocking card',
  tracker:   'bluetooth tracker tag',
  car:       'OBD2 scanner',
  // teaching
  board:     'LCD writing tablet',
  presenter: 'wireless presenter laser pointer',
  webcam:    'webcam 1080p microphone',
  mic:       'wireless lavalier microphone',
  projector: 'mini projector portable',
  // travel
  travel:    'universal travel adapter',
  luggage:   'digital luggage scale',
  organizer: 'electronics organizer travel bag'
};

module.exports = async (req, res) => {
  if (!process.env.ALIEXPRESS_APP_KEY || !process.env.ALIEXPRESS_APP_SECRET) {
    return res.status(500).json({ error: 'missing_config' });
  }
  const q = req.query || {};
  const niche = NICHES[q.niche] ? q.niche : 'audio';
  const lang = q.lang === 'ar' ? 'ar' : 'en';
  const trace = q.debug ? [] : null;
  try {
    const items = (await ali.search(NICHES[niche], { lang, size: 30, trace })).slice(0, 16);
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
    return res.status(200).json({ niche, lang, updated: new Date().toISOString(), items, mode: ali.mode(), trace: trace || undefined });
  } catch (e) {
    return res.status(502).json({ error: e.message === 'upstream' ? 'upstream' : 'fetch_failed', detail: e.detail, trace: trace || undefined });
  }
};
module.exports.NICHES = NICHES;
