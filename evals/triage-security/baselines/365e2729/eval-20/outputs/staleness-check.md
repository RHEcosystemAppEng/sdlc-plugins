# Step 0.3 – Matrix Staleness Check (TC-8001)

## Mode

Step 0.6: `FULLSEND_OUTPUT_DIR` absent → **interactive mode**. Step 0.7 skipped.

## Fixture Evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for Step 0.3) | 2026-07-12T10:00:00Z |
| Matrix source | `security-matrix-mock.md` (covers both configured streams) |
| `<!-- Last-Updated -->` timestamp | 2026-06-28T10:00:00Z |
| Computed matrix age | 14 days exactly (1,209,600 seconds) |
| Staleness threshold | older than 14 days (default) |

## Per-Stream Result

| Stream | Konflux Release Repo | Last-Updated | Age (days) | Stale (> 14 days)? | Action |
|--------|----------------------|--------------|------------|--------------------|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 | No | Proceed |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 | No | Proceed |

## Outcome

**PASS — matrix is fresh.** The age (14 days) is equal to, not greater than, the
14-day threshold, so the matrix is within the threshold. No staleness warning is
presented, no Refresh/Proceed/Stop prompt is needed, and triage proceeds directly to
Step 0.5 / Step 1.

A Last-Updated timestamp was found, so the "no timestamp" advisory does not apply.
The matrix file exists for both streams, so the Step 2.1 fallback is not triggered.
