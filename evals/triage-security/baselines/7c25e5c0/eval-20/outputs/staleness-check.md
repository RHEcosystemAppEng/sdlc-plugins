# Step 0.3 — Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z (fixed UTC scenario time)
- **Source HTML comment**: `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- **Parsed ISO 8601 timestamp**: 2026-06-28T10:00:00Z
- **Comparison clock**: 2026-07-12T10:00:00Z
- **Computed matrix age**: exactly 14 days (2026-06-28 → 2026-07-12)

## Staleness Evaluation

### Stream: 2.1.x (rhtpa-release.0.3.z)

The security-matrix.md file contains a `Last-Updated` timestamp of `2026-06-28T10:00:00Z`.

Compared against the evaluation clock `2026-07-12T10:00:00Z`, the matrix is **exactly 14 days old**.

The staleness threshold is "older than 14 days" — a strict greater-than comparison. A matrix that is exactly 14 days old does **not** exceed the threshold. It is within the acceptable freshness window.

**Result**: Pass — no staleness warning displayed. Proceeding silently to Step 0.5.

### Stream: 2.2.x (rhtpa-release.0.4.z)

Same matrix file covers both streams. Same timestamp and same evaluation.

**Result**: Pass — no staleness warning displayed. Proceeding silently to Step 0.5.

## Summary

| Stream | Last Updated | Age (days) | Threshold (days) | Stale? | Action |
|--------|-------------|------------|-------------------|--------|--------|
| 2.1.x | 2026-06-28T10:00:00Z | 14 | >14 | No | Proceed silently |
| 2.2.x | 2026-06-28T10:00:00Z | 14 | >14 | No | Proceed silently |

No user prompt or options were presented. The staleness check completed silently on success, and triage continues to Step 0.5 (JIRA Access Initialization) and beyond without interruption.
