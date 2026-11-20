# DoniaNova v10: most-wanted section, welcome promise, image/camera search.
# All visible strings are server-rendered HTML (Arabic or English), so the FR layer translates them.
from html import escape as e

def hot_section(lang):
    ar = lang == "ar"
    L = (lambda a, b: a if ar else b)
    return f"""<section id="hot" class="hot-s"><div class="wrap">
<div class="head"><div><span class="hot-pill">{e(L('يتحدّث كل ساعة','Updated hourly'))}</span>
<h2>{e(L('🔥 الأكثر طلباً الآن','🔥 Most wanted right now'))}</h2>
<p>{e(L('أكثر المنتجات مبيعاً في الأقسام الأكثر رواجاً، بتقييم 85% فأكثر فقط. هذا ما يشتريه الناس فعلاً.','The best sellers in the hottest sections, rated 85%+ only. This is what people actually buy.'))}</p></div>
<div class="filters hot-sort" id="hotSort" role="group" aria-label="{e(L('ترتيب','Sort'))}">
<button type="button" data-s="sold" aria-pressed="true">{e(L('🛒 الأكثر مبيعاً','🛒 Best sellers'))}</button>
<button type="button" data-s="rate" aria-pressed="false">{e(L('⭐ الأعلى تقييماً','⭐ Top rated'))}</button>
<button type="button" data-s="price" aria-pressed="false">{e(L('💰 الأقل سعراً','💰 Lowest price'))}</button></div></div>
<div class="grid" id="hotGrid">{''.join('<div class="skel"></div>' for _ in range(8))}</div>
<p class="hot-more"><a class="btn btn-gold" href="/{lang}/deals/#smartring">{e(L('🔥 كل الأقسام الرائجة','🔥 All trending sections'))} {"←" if ar else "→"}</a></p>
<template id="hotTpl"><article class="card deal glowcard hot-card"><span class="hot-rank"></span>
<div class="bds"><span class="bd bd-best" data-b="best">{e(L('⭐ الأكثر مبيعاً','⭐ Best seller'))}</span><span class="bd bd-top" data-b="top">{e(L('👍 الأعلى تقييماً','👍 Top rated'))}</span><span class="bd bd-hot" data-b="hot">{e(L('🔥 رائج','🔥 Trending'))}</span></div>
<a class="hl" target="_blank" rel="sponsored nofollow noopener"><img class="shot" alt="" loading="lazy" width="350" height="350"></a>
<h3></h3><div class="priceRow"><b></b><s></s></div>
<div class="meta"><span class="m-sold"></span> <span>{e(L('مبيع','sold'))}</span> · ★ <span class="m-rate"></span></div>
<div style="margin-top:auto"><a class="go buy" target="_blank" rel="sponsored nofollow noopener">{e(L('🛒 اشترِ الآن','🛒 Buy now'))}</a></div></article></template>
</div></section>"""

def promise_band(lang):
    ar = lang == "ar"
    P = [("⭐", "الأعلى تقييماً", "Top rated", "لا نعرض أي منتج تقييمه أقل من 85%", "Nothing rated under 85% makes the cut"),
         ("🛒", "الأكثر مبيعاً", "Best sellers", "ما اشتراه وجرّبه آلاف المشترين", "What thousands of buyers already bought and tried"),
         ("🔥", "الأكثر رواجاً", "Trending", "ما يطلبه الناس الآن، بأسعار تتحدث كل ساعة", "What people want now, prices refreshed hourly"),
         ("💯", "بصدق", "Honestly", "نذكر العيوب ولمن لا يناسب المنتج", "We name the downsides and who it does not suit")]
    cells = "".join(f'<div class="pr-c"><i aria-hidden="true">{ic}</i><b>{e(a if ar else b)}</b><span>{e(c if ar else d)}</span></div>' for ic, a, b, c, d in P)
    h = "نختار لك الأفضل، حتى لا تضيّع وقتك في المقارنة" if ar else "We pick the best, so you never waste time comparing"
    return f'<section class="pr-s"><div class="wrap"><div class="promise"><h2>{e(h)}</h2><div class="pr-g">{cells}</div></div></div></section>'

