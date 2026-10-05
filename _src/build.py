"""Buduje 5 podstron dema Taxi Syców PrusIKo. python _src/build.py"""
import os, json, html as H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://impulseo-pl.github.io/taxi-sycow-prusiko/'
TEL, TEL_H = '+48883835984', '883 835 984'
NAZWA = 'Taxi Syców PrusIKo'
TRASY = json.load(open(os.path.join(ROOT, 'assets', 'trasy.json'), encoding='utf-8'))

def km(k):
    return ('%.1f' % TRASY[k]['km']).replace('.', ',').replace(',0', '')

NAV = [('', 'Start'), ('przejazdy/', 'Przejazdy'), ('lotnisko/', 'Lotnisko Wrocław'), ('o-nas/', 'O nas'), ('kontakt/', 'Kontakt')]

I_TEL = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>'
I_SMS = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H9l-4.4 3.5c-.3.3-.6 0-.6-.3V17a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1z"/></svg>'

LOGO = '''<span class="brand-sign" aria-hidden="true"><i>TAXI</i></span><span class="brand-txt"><b>PrusIKo</b><small>Syców</small></span>'''

BIZ = {
    "@type": "TaxiService", "@id": URL + "#firma", "name": NAZWA,
    "legalName": "Prusiko Vasyl Prus", "taxID": "9112052716",
    "description": "Taksówka w Sycowie: przejazdy po mieście, do Oleśnicy i Wrocławia, na lotnisko Wrocław, do przychodni i szpitala, powroty z imprez i wesel.",
    "url": URL, "telephone": TEL,
    "provider": {"@type": "LocalBusiness", "name": NAZWA, "telephone": TEL,
                 "address": {"@type": "PostalAddress", "addressLocality": "Syców", "postalCode": "56-500", "addressRegion": "dolnośląskie", "addressCountry": "PL"}},
    "areaServed": [{"@type": "City", "name": n} for n in ("Syców", "Oleśnica", "Wrocław", "Międzybórz", "Kępno")],
}

FORM = '''<form class="book" id="zamow" autocomplete="on" novalidate>
  <div class="book-h"><b>Zamów kurs SMS-em</b><span>Wypełnij, a telefon sam przygotuje wiadomość do kierowcy</span></div>
  <label class="f"><span>Skąd</span><input name="skad" placeholder="np. Syców, ul. Mickiewicza 5" required></label>
  <label class="f"><span>Dokąd</span><input name="dokad" list="cele" placeholder="np. Lotnisko Wrocław" required>
  <datalist id="cele"><option>Lotnisko Wrocław</option><option>Wrocław Dworzec Główny</option><option>Oleśnica</option><option>Szpital w Oleśnicy</option><option>Kępno</option><option>Międzybórz</option></datalist></label>
  <div class="f when"><span>Kiedy</span>
    <div class="seg" role="radiogroup"><label><input type="radio" name="kiedy" value="teraz" checked><i>Teraz</i></label><label><input type="radio" name="kiedy" value="pozniej"><i>Na termin</i></label></div>
    <div class="termin"><input type="date" name="data" aria-label="Data"><input type="time" name="godz" aria-label="Godzina"></div>
  </div>
  <label class="f f-s"><span>Osób</span><select name="osoby"><option>1</option><option>2</option><option>3</option><option>4</option></select></label>
  <label class="f f-s"><span>Nr lotu <em>(opcjonalnie)</em></span><input name="lot" placeholder="np. FR 1234"></label>
  <label class="f f-w"><span>Uwagi <em>(opcjonalnie)</em></span><input name="uwagi" placeholder="np. duża walizka, czekam przy bramie"></label>
  <div class="book-go">
    <button class="btn btn-y" type="submit">''' + I_SMS + '''Wyślij SMS</button>
    <a class="btn btn-o" href="tel:''' + TEL + '''">''' + I_TEL + TEL_H + '''</a>
  </div>
  <p class="book-n" id="book-n" hidden></p>
</form>'''

