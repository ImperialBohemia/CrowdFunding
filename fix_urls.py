import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add campaign config
config_script = """  <script>
    // Konfigurace sbírky na Znesnáze21
    const CAMPAIGN_SLUG = "pomozte-nam-vratit-deti-domu"; // <-- ZDE VYPLŇTE PŘESNÝ NÁZEV (SLUG) KAMPANĚ
    const ZNESNAZE_BASE_URL = `https://www.znesnaze21.cz/sbirka/${CAMPAIGN_SLUG}/darovat`;
  </script>
"""
if "CAMPAIGN_SLUG" not in content:
    content = content.replace("<!-- Sklik (Seznam.cz) Měření: Seznam Event Measurement (SEM) -->", config_script + "\n  <!-- Sklik (Seznam.cz) Měření: Seznam Event Measurement (SEM) -->")

# Update click handlers to set the URL correctly before navigation
click_handlers = """
    // Aktualizace URL Znesnáze21 podle vybrané částky (pokud to Znesnáze21 podporuje přes parametry, jinak se použije base)
    function getDonationUrl() {
      // Pokud Znesnáze21 přijímá částku v URL, přidáme ji (např. ?amount=500). Zatím jen base URL.
      return ZNESNAZE_BASE_URL;
    }

    // Navázání konverzí na tlačítka
    document.getElementById('cta-button-main')?.addEventListener('click', function(e) {
      this.href = getDonationUrl();
      trackDonationConversion('hero_cta');
    });
    document.getElementById('sticky-btn-link')?.addEventListener('click', function(e) {
      this.href = getDonationUrl();
      trackDonationConversion('sticky_bar');
    });"""

old_handlers_pattern = r'// Navázání konverzí na tlačítka[\s\S]*?trackDonationConversion\(\'sticky_bar\'\);\n    }\);'

content = re.sub(old_handlers_pattern, click_handlers, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