def overlays(lang):
    """Welcome sheet (first visit) + image search dialog, on every page."""
    ar = lang == "ar"
    L = (lambda a, b: a if ar else b)
    welcome = f"""<div class="ovl" id="welcome" hidden role="dialog" aria-modal="true" aria-labelledby="wl-h"><div class="ovl-card wc">
<button type="button" class="ovl-x" data-close aria-label="{e(L('إغلاق','Close'))}">×</button>
<div class="wc-star" aria-hidden="true">✦</div>
<h2 id="wl-h">{e(L('أهلاً بك في دنيا نوفا 👋','Welcome to DoniaNova 👋'))}</h2>
<p>{e(L('لا داعي لتضييع ساعات في المقارنة. من بين آلاف المنتجات نختار لك:','No need to spend hours comparing. Out of thousands of products we pick for you:'))}</p>
<ul class="wc-l">
<li><i aria-hidden="true">⭐</i><div><b>{e(L('الأعلى تقييماً','Top rated'))}</b><span>{e(L('لا نعرض أي منتج تقييمه أقل من 85%','Nothing rated under 85% makes the cut'))}</span></div></li>
<li><i aria-hidden="true">🛒</i><div><b>{e(L('الأكثر مبيعاً','Best sellers'))}</b><span>{e(L('ما اشتراه وجرّبه آلاف المشترين','What thousands of buyers already bought and tried'))}</span></div></li>
<li><i aria-hidden="true">🔥</i><div><b>{e(L('الأكثر رواجاً','Trending'))}</b><span>{e(L('ما يطلبه الناس الآن، بأسعار تتحدث كل ساعة','What people want now, prices refreshed hourly'))}</span></div></li>
<li><i aria-hidden="true">💯</i><div><b>{e(L('بصدق','Honestly'))}</b><span>{e(L('نذكر العيوب ولمن لا يناسب المنتج','We name the downsides and who it does not suit'))}</span></div></li></ul>
<div class="wc-b"><a class="btn btn-gold" href="/{lang}/#hot" data-close>{e(L('🔥 شاهد الأكثر طلباً','🔥 See the most wanted'))}</a><button type="button" class="btn btn-ghost" data-close>{e(L('ابدأ التصفح','Start browsing'))}</button></div>
<small class="wc-new">{e(L('💡 جديد: ابحث بصورة المنتج أو بالكاميرا 📷','💡 New: search with a product photo or your camera 📷'))}</small>
</div></div>"""
    imgs = f"""<div class="ovl" id="imgs" hidden role="dialog" aria-modal="true" aria-labelledby="imgs-h"><div class="ovl-card imgs-card">
<button type="button" class="ovl-x" data-close aria-label="{e(L('إغلاق','Close'))}">×</button>
<h2 id="imgs-h">{e(L('📷 ابحث بالصورة','📷 Search by photo'))}</h2>
<p>{e(L('صوّر المنتج أو ارفع صورته، وسنتعرّف عليه ونبحث لك عن أفضل العروض.','Take a photo of the product or upload one, and we will recognise it and find the best deals.'))}</p>
<div class="imgs-pick"><label class="btn btn-gold"><span>{e(L('📸 التقط صورة','📸 Take a photo'))}</span><input type="file" accept="image/*" capture="environment" id="imgs-cam" hidden></label>
<label class="btn btn-ghost"><span>{e(L('🖼️ اختر صورة','🖼️ Choose a photo'))}</span><input type="file" accept="image/*" id="imgs-file" hidden></label></div>
<div class="imgs-stage" id="imgs-stage" hidden><img id="imgs-prev" alt=""><p class="imgs-st" id="imgs-st" aria-live="polite"></p><div class="imgs-guess" id="imgs-guess"></div></div>
<form class="imgs-form" id="imgs-form"><input type="search" id="imgs-q" autocomplete="off" placeholder="{e(L('أو اكتب اسم المنتج…','Or type the product name…'))}" aria-label="{e(L('اسم المنتج','Product name'))}"><button type="submit" class="btn btn-gold">{e(L('ابحث','Search'))}</button></form>
<small class="imgs-note">{e(L('🔒 لا نحفظ صورتك: تُستعمل فقط للتعرّف على المنتج ثم تُحذف.','🔒 We never store your photo: it is only used to recognise the product, then discarded.'))}</small>
<span hidden id="imgs-s-load">{e(L('نجهّز أداة التعرّف على الصور (مرة واحدة فقط)…','Loading the image recogniser (first time only)…'))}</span>
<span hidden id="imgs-s-think">{e(L('نتعرّف على المنتج…','Recognising the product…'))}</span>
<span hidden id="imgs-s-done">{e(L('هذا ما نراه في صورتك، اختر الأقرب:','This is what we see in your photo. Pick the closest:'))}</span>
<span hidden id="imgs-s-fail">{e(L('لم نتمكن من التعرّف على الصورة. اكتب اسم المنتج وسنبحث لك.','We could not recognise this photo. Type the product name and we will search for you.'))}</span>
</div></div>"""
    return welcome + imgs

def imgbtn(lang):
    t = "ابحث بالصورة أو الكاميرا" if lang == "ar" else "Search by photo or camera"
    return (f'<button type="button" class="imgs-btn" data-imgs aria-label="{e(t)}" title="{e(t)}">'
            '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 8h3l2-3h6l2 3h3v11H4z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><circle cx="12" cy="13" r="3.6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>')

