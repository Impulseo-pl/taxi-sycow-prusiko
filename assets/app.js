(function(){
  var T = window.TSP || {};

  // menu mobilne
  var bg = document.querySelector('.burger'), mn = document.getElementById('mnav');
  if (bg) bg.addEventListener('click', function(){
    var o = bg.getAttribute('aria-expanded') !== 'true';
    bg.setAttribute('aria-expanded', o); mn.classList.toggle('open', o);
  });

  // formularz -> gotowy SMS do kierowcy
  var f = document.getElementById('zamow');
  if (f) {
    var ds = document.querySelector('.dock-sms'); if (ds) ds.setAttribute('href', '#zamow');
    var later = function(){ f.classList.toggle('later', f.kiedy.value === 'pozniej'); };
    [].forEach.call(f.kiedy, function(r){ r.addEventListener('change', later); });
    var d = new Date(); d.setDate(d.getDate() + 1);
    f.data.value = d.toISOString().slice(0, 10); f.godz.value = '06:00';
    f.addEventListener('submit', function(e){
      e.preventDefault();
      var ok = true;
      ['skad', 'dokad'].forEach(function(n){
        var bad = !f[n].value.trim(); f[n].classList.toggle('bad', bad); if (bad) ok = false;
      });
      if (!ok) { (f.skad.value.trim() ? f.dokad : f.skad).focus(); return; }
      var kiedy = f.kiedy.value === 'teraz' ? 'teraz' :
        f.data.value.split('-').reverse().join('.') + ' godz. ' + f.godz.value;
      var t = 'Dzień dobry, zamawiam taxi.\nSkąd: ' + f.skad.value.trim() + '\nDokąd: ' + f.dokad.value.trim() +
        '\nKiedy: ' + kiedy + '\nOsób: ' + f.osoby.value;
      if (f.lot.value.trim()) t += '\nLot: ' + f.lot.value.trim();
      if (f.uwagi.value.trim()) t += '\nUwagi: ' + f.uwagi.value.trim();
      var ios = /iPad|iPhone|iPod/.test(navigator.userAgent);
      var mob = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
      var n = document.getElementById('book-n');
      n.hidden = false;
      if (mob) {
        n.textContent = 'Otwieramy SMS-a. Jeśli się nie otworzył, wyślij tę treść na ' + T.tel + ':\n\n' + t;
        location.href = 'sms:' + T.tel + (ios ? '&' : '?') + 'body=' + encodeURIComponent(t);
      } else {
        n.textContent = 'Wyślij tę wiadomość z telefonu na numer ' + T.tel.replace('+48', '') + ' albo po prostu zadzwoń:\n\n' + t;
      }
    });
  }

  // wejscia przy przewijaniu
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin: '0px 0px -8% 0px'});
    document.querySelectorAll('.sec-h,.ride,.steps li,.row,.who li,.split>div,.cta,.faq details').forEach(function(el){
      el.classList.add('rv'); io.observe(el);
    });
  }

  // mapy z trasami
  var boxes = document.querySelectorAll('.mapa');
  if (!boxes.length) return;
  var SY = [51.308, 17.7204];
  var NAMES = {olesnica: 'Oleśnica', wroclaw: 'Wrocław', lotnisko: 'Lotnisko Wrocław', kepno: 'Kępno', miedzyborz: 'Międzybórz'};
  var DIR = {kepno: 'right', miedzyborz: 'right', wroclaw: 'bottom', olesnica: 'left', lotnisko: 'left'};
  var OFF = {right: [8, 0], left: [-8, 0], bottom: [0, 8]};
  function go(){
    if (!window.L) return setTimeout(go, 60);
    fetch(T.base + 'assets/trasy.json').then(function(r){ return r.json(); }).then(function(R){
      boxes.forEach(function(box){ draw(box, R); });
    });
  }
  function draw(box, R){
    var mode = box.getAttribute('data-mode'), light = mode === 'kontakt';
    var m = L.map(box, {zoomControl: light, scrollWheelZoom: false, dragging: light, doubleClickZoom: light,
      boxZoom: false, keyboard: false, touchZoom: light, attributionControl: mode !== 'tlo'});
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom: 18, attribution: '© OpenStreetMap'}).addTo(m);
    if (mode === 'tlo') { m.setView([51.3085, innerWidth > 1020 ? 17.708 : 17.7204], 15); return; }
    var col = light ? '#111' : '#ffc21a', lines = {}, all = [];
    var keys = mode === 'lotnisko' ? ['lotnisko'] : Object.keys(R);
    keys.forEach(function(k){
      var ln = R[k].line, air = k === 'lotnisko';
      all = all.concat(ln);
      lines[k] = L.polyline(ln, {color: col, weight: air ? 5 : 3, opacity: air ? 1 : .75, className: 'rt'}).addTo(m);
      lines[k].base = {weight: air ? 5 : 3, opacity: air ? 1 : .75};
      L.circleMarker(ln[ln.length - 1], {radius: 6, color: '#111', weight: 3, fillColor: '#ffc21a', fillOpacity: 1})
        .addTo(m).bindTooltip(NAMES[k] + ' · ' + String(R[k].km).replace('.', ',') + ' km',
          {permanent: true, direction: mode === 'lotnisko' ? 'bottom' : DIR[k], className: 'tip', offset: OFF[mode === 'lotnisko' ? 'bottom' : DIR[k]]});
    });
    L.circleMarker(SY, {radius: 8, color: '#ffc21a', weight: 3, fillColor: '#111', fillOpacity: 1})
      .addTo(m).bindTooltip('Syców', {permanent: true, direction: 'top', className: 'tip', offset: [0, -10]});
    var b = L.latLngBounds(all.concat([SY])), wide = innerWidth > 1020;
    if (mode === 'lotnisko' && wide) m.fitBounds(b, {paddingTopLeft: [innerWidth * .5, 70], paddingBottomRight: [90, 70]});
    else if (mode === 'hero' && wide) m.fitBounds(b, {paddingTopLeft: [innerWidth * .36, 70], paddingBottomRight: [90, 230]});
    else m.fitBounds(b, {padding: [40, 40]});
    // rysowanie tras, gdy mapa wjedzie na ekran
    var paths = [].slice.call(box.querySelectorAll('path.rt'));
    paths.forEach(function(p){ var L0 = p.getTotalLength(); p.style.strokeDasharray = L0; p.style.strokeDashoffset = L0; });
    var play = function(){ paths.forEach(function(p, i){
      p.style.transition = 'stroke-dashoffset 1.8s ease ' + (0.2 + i * 0.22) + 's'; p.style.strokeDashoffset = 0;
      setTimeout(function(){ p.style.strokeDasharray = 'none'; p.style.transition = 'none'; }, 2400 + i * 220);
    }); };
    if ('IntersectionObserver' in window) {
      var o = new IntersectionObserver(function(es){ if (es[0].isIntersecting) { o.disconnect(); play(); } }, {threshold: .3});
      o.observe(box);
    } else play();
    // podswietlanie trasy z listy obok tej mapy
    var list = box.parentNode.querySelector('.routes');
    if (list) list.querySelectorAll('li').forEach(function(li){
      var k = li.getAttribute('data-r'), l = lines[k];
      if (!l) return;
      var on = function(){ li.classList.add('on'); l.setStyle({weight: 7, opacity: 1}).bringToFront(); };
      var off = function(){ li.classList.remove('on'); l.setStyle(l.base); };
      li.addEventListener('mouseenter', on); li.addEventListener('mouseleave', off);
      li.addEventListener('click', function(){
        list.querySelectorAll('li.on').forEach(function(x){ x.dispatchEvent(new Event('mouseleave')); }); on();
      });
    });
  }
  go();
})();
