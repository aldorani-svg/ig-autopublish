# One-time setup — Instagram auto-publisher

You do this **once**. After it's done, posts publish themselves Sun/Tue/Thu at
8:30pm Qatar time, with zero taps from you. Budget about 1 hour. I (Claude) can
sit with you and do the navigating/reading; the parts only you can do are the
logins and the one "Allow" click.

There are 3 things to set up: **(A) a Meta app + token**, **(B) a GitHub repo**,
**(C) paste the secrets in.**

---

## A. Meta app + access token  (the OAuth gate — only you can click "Allow")

**A1. Confirm your Instagram is a Business account and linked to your Page.**
You already did this — IG @laylaaldorani is linked to your Facebook Page
"Layla Al-Dorani". Good.

**A2. Create a developer app.**
1. Go to **developers.facebook.com** → log in with your Facebook → "My Apps" → **Create App**.
2. Use case: choose **Other** → type **Business** → name it `Layla Auto Publisher`.
3. When it's created, open the app's **Settings → Basic**. Copy the **App ID** and
   **App Secret** (click "Show"). Keep them safe — these are two of our secrets.

**A3. Give the app Instagram publishing permission + get a token.**
1. In the left menu, **Add product → Instagram → set up** (Instagram Graph API).
2. Open **Tools → Graph API Explorer** (top right, or developers.facebook.com/tools/explorer).
3. In the Explorer: set **Application** = `Layla Auto Publisher`.
4. Click **Add a Permission** and tick all of these:
   `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
   `pages_read_engagement`, `business_management`.
5. Click **Generate Access Token** → a Facebook window pops up → **log in and click Allow**.
   *(This is the one OAuth click only you can do.)*

**A4. Get your Instagram account id (numeric).**
Still in Graph API Explorer, run these (type in the path box, press Run):
1. `me/accounts` → find your Page, copy its **id**.
2. `<PAGE_ID>?fields=instagram_business_account` → copy the **id** it returns.
   **That number is your `IG_USER_ID`.**

**A5. Turn the short token into a 60-day token.**
The token from step A3 only lasts ~1 hour. On your Mac, in Terminal:
```
cd "/Users/laylaal-dorani/Personal branding/automation"
APP_ID=PASTE_APP_ID APP_SECRET=PASTE_APP_SECRET IG_ACCESS_TOKEN=PASTE_SHORT_TOKEN python3 refresh_token.py
```
It prints a **long-lived token (~60 days)**. That value is your `IG_ACCESS_TOKEN`.

You now have three values:  **IG_USER_ID**, **IG_ACCESS_TOKEN**, and (kept for refreshes) **APP_ID** + **APP_SECRET**.

---

## B. GitHub repo (free cloud that holds the queue + runs the schedule)

1. Make a free account at **github.com** if you don't have one.
2. Create a **new repository** → name `ig-autopublish` → set it **Private** → Create.
3. Upload this `automation` folder's contents to the repo. Easiest non-technical way:
   on the empty repo page click **uploading an existing file**, then drag in
   everything inside `automation/` (publish.py, queue.json, refresh_token.py,
   the `images` folder, and the `.github` folder). Commit.
   *(Or, if you're comfortable: `git init && git add . && git commit && git push` — see README.)*

> The repo can be **Private**. Instagram still reads the images because the
> publishing step uses your token; the raw image links work for the job.
> If a private repo ever blocks the image read, flip the repo to Public — the
> images are just your post graphics, nothing sensitive.

---

## C. Paste the secrets

In your GitHub repo: **Settings → Secrets and variables → Actions → New repository secret.**
Add two secrets (names must match exactly):

| Name | Value |
|------|-------|
| `IG_USER_ID` | the numeric id from A4 |
| `IG_ACCESS_TOKEN` | the long-lived token from A5 |

---

## D. Test it (no waiting for the schedule)

1. In the repo, open the **Actions** tab → enable workflows if prompted.
2. Click **"Publish to Instagram"** → **Run workflow** → tick **dry run** → Run.
   A green check means everything works except it didn't actually post.
3. Happy? Run it again with **dry run OFF** → this publishes **post #1 for real.**
   Check your Instagram. 🎉

After that, leave it alone. It posts #2 and #3 on the next Tue/Thu automatically,
and keeps going as long as the queue has items marked `"queued"`.

---

## Ongoing (the only recurring task)

- **Every ~50 days:** the token expires. You'll get an automatic email from
  GitHub when the health check fails. Re-run the A5 command to mint a fresh
  token and update the `IG_ACCESS_TOKEN` secret. ~2 minutes.
- **New content:** I generate a batch of posts (images + captions), you drop
  them into `images/` and add entries to `queue.json` with `"status": "queued"`.
  They publish in order on the schedule.
