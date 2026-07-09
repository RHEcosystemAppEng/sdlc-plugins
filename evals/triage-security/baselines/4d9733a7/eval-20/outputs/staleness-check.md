# Step 0.3 -- Matrix Staleness Check

## Timestamp Extraction

Read the `security-matrix.md` file at the configured Security Matrix Path for each version stream.

**HTML comment found at the top of the file:**
```
<!-- Last-Updated: 2026-06-28T10:00:00Z -->
```

**Parsed timestamp**: 2026-06-28T10:00:00Z (ISO 8601 format)

## Staleness Evaluation

- **Current date**: 2026-07-09
- **Last updated**: 2026-06-28
- **Days since last update**: 11 days
- **Threshold**: 14 days (default)
- **Result**: **FRESH** -- the matrix is 11 days old, which is within the 14-day threshold

## Outcome

The matrix is within the 14-day threshold. No staleness warning is displayed. The check completes silently and triage proceeds to Step 0.5 (JIRA Access Initialization) without any user prompt or interruption.

No options are presented to the user. No user interaction is required. The staleness check is silent on success.
