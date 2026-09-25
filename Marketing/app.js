/**
 * ORLIČAN OVERLAND & LIVING - MASTER INTERACTIVE ENGINE
 * High-performance, zero external dependencies, 10 deep-content articles, search & filtering
 */

document.addEventListener('DOMContentLoaded', () => {
  initLanguageSwitcher();
  initBlueprintHotspots();
  initConfigurator();
  initBlogFilterAndSearch();
  initArticleModals();
  initLeadModal();
});

/* ==========================================================================
   1. BILINGUAL DICTIONARY & SWITCHER (CZ / DE)
   ========================================================================== */
const I18N = {
  cz: {
    nav_model: "Koncept N-10S",
    nav_blueprint: "Anatomie",
    nav_worlds: "Využití",
    nav_calc: "Konfigurátor",
    nav_blog: "Magazín (10 článků)",
    nav_cta: "Poptat výrobní slot",
    
    hero_badge: "Originální renovace • Choceň • Izotermický návěs",
    hero_h1_1: "Armádní nezničitelnost.",
    hero_h1_2: "Luxusní soběstačný domov.",
    hero_desc: "Zrenovovaný vojenský skříňový návěs Orličan N-10S. 23 m² čistého obytného prostoru, patentovaná konstrukce s labutím krkem pro vyvýšenou ložnici a nezávislost bez nutnosti stavebního povolení.",
    hero_btn_explore: "Prozkoumat model N-10S",
    hero_btn_calc: "Kalkulátor ceny",
    
    metric_area_val: "23 m²",
    metric_area_lbl: "Obytná plocha",
    metric_insul_val: "60 mm",
    metric_insul_lbl: "PUR izotermický sendvič",
    metric_power_val: "10 kWh",
    metric_power_lbl: "LiFePO4 soběstačnost",
    metric_legal_val: "0 dní",
    metric_legal_lbl: "Bez stavebního řízení",

    blueprint_tag: "Konstrukční dokonalost",
    blueprint_title: "Anatomie vojenského návěsu Orličan N-10S",
    blueprint_sub: "Proč armádní chladírenská skříň překonává lodní kontejnery i klasické dřevěné maringotky.",

    worlds_tag: "3 Světy využití",
    worlds_title: "Jeden nepřemožitelný základ. Tři způsoby života.",
    worlds_sub: "Ať už hledáte útočiště na samotě, luxusní glamping s rychlou návratností, nebo expediční kolos.",

    calc_tag: "Transparentní kalkulátor",
    calc_title: "Sestavte si svůj Orličan N-10S",
    calc_sub: "Okamžitý výpočet rozpočtu dle požadovaného stupně výbavy.",
    calc_base_title: "Základní zrenovovaná skříň N-10S (9,36 × 2,5 m)",
    calc_base_desc: "Kompletně ošetřený a nalakovaný návěs (RAL 6031), izotermické panely, nová okna, sklopné schůdky, opěrné nohy.",
    
    blog_tag: "Odborný magazín",
    blog_title: "Průvodce soběstačným bydlením a expedicemi",
    blog_sub: "10 do hloubky zpracovaných témat: technická fakta, právní analýza pro ČR i Německo, energetické bilance a expedice.",

    cta_banner_title: "Máte pozemek nebo tahač? Rezervujte si prohlídku.",
    cta_banner_desc: "Přijeďte si prohlédnout hotový kus osobně. Vyzkoušejte prostor, ložnici v labutím krku a zkonzultujte dispozici.",
    cta_banner_btn: "Domluvit termín prohlídky"
  },
  de: {
    nav_model: "Konzept N-10S",
    nav_blueprint: "Anatomie",
    nav_worlds: "Einsatzbereiche",
    nav_calc: "Konfigurator",
    nav_blog: "Magazin (10 Artikel)",
    nav_cta: "Produktions-Slot anfragen",

    hero_badge: "Original-Restauration • Isothermer Armee-Kofferauflieger",
    hero_h1_1: "Militärische Härte.",
    hero_h1_2: "Autarker Luxus.",
    hero_desc: "Restaurierter Militär-Wohnauflieger Orlican N-10S. 23 m² Wohnfläche, Schwanenhals-Konstruktion für erhöhtes Schlafzimmer und vollständige Autarkie – ganz ohne Baugenehmigung.",
    hero_btn_explore: "Modell N-10S entdecken",
    hero_btn_calc: "Preis-Rechner",

    metric_area_val: "23 m²",
    metric_area_lbl: "Wohnfläche",
    metric_insul_val: "60 mm",
    metric_insul_lbl: "PUR Isothermer Sandwich",
    metric_power_val: "10 kWh",
    metric_power_lbl: "LiFePO4 Autarkie",
    metric_legal_val: "0 Tage",
    metric_legal_lbl: "Genehmigungsfrei",

    blueprint_tag: "Konstruktive Perfektion",
    blueprint_title: "Anatomie des Militär-Aufliegers Orlican N-10S",
    blueprint_sub: "Warum dieser Armee-Koffer jeden Seecontainer und jeden Bauwagen deklassiert.",

    worlds_tag: "3 Einsatzwelten",
    worlds_title: "Eine unverwüstliche Basis. Drei Lebensformen.",
    worlds_sub: "Ob autarker Rückzugsort auf dem Grundstück, profitables Glamping oder weltweites Expeditionsmobil.",

    calc_tag: "Transparenter Rechner",
    calc_title: "Konfigurieren Sie Ihren Orlican N-10S",
    calc_sub: "Echtzeit-Kalkulation passend zu Ihren Wünschen.",
    calc_base_title: "Restaurierter Basiskoffer N-10S (9,36 × 2,5 m)",
    calc_base_desc: "Vollständig sandgestrahlt und lackiert (RAL 6031), Isolierpaneele, neue Fenster, Einstiegstreppe, Schwerlast-Stützen.",

    blog_tag: "Fachmagazin",
    blog_title: "Leitfaden für autarkes Wohnen & Fernreisen",
    blog_sub: "10 fundierte Leitfäden: Technische Daten, deutsches Baurecht, Energiebilanzen und Expeditionsbau.",

    cta_banner_title: "Haben Sie ein Grundstück oder LKW? Besichtigung vereinbaren.",
    cta_banner_desc: "Besichtigen Sie das fertige Fahrzeug vor Ort. Erleben Sie das Raumgefühl im Schwanenhals und planen Sie Ihren Ausbau.",
    cta_banner_btn: "Besichtigungstermin anfragen"
  }
};

