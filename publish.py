#!/usr/bin/env python3
"""
publish.py — Publishes the next queued post to Instagram via the official
Instagram Graph API (Content Publishing).

It is designed to run unattended on a schedule (GitHub Actions). On each run it:
  1. Finds the first post in queue.json still marked "queued".
  2. Builds a PUBLIC url for that post's image (raw.githubusercontent.com).
  3. Creates a media container, waits for it to be ready, then publishes it.
  4. Flips that post's status to "posted" and stamps the time.

Required environment variables (set as GitHub Actions secrets / repo vars):
  IG_USER_ID        Instagram Business account id (numeric)
  IG_ACCESS_TOKEN   Long-lived access token with instagram_content_publish
  GITHUB_REPOSITORY owner/repo  (GitHub sets this automatically in Actions)
  GITHUB_REF_NAME   branch name (GitHub sets this automatically; default "main")

Flags:
  --dry-run      Do everything except the final publish call (safe test).
  --check-token  Print token validity + the connected account, then exit.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error

API_VERSION = "v21.0"
GRAPH = f"https://graph.facebook.com/{API_VERSION}"
HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE_PATH = os.path.join(HERE, "queue.json")


def _get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def _post(url, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def _explain(e):
    """Turn an HTTPError into a readable Graph API message."""
    try:
        payload = json.loads(e.read().decode())
        err = payload.get("error", {})
        return f"{err.get('type','?')}: {err.get('message','?')} (code {err.get('code','?')})"
    except Exception:
        return str(e)


def env(name, required=True, default=None):
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"ERROR: missing required environment variable {name}")
    return val


def check_token(token):
    try:
        me = _get(f"{GRAPH}/me?fields=id,username&access_token={urllib.parse.quote(token)}")
        print("Token OK. Connected account:", json.dumps(me))
    except urllib.error.HTTPError as e:
        sys.exit("Token check FAILED -> " + _explain(e))


def raw_url(repo, branch, rel_path):
    # The repo root IS the automation folder, so rel paths like "images/01.png"
    # map directly to raw.githubusercontent.com/<owner>/<repo>/<branch>/images/01.png
    rel_path = rel_path.replace(os.sep, "/")
    parts = "/".join(urllib.parse.quote(seg) for seg in rel_path.split("/"))
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{parts}"


def main():
    dry = "--dry-run" in sys.argv
    token = env("IG_ACCESS_TOKEN")

    if "--check-token" in sys.argv:
        check_token(token)
        return

    ig_user = env("IG_USER_ID")
    repo = env("GITHUB_REPOSITORY")
    branch = env("GITHUB_REF_NAME", required=False, default="main")

    with open(QUEUE_PATH) as f:
        queue = json.load(f)

    nxt = next((p for p in queue["posts"] if p.get("status") == "queued"), None)
    if not nxt:
        print("Queue empty: nothing marked 'queued'. Nothing to do.")
        return

    image_url = raw_url(repo, branch, nxt["image"])
    caption = nxt["caption"]
    print(f"Next post: {nxt['id']}")
    print(f"Image URL: {image_url}")

    # 1) create media container
    try:
        container = _post(f"{GRAPH}/{ig_user}/media", {
            "image_url": image_url,
            "caption": caption,
            "access_token": token,
        })
    except urllib.error.HTTPError as e:
        sys.exit("Create container FAILED -> " + _explain(e))
    creation_id = container["id"]
    print("Container created:", creation_id)

    # 2) wait until the container is FINISHED (images are usually instant)
    for _ in range(20):
        st = _get(f"{GRAPH}/{creation_id}?fields=status_code&access_token={urllib.parse.quote(token)}")
        code = st.get("status_code")
        print("  container status:", code)
        if code == "FINISHED":
            break
        if code == "ERROR":
            sys.exit("Container processing ERROR. Check the image URL is public.")
        time.sleep(3)

    if dry:
        print("DRY RUN: skipping publish. Everything up to publish succeeded.")
        return

    # 3) publish
    try:
        published = _post(f"{GRAPH}/{ig_user}/media_publish", {
            "creation_id": creation_id,
            "access_token": token,
        })
    except urllib.error.HTTPError as e:
        sys.exit("Publish FAILED -> " + _explain(e))
    print("PUBLISHED. Media id:", published.get("id"))

    # 4) mark posted
    nxt["status"] = "posted"
    nxt["published_media_id"] = published.get("id")
    with open(QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("queue.json updated.")


if __name__ == "__main__":
    main()
