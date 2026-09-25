#!/usr/bin/env python3
"""
Sklik Unified Client (Drak JSON API + Fénix REST API)
Provides instant programmatic and CLI access to Seznam Sklik.
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / ".env.sklik"
CACHE_PATH = Path(__file__).resolve().parent / ".sklik_cache.json"

class SklikClient:
    DRAK_BASE = "https://api.sklik.cz/drak/json"
    FENIX_BASE = "https://api.sklik.cz/v1"

    def __init__(self, env_file=CONFIG_PATH):
        self.config = self._load_config(env_file)
        self.drak_token = self.config.get("SKLIK_DRAK_TOKEN")
        self.fenix_refresh_token = self.config.get("SKLIK_FENIX_REFRESH_TOKEN")
        self.user_id = int(self.config.get("SKLIK_USER_ID", 0)) or None
        self.username = self.config.get("SKLIK_USERNAME")
        self.public_sem_id = self.config.get("SKLIK_PUBLIC_SEM_ID")
        self.private_sem_id = self.config.get("SKLIK_PRIVATE_SEM_ID")
        
        self.drak_session = None
        self.fenix_access_token = None
        self.fenix_token_expires = 0
        self._load_cache()

    def _load_config(self, path):
        cfg = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        cfg[k.strip()] = v.strip().strip("'\"")
        return cfg

    def _load_cache(self):
        if CACHE_PATH.exists():
            try:
                with open(CACHE_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.drak_session = data.get("drak_session")
                    self.fenix_access_token = data.get("fenix_access_token")
                    self.fenix_token_expires = data.get("fenix_token_expires", 0)
            except Exception:
                pass

    def _save_cache(self):
        try:
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "drak_session": self.drak_session,
                    "fenix_access_token": self.fenix_access_token,
                    "fenix_token_expires": self.fenix_token_expires
                }, f)
        except Exception:
            pass

    # ================= API DRAK =================
    def drak_login(self):
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
            self._save_cache()
            return self.drak_session

    def drak(self, method: str, *params, foreign_user_id=None):
        if not self.drak_session:
            self.drak_login()

        user_struct = {"session": self.drak_session}
        if foreign_user_id:
            user_struct["userId"] = foreign_user_id

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
                if data.get("status") == 401: # Session expired
                    self.drak_login()
                    user_struct["session"] = self.drak_session
                    payload = [user_struct, *params]
                    req2 = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
                    with urllib.request.urlopen(req2) as res2:
                        return json.loads(res2.read().decode("utf-8"))
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429:
                retry = int(e.headers.get("Retry-After", 2))
                time.sleep(retry)
                return self.drak(method, *params)
            raise

    # ================= API FÉNIX =================
    def fenix_refresh(self):
        url = f"{self.FENIX_BASE}/user/token"
        body = urllib.parse.urlencode({
            "grant_type": "refresh_token",
            "refresh_token": self.fenix_refresh_token
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
            self.fenix_access_token = data["access_token"]
            self.fenix_token_expires = time.time() + int(data.get("expires_in", 300))
            self._save_cache()
            return self.fenix_access_token

    def fenix(self, method: str, endpoint: str, body=None, params=None):
        if not self.fenix_access_token or time.time() > self.fenix_token_expires - 30:
            self.fenix_refresh()

        query_str = ""
        if params:
            query_str = "?" + urllib.parse.urlencode(params, doseq=True)

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
                    return {"status": 204, "message": "No Content / Success"}
                return json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 401: # expired
                self.fenix_refresh()
                headers["Authorization"] = f"Bearer {self.fenix_access_token}"
                req2 = urllib.request.Request(url, data=data_bytes, headers=headers, method=method.upper())
                with urllib.request.urlopen(req2) as res2:
                    return json.loads(res2.read().decode("utf-8"))
            elif e.code == 429:
                retry = int(e.headers.get("Retry-After", 2))
                time.sleep(retry)
                return self.fenix(method, endpoint, body, params)
            err_body = e.read().decode("utf-8")
            return {"error": e.code, "detail": err_body}

    # ================= CONVENIENCE METHODS =================
    def get_status(self):
        credit = self.drak("client.getCredit")
        camps = self.drak("campaigns.list", {"isDeleted": False}, {"offset": 0, "limit": 100})
        sem_ids = self.fenix("GET", "/sklik/event-measurement/sem-id/")
        conversions = self.fenix("GET", "/sklik/event-measurement/conversions/", params={"a": ["id", "name", "semEventName", "value", "isDeleted"]})

        return {
            "user": self.username,
            "userId": self.user_id,
            "credit": credit.get("clients", [{}])[0].get("credit", 0),
            "creditWithVat": credit.get("clients", [{}])[0].get("creditWithVat", 0),
            "activeCampaigns": [
                {"id": c["id"], "name": c["name"], "type": c["type"], "status": c["status"]}
                for c in camps.get("campaigns", [])
            ],
            "semIds": sem_ids.get("items", []),
            "semConversions": conversions.get("items", [])
        }

sklik = SklikClient()

def main():
    args = sys.argv[1:]
    if not args or args[0] in ["status", "info"]:
        st = sklik.get_status()
        print(json.dumps(st, indent=2, ensure_ascii=False))
    elif args[0] == "campaigns":
        camps = sklik.drak("campaigns.list", {"isDeleted": False}, {"offset": 0, "limit": 100})
        print(json.dumps(camps.get("campaigns", []), indent=2, ensure_ascii=False))
    elif args[0] == "groups":
        groups = sklik.drak("groups.list", {"isDeleted": False}, {"offset": 0, "limit": 100})
        print(json.dumps(groups.get("groups", []), indent=2, ensure_ascii=False))
    elif args[0] == "keywords":
        kws = sklik.drak("keywords.list", {"isDeleted": False}, {"offset": 0, "limit": 100})
        print(json.dumps(kws.get("keywords", []), indent=2, ensure_ascii=False))
    elif args[0] == "suggest" and len(args) > 1:
        query = args[1]
        res = sklik.drak("keywords.suggest", query, {"limit": 10})
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args[0] == "drak" and len(args) > 1:
        method = args[1]
        params = [json.loads(p) for p in args[2:]]
        res = sklik.drak(method, *params)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    elif args[0] == "fenix" and len(args) > 2:
        m, path = args[1], args[2]
        body = json.loads(args[3]) if len(args) > 3 else None
        res = sklik.fenix(m, path, body=body)
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print("Usage: python3 sklik_tool.py [status|campaigns|groups|keywords|suggest <phrase>|drak <method> ...|fenix <GET|POST> <path> ...]")

if __name__ == "__main__":
    main()