def page(path, title, desc, body, extra_ld=None, mapa=False):
    B = '../' * path.count('/')
    nav = ''.join('<a href="%s%s"%s>%s</a>' % (B, p, ' aria-current="page"' if p == path else '', t) for p, t in NAV[1:])
    mnav = ''.join('<a href="%s%s"%s>%s</a>' % (B, p, ' aria-current="page"' if p == path else '', t) for p, t in NAV)
    graph = [BIZ] + (extra_ld or [])
    if path:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": NAZWA, "item": URL},
            {"@type": "ListItem", "position": 2, "name": dict(NAV)[path], "item": URL + path}]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    leaflet = ('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">'
               '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js" defer></script>') if mapa else ''
    foot = ''.join('<li><a href="%s%s">%s</a></li>' % (B, p, t) for p, t in NAV)
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{URL}{path}">
<meta name="theme-color" content="#0c0c0d">
<meta property="og:type" content="website"><meta property="og:locale" content="pl_PL">
<meta property="og:title" content="{H.escape(title)}"><meta property="og:description" content="{H.escape(desc)}">
<meta property="og:url" content="{URL}{path}"><meta property="og:image" content="{URL}img/og.png">
<link rel="icon" href="{B}img/ikona.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{B}assets/styles.css">
{leaflet}
<script>(function(){{try{{if(matchMedia('(prefers-reduced-motion:reduce)').matches)return;if(location.search.indexOf('intro')<0){{if(sessionStorage.getItem('tsp-intro'))return;sessionStorage.setItem('tsp-intro','1')}}document.documentElement.classList.add('intro-on')}}catch(e){{}}}})();</script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<div id="intro" aria-hidden="true"><span class="intro-sign"><i>TAXI</i></span></div>
<header class="top">
  <div class="w top-in">
    <a class="brand" href="{B or './'}" aria-label="{NAZWA} — strona główna">{LOGO}</a>
    <nav class="nav" aria-label="Główna">{nav}</nav>
    <a class="btn btn-y top-tel" href="tel:{TEL}">{I_TEL}{TEL_H}</a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="mnav" aria-label="Menu"><span></span><span></span></button>
  </div>
  <nav class="mnav" id="mnav" aria-label="Menu mobilne">{mnav}</nav>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="w foot-in">
    <div class="foot-a">
      <a class="brand" href="{B or './'}">{LOGO}</a>
      <p>Taksówka w Sycowie. Kursy po mieście, do Oleśnicy, Wrocławia i na lotnisko.</p>
      <a class="foot-tel" href="tel:{TEL}">{TEL_H}</a>
    </div>
    <div><h4>Strona</h4><ul>{foot}</ul></div>
    <div><h4>Firma</h4><p>Prusiko Vasyl Prus<br>56-500 Syców<br>NIP 911-205-27-16</p></div>
  </div>
  <div class="w foot-b"><span>© 2026 {NAZWA}</span><span>Mapa: © współtwórcy OpenStreetMap</span></div>
</footer>
<div class="dock" aria-label="Szybki kontakt">
  <a href="tel:{TEL}" class="dock-tel">{I_TEL}Zadzwoń</a>
  <a href="{B}kontakt/#zamow" class="dock-sms">{I_SMS}Zamów SMS-em</a>
</div>
<script>window.TSP={{tel:"{TEL}",base:"{B}"}}</script>
<script src="{B}assets/app.js" defer></script>
<script src="{B}assets/licznik.js" defer></script>
</body>
</html>'''

def write(path, s):
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(s)

def trasy_tabela(B):
    rows = [('miedzyborz', 'Międzybórz'), ('kepno', 'Kępno'), ('olesnica', 'Oleśnica'), ('wroclaw', 'Wrocław, Rynek'), ('lotnisko', 'Lotnisko Wrocław')]
    li = ''.join(f'<li data-r="{k}"><span>Syców → {n}</span><b>{km(k)} km</b></li>' for k, n in rows)
    return f'<ul class="routes" id="routes">{li}</ul><p class="src">Odległość drogą według OpenStreetMap. Cenę kursu podajemy przez telefon.</p>'

# ---------- strona główna ----------
HOME = f'''
<section class="hero">
  <div class="hero-map mapa" data-mode="tlo" aria-hidden="true"></div>
  <div class="hero-veil"></div>
  <div class="w hero-in">
    <div class="hero-txt">
      <p class="kick"><span class="dot"></span>Syców · Oleśnica · Wrocław</p>
      <h1>Taxi Syców.<br><span class="y">Dzwonisz i jedziesz.</span></h1>
      <p class="lead">Kursy po Sycowie, do Oleśnicy, Wrocławia i na lotnisko. Odbierzemy Cię spod domu, przychodni, dworca albo z wesela. Bez aplikacji, bez rejestracji. Jeden telefon do kierowcy.</p>
      <a class="bigtel" href="tel:{TEL}"><small>Zamów taksówkę</small>{TEL_H}</a>
    </div>
    {FORM}
  </div>
