# Step 0.3 -- Matrix Staleness Check

## Evaluation Clock

- **Evaluation clock (fixed scenario time):** 2026-07-12T10:00:00Z
- This clock is used as the current date for Step 0.3, regardless of runner or grader wall clock.

## Timestamp Extraction

For each configured Version Stream, read the `security-matrix.md` file and extract the `Last-Updated` HTML comment.

### Source Timestamp

- **HTML comment found:** `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`
- **Parsed ISO 8601 timestamp:** 2026-06-28T10:00:00Z
- **Comparison clock:** 2026-07-12T10:00:00Z (evaluation clock)

## Staleness Calculation

- **Matrix Last-Updated:** 2026-06-28T10:00:00Z
- **Current date (evaluation clock):** 2026-07-12T10:00:00Z
- **Computed matrix age:** exactly 14 days (2026-06-28 to 2026-07-12 = 14 days)
- **Staleness threshold:** older than 14 days (> 14 days)

## Result

The matrix age (14 days) is **not older than** the 14-day threshold. At exactly 14 days, the matrix is within the acceptable range -- the staleness rule triggers only when the age is strictly greater than 14 days.

**Outcome: PASS -- no staleness warning displayed.**

The check proceeds silently. No warning message is presented to the user. No options (refresh now / proceed anyway / stop) are offered. The triage continues to Step 0.5 (JIRA Access Initialization) and beyond without interruption from the staleness check.

## Streams Checked

| Stream | Matrix File | Last-Updated | Age (days) | Status |
|--------|-------------|--------------|------------|--------|
| 2.1.x | security-matrix.md (rhtpa-release.0.3.z) | 2026-06-28T10:00:00Z | 14 | Fresh (within threshold) |
| 2.2.x | security-matrix.md (rhtpa-release.0.4.z) | 2026-06-28T10:00:00Z | 14 | Fresh (within threshold) |

Both streams use the same matrix file with the same Last-Updated timestamp. Both are within the 14-day threshold. No staleness warning is triggered for either stream.
