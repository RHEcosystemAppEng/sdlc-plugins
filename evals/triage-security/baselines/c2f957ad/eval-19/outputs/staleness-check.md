# Step 0.3 – Matrix Staleness Check — TC-8001

## Context

- **Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
- **Execution mode (Step 0.6)**: interactive (`FULLSEND_OUTPUT_DIR` absent) — Step 0.7 skipped
- **Step 0 configuration**: validated (Repository Registry, Jira Configuration, Code
  Intelligence, Security Configuration with Product Lifecycle, Version Streams, Source
  Repositories all present). Project key `TC`, Jira version prefix `RHTPA`,
  Vulnerability issue type ID `10024`, component label pattern `pscomponent:`.
- **Staleness threshold**: 14 days (default)

## Fixture Evidence

| Item | Value |
|---|---|
| Evaluation clock (comparison clock / "current date") | `2026-07-12T10:00:00Z` |
| Matrix file read | `evals/triage-security/files/security-matrix-stale-mock.md` (stands in for each stream's `security-matrix.md`) |
| Source Last-Updated HTML comment (line 1, verbatim) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC) |
| Computed matrix age | `2026-07-12T10:00:00Z` − `2026-05-01T10:00:00Z` = **72 days, 0 hours** (May 1→Jun 1: 31 d, Jun 1→Jul 1: 30 d, Jul 1→Jul 12: 11 d) |
| Threshold | 14 days |
| Result | **STALE** (72 > 14) |

The Version Streams table in Security Configuration lists two streams (`2.1.x`,
`2.2.x`). The supplied matrix fixture contains both streams and carries a single
Last-Updated timestamp, so the same timestamp and age apply to each stream.

| Stream | Konflux Release Repo | Last-Updated | Age (days) | Status |
|---|---|---|---|---|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-05-01T10:00:00Z | 72 | STALE |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-05-01T10:00:00Z | 72 | STALE |

## Staleness Warnings

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

Note: TC-8001 is scoped to `[rhtpa-2.2]` → stream **2.2.x**, but Step 0.3 checks
every configured stream. Step 2 analyzes all supported versions, so a stale 2.1.x
matrix also matters for cross-stream impact.

## Awaiting User Choice

**Triage is paused at Step 0.3.** No later step (0.5 Jira access, 0.8 assignment,
1 data extraction, etc.) has started, and no Jira mutation has been made. Pick an
option for each stale stream:

- **Refresh now** — run setup Step 10.6 matrix population for the stream. This
  writes a new `Last-Updated` timestamp, and triage then continues with the
  refreshed matrix.
- **Proceed anyway** — continue triage with the matrix as it is (72 days old).
  Releases after 2026-05-01 may be missing, and source commit references may be
  out of date.
- **Stop** — end triage here so you can look into the matrix.