V10_JS = r"""
/* ---------- v10: welcome, most wanted, image search ---------- */
(function(){
  var LG=document.documentElement.lang||'ar';
  function $(id){return document.getElementById(id)}
  function open(o){if(!o)return;o.hidden=false;document.body.classList.add('ovl-on');requestAnimationFrame(function(){o.classList.add('in')});}
  function close(o){if(!o)return;o.classList.remove('in');document.body.classList.remove('ovl-on');setTimeout(function(){o.hidden=true},220);}
  document.querySelectorAll('.ovl').forEach(function(o){
    o.addEventListener('click',function(ev){if(ev.target===o||ev.target.closest('[data-close]'))close(o)});
  });
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape')document.querySelectorAll('.ovl.in').forEach(close)});

  /* welcome: once per browser */
  var W=$('welcome');
  try{ if(W && !localStorage.getItem('dn-wel') && !/[?&]q=/.test(location.search)){ setTimeout(function(){open(W)},1400); localStorage.setItem('dn-wel','1'); } }catch(e){}

  /* most wanted */
  var grid=$('hotGrid'), tpl=$('hotTpl'), data=[];
  function fmt(n){n=+n||0;return n>=1000?(n/1000).toFixed(n>=10000?0:1).replace('.0','')+'k':String(n)}
  function draw(by){
    var items=data.slice();
    if(by==='rate')items.sort(function(a,b){return (parseFloat(b.rating)||0)-(parseFloat(a.rating)||0)||(+b.sold-+a.sold)});
    else if(by==='price')items.sort(function(a,b){return (+a.price)-(+b.price)});
    else items.sort(function(a,b){return (+b.sold)-(+a.sold)});
    var maxSold=Math.max.apply(null,data.map(function(p){return +p.sold||0}));
    var maxRate=Math.max.apply(null,data.map(function(p){return parseFloat(p.rating)||0}));
    grid.innerHTML='';
    items.slice(0,12).forEach(function(p,i){
      var n=tpl.content.firstElementChild.cloneNode(true), r=parseFloat(p.rating)||0;
      n.querySelector('.hot-rank').textContent='#'+(i+1);
      n.querySelectorAll('a').forEach(function(a){a.href=p.link});
      n.querySelector('img').src=p.img;
      n.querySelector('h3').textContent=p.title;
      n.querySelector('.priceRow b').textContent='$'+p.price;
      var s=n.querySelector('.priceRow s'); if(p.orig&&+p.orig>+p.price*1.05&&+p.orig<+p.price*2.5)s.textContent='$'+p.orig; else s.remove();
      n.querySelector('.m-sold').textContent=fmt(p.sold);
      n.querySelector('.m-rate').textContent=r?r.toFixed(1).replace('.0','')+'%':'—';
      var keep=(+p.sold===maxSold||+p.sold>=5000)?'best':(r>=maxRate-0.2&&r>=97?'top':'hot');
      n.querySelectorAll('[data-b]').forEach(function(b){if(b.getAttribute('data-b')!==keep)b.remove()});
      n.style.animationDelay=(i*35)+'ms';
      grid.appendChild(n);
    });
  }
  if(grid&&tpl){
    fetch('/api/trending/?lang='+LG).then(function(r){return r.json()}).then(function(j){
      data=(j&&j.items)||[]; if(!data.length)throw 0; draw('sold');
    }).catch(function(){var s=$('hot');if(s)s.hidden=true;});
    var sb=$('hotSort');
    if(sb)sb.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b||!data.length)return;
      sb.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});draw(b.getAttribute('data-s'));});
  }

  /* image search (on-device MobileNet, nothing is uploaded) */
  var I=$('imgs'); if(!I)return;
  var MODEL='https://storage.googleapis.com/tfjs-models/tfjs/mobilenet_v1_0.50_224/model.json';
  var TF='https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js';
  var M={ /* ImageNet label -> [search keywords, Arabic, French] */
    'cellular telephone':['smartphone','هاتف ذكي','smartphone'],'iPod':['wireless earbuds','سماعات لاسلكية','écouteurs sans fil'],
    'computer keyboard':['wireless keyboard','لوحة مفاتيح','clavier sans fil'],'typewriter keyboard':['mechanical keyboard','لوحة مفاتيح ميكانيكية','clavier mécanique'],
    'space bar':['wireless keyboard','لوحة مفاتيح','clavier sans fil'],'mouse':['wireless mouse','فأرة لاسلكية','souris sans fil'],
    'laptop':['laptop stand','حامل لابتوب','support ordinateur portable'],'notebook':['laptop stand','حامل لابتوب','support ordinateur portable'],
    'monitor':['portable monitor','شاشة محمولة','écran portable'],'screen':['portable monitor','شاشة','écran'],'desktop computer':['mini PC','حاسوب مكتبي صغير','mini PC'],
    'television':['smart TV box','جهاز تلفاز ذكي','box TV'],'remote control':['remote control','جهاز تحكم','télécommande'],
    'joystick':['game controller','يد تحكم','manette de jeu'],'loudspeaker':['bluetooth speaker','مكبر صوت','enceinte bluetooth'],
    'microphone':['wireless microphone','ميكروفون','micro sans fil'],'digital watch':['smart watch','ساعة ذكية','montre connectée'],
    'analog clock':['smart watch','ساعة','montre'],'stopwatch':['smart watch','ساعة','montre'],'reflex camera':['action camera','كاميرا','caméra'],
    'Polaroid camera':['instant camera','كاميرا فورية','appareil photo instantané'],'projector':['mini projector','بروجكتور داتاشو','vidéoprojecteur'],
    'printer':['thermal printer','طابعة','imprimante'],'hard disc':['portable SSD','قرص صلب','disque dur'],'modem':['wifi router','راوتر واي فاي','routeur wifi'],
    'electric fan':['portable fan','مروحة','ventilateur'],'hair drier':['hair dryer','مجفف شعر','sèche-cheveux'],'vacuum':['cordless vacuum cleaner','مكنسة كهربائية','aspirateur sans fil'],
    'iron':['steam iron','مكواة','fer à repasser'],'sunglasses':['sunglasses','نظارات شمسية','lunettes de soleil'],'backpack':['laptop backpack','حقيبة ظهر','sac à dos'],
    'wallet':['RFID wallet','محفظة','portefeuille'],'purse':['wallet','محفظة','porte-monnaie'],'running shoe':['running shoes','حذاء رياضي','chaussures de course'],
    'binoculars':['monocular telescope','منظار','monoculaire'],'flashlight':['LED flashlight','مصباح يدوي','lampe torche'],'torch':['LED flashlight','مصباح يدوي','lampe torche'],
    'table lamp':['LED desk lamp','مصباح مكتب','lampe de bureau'],'lampshade':['LED lamp','مصباح','lampe'],'spotlight':['LED light','إضاءة LED','lumière LED'],
    'power drill':['cordless drill','مثقاب','perceuse sans fil'],'screwdriver':['electric screwdriver set','مفك براغي','tournevis'],
    'scale':['digital scale','ميزان رقمي','balance numérique'],'water bottle':['smart water bottle','قارورة ماء','gourde'],'vacuum flask':['thermos bottle','ترمس','thermos'],
    'coffeemaker':['coffee maker','آلة قهوة','cafetière'],'espresso maker':['portable espresso maker','آلة إسبريسو','machine espresso'],
    'car mirror':['dash cam','كاميرا السيارة','dashcam'],'sports car':['car accessories','إكسسوارات السيارة','accessoires voiture'],
    'tripod':['phone tripod','حامل ثلاثي','trépied'],'lens cap':['camera lens','عدسة كاميرا','objectif'],'radio':['bluetooth radio speaker','راديو','radio'],
    'CD player':['bluetooth receiver','جهاز صوت','récepteur bluetooth'],'cassette player':['bluetooth speaker','جهاز صوت','enceinte'],
    'hand-held computer':['tablet','جهاز لوحي','tablette'],'web site':['tablet','شاشة','tablette'],'padlock':['smart lock','قفل ذكي','cadenas connecté'],
    'combination lock':['smart lock','قفل ذكي','cadenas connecté'],'safe':['smart safe','خزنة','coffre-fort'],'ballpoint':['smart pen','قلم','stylo'],
    'fountain pen':['pen','قلم','stylo'],'pencil box':['pencil case','مقلمة','trousse'],'umbrella':['umbrella','مظلة','parapluie'],'mailbag':['travel bag','حقيبة سفر','sac de voyage'],
    'switch':['smart switch','مفتاح ذكي','interrupteur connecté'],'electric guitar':['guitar','غيتار','guitare'],'acoustic guitar':['guitar','غيتار','guitare'],
    'toaster':['toaster','محمصة خبز','grille-pain'],'microwave':['microwave','ميكروويف','micro-ondes'],'mug':['smart mug','كوب','tasse'],
    'refrigerator':['mini fridge','ثلاجة صغيرة','mini frigo'],'washer':['portable washing machine','غسالة','lave-linge'],'oscilloscope':['multimeter','جهاز قياس','multimètre'],
    'barbell':['fitness equipment','أدوات رياضة','fitness'],'dumbbell':['dumbbell','دمبل','haltère'],'syringe':['','',''],'band aid':['','','']
  };
  var labels=null, model=null, loading=null;
  function st(id){var s=$('imgs-s-'+id);$('imgs-st').textContent=s?s.textContent:'';}
  function script(src){return new Promise(function(ok,ko){var s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=ko;document.head.appendChild(s);})}
  function ready(){
    if(!loading)loading=(window.tf?Promise.resolve():script(TF)).then(function(){
      return Promise.all([tf.loadLayersModel(MODEL),fetch('/img/labels.json').then(function(r){return r.json()})]);
    }).then(function(r){model=r[0];labels=r[1];});
    return loading;
  }
  function go(q){q=String(q||'').trim();if(q.length<2)return;location.href='/'+LG+'/deals/?q='+encodeURIComponent(q);}
  function classify(img){
    return tf.tidy(function(){
      var t=tf.browser.fromPixels(img).resizeBilinear([224,224]).toFloat().div(127.5).sub(1).expandDims(0);
      return model.predict(t).dataSync();
    });
  }
  function chips(out){
    var g=$('imgs-guess'); g.innerHTML='';
    if(!out.length){st('fail');$('imgs-q').focus();return;}
    st('done'); $('imgs-q').value=out[0].t;
    out.forEach(function(o,i){var b=document.createElement('button');b.type='button';b.className='imgs-chip'+(i===0?' on':'');
      b.innerHTML='<b></b>'+(o.p?'<small></small>':'');b.querySelector('b').textContent=o.t;if(o.p)b.querySelector('small').textContent=Math.round(o.p*100)+'%';
      b.onclick=function(){go(o.q)};g.appendChild(b);});
  }
  function shrink(img){ /* max 640px JPEG, enough to recognise a product */
    var k=Math.min(1,640/Math.max(img.naturalWidth,img.naturalHeight)),c=document.createElement('canvas');
    c.width=Math.round(img.naturalWidth*k);c.height=Math.round(img.naturalHeight*k);
    c.getContext('2d').drawImage(img,0,0,c.width,c.height);return c.toDataURL('image/jpeg',0.82);
  }
  function onDevice(img){
    st(model?'think':'load');
    return ready().then(function(){st('think');return new Promise(function(ok){setTimeout(ok,30)})}).then(function(){
      var p=classify(img), idx=Array.prototype.slice.call(p).map(function(v,i){return [v,i]}).sort(function(a,b){return b[0]-a[0]}).slice(0,8);
      var seen={}, mapped=[], raw=[];
      idx.forEach(function(x){
        var lab=labels[x[1]]||'', first=lab.split(',')[0].trim();
        var key=Object.keys(M).find(function(k){return lab.indexOf(k)===0||first===k});
        if(key){var m=M[key];if(!m[0]||seen[m[0]])return;seen[m[0]]=1;mapped.push({q:m[0],t:LG==='ar'?m[1]:LG==='fr'?m[2]:m[0],p:x[0]});}
        else if(x[0]>0.25&&LG==='en'){raw.push({q:first,t:first,p:x[0]});}
      });
      chips(mapped.concat(raw).slice(0,4));
    });
  }
  function handle(file){
    if(!file)return;
    var url=URL.createObjectURL(file), img=$('imgs-prev');
    $('imgs-stage').hidden=false; $('imgs-guess').innerHTML=''; img.src=url; st('think');
    new Promise(function(ok){if(img.complete&&img.naturalWidth)ok();else img.onload=ok;}).then(function(){
      return fetch('/api/vision/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:LG,img:shrink(img)})})
        .then(function(r){if(r.status!==200)throw 0;return r.json()})
        .then(function(j){
          if(!j.ok){chips([]);return;}
          chips(j.items.map(function(x){return {q:x.q,t:x.name||x.q}}));
        })
        .catch(function(){return onDevice(img)});
    }).catch(function(){st('fail');$('imgs-q').focus();});
  }
  ['imgs-cam','imgs-file'].forEach(function(id){var x=$(id);if(x)x.addEventListener('change',function(){handle(x.files&&x.files[0]);x.value='';})});
  $('imgs-form').addEventListener('submit',function(ev){ev.preventDefault();var v=$('imgs-q').value;
    var on=document.querySelector('.imgs-chip.on b'); if(on&&on.textContent===v){var c=document.querySelector('.imgs-chip.on');c.click();return;} go(v);});
  document.addEventListener('click',function(ev){var b=ev.target.closest('[data-imgs]');if(!b)return;ev.preventDefault();
    $('imgs-stage').hidden=true;$('imgs-q').value='';open(I);ready().catch(function(){});});
})();
"""

