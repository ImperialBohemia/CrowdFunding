import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

bad_block = """    function trackSocialShare(platform) {
      if (window.szn && window.szn.sem) {
        window.szn.sem('event', 'Contact');
      }
    });
      }
    }"""

good_block = """    function trackSocialShare(platform) {
      if (window.szn && window.szn.sem) {
        window.szn.sem('event', 'Contact');
      }
    }"""

content = content.replace(bad_block, good_block)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
