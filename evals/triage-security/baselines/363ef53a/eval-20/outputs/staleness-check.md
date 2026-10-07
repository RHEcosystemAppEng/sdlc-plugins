# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Version Streams checked**: 2.1.x, 2.2.x
- **Security Matrix Path**: security-matrix-mock.md (single file covers both streams)
- **Staleness threshold**: 14 days

## Timestamp Extraction

The matrix file contains the following HTML comment at the top:

```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

**Parsed timestamp**: 2026-06-28T10:00:00Z

## Staleness Calculation

- **Current date** (evaluation anchor): 2026-06-29T10:00:00Z
- **Last updated**: 2026-06-28T10:00:00Z
- **Age**: 1 day
- **Threshold**: 14 days
- **Stale?**: NO

## Result per Stream

| Stream | Matrix File | Last Updated | Age (days) | Stale? | Action |
|--------|-------------|--------------|------------|--------|--------|
| 2.1.x | security-matrix-mock.md | 2026-06-28T10:00:00Z | 1 | NO | Proceed |
| 2.2.x | security-matrix-mock.md | 2026-06-28T10:00:00Z | 1 | NO | Proceed |

## Decision

Both streams' security matrix was updated 1 day ago, which is well within the 14-day staleness threshold. No staleness warning is required. Proceeding to Step 1 (Data Extraction) without interruption.
