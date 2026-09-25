# Sklik SEM (Seznam Event Measurement) Audit & Precision Strategy

**Account:** `horoskopie.cz@email.cz`  
**User ID:** `697549`  
**API Drak:** Authenticated  
**API Fénix:** Authenticated (Full Admin Scopes: `sem`, `sem_id`, `sem_edit`, `sem_activate`, `campaign*`, `group*`, `ad*`, `conversion*`, `retargeting*`)  
**Credit:** 69.47 CZK (84.06 CZK with VAT)  

---

## 1. Verified Live SEM Configuration

Direct empirical extraction via API Fénix (`/sklik/event-measurement/`):

| Parameter | Value | Description |
|---|---|---|
| **Public SEM ID** | `hmaf4eme3mgcuspokyh7dpoc` | Frontend identifier for `sul.js` and Google Tag Manager |
| **Private SEM ID (S2S)** | `hmaf4emdzae5zzlv6066wilt` | Backend identifier passed in `event_data.sem_id` |
| **Configured Conversion** | `CompleteRegistration` | ID `100289271`, Name: **Lead**, Value: **10 CZK** |
| **Activation Status** | Ready to activate | Endpoint `POST /sklik/event-measurement/activate/` |

---

## 2. Transition Rules & Critical Warnings ("Upozornění na přechodná omezení")

1. **The Irreversible Switch:**
   - Activating SEM permanently discontinues processing of legacy Sklik conversion/retargeting tags.
   - Retargeting lists and combinations are transferred automatically.
2. **Single Primary Conversion Rule:**
   - When tracking multiple conversions, Sklik timeline graphs do not break down sub-conversions, and table sorting by filtered conversion metrics is disabled.
   - External bidding robots (e.g. Bidding Fox) optimize for **all conversions indiscriminately**. If secondary micro-conversions are added, bidding algorithms dilute optimization away from primary business leads.
   - **Recommendation:** Keep only `CompleteRegistration` (Lead) as the active primary conversion.
3. **No Duplicate S2S + Frontend Firing:**
   - Do not fire both client-side and backend S2S for the same user event until automatic `event_id` deduplication is officially confirmed; concurrent firing causes duplicate conversions.
4. **API Drak Restriction:**
   - SEM conversion breakdowns and event-based methods are not supported in API Drak. All SEM management must use API Fénix.

---

## 3. Implementation Code for Maximum Precision

### 3.1 Frontend Tag (`sul.js`) Deployment
Place inside the `<head>` of your website:

```html
<!-- Seznam Event Measurement (SEM) -->
<script async src="https://sem.seznam.cz/sul.js"></script>
<script>
  window.szn = window.szn || {};
  window.szn.sem = window.szn.sem || function() {
    (window.szn.sem.q = window.szn.sem.q || []).push(arguments);
  };

  // 1. Set consent state
  window.szn.sem('updateConsent', {
    ad_storage: 'granted',
    ad_user_data: 'granted',
    ad_personalization: 'granted'
  });

  // 2. Initialize with Public SEM ID
  window.szn.sem('init', 'hmaf4eme3mgcuspokyh7dpoc');

  // 3. Track PageView
  window.szn.sem('event', 'PageView');
</script>
```

### 3.2 Lead Conversion Trigger (Frontend)
Triggered upon user registration or lead completion:

```javascript
window.szn.sem('event', 'CompleteRegistration', {
  value: 10,
  currency: 'CZK',
  user_data: {
    // Plaintext in frontend - sul.js hashes automatically via SHA-256
    email: 'zakaznik@email.cz',
    phone: '420777123456'
  }
});
```

### 3.3 Server-to-Server (S2S) Implementation (Backend Fallback)
Send directly from your server to bypass ad-blockers and Safari cookie expiration:

- **Endpoint:** `POST https://sem.seznam.cz/rtgconv`
- **Headers:** `Content-Type: application/json`
- **Payload:**
```json
{
  "schema_version": "v2",
  "event_source": "web",
  "event_name": "CompleteRegistration",
  "event_type": "rtgconv",
  "event_time": 1726336800000,
  "event_id": "c1f72a44-018e-7abc-9def-0123456789ab",
  "event_url": "https://your-domain.cz/dekujeme",
  "user_ids": {
    "user_data": {
      "sid": "<VALUE_OF_COOKIE_sid>",
      "udid": "<VALUE_OF_COOKIE_udid>",
      "em": "<LOWERCASE_SHA256_HASHED_EMAIL>",
      "ph": "<E164_SHA256_HASHED_PHONE>"
    }
  },
  "consent_mode": {
    "ad_storage": "granted",
    "ad_user_data": "granted",
    "ad_personalization": "granted"
  },
  "event_data": {
    "sem_id": "hmaf4emdzae5zzlv6066wilt",
    "sznaiid": "<CLICK_ID_FROM_URL_QUERY>",
    "currency": "CZK",
    "value": 10
  }
}
```

---

## 4. Final Activation Protocol

1. **Verify Hits in Sandbox:**
   - Open Sklik UI $\rightarrow$ Správa měření $\rightarrow$ Sandbox (`https://www.sklik.cz/event-management/sandbox`).
   - Run a test registration to confirm `CompleteRegistration` events arrive with status `OK`.
2. **Execute Activation:**
   - Call `POST /sklik/event-measurement/activate/` via Fénix API or click "Začít používat SEM" in Sklik UI.
