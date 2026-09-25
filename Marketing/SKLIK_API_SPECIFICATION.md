# Sklik API Architecture & Integration Specification

Empirical specification and integration guide for Seznam Sklik APIs (API Drak and API Fénix).

---

## 1. Executive Summary & Interface Comparison

Seznam Sklik maintains two active API ecosystems:

| Parameter | **API Drak (Core / Full Management)** | **API Fénix (Modern REST)** |
|---|---|---|
| **Protocol** | JSON over HTTP POST / XML-RPC | RESTful JSON (OpenAPI 3.0) |
| **Endpoint Base** | `https://api.sklik.cz/drak/json/<method>` | `https://api.sklik.cz/v1/` (or `/latest/`) |
| **Authentication** | Permanent API token exchanged via `client.loginByToken` $\rightarrow$ Session ID | Permanent refresh token exchanged via `POST /user/token` $\rightarrow$ Bearer Access Token (1h validity) |
| **Rate Limit** | Propagates HTTP 429 when threshold exceeded | Global default 5 req/sec (IETF draft RateLimit headers, `Retry-After`) |
| **Key Advantage** | Full PPC CRUD: Positive keywords, CPC bidding, keyword suggestions/forecasting, retargeting, search query reports | Modern REST standard, Seznam Nákupy (Shopping feed/diagnostics/reviews), image uploads |

---

## 2. API Drak (JSON-RPC Protocol)

### 2.1 Communication Standard
- **Method:** `POST https://api.sklik.cz/drak/json/<method_name>`
- **Content-Type:** `application/json`
- **Request Body:** JSON Array `[ user_struct, ...parameters ]`
- **Currency Unit:** Financial fields (CPC, dayBudget, spend) are strictly in **haléře** ($1\text{ CZK} = 100\text{ haléřů}$).

### 2.2 Authentication Flow
```http
POST https://api.sklik.cz/drak/json/client.loginByToken
Content-Type: application/json

["<PERMANENT_API_TOKEN>"]
```
Response:
```json
{
  "status": 200,
  "statusMessage": "OK",
  "session": "93a6b2c48d...",
  "userId": 123456
}
```

### 2.3 Account Management (MCCA / Sub-Accounts)
In multi-account / agency scenarios, inject `userId` into the user struct:
```json
[
  { "session": "93a6b2c48d...", "userId": 789101 },
  { "includeDeleted": false }
]
```

### 2.4 Available Services & Methods
- **`campaigns.*`**: `create`, `list`, `update`, `remove`, `restore`, `check`, `createReport`, `readReport`, `listCampaignsTypes`
- **`groups.*`**: `create`, `list`, `update`, `remove`, `restore`, `check`, `createReport`, `readReport`
- **`ads.*`**: `create`, `list`, `update`, `remove`, `restore`, `check`, `createReport`, `readReport`
- **`banners.*`**: `create`, `list`, `update`, `remove`, `restore`, `check`, `createReport`, `readReport`
- **`keywords.*`**:
  - Positive keywords: `create`, `list`, `update`, `set`, `remove`, `restore`, `check`
  - Negative keywords: `negative.create`, `negative.list`, `negative.set`, `negative.remove`, `negative.restore`, `campaign.negative.*`
  - Research & Forecasting: `suggest` (phrases, avgSearchCount, CPC, competition score), `suggest.stats` (search volume history for up to 100 queries)
- **`retargeting.*`**:
  - `lists.*`: Create/list/update audience definitions
  - `combinations.*`: Boolean combination lists (AND/OR/NOT)
  - `emails.*`: First-party hashed email lists
  - `lookalikes.*`: Lookalike audience generator
- **`queries.*`**: `createReport`, `readReport` (Search term report)
- **`sitelinks.*`**: `create`, `list`, `campaign.set`, `group.set`, `group.stats`
- **`sharedbudgets.*`**: `create`, `list`, `update`, `remove`
- **`conversions.*`**: `create`, `list`, `update`, `get`, `check`
- **`client.*`**: `get`, `getCredit`, `stats`, `loginByToken`, `logout`

---

## 3. API Fénix (RESTful / OpenAPI Standard)