CSS_V10 = r"""
/* ---------- v10 ---------- */
.imgs-btn{flex:none;display:inline-grid;place-items:center;width:40px;height:40px;border-radius:12px;border:0;cursor:pointer;background:rgba(124,92,255,.12);color:var(--violet,#6B4BEF);transition:transform .2s,background .2s}
.imgs-btn:hover{transform:scale(1.07);background:rgba(124,92,255,.22)}
.msearch .imgs-btn{width:32px;height:32px;border-radius:999px;background:rgba(255,255,255,.12);color:#F2C266}
.hsearch,.dsearch{gap:6px}
.hsearch .imgs-btn,.dsearch .imgs-btn{background:rgba(124,92,255,.12)!important;color:#6B4BEF!important;padding:0!important;width:44px!important;height:44px!important;min-width:44px;border-radius:999px!important;box-shadow:none!important;flex:none}
@media (max-width:560px){.msearch .imgs-btn{display:none}.hsearch .imgs-btn,.dsearch .imgs-btn{width:40px!important;height:40px!important;min-width:40px}}
.promise{border-radius:22px;padding:24px;background:linear-gradient(135deg,#1B1155,#2A1880 55%,#140D42);color:#F1EEFF;position:relative;overflow:hidden;box-shadow:0 24px 50px -30px rgba(27,17,85,.8)}
.promise::after{content:"";position:absolute;inset:-80px -60px auto auto;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(242,194,102,.35),transparent 70%)}
.promise h2{font-size:clamp(19px,2.6vw,25px);margin:0 0 16px;color:#fff;position:relative;z-index:1}
.pr-g{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;position:relative;z-index:1}
.pr-c{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:14px;display:flex;flex-direction:column;gap:4px}
.pr-c i{font-style:normal;font-size:26px}.pr-c b{font-size:16px;color:#F2C266}.pr-c span{font-size:13.5px;color:#CFC9F0;line-height:1.5}
@media (max-width:820px){.pr-g{grid-template-columns:1fr 1fr}}
.hot-s{padding-top:26px}
.hot-pill{display:inline-block;font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;background:linear-gradient(135deg,#FF7FB0,#C2336F);color:#fff;margin-bottom:6px;animation:hotp 2.4s ease-in-out infinite}
@keyframes hotp{50%{box-shadow:0 0 0 6px rgba(255,127,176,.18)}}
.hot-card{position:relative;animation:enter .5s both}
.hot-rank{position:absolute;top:10px;inset-inline-end:10px;z-index:2;font:800 13px/1 var(--f-display,inherit);background:#140D42;color:#F2C266;border-radius:10px;padding:6px 8px;box-shadow:0 6px 14px -6px rgba(0,0,0,.5)}
.hot-card:nth-child(-n+3) .hot-rank{background:linear-gradient(135deg,#F2CF7E,#E6B95B);color:#140D42}
.hot-card h3{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:14.5px;line-height:1.45;min-height:2.9em}
.hot-more{text-align:center;margin-top:22px}
@keyframes enter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
body.ovl-on{overflow:hidden}
.ovl{position:fixed;inset:0;z-index:120;display:grid;place-items:center;padding:16px;background:rgba(10,6,34,.62);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);opacity:0;transition:opacity .22s}
.ovl.in{opacity:1}.ovl[hidden]{display:none}
.ovl-card{position:relative;width:min(520px,100%);max-height:calc(100vh - 32px);overflow:auto;background:var(--surface,#fff);color:var(--ink,#140D42);border-radius:24px;padding:26px 22px 20px;box-shadow:0 40px 80px -30px rgba(0,0,0,.6);transform:translateY(16px) scale(.97);transition:transform .25s}
.ovl.in .ovl-card{transform:none}
.ovl-x{position:absolute;top:12px;inset-inline-end:12px;width:36px;height:36px;border-radius:50%;border:0;background:rgba(124,92,255,.1);font-size:22px;line-height:1;cursor:pointer;color:inherit}
.wc{text-align:center;background:linear-gradient(180deg,#FFF8E8,var(--surface,#fff) 40%)}
.wc-star{width:58px;height:58px;margin:0 auto 8px;border-radius:18px;display:grid;place-items:center;font-size:30px;color:#F2C266;background:linear-gradient(135deg,#1B1155,#3B22B8);box-shadow:0 12px 24px -10px rgba(59,34,184,.7)}
.wc h2{font-size:23px;margin:4px 0 6px}.wc>p{margin:0 0 14px;color:var(--muted,#5B5680)}
.wc-l{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:8px;text-align:start}
.wc-l li{display:flex;gap:12px;align-items:center;padding:10px 12px;border-radius:14px;background:rgba(124,92,255,.07)}
.wc-l i{font-style:normal;font-size:22px;flex:none}.wc-l b{display:block;font-size:15px}.wc-l span{font-size:13px;color:var(--muted,#5B5680)}
.ovl-card .btn-ghost{color:#1B1155;background:rgba(124,92,255,.1);box-shadow:inset 0 0 0 1px rgba(124,92,255,.35);border:0}
.wc-b{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.wc-new{display:block;margin-top:12px;color:var(--muted,#5B5680)}
.imgs-card h2{font-size:22px;margin:0 0 6px}.imgs-card>p{margin:0 0 14px;color:var(--muted,#5B5680)}
.imgs-pick{display:flex;gap:8px;flex-wrap:wrap}.imgs-pick .btn{flex:1;justify-content:center;cursor:pointer;min-width:150px}
.imgs-stage{margin-top:14px;text-align:center}
.imgs-stage img{max-width:100%;max-height:220px;border-radius:16px;object-fit:contain;background:#F4F2FF}
.imgs-st{margin:10px 0 8px;font-weight:600}
.imgs-guess{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.imgs-chip{display:inline-flex;gap:8px;align-items:center;border:1px solid rgba(124,92,255,.35);background:#fff;color:#1B1155;border-radius:999px;padding:8px 14px;cursor:pointer;font:inherit}
.imgs-chip.on{background:linear-gradient(135deg,#F2CF7E,#E6B95B);border-color:transparent}
.imgs-chip small{opacity:.65}
.imgs-form{display:flex;gap:8px;margin-top:14px}.imgs-form input{flex:1;min-width:0;border:1px solid rgba(124,92,255,.3);border-radius:12px;padding:10px 12px;font:inherit}
.imgs-note{display:block;margin-top:12px;color:var(--muted,#5B5680);font-size:12.5px}
@media (prefers-color-scheme: dark){.wc{background:var(--surface)}.ovl-card .btn-ghost{color:inherit}.imgs-chip{background:transparent;color:inherit}}
@media (prefers-reduced-motion: reduce){.hot-card,.hot-pill{animation:none}.ovl,.ovl-card{transition:none}}
"""

