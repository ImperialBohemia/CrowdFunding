# Kompletní manuál: Crowdfunding a návrat dětí do rodiny

## 1. Porovnání klíčových platforem

| Vlastnost | Znesnáze21 | Donio.cz | Zahraniční (WhyDonate, 4fund) |
| :--- | :--- | :--- | :--- |
| **Poplatek platformy** | 4 % z vybrané částky | **0 %** (100 % jde žadateli) | 0 % až 4 % + karetní poplatky |
| **Ochrana před exekucí** | **Garantovaná:** standardně platí faktury pronajímateli | **Možná:** nutno domluvit na `pribehy@donio.cz` | **Žádná:** posílají na účet (exekutor zabaví) |
| **Nevybrání 100 % cíle** | Vyplácí celou vybranou částku | Vyplácí celou vybranou částku | Vyplácí celou vybranou částku |
| **Podpora a asistence** | Sociální pracovníci, právní poradenství | Uživatelská podpora, editace příběhu | Pouze technická podpora v EN |
| **Doporučení** | **Vítěz při exekuci a složité sociální situaci** | **Vítěz při potřebě maximalizace částky (0 %)** | **Nedoporučeno pro tuto situaci** |

---

## 2. Ochrana financí před exekucí a úřady

* **Zákaz výplaty na osobní účet:** Exekutor v ČR okamžitě obstaví jakoukoliv příchozí platbu.
* **Přímá úhrada třetí osobě:**
  * Kauce a nájem: Platforma posílá peníze přímo na účet pronajímatele.
  * Vybavení bytu: Platforma proplácí zálohové faktury obchodů (IKEA, Jysk apod.).
* **Daně:** Výtěžek sbírky je osvobozen od daně z příjmů (§ 4a zákona o daních z příjmů).
* **Úřad práce (dávky):** Přímá úhrada majiteli bytu se nepočítá jako příjem žadatele.

---

## 3. Souběh s pomocí od státu (Úřad práce)

* **Mimořádná okamžitá pomoc (MOP) na kauci:**
  * Jednorázová dávka hmotné nouze přímo na zaplacení kauce na byt.
  * Lze žádat na pobočce Úřadu práce ČR s návrhem nájemní smlouvy.
* **Příspěvek na bydlení:**
  * Nároková dávka po podpisu nájemní smlouvy a nastěhování.
  * Hradí podstatnou část nákladů na nájem a energie.

---

## 4. Požadavky OSPOD a soudu pro zrušení ústavní výchovy

* **Právní rámec:** Dle judikatury ÚS nesmí být děti v ústavu jen z důvodu chudoby.
* **Kritéria pro návrat dětí:**
  1. **Platná nájemní smlouva:** Byt s odpovídající kapacitou (min. 1 rok).
  2. **Vybavení pro děti:** Každé dítě musí mít vlastní postel, lůžkoviny a psací stůl.
  3. **Hygienické zázemí:** Funkční vytápění, teplá voda, lednice, sporák, pračka.
  4. **Pravidelný příjem:** Doložení práce, brigády nebo schválených sociálních dávek.
  5. **Spolupráce s OSPOD:** Účast na případových konferencích a souhlasné stanovisko kurátora.
* **Procesní krok:** Podání návrhu k okresnímu soudu na zrušení ústavní výchovy (§ 973 OZ).

---

## 5. Položkový rozpočet pro sbírku

* **Jistota (kauce):** 1–2 měsíční nájmy (cca 25 000 – 40 000 Kč).
* **První nájemné předem:** 1 měsíční nájem (cca 15 000 – 20 000 Kč).
* **Postele a matrace pro děti:** 8 000 – 15 000 Kč.
* **Základní spotřebiče (pračka, lednice):** 10 000 – 15 000 Kč.
* **Školní a osobní potřeby dětí:** 5 000 – 10 000 Kč.
* **Doporučená cílová částka sbírky:** **70 000 – 100 000 Kč**.

---

## 6. Postup založení sbírky krok za krokem

1. **Příprava úředních dokladů:**
   * Usnesení / rozsudek soudu (odůvodnění umístění z důvodu bydlení).
   * Individuální plán ochrany dítěte (IPOD) nebo zpráva OSPOD.
   * Občanský průkaz žadatele.
2. **Zajištění bydlení:** Získat písemný návrh nájemní smlouvy s vyčíslením kauce.
3. **Založení sbírky:** Nahrání formuláře na Znesnáze21 nebo Donio s doložením dokumentů.
4. **Nastavení přímé platby:** Požadavek na úhradu kauce přímo pronajímateli.
5. **Spuštění a medializace:** Okamžité sdílení a informování sociálního kurátora.



---

## 7. Nástroje pro monitoring a vyhledávání nájemních bytů

Repozitář obsahuje automatizované skripty pro hledání pronájmů přímo od majitelů bez provizí realitním kancelářím:

* **Přímý vyhledávač Bezrealitky.cz:**
  ```bash
  python3 scripts/find_bezrealitky.py --location Praha --max-price 18000
  ```
* **Multisearch agregátor (Bezrealitky + Domonaut API + Bazoš):**
  ```bash
  python3 scripts/multisearch_rentals.py --max-price 15000 --limit 10
  ```

---

* **Kompletní manuál psychologie a textu:** [PSYCHOLOGIE_A_STRATEGIE.md](file:///home/q/CrowdFunding/PSYCHOLOGIE_A_STRATEGIE.md)

