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
  // recording & camera
  recorder:  'digital voice recorder',
  ringlight: 'ring light tripod phone',
  gimbal:    'phone gimbal stabilizer',
  actioncam: 'action camera 4K',
  // translation
  translator:'AI voice translator device',
  transbuds: 'translation earbuds AI translator',
  scanpen:   'translation scanning pen',
  // memory
  microsd:   'micro SD card 128GB',
  cardreader:'USB C SD card reader',
  // display (data show)
  projector: 'mini projector portable',
  projscreen:'portable projector screen',
  hdmiwifi:  'wireless HDMI display dongle',
  monitor:   'portable monitor 15.6 inch',
  doccam:    'document camera visualizer',
  // business printing
  labelprn:  'thermal label printer',
  receiptprn:'bluetooth thermal receipt printer',
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
  board:    { min: 3 },
  recorder: { min: 8, drop: /case|bag|حقيبة|غطاء/i },
  ringlight:{ min: 4 },
  gimbal:   { min: 12 },
  actioncam:{ min: 25, drop: /mount|case|strap|battery|حامل|بطارية|حزام/i },
  translator:{ min: 15, drop: /case|bag|protector|حقيبة|غطاء|واقي/i },
  transbuds:{ min: 8 },
  scanpen:  { min: 15, drop: /refill|case|غطاء/i },
  microsd:  { min: 2, drop: /reader|قارئ/i },
  cardreader:{ min: 2 },
  projscreen:{ min: 8 },
  hdmiwifi: { min: 8 },
  monitor:  { min: 40, drop: /stand|case|bag|حامل|حقيبة|غطاء/i },
  doccam:   { min: 20 },
  labelprn: { min: 18, drop: /paper|sticker|label roll|ribbon|ورق|ملصق|شريط/i },
  receiptprn:{ min: 18, drop: /paper|roll|ورق|لفة/i }
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
