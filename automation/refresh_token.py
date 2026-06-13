#!/usr/bin/env python3
"""
refresh_token.py — Get a fresh 60-day Instagram/Facebook access token.

Long-lived tokens expire after ~60 days. Run this any time within that window
(it does NOT require re-doing the browser login) to mint a new 60-day token,
then paste the new value into your GitHub secret IG_ACCESS_TOKEN.

Usage:
  APP_ID=xxx APP_SECRET=yyy IG_ACCESS_TOKEN=current_token python refresh_token.py

It prints the new token and how many days it is valid.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

API_VERSION = "v21.0"
GRAPH = f"https://graph.facebook.com/{API_VERSION}"


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"ERROR: missing environment variable {name}")
    return v


def main():
    app_id = env("APP_ID")
    app_secret = env("APP_SECRET")
    token = env("IG_ACCESS_TOKEN")

    q = urllib.parse.urlencode({
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": token,
    })
    url = f"{GRAPH}/oauth/access_token?{q}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read().decode())["error"]["message"]
        except Exception:
            msg = str(e)
        sys.exit("Refresh FAILED -> " + msg)

    new_token = data.get("access_token", "")
    expires = data.get("expires_in")
    print("\n=== NEW LONG-LIVED TOKEN (paste into GitHub secret IG_ACCESS_TOKEN) ===\n")
    print(new_token)
    if expires:
        print(f"\nValid for ~{int(expires)//86400} days.")


if __name__ == "__main__":
    main()
