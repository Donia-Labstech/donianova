
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
    grid.innerHTML=items.map(function(p,i){
      var off=p.discount&&p.discount!=='0%'?'<span class="off">-'+esc(String(p.discount).replace('-',''))+'</span>':'';
      var orig=p.orig&&p.orig!==p.price?'<s>$'+esc(p.orig)+'</s>':'';
      var meta=[];if(p.sold)meta.push(esc(p.sold)+' '+esc(C.sold));if(p.rating)meta.push('★ '+esc(p.rating));
      return '<article class="card deal enter" style="animation-delay:'+(i*40)+'ms">'
        +'<a href="'+esc(p.link)+'" target="_blank" rel="sponsored nofollow noopener"><img class="shot" src="'+esc(p.img)+'" alt="" loading="lazy" width="350" height="350"></a>'
        +'<h3>'+esc(p.title)+'</h3>'
        +'<div class="priceRow"><b>$'+esc(p.price)+'</b>'+orig+off+'</div>'
        +'<div class="meta">'+meta.join(' · ')+'</div>'
        +'<div style="margin-top:auto"><a class="go" href="'+esc(p.link)+'" target="_blank" rel="sponsored nofollow noopener">'+esc(C.go)+'</a></div></article>';
    }).join('');
  }
  function load(n){
    tabs.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.n===n)});
    if(cache[n]){render(cache[n]);return;}
    skel();
    fetch('/api/products?niche='+encodeURIComponent(n)+'&lang='+C.lang).then(function(r){return r.json()}).then(function(j){
      if(j.error)throw j; cache[n]=j; render(j);
    }).catch(function(){grid.innerHTML='';st.innerHTML=esc(C.fail)+' <a href="'+C.home+'">DoniaNova</a>';});
  }
  tabs.addEventListener('click',function(ev){var b=ev.target.closest('button[data-n]');if(b)load(b.dataset.n);});
  load(tabs.querySelector('button').dataset.n);
})();