### 3.1 Authentication & Token Exchange
1. Generate refresh token in Sklik UI (`Nastavení účtu` $\rightarrow$ `Přístup k API`).
2. Exchange for short-lived access token:
```http
POST https://api.sklik.cz/v1/user/token
Content-Type: application/json

{
  "refresh_token": "<YOUR_API_TOKEN>",
  "user_id": 123456  // optional: linked sub-account
}
```
Response:
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "expires_in": 3600
}
```
3. Use in standard HTTP header: `Authorization: Bearer <access_token>`.

### 3.2 Key Endpoints
- **Seznam Nákupy (`/nakupy/...`)**:
  - `GET /nakupy/campaigns/`: List shopping campaigns
  - `GET /nakupy/feeds/`, `PATCH /nakupy/feeds/{feedId}`: XML feed management
  - `GET /nakupy/diagnostics/item`: Item inspection & rejection status
  - `GET /nakupy/categories/tree`: Product taxonomy
  - `GET /nakupy/reviews/`, `PUT /nakupy/reviews/{reviewId}/reaction`: Shop reviews & response management
- **Campaigns & Ads (`/sklik/...`)**:
  - `GET`, `POST /sklik/campaigns/`
  - `GET`, `POST, `PATCH /sklik/campaigns/{campaignId}/groups/`
  - `GET`, `POST`, `PATCH /sklik/campaigns/{campaignId}/groups/{groupId}/ads/`
  - `GET`, `POST`, `PUT`, `POST .../negative-keywords/delete`: Group & campaign negative keyword management
  - `POST /sklik/suggest/ad`: Smart creative suggestions
  - `GET`, `POST /sklik/images/`: Image asset upload and listing
  - `GET /sklik/reports/`, `GET /sklik/reports/{reportId}`: Async statistical reports
- **User & Diagnostics (`/user/...`)**:
  - `GET /user/me`: Current user metadata
  - `GET /user/me/credit`: Credit balances
  - `GET /user/linked-accounts`: Authorized client accounts

---

## 4. Production Integration Client (Python Reference)

```python
import time
import requests

class SklikClient:
    DRAK_BASE = "https://api.sklik.cz/drak/json"
    FENIX_BASE = "https://api.sklik.cz/v1"

    def __init__(self, token: str, user_id: int = None):
        self.token = token
        self.user_id = user_id
        self.session_id = None
        self.access_token = None
        self.access_token_expiry = 0

    # ---------------- API Drak Core ----------------
    def drak_login(self):
        url = f"{self.DRAK_BASE}/client.loginByToken"
        res = requests.post(url, json=[self.token], timeout=10)
        res.raise_for_status()
        data = res.json()
        if data.get("status") != 200:
            raise RuntimeError(f"Drak login failed: {data}")
        self.session_id = data["session"]
        return self.session_id

    def call_drak(self, method: str, *params):
        if not self.session_id:
            self.drak_login()

        user_struct = {"session": self.session_id}
        if self.user_id:
            user_struct["userId"] = self.user_id

        payload = [user_struct, *params]
        url = f"{self.DRAK_BASE}/{method}"

        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 2))
            time.sleep(retry_after)
            return self.call_drak(method, *params)

        response.raise_for_status()
        res_data = response.json()

        # Handle session expiration
        if res_data.get("status") == 401:
            self.drak_login()
            user_struct["session"] = self.session_id
            response = requests.post(url, json=[user_struct, *params], timeout=30)
            res_data = response.json()

        return res_data

    # ---------------- API Fénix Core ----------------
    def fenix_get_token(self):
        now = time.time()
        if self.access_token and now < self.access_token_expiry - 60:
            return self.access_token

        url = f"{self.FENIX_BASE}/user/token"
        body = {"refresh_token": self.token}
        if self.user_id:
            body["user_id"] = self.user_id

        res = requests.post(url, json=body, timeout=10)
        res.raise_for_status()
        data = res.json()
        self.access_token = data["access_token"]
        self.access_token_expiry = now + data.get("expires_in", 3600)
        return self.access_token

    def call_fenix(self, http_method: str, path: str, **kwargs):
        token = self.fenix_get_token()
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        url = f"{self.FENIX_BASE}{path}"

        res = requests.request(http_method, url, headers=headers, **kwargs)
        if res.status_code == 429:
            retry_after = int(res.headers.get("Retry-After", 2))
            time.sleep(retry_after)
            return self.call_fenix(http_method, path, **kwargs)

        res.raise_for_status()
        return res.json()
```

---

## 5. Architectural Recommendation

1. **Use API Drak (JSON Mode) for Search & Content Campaigns:**
   - Full keyword bid control (`cpc` in haléře).
   - Keyword suggestion & search volume forecasting (`keywords.suggest`, `keywords.suggest.stats`).
   - Retargeting lists and search term queries (`queries.*`).
2. **Use API Fénix for Product Ads & Creatives:**
   - Seznam Nákupy product catalog sync, feed updates, item diagnostics.
   - Image uploads and smart creative generation.
3. **Hybrid Engine:**
   - One single API token from Sklik UI authorizes both endpoints.
   - Maintain a unified wrapper (like `SklikClient` above) to handle routing automatically based on feature requirements.
