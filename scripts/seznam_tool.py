#!/usr/bin/env python3
"""
Seznam Master Unified CLI (Sklik Drak + Sklik Fénix + Seznam Webmaster)
Permanent integration for all Seznam services.
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / "Marketing" / ".env.sklik"

def load_config():
    cfg = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip().strip("'\"")
    for k, v in os.environ.items():
        if k.startswith("SKLIK_") or k.startswith("SEZNAM_"):
            cfg[k] = v
    return cfg

class SeznamMasterClient:
    DRAK_BASE = "https://api.sklik.cz/drak/json"
    FENIX_BASE = "https://api.sklik.cz/v1"
    WM_BASE = "https://reporter.seznam.cz/wm-api"

    def __init__(self):
        self.cfg = load_config()
        self.drak_token = self.cfg.get("SKLIK_DRAK_TOKEN")
        self.fenix_refresh_token = self.cfg.get("SKLIK_FENIX_REFRESH_TOKEN")
        self.user_id = int(self.cfg.get("SKLIK_USER_ID", 0)) or None
        self.username = self.cfg.get("SKLIK_USERNAME")
        self.public_sem_id = self.cfg.get("SKLIK_PUBLIC_SEM_ID")
        self.private_sem_id = self.cfg.get("SKLIK_PRIVATE_SEM_ID")
        self.wm_api_key = self.cfg.get("SEZNAM_WEBMASTER_API_KEY")
        self.wm_user_id = self.cfg.get("SEZNAM_WEBMASTER_USER_ID")

        self.drak_session = None
        self.fenix_access_token = None
        self.fenix_token_expires = 0

    # ---------- Sklik Drak ----------
    def drak_login(self):
        if not self.drak_token:
            raise RuntimeError("SKLIK_DRAK_TOKEN missing.")
        url = f"{self.DRAK_BASE}/client.loginByToken"
        req = urllib.request.Request(
            url,
            data=json.dumps([self.drak_token]).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            if data.get("status") != 200:
                raise RuntimeError(f"Drak login failed: {data}")
            self.drak_session = data["session"]
            return self.drak_session

    def drak(self, method: str, *params):
        if not self.drak_session:
            self.drak_login()
        user_struct = {"session": self.drak_session}
        payload = [user_struct, *params]
        url = f"{self.DRAK_BASE}/{method}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode("utf-8"))
                if data.get("status") == 401:
                    self.drak_login()
                    user_struct["session"] = self.drak_session
                    payload = [user_struct, *params]
                    req2 = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(req2) as res2:
                        return json.loads(res2.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(2)
                return self.drak(method, *params)
            raise

    # ---------- Sklik Fénix ----------
    def fenix_refresh(self):
        if not self.fenix_refresh_token:
            raise RuntimeError("SKLIK_FENIX_REFRESH_TOKEN missing.")
        url = f"{self.FENIX_BASE}/user/token"
        body = urllib.parse.urlencode({
            "grant_type": "refresh_token",
            "refresh_token": self.fenix_refresh_token
        }).encode("utf-8")
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"})
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            self.fenix_access_token = data["access_token"]
            self.fenix_token_expires = time.time() + int(data.get("expires_in", 300))
            return self.fenix_access_token

    def fenix(self, method: str, endpoint: str, body=None, params=None):
        if not self.fenix_access_token or time.time() > self.fenix_token_expires - 30:
            self.fenix_refresh()
        query_str = ("?" + urllib.parse.urlencode(params, doseq=True)) if params else ""
        url = f"{self.FENIX_BASE}{endpoint}{query_str}"
        headers = {
            "Authorization": f"Bearer {self.fenix_access_token}",
            "Content-Type": "application/json"
        }
        data_bytes = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req) as res:
                if res.status == 204:
                    return {"status": 204, "message": "No Content"}
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", "ignore")
            return {"error": e.code, "detail": err}

    # ---------- Seznam Webmaster API ----------
    def wm_request(self, path: str, method="GET", query=None):
        if not self.wm_api_key:
            return {"error": "SEZNAM_WEBMASTER_API_KEY missing"}
        q = f"?key={self.wm_api_key}"
        if query:
            q += "&" + urllib.parse.urlencode(query)
        url = f"{self.WM_BASE}{path}{q}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"}, method=method)
        try:
            with urllib.request.urlopen(req) as res:
                if res.status == 204:
                    return {"status": 204, "message": "No data available yet"}
                body = res.read().decode("utf-8")
                return json.loads(body) if body.strip() else {"status": res.status}
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", "ignore")
            return {"error": e.code, "detail": err}

    # ---------- Unified Status ----------
    def status(self):
        # Sklik Status
        credit = self.drak("client.getCredit")
        camps = self.drak("campaigns.list", {"isDeleted": False}, {"offset": 0, "limit": 100})
        sem_ids = self.fenix("GET", "/sklik/event-measurement/sem-id/")
        sem_conversions = self.fenix("GET", "/sklik/event-measurement/conversions/", params={"a": ["id", "name", "semEventName", "value", "isDeleted"]})
        
        # Webmaster Status
        wm_db = self.wm_request("/database-info")
        wm_web = self.wm_request("/web")

        return {
            "sklik": {
                "user": self.username,
                "userId": self.user_id,
                "credit": credit.get("clients", [{}])[0].get("credit", 0),
                "creditWithVat": credit.get("clients", [{}])[0].get("creditWithVat", 0),
                "activeCampaigns": [
                    {"id": c["id"], "name": c["name"], "type": c["type"], "status": c["status"]}
                    for c in camps.get("campaigns", [])
                ],
                "semIds": sem_ids.get("items", []),
                "semConversions": sem_conversions.get("items", [])
            },
            "webmaster": {
                "userId": self.wm_user_id,
                "database": wm_db,
                "web": wm_web
            }
        }

    def reindex(self, url: str):
        return self.wm_request("/web/document/reindex", method="POST", query={"url": url})

if __name__ == "__main__":
    client = SeznamMasterClient()
    args = sys.argv[1:]
    cmd = args[0] if args else "status"

    if cmd == "status":
        print(json.dumps(client.status(), indent=2, ensure_ascii=False))
    elif cmd == "reindex" and len(args) > 1:
        print(json.dumps(client.reindex(args[1]), indent=2, ensure_ascii=False))
    elif cmd == "campaigns":
        res = client.drak("campaigns.list", {"isDeleted": False}, {"offset": 0, "limit": 100})
        print(json.dumps(res.get("campaigns", []), indent=2, ensure_ascii=False))
    elif cmd == "drak" and len(args) > 1:
        method = args[1]
        params = [json.loads(p) for p in args[2:]]
        print(json.dumps(client.drak(method, *params), indent=2, ensure_ascii=False))
    elif cmd == "fenix" and len(args) > 2:
        m, path = args[1], args[2]
        body = json.loads(args[3]) if len(args) > 3 else None
        print(json.dumps(client.fenix(m, path, body=body), indent=2, ensure_ascii=False))
    else:
        print("Usage: python3 seznam_tool.py [status|campaigns|reindex <url>|drak <method>|fenix <GET|POST> <path>]")
