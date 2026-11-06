# Step 0.3 – Matrix Staleness Check — TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (`FULLSEND_OUTPUT_DIR` not set in this eval scenario)
**Step 0 result**: Security Configuration present and complete (Product Lifecycle, Version Streams, Source Repositories) — proceed to Step 0.3.

## Fixture / Extraction Evidence

| Item | Value |
|------|-------|
| Matrix file read | `security-matrix-stale-mock.md` (eval fixture standing in for each stream's `security-matrix.md`) |
| Source Last-Updated HTML comment (line 1, verbatim) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC) |
| Comparison clock (evaluation clock, used as "current date") | `2026-07-12T10:00:00Z` (2026-07-12 10:00:00 UTC) |
| Computed matrix age | 72 days, 0 hours (2026-07-12T10:00:00Z − 2026-05-01T10:00:00Z) |
| Staleness threshold | 14 days (default) |
| Result | **STALE** — 72 days > 14 days |

Age computation: May 1 → May 31 = 30 days, + June (30 days) = 60, + July 1 → July 12 = 12 → **72 days**.

Note: the evaluation clock (2026-07-12T10:00:00Z) is used as the current date per the scenario instructions, not the runner/grader wall clock.

## Per-Stream Check

The Version Streams table in Security Configuration lists two streams. The fixture provides a single matrix document containing both streams under one `Last-Updated` timestamp, so the same timestamp applies to each.

| Stream | Konflux Release Repo | Last-Updated | Age | Status |
|--------|----------------------|--------------|-----|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-05-01T10:00:00Z | 72 days | STALE (> 14 days) |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-05-01T10:00:00Z | 72 days | STALE (> 14 days) |

## Staleness Warning (presented to user)

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

## Why This Matters for TC-8001

The matrix's 2.2.x supportability table ends at 2.2.4 (built 2026-05-04, which is after the matrix's own Last-Updated value). Any 2.2.x release published between May and 2026-07-12 would be missing. That would affect Step 2 version impact analysis for quinn-proto (fixed in 0.11.14) and the Step 3 Affects Versions correction (PSIRT currently lists "RHTPA 2.0.0").

## Execution Status

**Blocked — waiting for the user to choose.** Per Step 0.3, triage does not continue to Step 0.5 (Jira Access) or later steps until the user picks Refresh now, Proceed anyway, or Stop for each stale stream. No Jira calls, `git show` commands, or matrix writes were made.

- **Refresh now** → run setup Step 10.6 matrix population for the selected stream. This writes a new `Last-Updated` timestamp, then triage continues with the refreshed matrix.
- **Proceed anyway** → continue to Step 0.5 using the current (stale) matrix data.
- **Stop** → end triage for TC-8001 with no changes.
