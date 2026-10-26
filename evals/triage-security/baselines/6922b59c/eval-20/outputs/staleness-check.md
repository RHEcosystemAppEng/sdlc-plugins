# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock (scenario time):** 2026-07-12T10:00:00Z
- **Matrix Last-Updated timestamp:** 2026-06-28T10:00:00Z
- **Computed matrix age:** 14 days (exactly)
- **Staleness threshold:** older than 14 days (>14 days)

## Streams Checked

### Stream 2.1.x (rhtpa-release.0.3.z)

- **Matrix file:** security-matrix-mock.md (Stream 1 section)
- **Last-Updated:** 2026-06-28T10:00:00Z
- **Age at evaluation clock:** 14 days
- **Result:** FRESH -- the matrix is exactly 14 days old, which does not exceed the staleness threshold of "older than 14 days." No staleness warning is required.

### Stream 2.2.x (rhtpa-release.0.4.z)

- **Matrix file:** security-matrix-mock.md (Stream 2 section)
- **Last-Updated:** 2026-06-28T10:00:00Z
- **Age at evaluation clock:** 14 days
- **Result:** FRESH -- the matrix is exactly 14 days old, which does not exceed the staleness threshold of "older than 14 days." No staleness warning is required.

## Outcome

Both version stream matrices have a Last-Updated timestamp of 2026-06-28T10:00:00Z, which is exactly 14 days before the evaluation clock of 2026-07-12T10:00:00Z. Since the staleness threshold requires the matrix to be **older than** 14 days (strictly greater than), a matrix that is exactly 14 days old is within the acceptable window. No staleness warning is issued and triage proceeds without interruption.
