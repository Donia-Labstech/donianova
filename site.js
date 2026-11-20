
(function(){
  var f=document.getElementById('filters');
  document.documentElement.classList.add('js');
  (function(){var u=location.href.split('#')[0],en=encodeURIComponent(u);
    document.querySelectorAll('.sb[data-net]').forEach(function(a){var n=a.dataset.net;
      a.href=n==='wa'?'https://wa.me/?text='+encodeURIComponent(document.title+' '+u):n==='fb'?'https://www.facebook.com/sharer/sharer.php?u='+en:'https://t.me/share/url?url='+en+'&text='+encodeURIComponent(document.title);});
    var c=document.querySelector('.sb-copy');if(c)c.addEventListener('click',function(){var sp=c.querySelector('span'),o=sp.textContent;
      var done=function(){sp.textContent=c.dataset.copied;setTimeout(function(){sp.textContent=o},1800)};
      if(navigator.clipboard)navigator.clipboard.writeText(u).then(done,function(){prompt('',u)});else prompt('',u);});})();
  var still0=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(f){f.addEventListener('click',function(ev){var b=ev.target.closest('button[data-cat]');if(!b)return;var c=b.dataset.cat;
    f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    var n=0,i=0;
    document.querySelectorAll('#grid .card').forEach(function(k){var show=(c==='all'||k.dataset.cat===c);k.hidden=!show;k.classList.remove('enter');
      if(show){n++;if(!still0){void k.offsetWidth;k.style.animationDelay=(i++*45)+'ms';k.classList.add('enter');}}});
    var ct=document.getElementById('count');if(ct)ct.textContent=ct.dataset.tpl.replace('{n}',n);
    var g=document.getElementById('picks');if(g&&g.getBoundingClientRect().top<0)g.scrollIntoView({behavior:still0?'auto':'smooth'});});}
  document.querySelectorAll('.card').forEach(function(k){k.addEventListener('pointermove',function(ev){var r=k.getBoundingClientRect();
    k.style.setProperty('--mx',(ev.clientX-r.left)+'px');k.style.setProperty('--my',(ev.clientY-r.top)+'px');});});
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target);}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});}
  else{document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});}
  try{document.querySelectorAll('.lang a').forEach(function(a){a.addEventListener('click',function(){localStorage.setItem('dn-lang',a.getAttribute('hreflang'))})})}catch(e){}
  var c=document.getElementById('sky');if(!c)return;var x=c.getContext('2d');
  var still=matchMedia('(prefers-reduced-motion: reduce)').matches,stars=[],w,h;
  function size(){var r=c.getBoundingClientRect(),d=devicePixelRatio||1;w=r.width;h=r.height;c.width=w*d;c.height=h*d;x.setTransform(d,0,0,d,0,0);
    stars=Array.from({length:Math.round(w*h/5000)},function(){return{x:Math.random()*w,y:Math.random()*h,r:Math.random()*1.2+.2,p:Math.random()*6.28}})}
  function draw(t){x.clearRect(0,0,w,h);var nx=document.documentElement.dir==='rtl'?w*.16:w*.84,ny=h*.42;
    var g=x.createRadialGradient(nx,ny,0,nx,ny,Math.min(w,h)*.55);g.addColorStop(0,'rgba(230,185,91,.35)');g.addColorStop(.35,'rgba(230,185,91,.08)');g.addColorStop(1,'rgba(230,185,91,0)');
    x.fillStyle=g;x.fillRect(0,0,w,h);stars.forEach(function(s){x.fillStyle='rgba(238,240,248,'+(.35+.45*Math.sin(s.p+(t||0)/1400))+')';x.beginPath();x.arc(s.x,s.y,s.r,0,6.28);x.fill()});
    if(!still)requestAnimationFrame(draw)}
  size();addEventListener('resize',size);draw(0);
})();