let currentLang = 'cz';

function initLanguageSwitcher() {
  const btns = document.querySelectorAll('.lang-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      const lang = btn.dataset.lang;
      if (lang === currentLang) return;
      
      currentLang = lang;
      btns.forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
      applyLanguage(lang);
    });
  });
}

function applyLanguage(lang) {
  const dict = I18N[lang];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });
  updateCalculatorPrices();
}

/* ==========================================================================
   2. BLUEPRINT HOTSPOT EXPLORER
   ========================================================================== */
function initBlueprintHotspots() {
  const buttons = document.querySelectorAll('.hotspot-btn');
  const cards = document.querySelectorAll('.detail-card');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.target;
      
      buttons.forEach(b => b.classList.remove('active'));
      cards.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      const activeCard = document.getElementById(targetId);
      if (activeCard) {
        activeCard.classList.add('active');
        activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('active'));
      buttons.forEach(b => b.classList.remove('active'));

      card.classList.add('active');
      const matchingBtn = document.querySelector(`.hotspot-btn[data-target="${card.id}"]`);
      if (matchingBtn) matchingBtn.classList.add('active');
    });
  });
}

/* ==========================================================================
   3. INTERACTIVE CONFIGURATOR & PRICING
   ========================================================================== */
const BASE_PRICE_CZK = 880000;
const CZK_TO_EUR_RATE = 25.0;