# ---------- Promo engine: campaign banner fed by /promos.json (codes per region, auto start/stop) ----------
def promo_bar(lang):
    ar = lang == "ar"
    L = (lambda a, b: a if ar else b)
    return f"""<div class="wrap"><section class="promo" id="promo" hidden aria-live="polite">
<div class="pm-top"><span class="pm-fire" aria-hidden="true">🛍️</span>
<div class="pm-h"><b id="pm-name"></b><span id="pm-ben"></span></div>
<div class="pm-clock" dir="ltr" id="pm-clock" aria-label="{e(L('ينتهي خلال','Ends in'))}"></div></div>
<div class="pm-codes" id="pm-codes" hidden><p class="pm-lead">{e(L('🎟️ أكواد خصم إضافية فوق التخفيض، انسخ الكود وألصقه عند الدفع:','🎟️ Extra discount codes on top of the sale. Copy a code and paste it at checkout:'))}</p><div class="pm-list" id="pm-list"></div>
<small class="pm-note">{e(L('صالحة لمنتجات مختارة، وكود واحد لكل طلب. تأكّد من الشروط في صفحة الدفع.','Valid on selected items, one code per order. Check the terms at checkout.'))}</small></div>
<a class="btn btn-gold pm-cta" href="/{lang}/#hot">{e(L('🔥 تسوّق الأكثر طلباً الآن','🔥 Shop the most wanted now'))}</a>
<template id="pm-tpl"><button type="button" class="pm-code"><b class="pm-c"></b><span><span class="pm-off"></span> <span>{e(L('عند الشراء بـ','on orders over'))}</span> <span class="pm-min"></span></span><em class="pm-cp">{e(L('انسخ','Copy'))}</em><em class="pm-ok">{e(L('تم النسخ ✓','Copied ✓'))}</em></button></template>
<span hidden id="pm-d">{e(L('ي','d'))}</span><span hidden id="pm-save">{e(L('وفّر','Save'))}</span>
</section></div>"""