(function(){
  var LG=document.documentElement.lang||'ar',ar=LG==='ar';
  var NOVA_FR={fab:'Demander à Nova',title:'Nova, votre assistant intelligent',sub:'Il cherche, compare et vous conseille',hi:'Bonjour 👋 Je suis Nova. Je cherche sur AliExpress et compare les produits à leur prix actuel : lecteurs de codes-barres, disques, accessoires de téléphone, matériel pour enseigner et voyager… Dites-moi ce dont vous avez besoin et votre budget.',ph:'Écrivez votre question…',send:'Envoyer',chips:['Compare les meilleurs SSD portables','Lecteur de codes-barres sans fil pour une petite boutique','De bons écouteurs pour les cours en ligne','Chargeur rapide et batterie externe pour voyager'],err:'Pas de réponse pour le moment. Réessayez dans un instant.',rate:'Limite de questions atteinte pour le moment. Réessayez dans quelques minutes.',fine:"L'assistant peut se tromper. Le prix final est sur AliExpress."};
  var T=LG==='fr'?NOVA_FR:ar?{fab:'اسأل نوفا',title:'نوفا، مساعدك الذكي',sub:'يبحث، يقارن ويقترح لك الأنسب',hi:'أهلاً 👋 أنا نوفا. أبحث لك في علي إكسبريس وأقارن بين المنتجات بأسعارها الحالية: قارئ باركود، أقراص صلبة، لواحق الهاتف، أدوات التعليم والسفر… أخبرني ماذا تحتاج وميزانيتك.',ph:'اكتب سؤالك…',send:'إرسال',chips:['قارن لي بين أفضل أقراص SSD المحمولة','قارئ باركود لاسلكي لمحل صغير','سماعة جيدة للحصص عن بعد','شاحن سريع وبطارية للسفر'],err:'تعذّر الرد الآن. جرّب بعد قليل.',rate:'وصلت إلى الحد المؤقت للأسئلة، جرّب بعد دقائق.',fine:'قد يخطئ المساعد. السعر النهائي على علي إكسبريس.'}
          :{fab:'Ask Nova',title:'Nova, your smart assistant',sub:'Searches, compares and suggests',hi:'Hi 👋 I am Nova. I search AliExpress and compare products at their current prices: barcode scanners, drives, phone accessories, teaching and travel gear… Tell me what you need and your budget.',ph:'Type your question…',send:'Send',chips:['Compare the best portable SSDs','Wireless barcode scanner for a small shop','Good earbuds for online classes','Fast charger and power bank for travel'],err:'No reply right now. Please try again shortly.',rate:'Question limit reached for now. Try again in a few minutes.',fine:'The assistant can make mistakes. Final price is on AliExpress.'};
  var hist=[];try{hist=JSON.parse(sessionStorage.getItem('nova')||'[]')}catch(e){}
  var star='<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 1 L19 13 L31 16 L19 19 L16 31 L13 19 L1 16 L13 13 Z" fill="#E6B95B"/></svg>';
  var fab=document.createElement('button');fab.className='nova-fab';fab.type='button';fab.innerHTML=star+'<span>'+T.fab+'</span>';fab.setAttribute('aria-expanded','false');
  document.body.appendChild(fab);
  var box=null,log,inp,busy=false;
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function inl(s){s=esc(s).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
    return s.replace(/(https?:\/\/[^\s)<]+|\/(?:ar|en|fr)\/(?:p\/[a-z0-9-]+\/|deals\/))/g,function(u){var ext=u.indexOf('http')===0;return '<a href="'+u+'"'+(ext?' target="_blank" rel="sponsored nofollow noopener"':'')+'>'+(ext?(ar?'عرض المنتج ↗':LG==='fr'?'Voir le produit ↗':'View product ↗'):(ar?'افتح الصفحة':LG==='fr'?'Ouvrir la page':'Open page'))+'</a>'});}
  function fmt(s){var L=s.split('\n'),o='',i=0;
    while(i<L.length){var l=L[i].trim();
      if(/^\|.*\|$/.test(l)){var rows=[];while(i<L.length&&/^\|.*\|$/.test(L[i].trim())){rows.push(L[i].trim());i++;}
        rows=rows.filter(function(r){return !/^\|[\s:\-|]+\|$/.test(r)});
        o+='<div class="tbl"><table>'+rows.map(function(r,ri){var c=r.slice(1,-1).split('|');return '<tr>'+c.map(function(x){return ri?'<td>'+inl(x.trim())+'</td>':'<th>'+inl(x.trim())+'</th>'}).join('')+'</tr>'}).join('')+'</table></div>';continue;}
      if(/^[-•*]\s+/.test(l)){o+='<ul>';while(i<L.length&&/^[-•*]\s+/.test(L[i].trim())){o+='<li>'+inl(L[i].trim().replace(/^[-•*]\s+/,''))+'</li>';i++;}o+='</ul>';continue;}
      if(/^#{1,4}\s/.test(l)){o+='<p><b>'+inl(l.replace(/^#+\s/,''))+'</b></p>';i++;continue;}
      if(l)o+='<p>'+inl(l)+'</p>';i++;}
    return o;}
  function add(role,text,cls){var d=document.createElement('div');d.className='m '+(role==='user'?'u':'a')+(cls?' '+cls:'');d.innerHTML=role==='user'?esc(text):fmt(text);log.appendChild(d);log.scrollTop=log.scrollHeight;return d;}
  function save(){try{sessionStorage.setItem('nova',JSON.stringify(hist.slice(-12)))}catch(e){}}
  function send(q){q=(q||'').trim();if(!q||busy)return;busy=true;inp.value='';add('user',q);hist.push({role:'user',content:q});save();
    var t=add('assistant','…','typing');
    fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:LG,messages:hist})})
      .then(function(r){return r.json().then(function(j){return{s:r.status,j:j}})})
      .then(function(x){t.remove();if(x.j.reply){add('assistant',x.j.reply);hist.push({role:'assistant',content:x.j.reply});save();}else add('assistant',x.s===429?T.rate:T.err);})
      .catch(function(){t.remove();add('assistant',T.err);}).then(function(){busy=false;inp.focus();});}
  function open(){
    if(box){box.hidden=!box.hidden;fab.setAttribute('aria-expanded',String(!box.hidden));if(!box.hidden)inp.focus();return;}
    box=document.createElement('section');box.className='nova';box.setAttribute('aria-label',T.title);
    box.innerHTML='<header>'+star.replace('<svg','<svg width="26" height="26"')+'<div><b>'+T.title+'</b><small>'+T.sub+'</small></div><button type="button" aria-label="close">×</button></header><div class="log" aria-live="polite"></div><div class="chips"></div><form><input id="nova-q" maxlength="600" autocomplete="off" placeholder="'+T.ph+'"><button type="submit">'+T.send+'</button></form><div class="fine">'+T.fine+'</div>';
    document.body.appendChild(box);log=box.querySelector('.log');inp=box.querySelector('input');
    add('assistant',T.hi);hist.forEach(function(m){add(m.role,m.content)});
    var ch=box.querySelector('.chips');if(!hist.length)T.chips.forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c;b.onclick=function(){ch.remove();send(c)};ch.appendChild(b)});
    box.querySelector('header button').onclick=function(){box.hidden=true;fab.setAttribute('aria-expanded','false')};
    box.querySelector('form').onsubmit=function(ev){ev.preventDefault();var c=box.querySelector('.chips');if(c)c.remove();send(inp.value)};
    fab.setAttribute('aria-expanded','true');inp.focus();}
  fab.addEventListener('click',open);
})();

