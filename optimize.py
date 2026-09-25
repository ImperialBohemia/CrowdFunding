import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Preconnect and Preload
head_additions = """
  <!-- Rychlostní optimalizace (Preload & Preconnect) -->
  <link rel="preconnect" href="https://sem.seznam.cz" crossorigin>
  <link rel="preconnect" href="https://www.znesnaze21.cz" crossorigin>
  <link rel="preload" as="image" href="images/family/mama-dcery-srdce.jpg">
"""
content = content.replace("<!-- SEO & Canonical -->", head_additions + "\n  <!-- SEO & Canonical -->")

# 2. Remove loading="lazy" from the first LCP image
content = content.replace('<img src="images/family/mama-dcery-srdce.jpg" alt="Maminka s Jolankou a Maruškou v srdci" loading="lazy" width="900" height="1200">', '<img src="images/family/mama-dcery-srdce.jpg" alt="Maminka s Jolankou a Maruškou v srdci" width="900" height="1200" fetchpriority="high">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
