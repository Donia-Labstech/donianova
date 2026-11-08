
(function(){
  var f=document.getElementById('filters');
  document.documentElement.classList.add('js');
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
