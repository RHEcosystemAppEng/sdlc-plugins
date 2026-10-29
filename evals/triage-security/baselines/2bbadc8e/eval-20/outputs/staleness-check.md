# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock (fixed UTC scenario time):** 2026-07-12T10:00:00Z
- **Matrix Last-Updated timestamp:** 2026-06-28T10:00:00Z
- **Computed matrix age:** 14 days exactly

## Staleness Threshold

The staleness threshold defined in the triage-security skill is **older than 14 days**. The matrix age is exactly 14 days, which is **not** older than 14 days. Therefore the matrix is **within the threshold** and is considered fresh.

## Version Streams Checked

The Security Configuration defines two version streams:

| Stream | Konflux Release Repo | Matrix Source |
|--------|----------------------|---------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | security-matrix-mock.md (Stream 1) |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | security-matrix-mock.md (Stream 2) |

Both streams share the same matrix file with the single `Last-Updated: 2026-06-28T10:00:00Z` timestamp.

## Result

**PASS -- matrix is fresh.** The security matrix was last updated 14 days ago (2026-06-28), which meets the 14-day freshness threshold at the evaluation clock time (2026-07-12). No staleness warning is raised. Triage proceeds without user intervention.

No user-facing warning is introduced for a fresh matrix. The evaluation clock and computed age are recorded here as fixture evidence only.