/* 3D tilt + glare + glowing rim for product and category cards */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduce)return;
  var SEL='.card,.cc', MAX=9;
  function prep(el){if(el._t)return;el._t=1;el.classList.add('tilt');
    var g=document.createElement('span');g.className='glare';g.setAttribute('aria-hidden','true');el.appendChild(g);
    var r=document.createElement('span');r.className='rim';r.setAttribute('aria-hidden','true');el.appendChild(r);}
  function move(el,x,y){var b=el.getBoundingClientRect(),px=(x-b.left)/b.width,py=(y-b.top)/b.height;
    if(px<0||px>1||py<0||py>1)return;
    el.style.setProperty('--ry',((px-.5)*2*MAX).toFixed(2)+'deg');
    el.style.setProperty('--rx',((.5-py)*2*MAX).toFixed(2)+'deg');
    el.style.setProperty('--gx',(px*100).toFixed(1)+'%');el.style.setProperty('--gy',(py*100).toFixed(1)+'%');
    el.style.setProperty('--mx',(x-b.left)+'px');el.style.setProperty('--my',(y-b.top)+'px');}
  function on(el){prep(el);el.classList.remove('enter');el.classList.add('tilting');}
  function off(el){el.classList.remove('tilting');el.style.setProperty('--rx','0deg');el.style.setProperty('--ry','0deg');}
  var cur=null;
  document.addEventListener('pointerover',function(ev){var el=ev.target.closest&&ev.target.closest(SEL);if(!el||el===cur)return;if(cur)off(cur);cur=el;on(el);},{passive:true});
  document.addEventListener('pointermove',function(ev){if(cur)move(cur,ev.clientX,ev.clientY);},{passive:true});
  document.addEventListener('pointerout',function(ev){if(!cur)return;var to=ev.relatedTarget;if(to&&cur.contains(to))return;off(cur);cur=null;},{passive:true});
  document.addEventListener('touchend',function(){if(cur){off(cur);cur=null;}},{passive:true});
  document.addEventListener('animationend',function(ev){var t=ev.target;if(t.classList&&t.classList.contains('enter')&&t.matches(SEL))t.classList.remove('enter');});
  function all(){document.querySelectorAll(SEL).forEach(prep);}
  all(); if('MutationObserver' in window){new MutationObserver(function(){all()}).observe(document.body,{childList:true,subtree:true});}
})();

