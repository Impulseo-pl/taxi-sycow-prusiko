# Taxi Syców PrusIKo — demo nowej strony

**Prusiko Vasyl Prus** · NIP 911-205-27-16 · Syców · tel. 883 835 984
Obecna strona: taxisycowprusiko.pl (Webador, wygenerowana AI)
Podgląd dema: https://impulseo-pl.github.io/taxi-sycow-prusiko/?team=1

## Budowanie

```
python _src/build.py        # 5 podstron + sitemap + robots
python _src/shots.py 1440   # zrzuty (wymaga serwera: python -m http.server 8125 w C:\Users\kluch)
```

Treść w `_src/build.py`, wygląd w `assets/styles.css`, formularz SMS i mapy w `assets/app.js`.
Trasy (`assets/trasy.json`) to realne odległości drogą z OSRM/OpenStreetMap.

## Analiza rynku (2026-10-05): co wzięliśmy, co wyrzuciliśmy

**Wzięte od dużych graczy:**
- numer telefonu jako główny element pierwszego ekranu (Super Taxi 19622, iTaxi, Taxi Berlin)
- przyklejony pasek „Zadzwoń / SMS” na telefonie (najlepszy lokalny wzór: taxiwnamyslowie.pl)
- osobna strona lotniska: rezerwacja z wyprzedzeniem, numer lotu (Welcome Pickups, Blacklane, Addison Lee)
- zamówienie bez aplikacji: formularz układa gotowego SMS-a do kierowcy (zamiast formularza e-mail)
- mapa z trasami i realnymi kilometrami: konkret zamiast pustych haseł
- dane firmy (NIP) w stopce, jak MotoFotoTaxi Oleśnica

**Wyrzucone ze starej strony:**
- zmyślone opinie („[[imię klienta]], Syców”, „Anna Kowalska”)
- formularz kontaktowy z e-mailem (na taksówkę nikt nie czeka na maila)
- zdjęcia stockowe z Pexels i logo „TSP” wygenerowane przez AI
- puste frazy: „Wykraczając poza zwyczajność”, „Dołącz do nas, gdy będziemy się rozwijać”

**Świadomie nie dodane (rzeczy dla korporacji):** aplikacja, logowanie, śledzenie auta, klasy aut, „VIP”, rekrutacja kierowców.

**Konkurencja w Sycowie** praktycznie nie ma stron (Jan Rak, Taxi-Bus Godlewski są tylko w katalogach).
Komfort Taxi i MotoFotoTaxi (Oleśnica) mają strony, ale **nikt nie podaje cen**. Katalog taxi-24.com.pl zajmuje wyniki na frazę „taxi Syców”.

## Do uzupełnienia od klienta (mocno podniesie stronę)

1. **Ceny tras**: Syców→Oleśnica, Wrocław, lotnisko (stała cena) i taryfa miejska. Nikt w okolicy tego nie publikuje.
2. **Zdjęcie auta i kierowcy, imię.** To największa przewaga nad aplikacjami. Dziś w demie nie ma żadnego zdjęcia, bo nie chcemy stocku.
3. Czy jeździ **24/7** / w jakich godzinach.
4. Płatność kartą/BLIK, faktura dla firm, fotelik dziecięcy, zwierzęta, duży bagaż. Wpisujemy tylko to, co potwierdzi.
5. Ile minut czeka na lotnisku przy opóźnionym locie.
6. Wizytówka Google: link i prawdziwe opinie za zgodą.
7. Logo. Obecne „TSP” jest z generatora. W demie jest znak z kogutem „TAXI”.
8. Adres: w rejestrach są dwa (Kościelna 21 i Kaliska 36/3), na stronie zostawiamy tylko „Syców”.

---
Realizacja: [Impulseo](https://impulseo.pl)