</section>

<div class="checker" aria-hidden="true"></div>

<section class="trasy">
  <div class="trasy-map mapa" data-mode="hero" aria-hidden="true"></div>
  <div class="w trasy-in">
    <div class="trasy-h"><h2>Z Sycowa<br>w każdą stronę</h2><p>Najedź na trasę, żeby zobaczyć ją na mapie.</p></div>
    <div>{trasy_tabela('')}</div>
  </div>
</section>

<section class="sec">
  <div class="w">
    <div class="sec-h"><h2>Dokąd jeździmy najczęściej</h2><p>Krótki kurs po mieście albo daleka trasa. Obsługujemy klientów prywatnych w Sycowie, Oleśnicy i Wrocławiu.</p></div>
    <div class="rides">
      <a class="ride ride-big" href="lotnisko/"><span class="ride-t">Lotnisko Wrocław</span><p>Kurs na samolot i odbiór po przylocie. Zarezerwuj przejazd z wyprzedzeniem, podaj numer lotu.</p><b class="ride-km">{km('lotnisko')} km</b><span class="more">Transfer na lotnisko</span></a>
      <a class="ride" href="przejazdy/#codzienne"><span class="ride-t">Codzienne przejazdy</span><p>Do pracy, do domu, na zakupy, w dowolne miejsce w Sycowie i okolicy.</p></a>
      <a class="ride" href="przejazdy/#wizyty"><span class="ride-t">Lekarz, szpital, urząd</span><p>Dowieziemy na wizytę na czas i odbierzemy, kiedy skończysz.</p></a>
      <a class="ride" href="przejazdy/#imprezy"><span class="ride-t">Wesela i imprezy</span><p>Bezpieczny powrót z wesela, osiemnastki czy spotkania ze znajomymi.</p></a>
      <a class="ride" href="przejazdy/#dworzec"><span class="ride-t">Dworzec i odbiory</span><p>Odbierzemy z dworca, przystanku albo spod szkoły. Dopasujemy się do Twojego grafiku.</p></a>
    </div>
  </div>
</section>

<section class="sec sec-light">
  <div class="w how">
    <div class="sec-h"><h2>Jak zamówić kurs</h2><p>Trzy sposoby, żaden nie wymaga aplikacji.</p></div>
    <ol class="steps">
      <li><h3>Zadzwoń</h3><p>Najszybciej. Powiedz, skąd i dokąd jedziesz, kierowca potwierdzi, kiedy będzie.</p><a href="tel:{TEL}">{TEL_H}</a></li>
      <li><h3>Napisz SMS</h3><p>Gdy nie możesz rozmawiać. Formularz na stronie sam ułoży wiadomość z adresem i godziną.</p><a href="kontakt/#zamow">Ułóż SMS</a></li>
      <li><h3>Zarezerwuj wcześniej</h3><p>Lotnisko, ślub, wizyta o 7 rano. Umów kurs dzień wcześniej i śpij spokojnie.</p><a href="lotnisko/">Kurs na lotnisko</a></li>
    </ol>
  </div>
</section>

