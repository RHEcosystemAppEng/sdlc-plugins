# Step 0.3 – Matrix Staleness Check — TC-8001

## Mode

- Step 0.6: `FULLSEND_OUTPUT_DIR` is absent, so the skill runs in **interactive mode**. Step 0.3 runs as written. Step 0.7 is skipped.

## Fixture Evidence

| Item | Value |
|------|-------|
| Evaluation clock (current date for Step 0.3) | 2026-07-12T10:00:00Z |
| Matrix source | `security-matrix-mock.md` (one mock file holding both stream matrices) |
| `Last-Updated` timestamp | `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` |
| Computed matrix age | 2026-07-12T10:00:00Z − 2026-06-28T10:00:00Z = **14 days, 0 hours (exactly 14.0 days)** |
| Staleness threshold | Older than **14 days** |
| Comparison | 14.0 days is not greater than 14 days |

## Per-Stream Result

| Stream | Konflux Release Repo | Last-Updated | Age (days) | Stale? | Action |
|--------|----------------------|--------------|------------|--------|--------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 | No | Proceed |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 | No | Proceed |

## Result

**PASS: the matrix is fresh. No staleness warning.** Both streams are exactly at the 14-day threshold. The skill warns only when a matrix is *older than* 14 days, so this one is still within the threshold. The skill does not show the user the "Refresh now / Proceed anyway / Stop" prompt and does not wait for a choice. The timestamp is present, so the "no Last-Updated timestamp" advisory does not apply either. The matrix file exists, so the Step 2.1 fallback is not needed.

The evaluation clock and computed age above are recorded only as fixture evidence. They do not create a user-facing warning.

Triage continues to Step 0.5 / 0.8 / Step 1 using the current matrix.
