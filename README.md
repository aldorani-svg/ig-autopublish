# @laylaaldorani — Instagram auto-publisher

A free, self-hosted pipeline that publishes Instagram posts on a schedule using
Instagram's official Graph API. No monthly fees, no third-party scheduler.

- **`queue.json`** — the posting queue. Topmost item with `"status":"queued"`
  publishes next; it flips to `"posted"` automatically after success.
- **`images/`** — the post graphics referenced by the queue.
- **`publish.py`** — the engine. Creates a media container and publishes it.
- **`refresh_token.py`** — mints a fresh 60-day token (run when the old one nears expiry).
- **`.github/workflows/publish.yml`** — the scheduler: Sun/Tue/Thu 20:30 Asia/Qatar.
- **`.github/workflows/token-health.yml`** — emails you if the token breaks.

## First time
See **SETUP.md** for the full one-time walkthrough.

## Push from the command line (optional, instead of drag-and-drop upload)
```
cd "/Users/laylaal-dorani/Personal branding/automation"
git init
git add .
git commit -m "Instagram auto-publisher"
git branch -M main
git remote add origin https://github.com/<your-username>/ig-autopublish.git
git push -u origin main
```

## Run a real post right now (after setup)
Actions tab → "Publish to Instagram" → Run workflow (dry run off).

## Add new content
1. Drop the image into `images/`.
2. Add an entry to the `posts` array in `queue.json`:
   ```json
   { "id": "04_recipe", "image": "images/04_recipe.png", "status": "queued",
     "caption": "Your caption...\n\n#hashtags" }
   ```
3. Commit / upload. It publishes on the next scheduled slot.

## Local test
```
IG_USER_ID=... IG_ACCESS_TOKEN=... GITHUB_REPOSITORY=you/ig-autopublish \
  python3 publish.py --dry-run
```