(function(){
  var tb=document.getElementById('topbar'),mega=document.getElementById('mega'),mb=document.querySelector('.mg-btn'),dd=document.querySelector('.tgdd'),tp=dd&&dd.querySelector('.tg-pill'),tm=dd&&dd.querySelector('.tgmenu');
  var veil=document.createElement('div');veil.className='veil';veil.hidden=true;document.body.appendChild(veil);
  function onS(){if(tb)tb.classList.toggle('stuck',scrollY>40)}onS();addEventListener('scroll',onS,{passive:true});
  function closeAll(){if(mega){mega.hidden=true;if(mb)mb.setAttribute('aria-expanded','false');}if(tm){tm.hidden=true;tp.setAttribute('aria-expanded','false');}document.body.classList.remove('sheet-mega','sheet-tg');veil.hidden=true;}
  function openMega(sheet){var o=mega.hidden;closeAll();if(!o)return;mega.hidden=false;if(mb)mb.setAttribute('aria-expanded','true');if(sheet){document.body.classList.add('sheet-mega');veil.hidden=false;}if(tb)tb.classList.add('stuck');}
  function openTg(sheet){var o=tm.hidden;closeAll();if(!o)return;tm.hidden=false;tp.setAttribute('aria-expanded','true');if(sheet){document.body.classList.add('sheet-tg');veil.hidden=false;}}
  if(mb&&mega)mb.addEventListener('click',function(ev){ev.stopPropagation();openMega(false)});
  if(tp&&tm)tp.addEventListener('click',function(ev){ev.stopPropagation();openTg(false)});
  document.addEventListener('click',function(ev){if(ev.target.closest('.mega .mg-grid,.tgmenu,.bbar'))return;if((mega&&!mega.hidden)||(tm&&!tm.hidden))closeAll();});
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape')closeAll()});
  if(mega)mega.addEventListener('click',function(ev){if(ev.target.closest('a'))closeAll()});
  var bs=document.querySelector('.bb-sec'),bn=document.querySelector('.bb-nova'),bt=document.querySelector('.bb-tg');
  if(bs)bs.addEventListener('click',function(ev){ev.stopPropagation();openMega(true)});
  if(bt)bt.addEventListener('click',function(ev){ev.stopPropagation();openTg(true)});
  if(bn)bn.addEventListener('click',function(){closeAll();var f=document.querySelector('.nova-fab');if(f)f.click()});
  veil.addEventListener('click',closeAll);
  document.querySelectorAll('.backbtn').forEach(function(b){b.addEventListener('click',function(){
    var same=document.referrer&&document.referrer.indexOf(location.origin)===0;
    if(same&&history.length>1)history.back();else location.href=b.dataset.home;});});
})();

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
