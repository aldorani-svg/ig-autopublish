---
name: new-post
description: Create and queue an Instagram post for @laylaaldorani — write the caption in brand voice, produce or place the image, and append it to queue.json so the GitHub Action publishes it on the next Sun/Tue/Thu 20:30 Doha slot. Use on "new post", "queue a post", or "/new-post".
---

Run this as `personal-brand`.

1. Read `brands/layla-al-dorani.md` and the last 4 captions in `queue.json` so the voice stays consistent.
2. Pick the pillar and topic, and say which offer it supports, if any.
3. Write the caption: hook, 3–5 short lines, reframe, a question, then 4–6 hashtags. Check any health claim against PubMed.
4. **Image:** use the image Layla supplies, or generate one with Higgsfield (quiet-luxury look, 1080×1350 portrait), only after she agrees to spend the credits.
   Save it as `images/NN_slug.png`, where NN is the next number.
5. Append to the `posts` array in `queue.json` (keep valid JSON):
   ```json
   { "id": "NN_slug", "image": "images/NN_slug.png", "status": "queued", "caption": "..." }
   ```
6. Validate with `python3 -c "import json;json.load(open('queue.json'))"`.
7. Tell Layla the publish slot: count the queued posts ahead of this one against the Sun/Tue/Thu 20:30 schedule.
   It only goes live after the change is committed and pushed to `main`, so ask before pushing.
