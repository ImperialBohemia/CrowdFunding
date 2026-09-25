# Nasazení testovacích kampaní Sklik: Obytné přívěsy & Návěsy

**Účet:** `horoskopie.cz@email.cz` (`697549`)  
**Datum auditu a čištění:** 2026-09-14  
**Výsledek hloubkového čištění:**
- **Kampaně:** V celém účtu existují **pouze 2 nesmazané kampaně** (nově vytvořené).
- **Sestavy:** V celém účtu existují **pouze 4 nesmazané sestavy** (2 ve vyhledávání, 2 v obsahu). Všech 213 starých osiřelých sestav bylo přes API smazáno (`groups.remove`).
- **Reklamy:** V celém účtu existuje **pouze 6 nesmazaných inzerátů** (4 ETA inzeráty ve vyhledávání, 2 kombinované v obsahu). Všech 242 starých inzerátů bylo přes API smazáno (`ads.remove`).
- **Klíčová slova:** V celém účtu existuje **pouze 16 pozitivních klíčových slov**. Všech 130 starých klíčových slov bylo smazáno (`keywords.remove`).

---

## 1. Aktuální stav živých entit v účtu

| Entita | Aktivní / Pozastavené (Nesmazané) | Smazané historické |
|---|---|---|
| **Kampaně** | **2** | 69 |
| **Sestavy** | **4** | 213 |
| **Reklamy** | **6** | 242 |
| **Klíčová slova** | **16** | 130 |

---

## 2. Vyhledávací kampaň (Search)

- **Název:** `[TEST] Obytné přívěsy & Návěsy | Vyhledávání`
- **ID kampaně:** `7958963`
- **Denní rozpočet:** 50 Kč (`5000` haléřů)
- **Typ:** `fulltext`
- **Stav:** `suspend`

### Sestava 1: `Obytné přívěsy & Karavany`
- **ID sestavy:** `176558387`
- **Výchozí CPC:** 4,50 Kč (`450` haléřů)
- **Klíčová slova (Pozitivní):**
  - `[obytné přívěsy]` (exact)
  - `"obytné přívěsy"` (phrase)
  - `[obytný přívěs prodej]` (exact)
  - `"obytný přívěs prodej"` (phrase)
  - `[obytný přívěs celoroční]` (exact)
  - `"obytný přívěs celoroční"` (phrase)
  - `[obytný návěs]` (exact)
  - `"obytný návěs"` (phrase)
  - `[luxusní karavan celoroční]` (exact)
- **Vylučující slova (Negativní):**
  - `nejlevnější`, `daruji`, `vrak`, `na nářadí`, `včelín`, `ubytování na víkend`, `model 1:43` (shoda `negativeBroad`)
- **Inzeráty (Rozšířené textové - ETA):**
  - **Ad 1 (ID `704923642`):**
    - Titulek 1: *Obytné Přívěsy & Návěsy*
    - Titulek 2: *Celoroční Luxus bez Povolení*
    - Titulek 3: *Česká Výroba Orličan*
    - Popis 1: *23 m² obytné plochy, 60mm PUR izolace a soběstačný off-grid systém. Prohlédněte model.*
    - Popis 2: *Žijte na svém pozemku ihned bez stavebního řízení. Konfigurátor a kalkulace online.*
    - Cesta: `/obytne/privesy` | URL: `https://horoskopie.cz/`
  - **Ad 2 (ID `704923641`):**
    - Titulek 1: *Luxusní Obytný Návěs N-10S*
    - Titulek 2: *Alternativa k Tiny House*
    - Titulek 3: *Nezávislost na Pozemku*
    - Popis 1: *Armádní odolnost a moderní komfort. Vyvýšená ložnice, koupelna a rekuperace vzduchu.*
    - Popis 2: *Rezervujte si výrobní slot pro sezónu. Kompletní specifikace a ceník najdete na webu.*
    - Cesta: `/orlican/modely` | URL: `https://horoskopie.cz/`

### Sestava 2: `Celoroční maringotky & Tiny House`
- **ID sestavy:** `176558388`
- **Výchozí CPC:** 5,00 Kč (`500` haléřů)
- **Klíčová slova (Pozitivní):**
  - `[celoroční maringotka]` (exact)
  - `"celoroční maringotka"` (phrase)
  - `[maringotka k trvalému bydlení]` (exact)
  - `"maringotka k trvalému bydlení"` (phrase)
  - `[tiny house na podvozku]` (exact)
  - `"tiny house na podvozku"` (phrase)
  - `[mobilní dům celoroční zateplený]` (exact)
