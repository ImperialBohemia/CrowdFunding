import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_script = """    function trackSocialShare(platform) {
      if (window.szn && window.szn.sem) {
        window.szn.sem('event', 'Contact');
      }
    }"""

import re
content = re.sub(r'    function trackSocialShare\(platform\) \{[\s\S]*?    \}', new_script, content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