PROMO_JS = r"""
/* ---------- promo engine ---------- */
(function(){
  var box=document.getElementById('promo'); if(!box)return;
  var LG=document.documentElement.lang||'ar';
  var tz=''; try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){}
  var GCC=/Riyadh|Dubai|Kuwait|Qatar|Bahrain|Muscat/, FR=/Europe\/Paris/,
      GLOBAL=/Algiers|Casablanca|El_Aaiun|Cairo|Baghdad|Beirut|Tripoli|Khartoum|Nouakchott|Damascus|Aden|Mogadishu|Djibouti/;
  var OUT=/^(Europe|America|Australia|Pacific|Asia\/(Tokyo|Seoul|Jerusalem|Tel_Aviv|Tunis|Amman|Karachi|Kolkata|Calcutta|Dhaka|Manila|Bangkok|Singapore|Kuala_Lumpur|Ho_Chi_Minh|Hong_Kong|Taipei|Kathmandu|Colombo)|Africa\/(Tunis|Dakar|Abidjan|Kampala|Kigali|Lusaka|Maputo|Luanda|Dar_es_Salaam))/;
  var reg=GCC.test(tz)?'gcc':FR.test(tz)?'fr':GLOBAL.test(tz)?'global':OUT.test(tz)?(LG==='fr'?'fr':null):'global';
  fetch('/promos.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(P){
    var now=Date.now(), c=(P.campaigns||[]).filter(function(c){return now>=Date.parse(c.start)&&now<=Date.parse(c.end)})[0];
    if(!c)return;
    var R=reg&&c.regions&&c.regions[reg], start=Date.parse((R&&R.start)||c.start), end=Date.parse((R&&R.end)||c.end);
    if(R&&(now<start||now>end))R=null;
    if(!R)end=Date.parse(c.end);
    var name=(R&&R.name&&R.name[LG])||(c.name&&c.name[LG])||'', ben=(c.benefit&&c.benefit[LG])||'';
    document.getElementById('pm-name').textContent=name;
    document.getElementById('pm-ben').textContent=ben;
    var dd=document.getElementById('pm-d').textContent, sv=document.getElementById('pm-save').textContent;
    function pad(x){return (x<10?'0':'')+x}
    function tick(){var t=Math.max(0,Math.floor((end-Date.now())/1000));if(!t){box.hidden=true;return;}
      var D=Math.floor(t/86400),H=Math.floor(t%86400/3600),M=Math.floor(t%3600/60),S=t%60;
      document.getElementById('pm-clock').innerHTML=(D?'<span><b>'+D+'</b><i>'+dd+'</i></span>':'')+'<span><b>'+pad(H)+'</b><i>:</i></span><span><b>'+pad(M)+'</b><i>:</i></span><span><b>'+pad(S)+'</b></span>';}
    tick();setInterval(tick,1000);
    if(R&&R.codes&&R.codes.length){
      var list=document.getElementById('pm-list'),tpl=document.getElementById('pm-tpl'),cur=R.cur||'$';
      function money(v){return cur==='$'||cur==='€'?cur+v:v+' '+cur}
      R.codes.slice(0,6).forEach(function(k){
        var n=tpl.content.firstElementChild.cloneNode(true);
        n.querySelector('.pm-c').textContent=k[0];
        n.querySelector('.pm-off').textContent=sv+' '+money(k[2]);
        n.querySelector('.pm-min').textContent=money(k[1]);
        n.addEventListener('click',function(){
          var done=function(){n.classList.add('ok');setTimeout(function(){n.classList.remove('ok')},1600)};
          if(navigator.clipboard)navigator.clipboard.writeText(k[0]).then(done,done);else done();
        });
        list.appendChild(n);
      });
      document.getElementById('pm-codes').hidden=false;
    }
    box.hidden=false;
  }).catch(function(){});
})();
"""

