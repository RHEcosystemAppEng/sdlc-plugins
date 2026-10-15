# Step 0.3 -- Matrix Staleness Check

## Fixture Evidence

- **Evaluation clock**: 2026-07-12T10:00:00Z
- **Matrix Last-Updated timestamp**: 2026-06-28T10:00:00Z (from `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` HTML comment)
- **Computed matrix age**: 14 days
- **Staleness threshold**: 14 days (default)

## Version Streams Checked

The Security Configuration defines two version streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

Both streams share a single mock `security-matrix.md` file with the same `Last-Updated` timestamp.

## Staleness Evaluation

The matrix age (14 days) is **not** older than the 14-day threshold -- the condition is strictly "older than 14 days", and exactly 14 days does not exceed that threshold.

## Result

**PASS -- matrix is fresh.** No staleness warning is raised. Proceeding with triage using the current matrix data.

No user intervention required. No refresh prompt presented.