<section class="sec">
  <div class="w split">
    <div>
      <h2>Zniżki dla stałych klientów</h2>
      <p class="big">Jeździsz z nami regularnie: do pracy, na dializy, na zakupy co tydzień? Zapytaj kierowcę o zniżkę. Cenimy tych, którzy wracają.</p>
      <a class="btn btn-y" href="tel:{TEL}">{I_TEL}Zapytaj o zniżkę</a>
    </div>
    <ul class="who">
      <li><b>Seniorzy</b><span>Pomoc przy wsiadaniu, kurs do lekarza i z powrotem.</span></li>
      <li><b>Rodziny z dziećmi</b><span>Zakupy, wizyty, dworzec, wyjazd na wakacje.</span></li>
      <li><b>Firmy i delegacje</b><span>Spotkanie we Wrocławiu, pociąg, samolot o świcie.</span></li>
      <li><b>Wieczór na mieście</b><span>Zostaw auto w domu i wróć bezpiecznie.</span></li>
    </ul>
  </div>
</section>

<section class="sec sec-y">
  <div class="w cta">
    <h2>Potrzebujesz taksówki w Sycowie?</h2>
    <a class="bigtel bigtel-d" href="tel:{TEL}"><small>Zadzwoń teraz</small>{TEL_H}</a>
  </div>
</section>
'''

# ---------- przejazdy ----------
FAQ = [
    ("Czy mogę zamówić taksówkę z wyprzedzeniem?", "Tak. Zadzwoń albo wyślij SMS z datą, godziną i adresem odbioru. Kursy na lotnisko i wczesne poranne najlepiej umawiać dzień wcześniej."),
    ("Czy jeździcie poza Syców?", "Tak. Jeździmy do Oleśnicy, Wrocławia, na lotnisko Wrocław i do okolicznych miejscowości. Dalsze trasy ustal z kierowcą przez telefon."),
    ("Ile kosztuje kurs?", "Cenę konkretnego kursu podaje kierowca przy zamówieniu. Powiedz, skąd i dokąd jedziesz, a od razu usłyszysz kwotę."),
    ("Czy odbierzecie mnie z wesela albo imprezy?", "Tak. Możesz umówić odbiór na konkretną godzinę albo zadzwonić, kiedy będziesz gotowy do powrotu."),
    ("Czy są zniżki?", "Tak, dla stałych klientów. Zapytaj kierowcę przy zamówieniu."),
]
FAQ_HTML = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
FAQ_LD = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

PRZEJAZDY = f'''
<section class="phead"><div class="w">
  <p class="kick"><span class="dot"></span>Przejazdy</p>
  <h1>Taksówka na każdą trasę w Sycowie i okolicy</h1>
  <p class="lead">Przewozimy osoby prywatne i wszystkich, którzy cenią punktualność. Cztery rodzaje kursów, jeden numer: <a href="tel:{TEL}">{TEL_H}</a>.</p>
</div></section>

<section class="sec"><div class="w rows">
  <article class="row" id="codzienne"><div class="row-n">Po mieście</div><div><h2>Codzienne przejazdy</h2><p>Do pracy, do domu, na zakupy, na pociąg. Szybki kurs w Sycowie i do okolicznych miejscowości: Międzybórz ({km('miedzyborz')} km), Kępno ({km('kepno')} km), Oleśnica ({km('olesnica')} km). Wystarczy jeden telefon.</p></div></article>
  <article class="row" id="wizyty"><div class="row-n">Zdrowie i urzędy</div><div><h2>Lekarz, szpital, urząd</h2><p>Zawieziemy do przychodni, na badania, do szpitala w Oleśnicy czy Wrocławiu i do urzędu. Umów kurs wcześniej, żeby zdążyć na godzinę wizyty. Jeśli wizyta się przeciągnie, zadzwoń i odbierzemy Cię w drodze powrotnej.</p></div></article>
  <article class="row" id="lotnisko"><div class="row-n">Dalekie trasy</div><div><h2>Lotnisko i Wrocław</h2><p>Lotnisko Wrocław to {km('lotnisko')} km drogą od Sycowa, Rynek we Wrocławiu {km('wroclaw')} km. Zarezerwuj przejazd z wyprzedzeniem, a przy odbiorze z lotniska podaj numer lotu.</p><a class="lnk" href="../lotnisko/">Więcej o kursach na lotnisko</a></div></article>
  <article class="row" id="imprezy"><div class="row-n">Wieczorem</div><div><h2>Wesela, imprezy, spotkania</h2><p>Bezpieczny powrót z wesela, osiemnastki, sylwestra czy spotkania ze znajomymi. Nie martw się o prowadzenie, zadzwoń po taxi.</p></div></article>
  <article class="row" id="dworzec"><div class="row-n">Odbiory</div><div><h2>Odbiór i dowóz</h2><p>Odbierzemy Cię z dworca, imprezy albo zawieziemy na zakupy. Elastycznie dopasowujemy się do Twojego grafiku.</p></div></article>
