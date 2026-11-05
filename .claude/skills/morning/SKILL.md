---
name: morning
description: Layla's daily brief — today's calendar, inbox items that need her, the 3 things that matter today across all brands, and any decisions waiting on her. Use when she says good morning, "what's today", "brief me", or "/morning".
---

Run this as the `chief-of-staff`. Keep the brief short enough to read in 60 seconds on a phone.

1. Read `ops/priorities.md` and `ops/tasks.md`.
2. **Calendar:** list today's Google Calendar events in Doha time. Flag conflicts, missing prep and any day with more than 10 hours booked.
3. **Inbox:** search Gmail for unread or important messages from the last 24 hours. Show only what needs Layla today, sorted by brand. Draft replies where useful and leave them as drafts.
4. **Instagram queue:** count the `queued` posts in `queue.json`. If there are fewer than 3, flag it and offer to have `personal-brand` fill it.
5. **Revenue:** give a one-line status against the 90-day target from `ops/revenue-log.md`.

Output:
```
☀️ <Day, date>
THE 3 THINGS: 1… 2… 3…
CALENDAR: …
NEEDS YOU: …  (drafts ready: n)
DECISIONS: …
```
