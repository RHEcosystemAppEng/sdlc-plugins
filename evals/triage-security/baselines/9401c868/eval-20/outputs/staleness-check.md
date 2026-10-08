# Step 0.3 -- Matrix Staleness Check

## Configuration

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Staleness Evaluation

Both version streams share a single security-matrix.md file for this eval.

- **Matrix Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Current date (eval override)**: `2026-06-29T10:00:00Z`
- **Age**: 1 day
- **Staleness threshold**: 14 days

## Result: FRESH -- Proceed

The security matrix was last updated 1 day ago, which is well within the 14-day
staleness threshold. No refresh is needed.

| Stream | Last Updated | Age (days) | Threshold (days) | Status |
|--------|-------------|------------|-------------------|--------|
| 2.1.x | 2026-06-28 | 1 | 14 | Fresh |
| 2.2.x | 2026-06-28 | 1 | 14 | Fresh |

**Decision**: Proceed with triage using the current matrix data. No user
intervention required.
