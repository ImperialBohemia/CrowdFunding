import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

schema_script = """
  <!-- Schema.org (JSON-LD) pro SEO -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Charity",
    "name": "Návrat dětí domů (Jolanka a Maruška)",
    "description": "Rodina z ubytovny shání finanční prostředky na kauci za byt, aby jim soud vrátil děti z Klokánku.",
    "url": "https://navratdetidomu.cz/",
    "potentialAction": {
      "@type": "DonateAction",
      "target": {
        "@type": "EntryPoint",
        "urlTemplate": "https://www.znesnaze21.cz/sbirka/pomozte-nam-vratit-deti-domu/darovat"
      }
    }
  }
  </script>
"""

content = content.replace("</head>", schema_script + "</head>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
