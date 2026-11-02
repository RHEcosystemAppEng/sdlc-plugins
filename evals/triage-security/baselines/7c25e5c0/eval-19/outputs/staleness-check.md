# Step 0.3 — Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock**: `2026-07-12T10:00:00Z` (fixed UTC scenario time)
- **Source HTML comment**: `<!-- Last-Updated: 2026-05-01T10:00:00Z -->`
- **Parsed ISO 8601 timestamp**: `2026-05-01T10:00:00Z`
- **Comparison clock**: `2026-07-12T10:00:00Z`
- **Computed matrix age**: 72 days (May 1 → July 12)
- **Staleness threshold**: 14 days (default)
- **Result**: 72 days > 14 days → **STALE**

## Extraction Evidence

Step 0.3 reads each version stream's `security-matrix.md` and extracts the
`<!-- Last-Updated: <ISO-8601> -->` HTML comment from the top of the file.

The stale matrix fixture contains this comment on line 1:

```
<!-- Last-Updated: 2026-05-01T10:00:00Z -->
```

The ISO 8601 value `2026-05-01T10:00:00Z` is parsed and compared against the
evaluation clock `2026-07-12T10:00:00Z`.

**Age calculation**: From 2026-05-01 to 2026-07-12:
- May: 30 remaining days (May 1 → May 31)
- June: 30 days
- July: 12 days
- **Total: 72 days**

## Staleness Warning

Step 0.3 runs **before** Step 0.5 (JIRA Access Initialization). No Jira
operations are attempted before the staleness check completes.

### Stream: 2.1.x (rhtpa-release.0.3.z)

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

Waiting for user choice before proceeding.

### Stream: 2.2.x (rhtpa-release.0.4.z)

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** — re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** — continue triage with the current matrix
> 3. **Stop** — halt triage so I can investigate

Waiting for user choice before proceeding.

## Step Ordering

Step 0.3 (Matrix Staleness Check) executes **before** Step 0.5 (JIRA Access
Initialization). The staleness check is a local-only operation — it reads the
matrix file and compares timestamps. No Jira connections, API calls, or external
queries are made before this check completes and the user responds.

If the user chooses **Refresh now**, the skill invokes the matrix population logic
from setup Step 10.6 for the selected stream. After population completes (which
writes an updated `Last-Updated` timestamp), triage continues with the refreshed
matrix.

If the user chooses **Proceed anyway**, triage continues with the current
(potentially outdated) matrix data.

If the user chooses **Stop**, triage halts immediately.
