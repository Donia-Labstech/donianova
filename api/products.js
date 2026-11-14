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
  organizer: 'electronics organizer travel bag',
  // wireless world
  qrscan:    'wireless QR code scanner bluetooth 2D handheld',
  ringscan:  'wearable ring barcode scanner bluetooth',
  wmouse:    'wireless mouse rechargeable silent bluetooth',
  wcombo:    'wireless keyboard mouse combo',
  wcharge:   '3 in 1 magnetic wireless charger stand',
  btspeaker: 'portable bluetooth speaker waterproof',
  headphone: 'wireless bluetooth headphones noise cancelling over ear',
  btreceiver:'bluetooth 5.3 audio receiver transmitter',
  carplay:   'wireless carplay android auto adapter',
  wifi:      'USB WiFi adapter dual band 5GHz',
  extender:  'WiFi range extender repeater'
};

// Never list spy / covert-surveillance gear (illegal in many countries, against our values)
const BANNED = /\bspy\b|hidden (camera|recorder)|covert|eavesdrop|wiretap|bug detector|تجسس|الجاسوس|جاسوس|تنصت|مخفي|خفية/i;

// Per-niche guards: drop accessories that match the keywords but are not the product itself
const ACCESSORY = /enclosure|case|adapter|caddy|حافظة|علبة|الضميمة|محول|صندوق|غلاف|حاوية/i;
const WIRED = /\bwired\b|(?<!لا)سلكي/i;
const RULES = {
  qrscan:   { min: 12, keep: /scanner|reader|ماسح|قارئ/i, drop: /\bwired\b|stand only|holder only|cradle only/i },
  ringscan: { min: 15, keep: /ring|finger|wearable|خاتم|إصبع|اصبع/i },
  wmouse:   { min: 4, drop: /pad\b|mat\b|mouse ?pad|\bwired\b|لوحة ماوس|(?<!لا)سلكي/i },
  wcombo:   { min: 10, drop: WIRED },
  wcharge:  { min: 8, keep: /wireless|magnetic|magsafe|qi|لاسلكي|مغناطيس/i, drop: /case|cable only|غطاء|حافظة/i },
  btspeaker:{ min: 8, drop: /case|bag|cable|حقيبة|غطاء/i },
  headphone:{ min: 10, drop: /ear ?pads?|cushion|case|stand|وسادة|حامل|غطاء/i },
  btreceiver:{ min: 3 },
  carplay:  { min: 15, drop: /cable only|holder|حامل/i },
  wifi:     { min: 3, keep: /wi-?fi|wireless|لاسلكي|واي ?فاي/i },
  extender: { min: 6, keep: /extender|repeater|booster|موسع|مكرر|مقوي/i },
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
  gimbal:   { min: 12, keep: /gimbal|stabili[sz]er|osmo|مثبت|جيمبال/i },
  actioncam:{ min: 25, drop: /mount|case|strap|battery|memory card|micro ?sd|tf card|sd card|حامل|بطارية|حزام|بطاقة ذاكرة|مايكرو/i, keep: /camera|cam\b|كاميرا|osmo|gopro|insta360/i },
  translator:{ min: 15, drop: /case|bag|protector|حقيبة|غطاء|واقي/i },
  transbuds:{ min: 8 },
  scanpen:  { min: 15, drop: /refill|case|غطاء/i },
  microsd:  { min: 5, drop: /reader|قارئ|\b(64|128|256|512) ?MB\b/i, keep: /sandisk|samsung|kingston|lexar|netac|kioxia|pny|team ?group|transcend|sandisk|سانديسك|سامسونج|كينغستون|ليكسار|نيتاك/i },
  cardreader:{ min: 2 },
  projscreen:{ min: 8 },
  hdmiwifi: { min: 8 },
  monitor:  { min: 40, drop: /stand|case|bag|حامل|حقيبة|غطاء/i },
  doccam:   { min: 20 },
  labelprn: { min: 18, drop: /paper|sticker|label roll|ribbon|ورق|ملصق|شريط/i },
  receiptprn:{ min: 18, drop: /paper|roll|ورق|لفة/i }
};

// Free-text search: Arabic (or mixed) queries are turned into short English keywords,
// because AliExpress matches English titles far better.
async function toKeywords(q) {
  if (!/[\u0600-\u06FF]/.test(q) || !process.env.DEEPSEEK_API_KEY) return q;
  try {
    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + process.env.DEEPSEEK_API_KEY },
      body: JSON.stringify({ model: 'deepseek-chat', temperature: 0, max_tokens: 20, messages: [
        { role: 'system', content: 'Convert the shopping query into 2-6 short English AliExpress search keywords for the product itself (not accessories). Reply with the keywords only.' },
        { role: 'user', content: q } ] })
    });
    const j = await r.json();
    const kw = (j.choices && j.choices[0] && j.choices[0].message.content || '').replace(/[^\w\s\-+.]/g, ' ').replace(/\s+/g, ' ').trim();
    return kw || q;
  } catch (e) { return q; }
}

async function nicheItems(niche, lang, trace) {
  const rule = RULES[niche] || {};
  return (await ali.search(NICHES[niche], { lang, size: 50, trace }))
    .filter(p => !BANNED.test(p.title))
    .filter(p => !(rule.min && Number(p.price) < rule.min))
    .filter(p => !(rule.drop && rule.drop.test(p.title)))
    .filter(p => !(rule.keep && !rule.keep.test(p.title)))
    // quality guard: hide poorly rated listings (keeps new items that have no rating yet)
    .filter(p => { const r = parseFloat(p.rating); return !(r > 0 && r < 85); })
    .slice(0, 16);
}

module.exports = async (req, res) => {
  if (!process.env.ALIEXPRESS_APP_KEY || !process.env.ALIEXPRESS_APP_SECRET) {
    return res.status(500).json({ error: 'missing_config' });
  }
  const q = req.query || {};
  const text = String(q.q || '').replace(/[<>"'`]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 60);
  if (text.length >= 2) {
    const lang = q.lang === 'ar' ? 'ar' : 'en';
    try {
      const kw = await toKeywords(text);
      const items = (await ali.search(kw, { lang, size: 50 }))
        .filter(p => !BANNED.test(p.title))
        .filter(p => { const r = parseFloat(p.rating); return !(r > 0 && r < 85); })
        .slice(0, 24);
      res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
      return res.status(200).json({ q: text, kw, lang, updated: new Date().toISOString(), items });
    } catch (e) {
      return res.status(502).json({ error: e.message === 'upstream' ? 'upstream' : 'fetch_failed' });
    }
  }
  const niche = NICHES[q.niche] ? q.niche : 'audio';
  const lang = q.lang === 'ar' ? 'ar' : 'en';
  const trace = q.debug ? [] : null;
  try {
    const items = await nicheItems(niche, lang, trace);
    res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');
    return res.status(200).json({ niche, lang, updated: new Date().toISOString(), items, mode: ali.mode(), trace: trace || undefined });
  } catch (e) {
    return res.status(502).json({ error: e.message === 'upstream' ? 'upstream' : 'fetch_failed', detail: e.detail, trace: trace || undefined });
  }
};
module.exports.NICHES = NICHES;
module.exports.nicheItems = nicheItems;
module.exports.searchText = async (text, lang) => {
  const kw = await toKeywords(text);
  const items = (await ali.search(kw, { lang, size: 50 }))
    .filter(p => !BANNED.test(p.title))
    .filter(p => { const r = parseFloat(p.rating); return !(r > 0 && r < 85); });
  return { kw, items };
};
