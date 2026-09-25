#!/usr/bin/env python3
"""
Seznam Webmaster API CLI Client
Reads SEZNAM_WEBMASTER_API_KEY from Marketing/.env.sklik
"""

import sys
import os
import urllib.request
import urllib.parse
import json
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / "Marketing" / ".env.sklik"

def load_key():
    if not ENV_PATH.exists():
        return os.environ.get("SEZNAM_WEBMASTER_API_KEY")
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("SEZNAM_WEBMASTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip("'\"")
    return os.environ.get("SEZNAM_WEBMASTER_API_KEY")

class SeznamWebmaster:
    BASE = "https://reporter.seznam.cz/wm-api"

    def __init__(self, key=None):
        self.key = key or load_key()
        if not self.key:
            raise ValueError("SEZNAM_WEBMASTER_API_KEY is not configured.")

    def request(self, path, method="GET", query=None):
        q = f"?key={self.key}"
        if query:
            q += "&" + urllib.parse.urlencode(query)
        url = f"{self.BASE}{path}{q}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"}, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                if resp.status == 204:
                    return {"status": 204, "message": "No data available yet"}
                body = resp.read().decode("utf-8")
                return json.loads(body) if body.strip() else {"status": resp.status}
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", "ignore")
            return {"error": e.code, "detail": err}

    def status(self):
        return {
            "database": self.request("/database-info"),
            "web": self.request("/web"),
            "documents": self.request("/web/documents")
        }

    def document(self, url):
        return self.request("/web/document", query={"url": url})

    def reindex(self, url):
        return self.request("/web/document/reindex", method="POST", query={"url": url})

if __name__ == "__main__":
    client = SeznamWebmaster()
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "status":
        print(json.dumps(client.status(), indent=2, ensure_ascii=False))
    elif action == "reindex" and len(sys.argv) > 2:
        print(json.dumps(client.reindex(sys.argv[2]), indent=2, ensure_ascii=False))
    elif action == "doc" and len(sys.argv) > 2:
        print(json.dumps(client.document(sys.argv[2]), indent=2, ensure_ascii=False))
    else:
        print("Usage: python3 test_seznam_api.py [status|reindex <url>|doc <url>]")
