# APC Homepage Structure

## Účel

Toto je pracovný návrh homepage pre nový APC web v Boxcar template.

Nerieši finálny dizajn do detailu. Rieši:

- poradie sekcií
- čo do nich dať
- odkiaľ zobrať obsah
- čo je fakt a čo je návrh

## Cieľ homepage

Homepage má jasne odkomunikovať, že APC je:

- showroom a predajca strojov
- servisné miesto
- poskytovateľ požičovne a motoškoly
- zároveň e-shop s doplnkovým sortimentom

## Navrhované sekcie

### 1. Hero

Úloha:

- okamžite povedať, čo APC je
- ukázať hlavné vstupy do webu
- nasmerovať používateľa na stroje, servis, požičovňu alebo kontakt

Obsah:

- hlavný headline:
  - treba dopísať
  - pracovný návrh: `Showroom, servis a stroje pre jazdu bez kompromisov`
- subheadline:
  - pracovný návrh: `APC Shop v Bardejove spája predaj štvorkoliek, motocyklov, servis, požičovňu a motoškolu na jednom mieste.`
- CTA 1:
  - `Pozrieť stroje`
- CTA 2:
  - `Objednať servis`

Zdroj:

- faktický základ zo scraped homepage, servisu a kontaktných údajov
- headline je zatiaľ návrh

### 2. Quick Entry Grid

Úloha:

- spraviť z homepage orientačný rozcestník

Karty:

- Štvorkolky
- Motocykle
- Auto-moto kozmetika
- Oblečenie a prilby
- Náhradné diely
- Bazár
- Požičovňa
- Servis

Zdroj:

- potvrdené zo scraped homepage

Template fit:

- Boxcar category / inventory cards

### 3. APC V Kocke

Úloha:

- krátko vysvetliť, prečo je APC dôveryhodné

Obsah:

- showroom v Bardejove
- predaj strojov a výbavy
- servis motocyklov, skútrov, ATV, UTV a side-by-side
- požičovňa a motoškola

Pracovný text:

`APC je miesto, kde si vyberiete stroj, vybavíte servis, požičiate techniku a zlepšíte jazdu. V Bardejove spájame predaj, servis a jazdecké služby do jedného funkčného showroomu.`

Zdroj:

- kombinácia scraped servis/kontakt/homepage
- formulácia je návrh, fakty sú podložené

### 4. Hlavné Služby

Úloha:

- ukázať, že APC nie je len e-shop

Karty:

- Servis
  - text: servis motocyklov, skútrov, ATV, UTV a side-by-side, vrátane záručného a pozáručného servisu
- Požičovňa
  - text: krátkodobé požičanie vybraných strojov, momentálne treba doplniť presnejšie podmienky
- Motoškola
  - text: MOTOSAFE kurz bezpečnej jazdy v spolupráci s MOTO-ŠKOLOU Jariabka
- Bazár
  - text: výber jazdených strojov a doplnkový predaj

Zdroj:

- servis a motoškola sú potvrdené
- požičovňa a bazár sú potvrdené navigáciou a štruktúrou webu, text bude treba dopracovať

### 5. Top Kategórie / Stroje

Úloha:

- premostiť prezentačný web s predajom

Odporúčané bloky:

- Štvorkolky
- Motocykle
- UTV / side-by-side
- Príslušenstvo a diely

Poznámka:

- na starej homepage je kategórií veľa, na novej by som ich zredukoval na 4 až 6 najsilnejších vstupov

Zdroj:

- kategórie z homepage a `data_source/eshop/categories.md`

### 6. Servis Highlight

Úloha:

- vytiahnuť servis ako samostatný conversion blok

Obsah:

- servis pre motocykle, skútre, ATV, UTV a side-by-side
- záručný a pozáručný servis
- pneuservis
- kontakt na servis:
  - Patrik
  - `+421 948 058 400`

CTA:

- `Objednať servis`

Zdroj:

- priamo zo scraped stránky `servis`

### 7. Motoškola Highlight

Úloha:

- odlíšiť APC od čisto predajných webov

Obsah:

- MOTOSAFE kurz bezpečnej jazdy
- spolupráca s MOTO-ŠKOLOU Jariabka
- pre začiatočníkov aj pokročilých
- cena podľa súčasného webu:
  - `159 € s DPH`

CTA:

- `Zistiť viac o motoškole`

Zdroj:

- priamo zo scraped stránky `motoskola`

### 8. Benefity

Úloha:

- dodať rýchle dôvody na dôveru

Položky potvrdené z homepage:

- Expedícia do 24 hodín od objednania
- Doprava nad 100 € zadarmo
- Individuálny prístup k zákazníkovi

Poznámka:

- treba zvážiť, či tieto tri body nechceme mierne preformulovať do konzistentnejšieho štýlu

### 9. Blog / Novinky

Úloha:

- ukázať, že APC žije aj mimo katalógu

Odporúčanie:

- zobraziť 3 posledné alebo najrelevantnejšie články

Silné kandidáty:

- `INDIAN MOTORCYCLE UŽ AJ NA VÝCHODE`
- `Segway FUGLEMAN UT10 X`
- cashback / promo články len ak sú ešte relevantné

Zdroj:

- `data_source/scraped/apcshop/blog_posts.json`

### 10. Kontakt A Showroom

Úloha:

- uzavrieť homepage praktickými údajmi

Obsah:

- ALFA PRO CONCEPT s.r.o.
- Duklianska 4340, 085 01 Bardejov
- `info@apcshop.eu`
- `+421 918 678 678`
- Po - Pia `8:00 - 17:00`
- So - Ne `Zatvorené`

CTA:

- `Kontaktovať APC`
- `Zobraziť na mape`

Zdroj:

- scraped kontakt + obchodné podmienky

## Sekcie, ktoré možno vynechať

Ak bude homepage príliš dlhá, ako prvé by som škrtol:

- samostatný bazár blok
- samostatný blog blok

Servis a motoškola by som ponechal, lebo robia APC odlišným.

## Mapovanie na existujúci Boxcar template

Najlepšia pracovná skladba:

- Hero: `index.html` hero / banner pattern
- Quick entry grid: category cards z homepage variánt
- Služby a benefity: icon cards / feature blocks
- Top kategórie alebo stroje: inventory cards
- Blog: blog-list cards
- Kontakt: contact / CTA block

## Čo ešte chýba pred implementáciou

- finálny headline a tone of voice
- rozhodnutie, ktoré značky chceme ukázať na homepage
- výber 4 až 8 konkrétnych strojov alebo kategórií
- rozhodnutie, či homepage bude viac prezentačná alebo viac predajná

## Praktický ďalší krok

Pri implementácii do template odporúčam ísť v tomto poradí:

1. hero
2. quick entry grid
3. služby
4. servis highlight
5. motoškola highlight
6. benefity
7. blog
8. kontakt
