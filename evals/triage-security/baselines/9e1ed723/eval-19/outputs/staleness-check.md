# Step 0.3 – Matrix Staleness Check — TC-8001

## Execution context

- **Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
- **Mode (Step 0.6)**: interactive (`FULLSEND_OUTPUT_DIR` absent) — the Step 0.3 staleness check applies
- **Step 0 (configuration)**: Passed — Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present.
- **Version Streams evaluated** (from Security Configuration):

| Stream | Konflux Release Repo | Matrix source used in this eval |
|--------|----------------------|---------------------------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | `security-matrix-stale-mock.md` (Stream 1) |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | `security-matrix-stale-mock.md` (Stream 2) |

## Extraction evidence

| Item | Value |
|------|-------|
| Source Last-Updated HTML comment (line 1 of matrix) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC) |
| Comparison clock (evaluation clock, fixed UTC scenario time) | `2026-07-12T10:00:00Z` |

## Fixture evidence — age computation

| Item | Value |
|------|-------|
| Evaluation clock | 2026-07-12T10:00:00Z |
| Matrix Last-Updated | 2026-05-01T10:00:00Z |
| Computed matrix age | **72 days** (May 1 → May 31 = 30 days, + May 31 → June 30 = 30 days, + June 30 → July 12 = 12 days; 2026-07-12T10:00Z − 2026-05-01T10:00Z = exactly 72 × 24 h) |
| Staleness threshold (default) | 14 days |
| Result | **STALE** — 72 days > 14 days (58 days past threshold) |

Both streams are defined in the same matrix fixture and share the single
Last-Updated timestamp, so both are evaluated as stale.

## Staleness warning (presented to the user)

> "Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate"

> "Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate"

## User options

| Option | Effect |
|--------|--------|
| 1. Refresh now | Invoke the setup Step 10.6 matrix population logic for the selected stream; it writes an updated `Last-Updated` timestamp, then triage continues with the refreshed matrix. |
| 2. Proceed anyway | Continue triage (Step 0.5 onward) using the current 72-day-old matrix. Risk: releases after 2026-05-01 (e.g. newer 2.2.x builds) and updated pinned source commits may be missing from the version impact analysis. |
| 3. Stop | Halt triage of TC-8001 so the engineer can investigate the matrix before re-running. |

## Status

**Blocked — awaiting user choice.** Per Step 0.3, triage does not proceed to
Step 0.5 (Jira Access), Step 0.8, or Step 1 until the engineer selects one of the
options above for each stale stream. No Jira calls, `git show` commands, or
matrix writes have been performed.
