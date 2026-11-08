
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
  var ar=(document.documentElement.lang||'ar')==='ar';
  var T=ar?{fab:'اسأل نوفا',title:'نوفا، مساعدك الذكي',sub:'يقترح لك الجهاز المناسب من مختاراتنا',hi:'أهلاً 👋 أنا نوفا. أخبرني ماذا تحتاج (للتدريس، للسفر، للاستماع...) وميزانيتك تقريباً، وأقترح لك الأنسب.',ph:'اكتب سؤالك…',send:'إرسال',chips:['سماعة جيدة للحصص عن بعد','ماذا أحتاج للسفر؟','هل بطاقة RFID مفيدة فعلاً؟'],err:'تعذّر الرد الآن. جرّب بعد قليل.',rate:'وصلت إلى الحد المؤقت للأسئلة، جرّب بعد دقائق.',fine:'قد يخطئ المساعد. السعر النهائي على علي إكسبريس.'}
          :{fab:'Ask Nova',title:'Nova, your smart assistant',sub:'Finds the right gear from our picks',hi:'Hi 👋 I am Nova. Tell me what you need (teaching, travel, listening...) and a rough budget, and I will suggest the best fit.',ph:'Type your question…',send:'Send',chips:['Good earbuds for online classes','What do I need for travel?','Is an RFID card really useful?'],err:'No reply right now. Please try again shortly.',rate:'Question limit reached for now. Try again in a few minutes.',fine:'The assistant can make mistakes. Final price is on AliExpress.'};
  var hist=[];try{hist=JSON.parse(sessionStorage.getItem('nova')||'[]')}catch(e){}
  var star='<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 1 L19 13 L31 16 L19 19 L16 31 L13 19 L1 16 L13 13 Z" fill="#E6B95B"/></svg>';
  var fab=document.createElement('button');fab.className='nova-fab';fab.type='button';fab.innerHTML=star+'<span>'+T.fab+'</span>';fab.setAttribute('aria-expanded','false');
  document.body.appendChild(fab);
  var box=null,log,inp,busy=false;
  function esc(s){return s.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function fmt(s){s=esc(s).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
    return s.replace(/(https?:\/\/[^\s)]+|\/(?:ar|en)\/(?:p\/[a-z0-9-]+\/|deals\/))/g,function(u){var ext=u.indexOf('http')===0;return '<a href="'+u+'"'+(ext?' target="_blank" rel="sponsored nofollow noopener"':'')+'>'+(ext?u:(ar?'افتح الصفحة':'Open page'))+'</a>'});}
  function add(role,text,cls){var d=document.createElement('div');d.className='m '+(role==='user'?'u':'a')+(cls?' '+cls:'');d.innerHTML=role==='user'?esc(text):fmt(text);log.appendChild(d);log.scrollTop=log.scrollHeight;return d;}
  function save(){try{sessionStorage.setItem('nova',JSON.stringify(hist.slice(-12)))}catch(e){}}
  function send(q){q=(q||'').trim();if(!q||busy)return;busy=true;inp.value='';add('user',q);hist.push({role:'user',content:q});save();
    var t=add('assistant','…','typing');
    fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({lang:ar?'ar':'en',messages:hist})})
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