function initConfigurator() {
  const checkboxes = document.querySelectorAll('.calc-option input[type="checkbox"]');
  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      const parent = cb.closest('.calc-option');
      parent.classList.toggle('selected', cb.checked);
      updateCalculatorPrices();
    });
  });
  updateCalculatorPrices();
}

function updateCalculatorPrices() {
  let totalCZK = BASE_PRICE_CZK;
  const listContainer = document.getElementById('summaryAddonsList');
  if (!listContainer) return;
  listContainer.innerHTML = '';

  const checkboxes = document.querySelectorAll('.calc-option input[type="checkbox"]:checked');
  
  checkboxes.forEach(cb => {
    const price = parseInt(cb.dataset.price, 10);
    const title = cb.dataset.nameCz && currentLang === 'cz' ? cb.dataset.nameCz : cb.dataset.nameDe;
    totalCZK += price;

    const li = document.createElement('li');
    li.className = 'summary-item';
    li.innerHTML = `
      <span class="label">${title}</span>
      <span class="value">+${formatPrice(price, 'CZK')}</span>
    `;
    listContainer.appendChild(li);
  });

  const totalEUR = Math.round(totalCZK / CZK_TO_EUR_RATE);
  
  const elCZK = document.getElementById('totalPriceCZK');
  const elEUR = document.getElementById('totalPriceEUR');
  
  if (elCZK) elCZK.textContent = formatPrice(totalCZK, 'CZK');
  if (elEUR) elEUR.textContent = `≈ ${formatPrice(totalEUR, 'EUR')}`;
}

function formatPrice(amount, currency) {
  if (currency === 'CZK') {
    return amount.toLocaleString('cs-CZ') + ' Kč';
  } else {
    return '€ ' + amount.toLocaleString('de-DE');
  }
}

/* ==========================================================================
   4. FULL 10 DEEP ARTICLES DATABASE
   ========================================================================== */
