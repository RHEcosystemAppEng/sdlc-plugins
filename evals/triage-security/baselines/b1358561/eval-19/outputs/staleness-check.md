# Step 0.3 – Matrix Staleness Check — TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (no `FULLSEND_OUTPUT_DIR`). Step 0 configuration validation passed: Repository Registry, Jira Configuration (Project key TC, Cloud ID present), Code Intelligence, and Security Configuration (Product Lifecycle, Version Streams, Source Repositories) are all present.

## Fixture / Extraction Evidence

| Item | Value |
|------|-------|
| Matrix source file | `security-matrix-stale-mock.md` (covers both configured streams: 2.1.x / rhtpa-release.0.3.z and 2.2.x / rhtpa-release.0.4.z) |
| Source Last-Updated HTML comment (verbatim) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC) |
| Comparison clock (evaluation clock) | `2026-07-12T10:00:00Z` (fixed UTC scenario time) |
| Computed matrix age | **72 days** (May 1 → Jun 1 = 31 days, Jun 1 → Jul 1 = 30 days, Jul 1 → Jul 12 = 11 days; exactly 72 × 24h) |
| Staleness threshold | 14 days (default) |
| Result | **STALE** — 72 days > 14 days |

The timestamp was found, so the "no timestamp" branch (step 4) does not apply, and the file is present, so the "missing file" branch (step 5) does not apply either.

## Staleness Warning — Stream 2.1.x (rhtpa-release.0.3.z)

> "Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate"

## Staleness Warning — Stream 2.2.x (rhtpa-release.0.4.z)

> "Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate"

## Observations Supporting the Warning

- The 2.2.x Supportability Matrix contains a row for 2.2.4 (build 0.4.12, Build Date 2026-05-04), which is *after* the matrix's own Last-Updated timestamp (2026-05-01). The timestamp is therefore inconsistent with the matrix contents and is unreliable, which is another reason to refresh.
- Releases made in the 72 days since the last update (for example a 2.2.5, or a new 2.3.x stream) may be missing. A missing release would cause Step 2 version-impact analysis for quinn-proto (fixed in 0.11.14) to be incomplete, and could affect the Step 3 correction of the PSIRT-assigned Affects Versions (`RHTPA 2.0.0`).

## Status

**Waiting for the user's choice. Triage is paused at Step 0.3.** Steps 0.5 onward (Jira access, assignment, data extraction, version impact analysis, and so on) do not run until the user picks one of these:

- **Refresh now** → run setup Step 10.6 matrix population for the selected stream(s), which writes a new `Last-Updated` timestamp, then continue with the refreshed matrix.
- **Proceed anyway** → continue to Step 0.5 using the current (stale) matrix, and note the staleness in the triage summary.
- **Stop** → halt triage.

No Jira MCP calls, `git show` commands, or other external tools were run.
