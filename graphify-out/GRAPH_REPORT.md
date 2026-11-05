# Graph Report - ig-autopublish  (2026-11-05)

## Corpus Check
- 7 files · ~2,279 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 1 file(s) not represented in the graph (top: (none) 1)

## Summary
- 78 nodes · 99 edges · 9 communities (8 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `59b151fd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- keepalive.yml
- publish.yml
- dry_run
- steps
- main
- @laylaaldorani — Instagram auto-publisher
- One-time setup — Instagram auto-publisher
- sys

## God Nodes (most connected - your core abstractions)
1. `main()` - 10 edges
2. `steps` - 6 edges
3. `check_token()` - 6 edges
4. `@laylaaldorani — Instagram auto-publisher` - 6 edges
5. `One-time setup — Instagram auto-publisher` - 6 edges
6. `_explain()` - 5 edges
7. `steps` - 4 edges
8. `dry_run` - 4 edges
9. `_get()` - 4 edges
10. `main()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `env()`  [EXTRACTED]
  publish.py → publish.py  _Bridges community 8 → community 4_

## Import Cycles
- None detected.

## Communities (9 total, 1 thin omitted)

### Community 0 - "keepalive.yml"
Cohesion: 0.13
Nodes (14): jobs, keepalive, runs-on, steps, name, on, schedule, workflow_dispatch (+6 more)

### Community 1 - "publish.yml"
Cohesion: 0.20
Nodes (9): concurrency, cancel-in-progress, group, jobs, publish, name, permissions, contents (+1 more)

### Community 2 - "dry_run"
Cohesion: 0.22
Nodes (9): default, description, type, dry_run, on, schedule, workflow_dispatch, cron (+1 more)

### Community 3 - "steps"
Cohesion: 0.22
Nodes (9): IG_ACCESS_TOKEN, IG_USER_ID, steps, env, name, run, uses, with (+1 more)

### Community 4 - "main"
Cohesion: 0.39
Nodes (6): check_token(), _explain(), _get(), main(), _post(), raw_url()

### Community 6 - "@laylaaldorani — Instagram auto-publisher"
Cohesion: 0.29
Nodes (6): Add new content, First time, @laylaaldorani — Instagram auto-publisher, Local test, Push from the command line (optional, instead of drag-and-drop upload), Run a real post right now (after setup)

### Community 7 - "One-time setup — Instagram auto-publisher"
Cohesion: 0.29
Nodes (6): A. Meta app + access token  (the OAuth gate — only you can click "Allow"), B. GitHub repo (free cloud that holds the queue + runs the schedule), C. Paste the secrets, D. Test it (no waiting for the schedule), One-time setup — Instagram auto-publisher, Ongoing (the only recurring task)

### Community 8 - "sys"
Cohesion: 0.67
Nodes (3): env(), env(), main()

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `publish` connect `publish.yml` to `steps`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Should `keepalive.yml` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `steps` connect `steps` to `publish.yml`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._