const ARTICLES = {
  1: {
    category: "konstrukce",
    badge: "Konstrukční srovnání",
    date: "12. Září 2026 • 7 min čtení",
    title: "Orličan N-10S vs. Lodní kontejner: Proč armádní sendvič vyhrává na celé čáře",
    takeaway: "Lodní kontejner je ocelová bedna na přepravu rudy; Orličan je armádní izotermický operační sál s nulovými tepelnými mosty a 6t podvozkem.",
    content: `
      <h3>Mýtus o levných lodních kontejnerech</h3>
      <p>Mnoho lidí začíná svůj sen o alternativním bydlení myšlenkou na 20ft nebo 40ft lodní kontejner. Realita na stavbě je však drsná: ocelový kontejner je konstruován pro přepravu nákladu, nikoliv pro lidi. Trpí brutálními tepelnými mosty, v létě funguje jako pec a v zimě v něm kondenzují litry vody přímo za izolací, což vede k neviditelné hnilobě a korozi nosného plechu.</p>
      
      <h3>Tajemství sendvičové technologie Orličan Choceň</h3>
      <p>Československý vojenský návěs <strong>Orličan N-10S</strong> byl vyvinut armádou jako pojízdná velitelská stanice, chladírna a polní operační sál. To znamenalo jediné: absolutní požadavek na tepelnou stabilitu za teplot od -40 °C do +50 °C.</p>
      <ul>
        <li><strong>60 mm polyuretanové izotermické jádro:</strong> Vstřikováno pod tlakem mezi kompozitní pláště. Nulové tepelné mosty po celém obvodu.</li>
        <li><strong>Labutí krk (Gooseneck):</strong> Poskytuje přirozeně vyvýšený prostor pro manželskou ložnici (Master Bedroom), pod kterým venku vzniká chráněná terasa na posezení nebo parkování čtyřkolky.</li>
        <li><strong>Nulová koroze nosné skříně:</strong> Materiály nepodléhají rzi a degradaci jako plechové kontejnery.</li>
      </ul>

      <h3>Ekonomická bilance po dokončení</h3>
      <p>Když k pořizovací ceně lodního kontejneru připočtete vyřezání oken, navaření ztužujících rámů, nástřik PUR pěny, vyrovnání stěn a stavbu základových patek, dostáváte se na částku přes 650 000 Kč – a stále máte ocelovou bednu bez kol. Zrenovovaný Orličan N-10S za 880 000 Kč nabízí hotový zateplený prostor na kolech, který lze kdykoliv převézt nebo prodat dál bez ztráty hodnoty.</p>
    `
  },
  2: {
    category: "pravo",
    badge: "Právo & Legislativa",
    date: "8. Září 2026 • 9 min čtení",
    title: "Bydlení v návěsu bez stavebního povolení: Kompletní rozbor pro ČR a Německo",
    takeaway: "Návěs spočívající na vlastních kolech a mechanických nohách bez pevných základů je mobilním vozidlem, nikoliv pevnou stavbou.",
    content: `
      <h3>Jak se dívá stavební zákon na obytný návěs na pozemku?</h3>
      <p>Jedna z nejčastějších otázek našich zákazníků zní: <em>„Mohu Orličan N-10S postavit na louku, zahradu nebo parcelu mimo zastavitelné území bez zdlouhavého stavebního řízení?“</em></p>
      
      <h3>Právní status v České republice</h3>
      <p>Návěs Orličan N-10S je z hlediska zákona <strong>mobilním přípojným vozidlem</strong> opatřeným technickým průkazem nebo výrobním štítkem. Pokud spočívá na svých kolech a výsuvných nohách a není pevně spojen se zemí základovou deskou či piloty, nejedná se o stavbu v klasickém smyslu stavebního zákona.</p>
      <ul>
        <li><strong>Žádná základová deska:</strong> Díky masivním mechanickým opěrným nohám nepotřebujete betonovat základ. Návěs stojí stabilně na roznášecích dřevěných či ocelových deskách.</li>
        <li><strong>Off-Grid přípojky:</strong> Využití solárního systému a vnitřních nádrží na vodu eliminuje nutnost pevných inženýrských přípojek, které by mohly být předmětem územního souhlasu.</li>
      </ul>

      <h3>Specifika pro Německo (Baugenehmigungsfrei in DE)</h3>
      <p>V Německu platí specifická pravidla jednotlivých spolkových zemí (Landesbauordnung). Bydlení v maringotce či návěsu (*Wohnen im Bauwagen / Tiny House auf Rädern*) je v mnoha regionech (např. v Bavorsku na venkovských usedlostech) posuzováno jako dočasné umístění mobilního prostředku (*fliegender Bau*).</p>
    `
  },
  3: {
    category: "offgrid",
    badge: "Technologie & Baterie",
    date: "1. Září 2026 • 6 min čtení",
    title: "Solární nezávislost v podvozku: Jak napájet 23 m² celoročně ze slunce",
    takeaway: "Integrací LiFePO4 banky do spodních schrán ušetříte 2 m² vnitřního prostoru a udržíte těžiště nízko pro stabilitu.",
    content: `
      <h3>Proč neplýtvat obytným prostorem pro technologii</h3>
      <p>U běžných Tiny House zabírají baterie, měniče a bojlery cenné metry uvnitř skříně. Orličan N-10S má obrovskou výhodu v <strong>originálních podpodlahových schránkách</strong>.</p>
      
      <h3>Architektura systému Victron Energy:</h3>
      <ul>
        <li><strong>Bateriové úložiště:</strong> LiFePO4 články s kapacitou 10,2 kWh (48V systém), vyhřívané pro bezproblémový provoz v mrazech do -25 °C.</li>
        <li><strong>Solární pole:</strong> 1 200 Wp v celočerných monokrystalických panelech na střeše s MPPT regulátorem Victron SmartSolar.</li>
        <li><strong>Měnič / Nabíječ:</strong> Victron MultiPlus-II 48/5000VA s čistou sinusovkou, schopný napájet indukční desku i espresso kávovar současně.</li>
        <li><strong>Rekuperace:</strong> Decentrální jednotka s keramickým entalpickým výměníkem pro stálou výměnu vzduchu bez tepelných ztrát a bez rosení oken.</li>
      </ul>
      <p>Tento systém zaručuje nepřetržitý provoz lednice, osvětlení, notebooků, čerpadla vody i rekuperace od března do října na 100 % ze slunce.</p>
    `
  },
  4: {
    category: "expedice",
    badge: "Expedice & 4x4 / 6x6",
    date: "25. Srpna 2026 • 8 min čtení",
    title: "Tatra 815 6x6 + N-10S: Průvodce stavbou expediční soupravy kolem světa",
    takeaway: "Tatrovácký páteřový rám absorbuje terénní rázy a chrání návěs; výměnný koncept umožňuje odpojit základnu a prozkoumávat terén jen tahačem.",
    content: `
      <h3>Kombinace tatrováckého podvozku a chladírenské skříně</h3>
      <p>Pro náročné dálkové cestovatele, kteří míří do Střední Asie, na Island nebo do afrických pouští, představuje souprava tahače <strong>Tatra 815 6x6</strong> a obytného návěsu Orličan N-10S vrchol technické odolnosti.</p>
      <ul>
        <li><strong>Výkyvné polonápravy Tatry:</strong> Legendární páteřový rám absorbuje veškeré torzní kroucení v terénu, takže do točny návěsu se nepřenášejí destruktivní rázy.</li>
        <li><strong>Výměnný koncept:</strong> Na rozdíl od pevné vestavby na nákladním autě můžete návěs kdekoliv v kempu či základním táboře odpojit na opěrné nohy a samotným tahačem vyrazit na nákup či průzkum těžkého terénu.</li>
        <li><strong>Standardní točna 2\":</strong> Umožňuje zapřažení za jakýkoliv vojenský či civilní tahač (Tatra, MAN KAT1, Mercedes Actros 4x4 / 6x6).</li>
      </ul>
    `
  },
  5: {
    category: "glamping",
    badge: "Glamping & Investice",
    date: "18. Srpna 2026 • 5 min čtení",
    title: "Glamping byznys plán: Výpočet návratnosti při sazbě 3 800 Kč za noc",
    takeaway: "S konzervativní 45% obsazeností generuje jednotka roční čistý zisk 483 000 Kč s návratností 2,6 roku.",
    content: `
      <h3>Zážitkové ubytování láká na autenticitu a vojenský minimalismus</h3>
      <p>Zatímco trh s běžnými dřevěnými chatkami je přesycený, zrenovovaný armádní návěs s luxusním dubovým interiérem a ložnicí v labutím krku je virální magnet na sociálních sítích.</p>
      
      <h3>Modelový finanční plán pro 1 jednotku:</h3>
      <ul>
        <li><strong>Pořizovací investice:</strong> 880 000 Kč (návěs) + 380 000 Kč (vestavba) = 1 260 000 Kč.</li>
        <li><strong>Průměrná cena za noc:</strong> 3 800 Kč (víkendy a sezóna až 4 500 Kč).</li>
        <li><strong>Obsazenost:</strong> Konzervativních 45 % (164 nocí v roce).</li>
        <li><strong>Roční hrubý příjem:</strong> 164 × 3 800 Kč = <strong>623 200 Kč</strong>.</li>
        <li><strong>Provozní náklady (úklid, praní, dřevo, marketing):</strong> cca 140 000 Kč / rok.</li>
        <li><strong>Čistý roční zisk:</strong> ~483 000 Kč.</li>
      </ul>
      <p><strong>Doba návratnosti investice: 2,6 roku.</strong> Zůstatková hodnota návěsu navíc v čase neklesá – armádní technika v tomto stavu si drží hodnotu lépe než běžná nemovitost.</p>
    `
  },
  6: {
    category: "offgrid",
    badge: "Technologie & Mikroklima",
    date: "14. Srpna 2026 • 6 min čtení",
    title: "Decentrální rekuperace vs. Vlhkost: Proč v zatepleném návěsu nezamrzá vzduch",
    takeaway: "Keramický entalpický výměník vrací zpět až 88 % tepla a udržuje vlhkost vzduchu na optimálních 45–50 %.",
    content: `
      <h3>Problém hermeticky uzavřených malých prostor</h3>
      <p>Protože izotermický plášť Orličan N-10S má absolutně nulovou prodyšnost (žádné netěsnosti), dýchání dvou dospělých osob vyprodukuje během noci až 1,5 litru vodní páry. Bez řízeného větrání by se vlhkost srážela na sklech oken a vytvářela těžký vzduch s vysokou hladinou CO2.</p>
      
      <h3>Řešení: Dvojice synchronizovaných jednotek s keramickým jádrem</h3>
      <ul>
        <li><strong>70sekundový cyklus odtahu:</strong> Teplý vydýchaný vzduch z interiéru proudí přes keramický akumulátor, který absorbuje jeho teplo.</li>
        <li><strong>70sekundový cyklus přívodu:</strong> Ventilátor změní směr, nasává čerstvý studený vzduch zvenčí, který se ohřívá od nahřáté keramiky. Účinnost zpětného zisku tepla je až 88 %.</li>
        <li><strong>Automatická regulace vlhkosti:</strong> Čidlo samo zvýší otáčky při vaření nebo po sprchování.</li>
      </ul>
    `
  },
  7: {
    category: "konstrukce",
    badge: "Výroba & Řemeslo",
    date: "9. Srpna 2026 • 8 min čtení",
    title: "Renovace vojenského návěsu krok za krokem: Od vojenského skladu po hotový luxus",
    takeaway: "Pískování korundem, antikorozní epoxidový základ a polyuretanový finiš RAL 6031 garantují 30letou životnost rámu.",
    content: `
      <h3>Výběr armádních uloženek</h3>
      <p>Základem každé naší stavby je pečlivě vybraný návěs Orličan N-10S z armádních rezervních skladů, který nestál desetiletí na dešti. Hledáme kusy s nepoškozenými sendvičovými panely a zdravým podvozkem.</p>
      
      <h3>Průběh dílenské renovace:</h3>
      <ul>
        <li><strong>1. Fáze: Odstrojení a otryskání:</strong> Rám podvozku je kompletně otryskán korundem na čistý kov Sa 2,5.</li>
        <li><strong>2. Fáze: Třívrstvý nátěrový systém:</strong> Silnovrstvý zinkový epoxidový základ + dvousložkový polyuretanový vrchní lak v armádním polomatném odstínu RAL 6031.</li>
        <li><strong>3. Fáze: Revize podvozku a brzd:</strong> Výměna brzdových válců, rozvodů vzduchu, repasované mechanické opěrné nohy s novými ložisky.</li>
        <li><strong>4. Fáze: Montáž termoizolačních oken:</strong> Vyfrézování přesných otvorů a osazení oken s trojsklem a hliníkovými rámy s přerušeným tepelným mostem.</li>
      </ul>
    `
  },
  8: {
    category: "expedice",
    badge: "Test & Zima",
    date: "2. Srpna 2026 • 7 min čtení",
    title: "Zimní test v -25 °C v Alpách: Spotřeba a tepelná bilance návěsu",
    takeaway: "Díky 60mm PUR izolaci stačí dieselovému topení 2 kW výkonu pro udržení +22 °C uvnitř při spotřebě pouhých 2,4 litru nafty za 24 hodin.",
    content: `
      <h3>Extrémní zimní zkouška v nadmořské výšce 1 800 m n. m.</h3>
      <p>V lednu jsme vzali hotový kus Orličan N-10S do rakouských Alp na týdenní pobyt v teplotách klesajících v noci k -25 °C. Cílem bylo změřit reálné tepelné ztráty, chování lithiových baterií a spotřebu paliva.</p>
      
      <h3>Výsledky měření:</h3>
      <ul>
        <li><strong>Spotřeba nafty:</strong> Nezávislé teplovzdušné topení Autoterm 4 kW běželo na nízký výkon (cca 1,8 kW). Za 24 hodin spálilo 2,4 až 2,8 litru motorové nafty.</li>
        <li><strong>Teplota podlahy:</strong> Díky zateplenému sendviči a sálavému teplu měla podlaha příjemných 19 °C bez nutnosti zapínat elektrické rohože.</li>
        <li><strong>Vyhřívání baterií:</strong> Podpodlahová schránka s LiFePO4 bateriemi byla temperována malým 12V topným tělískem, takže teplota článků neklesla pod +10 °C (nutné pro nabíjení).</li>
      </ul>
    `
  },
  9: {
    category: "pravo",
    badge: "Homologace & Export",
    date: "28. Července 2026 • 6 min čtení",
    title: "LKW Wohnauflieger v Německu: TÜV, § 21 StVZO a export do DACH regionu",
    takeaway: "Návěs má originální štítek výrobce Orličan Choceň, což umožňuje bezproblémové individuální schválení v Německu (Einzelbetriebserlaubnis).",
    content: `
      <h3>Proč němečtí zákazníci tolik vyhledávají české vojenské návěsy</h3>
      <p>V Německu je kategorie <em>LKW Wohnauflieger</em> obrovským hitem, ale německé manufaktury účtují za podobné stavby částky začínající na 120 000 EUR. Český zrenovovaný Orličan N-10S představuje bezkonkurenční poměr ceny a kvality.</p>
      
      <h3>Legislativní postup pro registraci v DE:</h3>
      <ul>
        <li><strong>Dovozová technická kontrola (§ 21 StVZO):</strong> Zkouška brzdové soustavy na válcové zkušebně, kontrola osvětlení a čepu točny.</li>
        <li><strong>Klasifikace Wohnmobil:</strong> Zápis do německého technického průkazu jako <em>Sonder-Kfz Wohnmobil</em>, což přináší výhodné pojištění a osvobození od mýta pro soukromé účely.</li>
        <li><strong>Prodej jako stacionární objekt:</strong> Pro zákazníky, kteří návěs usadí na soukromý pozemek v Bavorsku, není registrace na značky vůbec nutná – návěs je přepraven na převozních značkách nebo podvalníku.</li>
      </ul>
    `
  },
  10: {
    category: "offgrid",
    badge: "Soběstačnost & Sanita",
    date: "20. Července 2026 • 6 min čtení",
    title: "Off-Grid voda a toaleta bez chemie: Separační vs. Spalovací toaleta Cinderella",
    takeaway: "Suchá separační toaleta šetří až 35 litrů vody denně a umožňuje fungovat 4 týdny bez nutnosti vývozu jímky.",
    content: `
      <h3>Jak vyřešit hygienu na pozemku bez kanalizace</h3>
      <p>U mobilního bydlení je největší výzvou hospodaření s vodou a odpadem. Standardní splachovací WC spotřebuje 6 až 9 litrů pitné vody na jedno spláchnutí, což by vyžadovalo obrovskou jímku a neustálé doplňování nádrží.</p>
      
      <h3>Srovnání dvou nejlepších technologií:</h3>
      <ul>
        <li><strong>Varianta A: Separační kompostovací toaleta (Doporučeno pro Tiny House):</strong> Mechanicky odděluje pevnou a tekutou složku. Pevná složka je zasypávána pilinami a odvětrávána ventilátorem s uhlíkovým filtrem – 100% bez zápachu a chemie. Vynáší se jednou za 3–4 týdny na kompost.</li>
        <li><strong>Varianta B: Spalovací toaleta Cinderella (Luxusní varianta):</strong> Využívá plyn nebo elektřinu k okamžitému spálení odpadu při 600 °C na sterilní popel (cca šálek popela za týden).</li>
        <li><strong>Hospodaření s šedou vodou:</strong> Voda ze sprchy a dřezu prochází mechanickým a pískovým biofiltrem a může být bezpečně vsakována na pozemku k zalévání dřevin.</li>
      </ul>
    `
  }
};

