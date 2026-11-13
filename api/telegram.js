// DoniaNova Telegram bot (webhook).
// Env: TELEGRAM_BOT_TOKEN (from @BotFather), CRON_SECRET (already set), optional TELEGRAM_CHANNEL (e.g. @donianova_deals)
// One-time setup: open /api/telegram?setup=1&key=CRON_SECRET
const crypto = require('crypto');
const products = require('./products.js');
const ali = require('./_ali.js');
const NAMES = require('./_names.js');
const SITE = 'https://donianova.vercel.app';
const TG = m => `https://api.telegram.org/bot${process.env.TELEGRAM_BOT_TOKEN}/${m}`;
const hookSecret = () => crypto.createHash('sha256').update('tg:' + (process.env.CRON_SECRET || '')).digest('hex').slice(0, 48);

async function api(method, body) {
  const r = await fetch(TG(method), { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  return r.json();
}
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Featured sections shown as buttons
const MENU = ['barcode', 'ssd', 'projector', 'translator', 'powerbank', 'audio', 'board', 'monitor', 'charger', 'actioncam', 'microsd', 'travel'];
function menuKeyboard() {
  const rows = [];
  for (let i = 0; i < MENU.length; i += 2) rows.push(MENU.slice(i, i + 2).map(k => ({ text: NAMES.ar[k] || k, callback_data: 'cat:' + k })));
  rows.unshift([{ text: '🏆 مقارنة اليوم', callback_data: 'today' }]);
  rows.push([{ text: '🌐 كل الأقسام في الموقع', url: SITE + '/ar/deals/' }]);
  rows.push([{ text: '📢 قناة العروض اليومية', url: 'https://t.me/donianova_deals' }]);
  return { inline_keyboard: rows };
}

function caption(p) {
  const price = Number(p.price) || 0, orig = Number(p.orig) || price;
  const off = orig > price ? Math.round((1 - price / orig) * 100) : 0;
  const trusted = off > 0 && off < 60;
  const lines = [`<b>${esc(p.title.slice(0, 120))}</b>`, '',
    `💰 <b>$${price}</b>` + (trusted ? `  <s>$${orig}</s>  (‑${off}%)` : ''),
    (p.rating ? `⭐ ${esc(p.rating)}` : '⭐ جديد') + (p.sold ? `   🛒 ${p.sold} مبيع` : '')];
  return lines.join('\n');
}

async function sendProducts(chat, items, title) {
  const top = items.slice(0, 4);
  if (!top.length) return api('sendMessage', { chat_id: chat, text: 'لم أجد نتائج مناسبة 😕 جرّب كلمة أبسط، أو اختر قسماً:', reply_markup: menuKeyboard() });
  await api('sendMessage', { chat_id: chat, text: title, parse_mode: 'HTML' });
  const links = await Promise.all(top.map(p => ali.shortLink(p.id)));
  for (let i = 0; i < top.length; i++) {
    const p = top[i], link = links[i] || SITE + '/ar/deals/';
    await api('sendPhoto', { chat_id: chat, photo: p.img, caption: caption(p), parse_mode: 'HTML',
      reply_markup: { inline_keyboard: [[{ text: '🛒 اطلبه الآن', url: link }]] } });
  }
  return api('sendMessage', { chat_id: chat, text: '🔎 ابحث عن منتج آخر بكتابة اسمه، أو اختر قسماً:', reply_markup: menuKeyboard() });
}

async function sendToday(chat) {
  const r = await fetch(SITE + '/api/today'); const t = await r.json();
  if (t.error) return api('sendMessage', { chat_id: chat, text: 'مقارنة اليوم قيد التحضير، حاول بعد قليل 🙏' });
  return api('sendPhoto', { chat_id: chat, photo: t.winner.img, caption: esc(t.post).slice(0, 1000), parse_mode: 'HTML',
    reply_markup: { inline_keyboard: [[{ text: '🛒 اطلب اختيار اليوم', url: t.winner.link }], [{ text: '🔎 قارن القسم كاملاً', url: `${SITE}/ar/deals/#${t.niche}` }]] } });
}

const WELCOME = '👋 أهلاً بك في <b>DoniaNova</b>\n\nأساعدك تختار أجهزة التقنية والتعليم والسفر من علي إكسبريس <b>بأرقام حقيقية</b>: السعر، التقييم، والمبيعات.\n\n✍️ اكتب اسم أي منتج (مثلاً: <i>قارئ باركود</i> أو <i>SSD 1TB</i>)\n👇 أو اختر قسماً:';

// Point Telegram to this endpoint (idempotent; it can only ever point to our own URL).
async function ensureWebhook() {
  const info = await api('getWebhookInfo', {});
  if (info.result && info.result.url === SITE + '/api/telegram/') return info;
  await api('setMyCommands', { commands: [
    { command: 'start', description: 'البداية والأقسام' }, { command: 'today', description: 'مقارنة اليوم' }, { command: 'deals', description: 'تصفّح الأقسام' }] });
  return api('setWebhook', { url: SITE + '/api/telegram/', secret_token: hookSecret(), allowed_updates: ['message', 'callback_query'] });
}

module.exports = async (req, res) => {
  const q = req.query || {};
  const key = process.env.CRON_SECRET;
  // public link used by the site: redirect to the bot's t.me page
  if (q.go) {
    let to = SITE + '/ar/';
    try {
      if (process.env.TELEGRAM_BOT_TOKEN) {
        const me = await api('getMe', {}); if (me.result && me.result.username) to = 'https://t.me/' + me.result.username;
        await ensureWebhook();   // self-setup: no secret link needed
      }
    } catch (e) {}
    res.setHeader('Cache-Control', 'no-store');
    res.setHeader('Location', to);
    return res.status(302).end();
  }
  if (!process.env.TELEGRAM_BOT_TOKEN) return res.status(500).json({ error: 'missing TELEGRAM_BOT_TOKEN' });

  // one-time webhook setup
  if (q.setup) {
    if (!key || q.key !== key) return res.status(401).json({ error: 'unauthorized' });
    const a = await api('setWebhook', { url: SITE + '/api/telegram/', secret_token: hookSecret(), allowed_updates: ['message', 'callback_query'] });
    const b = await api('setMyCommands', { commands: [
      { command: 'start', description: 'البداية والأقسام' }, { command: 'today', description: 'مقارنة اليوم' }, { command: 'deals', description: 'تصفّح الأقسام' }] });
    const me = await api('getMe', {});
    return res.status(200).json({ webhook: a, commands: b, bot: me.result && me.result.username });
  }

  // daily post to a channel (Vercel Cron)
  if (q.daily) {
    if (!key || (req.headers.authorization !== 'Bearer ' + key && q.key !== key)) return res.status(401).json({ error: 'unauthorized' });
    if (!process.env.TELEGRAM_CHANNEL) return res.status(200).json({ skipped: 'no channel' });
    return res.status(200).json(await sendToday(process.env.TELEGRAM_CHANNEL));
  }

  // webhook updates from Telegram
  if (req.headers['x-telegram-bot-api-secret-token'] !== hookSecret()) return res.status(401).end();
  const u = req.body || {};
  try {
    if (u.callback_query) {
      const cq = u.callback_query, chat = cq.message.chat.id, data = cq.data || '';
      await api('answerCallbackQuery', { callback_query_id: cq.id });
      if (data === 'today') await sendToday(chat);
      else if (data.startsWith('cat:') && products.NICHES[data.slice(4)]) {
        const n = data.slice(4);
        await sendProducts(chat, await products.nicheItems(n, 'ar'), `🔥 أفضل عروض <b>${esc(NAMES.ar[n] || n)}</b> الآن:`);
      }
    } else if (u.message && u.message.text) {
      const chat = u.message.chat.id, text = u.message.text.trim();
      if (/^\/start|^\/deals/.test(text)) await api('sendMessage', { chat_id: chat, text: WELCOME, parse_mode: 'HTML', reply_markup: menuKeyboard() });
      else if (/^\/today/.test(text)) await sendToday(chat);
      else if (text.length >= 2 && text.length <= 80) {
        await api('sendChatAction', { chat_id: chat, action: 'typing' });
        const { items } = await products.searchText(text, 'ar');
        await sendProducts(chat, items, `🔎 نتائج «${esc(text)}» — الأكثر مبيعاً والأعلى تقييماً:`);
      }
    }
  } catch (e) { /* never make Telegram retry forever */ }
  return res.status(200).json({ ok: true });
};
