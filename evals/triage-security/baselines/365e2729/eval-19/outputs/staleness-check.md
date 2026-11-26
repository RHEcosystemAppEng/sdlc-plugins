# Step 0.3 – Matrix Staleness Check — TC-8001

## Context

- **Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
- **Execution mode**: Interactive (`FULLSEND_OUTPUT_DIR` is absent — Step 0.6 detection), so the interactive staleness check applies.
- **Step 0 (configuration)**: Passed. Repository Registry, Jira Configuration (Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present in `claude-md-security-config.md`.
- **Staleness threshold**: 14 days (default)

## Fixture / Clock Evidence

| Item | Value |
|------|-------|
| Evaluation clock (comparison "current date") | `2026-07-12T10:00:00Z` |
| Matrix source file | `security-matrix-stale-mock.md` (supplied fixture covering both configured streams) |
| Source Last-Updated HTML comment (verbatim, line 1) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC) |
| Computed matrix age | `2026-07-12T10:00:00Z` − `2026-05-01T10:00:00Z` = **72 days, 0 hours** |
| Threshold | 14 days |
| Result | **STALE** (72 > 14) |

Age arithmetic: May 1 → June 1 = 31 days; June 1 → July 1 = 30 days; July 1 → July 12 = 11 days; total = 72 days (same 10:00:00Z time of day, so exactly 72 days).

## Per-Stream Check

The Version Streams table in Security Configuration lists two streams. The supplied
matrix fixture contains both stream sections under a single `Last-Updated` timestamp,
so the same timestamp applies to each stream.

| Stream | Konflux Release Repo | Timestamp found | Last-Updated | Age (days) | Status |
|--------|----------------------|-----------------|--------------|------------|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | Yes | 2026-05-01T10:00:00Z | 72 | STALE |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | Yes | 2026-05-01T10:00:00Z | 72 | STALE |

Note: TC-8001 is scoped to stream 2.2.x (summary suffix `[rhtpa-2.2]`), but Step 0.3 runs
for every configured Version Stream before triage. Both streams are stale.

## Staleness Warnings (presented to the engineer)

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

## Status: BLOCKED — awaiting user choice

Triage is paused at Step 0.3. Per the skill, I wait for the engineer's choice
for each stale stream before proceeding to Step 0.5 (Jira access) and later steps.
No Jira calls, `git show` commands, or matrix writes have been performed.

- **Refresh now** → run setup Step 10.6 matrix population for the selected stream, which
  writes an updated `Last-Updated` timestamp, then continue with the refreshed matrix.
- **Proceed anyway** → continue triage (Step 0.5 onward) using the current 72-day-old
  matrix; version impact results may miss releases after 2026-05-01. For example, the
  2.2.x matrix lists 2.2.4 (build date 2026-05-04), which is after the matrix timestamp.
  That inconsistency is another reason the matrix contents should be checked.
- **Stop** → halt triage of TC-8001 so the engineer can investigate.
