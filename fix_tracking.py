import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

start_marker = "// Sklik měření (SEM & Retargeting)"
end_marker = "    function trackSocialShare(platform) {"

if start_marker in content and end_marker in content:
    pre = content.split(start_marker)[0]
    post = end_marker + content.split(end_marker)[1]
    
    new_script = """// Sklik měření (SEM & Retargeting)
    function updateSklik(granted) {
      const mode = granted ? 'granted' : 'denied';
      if (window.szn && window.szn.sem) {
        window.szn.sem('updateConsent', {
          ad_storage: mode,
          ad_user_data: mode,
          ad_personalization: mode
        });
      }
    }

    // Odeslání konverze Sklik s reálnou zvolenou částkou
    function trackDonationConversion(source) {
      const val = currentDonationAmount || 500;
      if (window.szn && window.szn.sem) {
        // Spárováno s primární konverzí v účtu Sklik (ID: 100289271, semEventName: Search)
        window.szn.sem('event', 'Search', {
          value: val,
          currency: 'CZK'
        });
        // Další SEM eventy pro přesnější segmentaci
        window.szn.sem('event', 'Donate', {
          value: val,
          currency: 'CZK'
        });
        window.szn.sem('event', 'Lead', {
          value: val,
          currency: 'CZK'
        });
        window.szn.sem('event', 'InitiateCheckout', {
          value: val,
          currency: 'CZK'
        });
      }
    }

"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(pre + new_script + post)
    print("Replaced")
else:
    print("Markers not found")