</div></section>

<section class="sec sec-light"><div class="w faq-w">
  <div class="sec-h"><h2>Pytania przed kursem</h2></div>
  <div class="faq">{FAQ_HTML}</div>
</div></section>
'''

# ---------- lotnisko ----------
LOTNISKO = f'''
<section class="phead phead-map">
  <div class="hero-map mapa" data-mode="lotnisko" aria-hidden="true"></div>
  <div class="hero-veil"></div>
  <div class="w">
    <p class="kick"><span class="dot"></span>Lotnisko Wrocław</p>
    <h1>Taxi z Sycowa na lotnisko we Wrocławiu</h1>
    <p class="lead">{km('lotnisko')} km drogą spod Twoich drzwi do terminalu. Bez szukania parkingu i bez ciągania walizek do autobusu.</p>
    <a class="bigtel" href="tel:{TEL}"><small>Zarezerwuj kurs</small>{TEL_H}</a>
  </div>
</section>

<section class="sec"><div class="w split">
  <div>
    <h2>Na samolot</h2>
    <p class="big">Umów kurs dzień wcześniej. Podaj godzinę wylotu, a ustalimy godzinę odbioru z zapasem na kontrolę bezpieczeństwa.</p>
    <h2 class="mt">Z samolotu</h2>
    <p class="big">Przyślij numer lotu i godzinę przylotu. Kierowca będzie wiedział, kiedy wylądujesz, i ustali z Tobą miejsce spotkania przed terminalem.</p>
  </div>
  <div class="card-y">
    <h3>Co podać przy rezerwacji</h3>
    <ul class="check">
      <li>Adres odbioru w Sycowie lub okolicy</li>
      <li>Datę i godzinę wylotu albo przylotu</li>
      <li>Numer lotu (przy odbiorze z lotniska)</li>
      <li>Liczbę osób i walizek</li>
      <li>Numer telefonu, pod którym będziesz dostępny</li>
    </ul>
    <a class="btn btn-d" href="../kontakt/#zamow">{I_SMS}Wyślij to SMS-em</a>
  </div>
</div></section>

<section class="sec sec-light"><div class="w">
  <div class="sec-h"><h2>Po drodze na lotnisko</h2><p>Jedziemy przez Oleśnicę, więc możemy zabrać pasażerów z kilku adresów. Ustal to przy zamówieniu.</p></div>
  {trasy_tabela('../')}
</div></section>
'''

# ---------- o nas ----------
ONAS = f'''
<section class="phead"><div class="w">
  <p class="kick"><span class="dot"></span>O nas</p>
  <h1>Lokalna taksówka z Sycowa</h1>
  <p class="lead">Taxi Syców PrusIKo powstało z prostej potrzeby: bezpośredniego kontaktu z ludźmi i pomagania im w codziennych podróżach.</p>
</div></section>

