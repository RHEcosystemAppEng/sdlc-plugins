# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z
- **Matrix Last-Updated timestamp**: 2026-06-28T10:00:00Z
- **Computed matrix age**: 14 days (exactly)
- **Staleness threshold**: older than 14 days (>14 days)

## Version Streams Checked

The Security Configuration defines two version streams, both covered by a single security matrix file:

| Stream | Konflux Release Repo | Matrix Last-Updated | Age (days) |
|--------|----------------------|---------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | 2026-06-28T10:00:00Z | 14 |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | 2026-06-28T10:00:00Z | 14 |

## Result

**PASS -- Matrix is not stale.**

The security matrix was last updated on 2026-06-28T10:00:00Z, which is exactly 14 days before the evaluation clock (2026-07-12T10:00:00Z). The staleness threshold triggers when the matrix is **older than** 14 days (strictly greater than 14 days). At exactly 14 days, the matrix is within the acceptable freshness window.

No staleness warning is raised. Proceeding to triage without user intervention.
