# Step 0.3 – Matrix Staleness Check — TC-8001

**Issue**: TC-8001 — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
**Mode**: Interactive (eval simulation — no Jira MCP, git, or external tools invoked)

## Fixture Evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for Step 0.3) | `2026-07-12T10:00:00Z` (fixed UTC scenario time) |
| Matrix file | `security-matrix-stale-mock.md` (covers both streams: 2.1.x / `rhtpa-release.0.3.z` and 2.2.x / `rhtpa-release.0.4.z`) |
| Computed matrix age | **72 days** (exactly 72 days, 0 hours: 2026-05-01T10:00:00Z → 2026-07-12T10:00:00Z) |
| Staleness threshold | 14 days (default) |
| Result | **STALE** — 72 days > 14 days |

Age computation: May 1 → June 1 = 31 days; June 1 → July 1 = 30 days; July 1 → July 12 = 11 days; total = 72 days (both timestamps at 10:00:00 UTC, so no partial day).

## Extraction Evidence

| Item | Value |
|------|-------|
| Source HTML comment (line 1 of matrix file) | `<!-- Last-Updated: 2026-05-01T10:00:00Z -->` |
| Parsed ISO 8601 timestamp | `2026-05-01T10:00:00Z` (2026-05-01 10:00:00 UTC, offset +00:00) |
| Comparison clock | `2026-07-12T10:00:00Z` (evaluation clock) |
| Difference | 72 days, 0:00:00 |

Note: the project CLAUDE.md Version Streams table has no explicit Security Matrix Path column; the supplied fixture `security-matrix-stale-mock.md` is used as the matrix for both configured streams. Since both streams share the same file and timestamp, both are stale.

## Per-Stream Results

| Stream | Konflux Release Repo | Last-Updated | Age | Status |
|--------|----------------------|--------------|-----|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-05-01T10:00:00Z | 72 days | STALE |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-05-01T10:00:00Z | 72 days | STALE |

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

## Gate Status

**Waiting for the user's choice before proceeding.** Triage does not continue to Step 0.5 / Step 1 until the user selects an option for each stale stream.

- **Refresh now** → invoke setup Step 10.6 matrix population for the selected stream; it writes an updated `Last-Updated` timestamp, and triage continues with the refreshed matrix. (No matrix write has been performed in this eval; the `Last-Updated` timestamp remains unchanged.)
- **Proceed anyway** → continue triage using the current (72-day-old) matrix data.
- **Stop** → halt triage for investigation.

Context for the user's decision: the stale matrix may be missing releases after 2026-05-01 (the latest recorded 2.2.x release is 2.2.4, built 2026-05-04 — itself after the Last-Updated timestamp, which suggests the timestamp was not refreshed when that row was added, or further releases may exist). Since TC-8001 targets the 2.2.x stream ([rhtpa-2.2]) and is due 2026-07-15, a refresh is recommended before computing version impact.
