# Step 0.3 – Matrix Staleness Check — TC-8001

**Issue:** TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Execution mode:** Interactive (Step 0.6: `FULLSEND_OUTPUT_DIR` absent — eval simulation; no Jira/git/external calls made)

## Fixture / Extraction Evidence

| Item | Value |
|------|-------|
| Evaluation clock (comparison "current date") | `2026-07-12T10:00:00Z` |
| Matrix file read | `security-matrix-stale-mock.md` (combined fixture covering both configured streams) |
| Source HTML comment (line 1 of matrix) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01, 10:00:00 UTC) |
| Comparison clock | `2026-07-12T10:00:00Z` (fixed evaluation clock, not runner wall clock) |
| Computed matrix age | **72 days** (May 1→Jun 1 = 31 d, Jun 1→Jul 1 = 30 d, Jul 1→Jul 12 = 11 d; exact 72 × 24 h) |
| Staleness threshold | 14 days (default) |
| Result | **STALE** — 72 days > 14 days |

## Version Streams Checked (from Security Configuration)

| Stream | Konflux Release Repo | Matrix Section | Last-Updated | Age | Status |
|--------|----------------------|----------------|--------------|-----|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | Stream 1: rhtpa-release.0.3.z | 2026-05-01T10:00:00Z | 72 days | STALE |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | Stream 2: rhtpa-release.0.4.z | 2026-05-01T10:00:00Z | 72 days | STALE |

Note: the Security Configuration Version Streams table has no explicit Security Matrix
Path column; the provided fixture file is used as the matrix for both streams, and its
single Last-Updated timestamp applies to each stream.

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

## Gate

**Triage is paused awaiting the user's choice** (Refresh now / Proceed anyway / Stop).
No further steps (0.5 onward: Jira access, data extraction, version impact analysis)
are executed until the user responds.

- If **Refresh now**: invoke setup Step 10.6 matrix population for the selected stream,
  which writes an updated `Last-Updated` timestamp, then continue with the refreshed matrix.
- If **Proceed anyway**: continue triage using the current (stale) matrix. Risk: the
  2.2.x matrix lists builds only up to 2.2.4 (build date 2026-05-04); any releases after
  that date (e.g., a later 2.2.x or 2.3.x stream) would be missed in the version impact analysis.
- If **Stop**: halt triage; no Jira changes are made to TC-8001.