CSS_PROMO = r"""
.promo{margin:18px 0 6px;border-radius:22px;padding:18px 18px 16px;color:#fff;position:relative;overflow:hidden;
 background:radial-gradient(120% 140% at 100% 0%,#3B1F8F 0%,#140D42 45%,#07041A 100%);box-shadow:0 24px 50px -28px rgba(20,13,66,.9),inset 0 0 0 1px rgba(242,194,102,.35)}
.promo::before{content:"";position:absolute;inset:-40% -10% auto auto;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(242,194,102,.28),transparent 65%);pointer-events:none}
.pm-top{display:flex;align-items:center;gap:14px;flex-wrap:wrap;position:relative}
.pm-fire{font-size:30px;filter:drop-shadow(0 4px 10px rgba(242,194,102,.5))}
.pm-h{flex:1;min-width:200px;display:flex;flex-direction:column}
.pm-h b{font-size:clamp(18px,2.6vw,24px);background:linear-gradient(90deg,#F2CF7E,#fff 60%,#F2CF7E);-webkit-background-clip:text;background-clip:text;color:transparent}
.pm-h span{color:#CFC9F0;font-size:14px}
.pm-clock{display:flex;gap:4px;align-items:center;direction:ltr;unicode-bidi:isolate}
.pm-clock span{display:inline-flex;align-items:baseline;gap:2px}
.pm-clock b{font:800 20px/1 var(--f-display,inherit);background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:10px;padding:8px 9px;min-width:38px;text-align:center;color:#F2CF7E}
.pm-clock i{font-style:normal;color:#CFC9F0;font-size:12px}
.pm-codes{position:relative;margin-top:12px}
.pm-lead{margin:0 0 8px;color:#E8E4FF;font-size:14px}
.pm-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.pm-code{position:relative;display:flex;flex-direction:column;gap:2px;align-items:flex-start;text-align:start;border:1.5px dashed rgba(242,194,102,.7);background:rgba(242,194,102,.08);color:#fff;border-radius:14px;padding:10px 12px;cursor:pointer;font:inherit;transition:transform .15s,background .15s}
.pm-code:hover{transform:translateY(-2px);background:rgba(242,194,102,.16)}
.pm-c{font:800 15px/1.2 ui-monospace,Menlo,Consolas,monospace;letter-spacing:.5px;color:#F2CF7E;direction:ltr}
.pm-code>span{font-size:12.5px;color:#DCD7F7}
.pm-code em{position:absolute;top:8px;inset-inline-end:10px;font-style:normal;font-size:11px;font-weight:700;color:#140D42;background:#F2CF7E;border-radius:999px;padding:2px 8px}
.pm-code .pm-ok{display:none;background:#3DDC97}.pm-code.ok .pm-ok{display:inline}.pm-code.ok .pm-cp{display:none}
.pm-note{display:block;margin-top:8px;color:#B9B2E3;font-size:12px}
.pm-cta{position:relative;margin-top:12px}
@media (max-width:560px){.pm-clock b{font-size:17px;min-width:32px;padding:7px}.pm-list{grid-template-columns:1fr 1fr}}
"""