- **Vylučující slova (Negativní):**
  - `nejlevnější`, `daruji`, `vrak`, `na nářadí`, `včelín`, `ubytování na víkend`, `model 1:43` (shoda `negativeBroad`)
- **Inzeráty (Rozšířené textové - ETA):**
  - **Ad 1 (ID `704923640`):**
    - Titulek 1: *Celoroční Bydlení na Pozemku*
    - Titulek 2: *Tiny House na Podvozku N-10S*
    - Titulek 3: *Bez Stavebního Povolení*
    - Popis 1: *Masivní izolace do mrazu i veder. Plně vybavená kuchyň, koupelna a solární systém.*
    - Popis 2: *Vyhněte se stavebnímu povolení. Podívejte se na virtuální prohlídku a kalkulátor ceny.*
    - Cesta: `/tiny-house/celorocni` | URL: `https://horoskopie.cz/`
  - **Ad 2 (ID `704923639`):**
    - Titulek 1: *Maringotka k Trvalému Bydlení*
    - Titulek 2: *Zateplený Návěs Orličan*
    - Titulek 3: *Kompletní Vybavení na Klíč*
    - Popis 1: *23 m² čisté obytné plochy. Nezávislé topení, fotovoltaika, rekuperace a moderní design.*
    - Popis 2: *Poptat výrobní slot a prohlídku hotového kusu. Více informací a kalkulace na webu.*
    - Cesta: `/maringotka/zateplena` | URL: `https://horoskopie.cz/`

### Rozšíření o Sitelinky (Přiřazeno ke kampani `7958963`):
1. **Kalkulátor ceny** (ID `4442844`): `https://horoskopie.cz/#kalkulator`
2. **Technická specifikace** (ID `4442845`): `https://horoskopie.cz/#anatomie`
3. **Využití a varianty** (ID `4442846`): `https://horoskopie.cz/#vyuziti`
4. **Poptat výrobní slot** (ID `4442847`): `https://horoskopie.cz/`

---

## 3. Obsahová kampaň (Display / In-Market)

- **Název:** `[TEST] Obytné přívěsy & Návěsy | Obsahová síť`
- **ID kampaně:** `7958964`
- **Denní rozpočet:** 50 Kč (`5000` haléřů)
- **Typ:** `context`
- **Stav:** `suspend`

### Sestava 1: `Záměry | Karavany a obytné automobily`
- **ID sestavy:** `176558414`
- **Výchozí CPC:** 2,50 Kč (`250` haléřů)
- **Cílení (In-Market Intent):**
  - Kategorie: *Karavany a obytné automobily* (ID `10245`, velikost publika v ČR: 40 798 uživatelů)
  - Intent ID: `19020035`
- **Inzerát (Kombinovaná reklama - ID `704923666`):**
  - Krátký titulek: *Obytné Přívěsy N10S*
  - Dlouhý titulek: *Celoroční soběstačné bydlení na pozemek bez stavebního řízení.*
  - Popis: *23 m² čistého luxusu, 60mm PUR izolace a kompletní soběstačnost. Zjistěte více.*
  - Název firmy: *Orličan Overland*
  - Obrázky: Obdélníkový (ID `8335874`, 1280x671) + Čtvercový (ID `8335871`, 738x738)
  - Cílová URL: `https://horoskopie.cz/`

### Sestava 2: `Záměry | Přívěsy a návěsy`
- **ID sestavy:** `176558415`
- **Výchozí CPC:** 2,00 Kč (`200` haléřů)
- **Cílení (In-Market Intent):**
  - Kategorie: *Přívěsy a návěsy* (ID `10277`, velikost publika v ČR: 7 052 uživatelů)
  - Intent ID: `19020036`
- **Inzerát (Kombinovaná reklama - ID `704923665`):**
  - Krátký titulek: *Zrenovovaný Návěs N10S*
  - Dlouhý titulek: *Armádní konstrukce předělaná na soběstačný celoroční domov.*
  - Popis: *Odolné zateplení, solární napájení a nezávislost na sítích. Prohlédněte specifikaci.*
  - Název firmy: *Orličan Overland*
  - Obrázky: Obdélníkový (ID `8335874`, 1280x671) + Čtvercový (ID `8335871`, 738x738)
  - Cílová URL: `https://horoskopie.cz/`
