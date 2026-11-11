
(function(){
  var C=window.DEALS||{}, grid=document.getElementById('deals'), st=document.getElementById('status'), tabs=document.getElementById('tabs');
  if(!grid)return;
  var cache={};
  function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function skel(){grid.innerHTML=new Array(9).join('<div class="skel"></div>');st.textContent=C.loading;}
  function render(data){
    var items=(data&&data.items)||[];
    if(!items.length){grid.innerHTML='';st.innerHTML=esc(C.empty);return;}
    var t=new Date(data.updated);
    st.textContent=C.updated+': '+t.toLocaleString(C.lang==='ar'?'ar':'en',{dateStyle:'medium',timeStyle:'short'});
    var B=C.B||{};
    grid.innerHTML=items.map(function(p,i){
      var d=parseInt(String(p.discount||'0').replace(/[^0-9]/g,''))||0, r=parseFloat(String(p.rating||'0'))||0, sold=+p.sold||0;
      var badges=[];
      if(d>=50)badges.push('<span class="bd bd-hot">🔥 '+(C.lang==='ar'?B.off+' '+d+'%':'-'+d+'% '+B.off)+'</span>');
      if(sold>=1000)badges.push('<span class="bd bd-best">'+esc(B.best)+'</span>');
      else if(r>=97)badges.push('<span class="bd bd-top">'+esc(B.top)+' '+r.toFixed(0)+'%</span>');
      var off=d&&d<50?'<span class="off">-'+d+'%</span>':'';
      var orig=p.orig&&p.orig!==p.price?'<s>$'+esc(p.orig)+'</s>':'';
      var sv=(+p.orig-+p.price);var save=sv>=2?'<div class="save">'+esc(B.save)+' $'+sv.toFixed(2)+'</div>':'';
      var meta=[];if(sold)meta.push(esc(sold)+' '+esc(C.sold));if(r)meta.push('★ '+esc(p.rating));
      return '<article class="card deal glowcard enter" style="animation-delay:'+(i*40)+'ms">'
        +'<div class="bds">'+badges.slice(0,2).join('')+'</div>'
        +'<a href="'+esc(p.link)+'" target="_blank" rel="sponsored nofollow noopener"><img class="shot" src="'+esc(p.img)+'" alt="" loading="lazy" width="350" height="350"></a>'
        +'<h3>'+esc(p.title)+'</h3>'
        +'<div class="priceRow"><b>$'+esc(p.price)+'</b>'+orig+off+'</div>'+save
        +'<div class="meta">'+meta.join(' · ')+'</div>'
        +'<div style="margin-top:auto"><a class="go buy" href="'+esc(p.link)+'" target="_blank" rel="sponsored nofollow noopener">'+esc(C.go)+'</a></div></article>';
    }).join('');
  }
  function hero(n){var h=document.getElementById('cathero');if(!h)return;
    h.className='cathero tone-'+((C.tones||{})[n]||'violet');
    document.getElementById('ch-i').textContent=(C.icons||{})[n]||'✦';
    document.getElementById('ch-n').textContent=(C.names||{})[n]||'';
    document.getElementById('ch-h').textContent=(C.hooks||{})[n]||'';
    h.classList.remove('pulse');void h.offsetWidth;h.classList.add('pulse');}
  (function(){var cd=document.getElementById('cd');if(!cd)return;var B=C.B,start=new Date(2026,10,11,0,0,0),end=new Date(2026,10,19,0,0,0);
    function pad(x){return (x<10?'0':'')+x}
    function tick(){var now=new Date();if(now>=end){cd.hidden=true;return;}cd.hidden=false;
      if(now<start){var t=Math.floor((start-now)/1000),D=Math.floor(t/86400),H=Math.floor(t%86400/3600),M=Math.floor(t%3600/60),S=t%60;
        document.getElementById('cd-t').textContent=B.cdT;document.getElementById('cd-s').textContent=B.cdS;
        document.getElementById('cd-c').innerHTML=[[D,B.d],[H,B.h],[M,B.m],[S,B.s]].map(function(x){return '<span><b>'+pad(x[0])+'</b><i>'+x[1]+'</i></span>'}).join('');}
      else{cd.classList.add('live');document.getElementById('cd-t').textContent=B.liveT;document.getElementById('cd-s').textContent=B.liveS;document.getElementById('cd-c').innerHTML='';}}
    tick();setInterval(tick,1000);})();
  var S=C.S||{}, qi=document.getElementById('q'), sugg=document.getElementById('sugg'), sform=document.getElementById('sform');
  function norm(x){return String(x||'').toLowerCase().replace(/[\u064B-\u0652\u0640]/g,'').replace(/[أإآ]/g,'ا').replace(/ة/g,'ه').replace(/ى/g,'ي').trim()}
  function suggest(v){if(!sugg)return;var n=norm(v);if(n.length<2){sugg.innerHTML='';return;}
    var hits=Object.keys(C.names||{}).filter(function(k){return norm(C.names[k]).indexOf(n)>-1||norm((C.hooks||{})[k]).indexOf(n)>-1||k.indexOf(n)>-1}).slice(0,6);
    sugg.innerHTML=hits.length?'<span>'+esc(S.cats)+'</span>'+hits.map(function(k){return '<button type="button" data-n="'+k+'">'+esc((C.icons||{})[k]||'✦')+' '+esc(C.names[k])+'</button>'}).join(''):'';}
  function search(v){v=String(v||'').trim();if(v.length<2){st.textContent=S.short;return;}
    var h=document.getElementById('cathero');h.className='cathero tone-blue';
    document.getElementById('ch-i').textContent='🔍';document.getElementById('ch-n').textContent=S.res+' '+S.for+' «'+v+'»';document.getElementById('ch-h').textContent=S.hook;
    h.classList.remove('pulse');void h.offsetWidth;h.classList.add('pulse');
    tabs.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed','false')});
    try{history.replaceState(null,'','?q='+encodeURIComponent(v))}catch(e){}
    var key='q:'+v.toLowerCase();if(cache[key]){render(cache[key]);return;}
    skel();
    fetch('/api/products?q='+encodeURIComponent(v)+'&lang='+C.lang).then(function(r){return r.json()}).then(function(j){
      if(j.error)throw j; cache[key]=j; if(!(j.items||[]).length){grid.innerHTML='';st.textContent=S.none;return;} render(j);
    }).catch(function(){grid.innerHTML='';st.innerHTML=esc(C.fail);});
    if(innerWidth<760)h.scrollIntoView({behavior:'smooth',block:'start'});}
  if(sform){sform.addEventListener('submit',function(ev){ev.preventDefault();qi.blur();search(qi.value);});
    qi.addEventListener('input',function(){suggest(qi.value)});
    sugg.addEventListener('click',function(ev){var b=ev.target.closest('button[data-n]');if(!b)return;sugg.innerHTML='';qi.value='';load(b.dataset.n);try{history.replaceState(null,'',location.pathname+'#'+b.dataset.n)}catch(e){}});}
  function load(n){
    hero(n);
    tabs.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.n===n)});
    if(cache[n]){render(cache[n]);return;}
    skel();
    fetch('/api/products?niche='+encodeURIComponent(n)+'&lang='+C.lang).then(function(r){return r.json()}).then(function(j){
      if(j.error)throw j; cache[n]=j; render(j);
    }).catch(function(){grid.innerHTML='';st.innerHTML=esc(C.fail)+' <a href="'+C.home+'">DoniaNova</a>';});
  }
  tabs.addEventListener('click',function(ev){var b=ev.target.closest('button[data-n]');if(!b)return;load(b.dataset.n);try{history.replaceState(null,'',location.pathname+'#'+b.dataset.n)}catch(e){}
    if(innerWidth<760)st.scrollIntoView({behavior:'smooth',block:'start'});});
  var h=(location.hash||'').slice(1), sp=null;try{sp=new URLSearchParams(location.search)}catch(e){}
  var q0=sp&&sp.get('q');
  if(q0&&q0.trim().length>=2){qi.value=q0;suggest(q0);search(q0);}
  else{load(tabs.querySelector('button[data-n="'+h+'"]')?h:tabs.querySelector('button').dataset.n);
    if(sp&&sp.has('q')&&qi){qi.focus();}}
})();
