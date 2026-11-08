
(function(){
  var f=document.getElementById('filters');
  if(f){f.addEventListener('click',function(ev){var b=ev.target.closest('button[data-cat]');if(!b)return;var c=b.dataset.cat;
    f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    document.querySelectorAll('#grid .card').forEach(function(k){k.hidden=!(c==='all'||k.dataset.cat===c)});});}
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