<section class="sec"><div class="w rows">
  <article class="row"><div class="row-n">Zasada 1</div><div><h2>Punktualnie</h2><p>Rozumiemy, że czas to pieniądz. Jesteśmy na czas, niezależnie od tego, czy jedziesz na zakupy, na lotnisko, do przychodni czy na wesele.</p></div></article>
  <article class="row"><div class="row-n">Zasada 2</div><div><h2>Czysto i wygodnie</h2><p>Komfort podróży to dla nas priorytet. Auta są zawsze czyste i zadbane.</p></div></article>
  <article class="row"><div class="row-n">Zasada 3</div><div><h2>Bezpiecznie</h2><p>Kierowcy mają wszystkie wymagane kwalifikacje. Pojazdy regularnie serwisujemy, żeby każda trasa po Sycowie, Oleśnicy i Wrocławiu była spokojna.</p></div></article>
  <article class="row"><div class="row-n">Zasada 4</div><div><h2>Po ludzku</h2><p>Dzwonisz bezpośrednio do kierowcy, nie do centrali. Stali klienci dostają zniżki, bo cenimy tych, którzy wracają.</p></div></article>
</div></section>

<section class="sec sec-y"><div class="w cta">
  <h2>Zadzwoń i jedź</h2>
  <a class="bigtel bigtel-d" href="tel:{TEL}"><small>Taxi Syców</small>{TEL_H}</a>
</div></section>
'''

# ---------- kontakt ----------
KONTAKT = f'''
<section class="phead"><div class="w">
  <p class="kick"><span class="dot"></span>Kontakt</p>
  <h1>Zamów taksówkę w Sycowie</h1>
  <p class="lead">Najszybciej telefonicznie. Jeśli nie możesz rozmawiać, wypełnij formularz: telefon przygotuje SMS do kierowcy z adresem i godziną.</p>
</div></section>

<section class="sec"><div class="w split split-k">
  <div class="kontakt">
    <a class="bigtel" href="tel:{TEL}"><small>Telefon i SMS</small>{TEL_H}</a>
    <dl>
      <dt>Obszar</dt><dd>Syców, Oleśnica, Wrocław i okolice</dd>
      <dt>Firma</dt><dd>Prusiko Vasyl Prus<br>56-500 Syców<br>NIP 911-205-27-16</dd>
    </dl>
  </div>
  {FORM}
</div></section>

<section class="sec sec-light"><div class="w">
  <div class="sec-h"><h2>Gdzie dojeżdżamy</h2></div>
  <div class="map-box mapa" data-mode="kontakt"></div>
  {trasy_tabela('../')}
</div></section>
'''

write('', page('', 'Taxi Syców — taksówka Syców, Oleśnica, Wrocław, lotnisko | PrusIKo',
               'Taxi Syców: tel. 883 835 984. Kursy po Sycowie, do Oleśnicy, Wrocławia i na lotnisko Wrocław. Odbiory z wesel, wizyty u lekarza, zniżki dla stałych klientów.',
               HOME, mapa=True))
write('przejazdy', page('przejazdy/', 'Przejazdy taxi Syców — lekarz, dworzec, wesela | PrusIKo',
               'Codzienne kursy w Sycowie, dojazdy do przychodni i szpitala, odbiory z dworca, powroty z wesel i imprez. Taxi Syców tel. 883 835 984.',
               PRZEJAZDY, extra_ld=[FAQ_LD]))
write('lotnisko', page('lotnisko/', 'Taxi Syców lotnisko Wrocław — transfer %s km | PrusIKo' % km('lotnisko'),
               'Taxi z Sycowa i Oleśnicy na lotnisko Wrocław i z powrotem. Rezerwacja z wyprzedzeniem, odbiór po przylocie z numerem lotu. Tel. 883 835 984.',
               LOTNISKO, mapa=True))
write('o-nas', page('o-nas/', 'O nas — lokalna taksówka z Sycowa | PrusIKo',
               'Taxi Syców PrusIKo: punktualnie, czysto, bezpiecznie. Dzwonisz bezpośrednio do kierowcy. Zniżki dla stałych klientów.', ONAS))
write('kontakt', page('kontakt/', 'Kontakt i zamówienie taxi Syców — 883 835 984 | PrusIKo',
               'Zamów taksówkę w Sycowie telefonicznie lub SMS-em: 883 835 984. Kursy do Oleśnicy, Wrocławia i na lotnisko.', KONTAKT, mapa=True))

sm = ''.join(f'<url><loc>{URL}{p}</loc></url>' for p, _ in NAV)
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {URL}sitemap.xml\n')
print('ok')
