# Launch approval pack (2026-11-07)

`launch-approval-2026-11-07.csv` has one row per new page (816). Sort by **Batch**. Regenerate with:
`npm run build`, `python3 -I tools/uniqueness.py --csv /tmp/uq.csv`, `python3 -I tools/launch_pack.py`, `npm run build`.

| Batch | Pages | What it is | Recommendation |
|---|---|---|---|
| A. Approve now | 479 | Search page with its live search wired, 70%+ unique wording, at least 2 pages linking in; 68 school pages with sold figures | Approve |
| B. Hold: waiting for Jerry | 97 | The page has a listings box but no saved search yet | Approve when Jerry's sheets come back |
| C. Hold: waiting for Pete | 76 | School pages with no sold figures yet | Approve when Pete's exports are loaded |
| E. Auto-generated | 164 | Market stats, bedroom searches, presale pages and similar, built from data | Goes live with batch A |

A hold is not a deletion. In the preview each held page shows a note saying why. In the launch build it is noindex, out of the sitemap, out of the footer and out of generated link lists (the main menu still lists five held hubs; see `docs/06`).
Pages under 5 active listings (3-month average) are set to noindex automatically by the listing gate; none of the new pages are affected today.

## Update 2026-11-08
Jared approved the 46 school pages that have Pete's sold figures (listed under `later` in `approvals.json`). Total approved: 689 pages. The 139 "Not yet" pages are all held: 97 wait for Jerry (batch B), 42 wait for Pete (batch C). This approves pages only; nothing is launched.