/* ==========================================================================
   5. BLOG FILTER AND LIVE SEARCH
   ========================================================================== */
function initBlogFilterAndSearch() {
  const catBtns = document.querySelectorAll('.cat-btn');
  const searchInput = document.getElementById('blogSearchInput');
  const cards = document.querySelectorAll('.blog-card');
  const counterEl = document.getElementById('articleCountDisplay');

  let activeCat = 'all';
  let searchQuery = '';

  function filterArticles() {
    let visibleCount = 0;

    cards.forEach(card => {
      const id = card.dataset.articleId;
      const article = ARTICLES[id];
      if (!article) return;

      const matchesCat = (activeCat === 'all') || (article.category === activeCat);
      const textCorpus = (article.title + ' ' + article.badge + ' ' + article.content).toLowerCase();
      const matchesSearch = !searchQuery || textCorpus.includes(searchQuery.toLowerCase());

      if (matchesCat && matchesSearch) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    if (counterEl) {
      counterEl.textContent = `${visibleCount} z 10 článků`;
    }
  }

  catBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      catBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCat = btn.dataset.category;
      filterArticles();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim();
      filterArticles();
    });
  }
}

/* ==========================================================================
   6. ARTICLE MODAL READER
   ========================================================================== */
function initArticleModals() {
  const modal = document.getElementById('articleModal');
  const closeBtn = document.getElementById('closeArticleModal');
  const modalBody = document.getElementById('modalArticleBody');
  const cards = document.querySelectorAll('[data-article-id]');

  cards.forEach(card => {
    card.addEventListener('click', () => {
      const id = card.dataset.articleId;
      const article = ARTICLES[id];
      if (!article) return;

      modalBody.innerHTML = `
        <span class="badge-tactical" style="margin-bottom: 12px;">${article.badge}</span>
        <div class="blog-date" style="margin-bottom: 8px;">${article.date}</div>
        <h2 style="font-size: 2.2rem; margin-bottom: 16px; color: #fff; line-height: 1.2;">${article.title}</h2>
        
        <div class="modal-author-box">
          <div class="author-avatar">O</div>
          <div class="author-info">
            <span class="author-name">Konstrukční & Renovační tým Orličan</span>
            <span class="author-role">Specialisté na armádní izotermické nástavby & off-grid systémy</span>
          </div>
        </div>

        <div class="article-takeaways">
          <div class="takeaways-title">Klíčový závěr článku:</div>
          <p style="margin: 0; color: #fff; font-size: 1rem; font-weight: 500;">${article.takeaway}</p>
        </div>

        <div class="article-content">${article.content}</div>

        <div style="margin-top: 40px; padding-top: 24px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
          <div>
            <span style="color: var(--text-muted); font-size: 0.9rem;">Chcete podobné řešení pro svůj pozemek či expedici?</span>
          </div>
          <button class="btn btn-primary btn-sm open-lead-modal" onclick="document.getElementById('articleModal').classList.remove('open');">Nezávazně poptat stavbu</button>
        </div>
      `;

      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', closeModal);
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeModal();
    }
  });

  function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }
}

/* ==========================================================================
   7. LEAD GENERATION / QUOTE MODAL
   ========================================================================== */
function initLeadModal() {
  const leadModal = document.getElementById('leadModal');
  const openBtns = document.querySelectorAll('.open-lead-modal');
  const closeBtn = document.getElementById('closeLeadModal');
  const form = document.getElementById('leadForm');
  const successMsg = document.getElementById('leadSuccessMsg');

  document.addEventListener('click', (e) => {
    if (e.target.closest('.open-lead-modal')) {
      e.preventDefault();
      leadModal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      leadModal.classList.remove('open');
      document.body.style.overflow = '';
    });
  }

  if (leadModal) {
    leadModal.addEventListener('click', (e) => {
      if (e.target === leadModal) {
        leadModal.classList.remove('open');
        document.body.style.overflow = '';
      }
    });
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      form.style.display = 'none';
      if (successMsg) successMsg.style.display = 'block';
      setTimeout(() => {
        leadModal.classList.remove('open');
        document.body.style.overflow = '';
        form.reset();
        form.style.display = 'flex';
        if (successMsg) successMsg.style.display = 'none';
      }, 3500);
    });
  }
}
