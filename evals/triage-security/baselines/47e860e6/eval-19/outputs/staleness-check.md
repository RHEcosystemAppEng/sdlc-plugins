# Step 0.3 – Matrix Staleness Check — TC-8001

**Issue:** TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode:** Interactive (FULLSEND_OUTPUT_DIR absent; simulated eval, no external calls)

## Step 0 prerequisite (configuration validated)

`claude-md-security-config.md` contains Repository Registry, Jira Configuration (Project key TC,
Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432), Code Intelligence, and Security Configuration
(Product Lifecycle, Version Streams, Source Repositories). Configuration is valid, so Step 0.3 runs.

Version Streams to check:

| Stream | Konflux Release Repo |
|--------|----------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z |

Note: the Version Streams table does not have a Security Matrix Path column. For this eval the
matrix comes from the fixture `security-matrix-stale-mock.md`. That one file holds both
streams (Stream 1: 2.1.x, Stream 2: 2.2.x) and has a single Last-Updated header, so the same
timestamp applies to both streams.

## Extraction evidence

| Item | Value |
|------|-------|
| Source file | `security-matrix-stale-mock.md` (line 1) |
| Source Last-Updated HTML comment (verbatim) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC) |
| Comparison clock (evaluation clock, fixed scenario time) | `2026-07-12T10:00:00Z` |
| Runner/grader wall clock | Ignored, as the eval instructions require |

## Age computation (fixture evidence)

- 2026-05-01T10:00Z → 2026-06-01T10:00Z = 31 days (May)
- 2026-06-01T10:00Z → 2026-07-01T10:00Z = 30 days (June)
- 2026-07-01T10:00Z → 2026-07-12T10:00Z = 11 days
- **Matrix age = 72 days** (exactly 72 × 24 h; no partial day)
- Staleness threshold = **14 days** (default)
- 72 > 14 → **STALE**

| Stream | Last-Updated | Age at evaluation clock | Threshold | Result |
|--------|--------------|-------------------------|-----------|--------|
| 2.1.x | 2026-05-01T10:00:00Z | 72 days | 14 days | STALE: warning issued |
| 2.2.x | 2026-05-01T10:00:00Z | 72 days | 14 days | STALE: warning issued |

## Staleness warning (presented to user)

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

## Why this matters for TC-8001

The issue is tagged `[rhtpa-2.2]`, so the 2.2.x stream matrix is the main input to Step 2
version impact analysis. If the matrix is stale, it may be missing 2.2.x releases from after
2026-05-01, or their pinned backend tags. A missing release could carry a different quinn-proto
version than the current newest entry (2.2.4 / `v0.4.12`, quinn-proto 0.11.14).

## Status

**Blocking: waiting for the user's choice** (Refresh now / Proceed anyway / Stop) before
continuing to Step 0.5 (Jira Access Initialization). Nothing was read from or written to Jira,
git, or `security-matrix.md`.

- If **Refresh now**: run setup Step 10.6 matrix population for the selected stream(s). This writes
  a new `Last-Updated` timestamp. Then continue triage with the refreshed matrix.
- If **Proceed anyway**: continue triage with the current (72-day-old) matrix, and note in the
  triage summary that it was stale.
- If **Stop**: halt triage. Make no Jira changes.
