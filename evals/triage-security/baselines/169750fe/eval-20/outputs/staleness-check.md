# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z
- **Matrix Last-Updated timestamp**: 2026-06-28T10:00:00Z
- **Computed matrix age**: 14 days (exactly)

## Staleness Determination

The skill threshold is **older than 14 days** (strict inequality). A matrix that is exactly 14 days old does **not** exceed the threshold.

- 2026-07-12T10:00:00Z minus 2026-06-28T10:00:00Z = 14 days 0 hours 0 minutes
- 14 days is **not** older than 14 days (14 > 14 is false)

## Result

**PASS -- matrix is fresh.** No staleness warning is displayed. No user prompt or options are presented. Triage proceeds silently to Step 0.5 and beyond without interruption.

## Streams Checked

| Stream | Matrix Source | Last-Updated | Age (days) | Stale? |
|--------|-------------|--------------|------------|--------|
| 2.1.x | security-matrix-mock.md (Stream 1: rhtpa-release.0.3.z) | 2026-06-28T10:00:00Z | 14 | No |
| 2.2.x | security-matrix-mock.md (Stream 2: rhtpa-release.0.4.z) | 2026-06-28T10:00:00Z | 14 | No |

Both streams share the same matrix file and Last-Updated timestamp. Neither exceeds the 14-day staleness threshold.