CSS_GLOW = r"""
.mainnav a,.mainnav .mg-btn{white-space:nowrap}
/* glowing "Deals" in the header: a lamp that switches on and off + neon text */
.mainnav a.nav-hot{position:relative;display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding-inline:12px 14px;
 background:linear-gradient(135deg,rgba(242,194,102,.16),rgba(255,127,176,.14));box-shadow:inset 0 0 0 1px rgba(242,194,102,.45);animation:hotRing 2.4s ease-in-out infinite}
.nav-hot .lamp{display:inline-block;font-size:17px;line-height:1;animation:lampFlick 2.4s steps(1,end) infinite;filter:grayscale(1) brightness(.55)}
.nav-hot .neon{color:#FFE7A8;font-weight:800;animation:neon 2.4s ease-in-out infinite}
@keyframes lampFlick{0%,8%{filter:grayscale(1) brightness(.55);text-shadow:none}
 10%,14%{filter:none;text-shadow:0 0 10px #FFD36B,0 0 22px #FFB800}16%{filter:grayscale(1) brightness(.55)}
 19%,62%{filter:none;text-shadow:0 0 12px #FFD36B,0 0 26px #FFB800,0 0 40px rgba(255,184,0,.6)}
 64%,100%{filter:grayscale(1) brightness(.55);text-shadow:none}}
@keyframes neon{0%,8%,64%,100%{text-shadow:none;opacity:.85}19%,62%{text-shadow:0 0 6px rgba(255,211,107,.9),0 0 16px rgba(255,184,0,.7);opacity:1}}
@keyframes hotRing{0%,8%,64%,100%{box-shadow:inset 0 0 0 1px rgba(242,194,102,.35)}19%,62%{box-shadow:inset 0 0 0 1px rgba(242,194,102,.9),0 0 18px rgba(255,184,0,.45),0 0 34px rgba(255,127,176,.25)}}
.mainnav a.nav-hot[aria-current="page"]{background:linear-gradient(135deg,#F2CF7E,#E6B95B)}.mainnav a.nav-hot[aria-current="page"] .neon{color:#140D42}
.bbar a[href$="/deals/"] i{animation:lampFlick 2.4s steps(1,end) infinite}
.g-new{display:inline-block;margin:0 0 6px;font-size:12px;font-weight:800;color:#fff;background:linear-gradient(135deg,#FF7FB0,#C2336F);border-radius:999px;padding:3px 10px;animation:hotp 2.4s ease-in-out infinite}
@media (prefers-reduced-motion: reduce){.mainnav a.nav-hot,.nav-hot .lamp,.nav-hot .neon,.bbar a i,.g-new{animation:none!important;filter:none}}
"""
