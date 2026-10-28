# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock (current date):** 2026-07-12T10:00:00Z
- **Matrix Last-Updated timestamp:** 2026-06-28T10:00:00Z
- **Computed matrix age:** 14 days

## Version Streams Checked

### Stream 2.1.x (rhtpa-release.0.3.z)

- **Matrix file:** security-matrix-mock.md (Stream 1)
- **Last-Updated:** 2026-06-28T10:00:00Z
- **Age:** 14 days
- **Result:** FRESH -- the matrix is exactly 14 days old, which is within the staleness threshold (older than 14 days triggers a warning). No staleness warning required.

### Stream 2.2.x (rhtpa-release.0.4.z)

- **Matrix file:** security-matrix-mock.md (Stream 2)
- **Last-Updated:** 2026-06-28T10:00:00Z
- **Age:** 14 days
- **Result:** FRESH -- the matrix is exactly 14 days old, which is within the staleness threshold (older than 14 days triggers a warning). No staleness warning required.

## Conclusion

Both version streams have a matrix age of exactly 14 days, which does not exceed the 14-day staleness threshold. The staleness check passes for all streams. No user warning or refresh prompt is needed. Proceeding with triage using the current matrix data.
