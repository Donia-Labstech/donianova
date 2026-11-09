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
  ssd:       'external portable SSD 1TB solid state drive',
  hdd:       'external hard drive 1TB USB 3.0 portable HDD',
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

// Per-niche guards: drop accessories that match the keywords but are not the product itself
const ACCESSORY = /enclosure|case|adapter|caddy|حافظة|علبة|الضميمة|محول|صندوق|غلاف|حاوية/i;
const RULES = {
  ssd:      { min: 20, drop: ACCESSORY },
  hdd:      { min: 20, drop: ACCESSORY },
  flash:    { min: 3 },
  barcode:  { min: 8 },
  watch:    { min: 8, drop: /strap|band|protector|سوار|حزام|واقي/i },
  projector:{ min: 25, drop: /screen|bracket|mount|شاشة عرض|حامل/i },
  webcam:   { min: 6, drop: /cover|غطاء/i },
  keyboard: { min: 6 },
  powerbank:{ min: 6, drop: ACCESSORY },
  board:    { min: 3 }
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
    const rule = RULES[niche] || {};
    const items = (await ali.search(NICHES[niche], { lang, size: 50, trace }))
      .filter(p => !(rule.min && Number(p.price) < rule.min))
      .filter(p => !(rule.drop && rule.drop.test(p.title)))
      .slice(0, 16);
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
    return res.status(200).json({ niche, lang, updated: new Date().toISOString(), items, mode: ali.mode(), trace: trace || undefined });
  } catch (e) {
    return res.status(502).json({ error: e.message === 'upstream' ? 'upstream' : 'fetch_failed', detail: e.detail, trace: trace || undefined });
  }
};
module.exports.NICHES = NICHES;
