# Step 0.3 -- Matrix Staleness Check

## Stream: 2.1.x (rhtpa-release.0.3.z)

- **Security Matrix Path**: security-matrix-mock.md (shared file covering both streams)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Current date**: 2026-07-01
- **Age**: 3 days
- **Threshold**: 14 days
- **Result**: FRESH -- the matrix was updated 3 days ago, which is within the 14-day staleness threshold.

No warning displayed. Proceeding silently to the next step.

## Stream: 2.2.x (rhtpa-release.0.4.z)

- **Security Matrix Path**: security-matrix-mock.md (shared file covering both streams)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Current date**: 2026-07-01
- **Age**: 3 days
- **Threshold**: 14 days
- **Result**: FRESH -- the matrix was updated 3 days ago, which is within the 14-day staleness threshold.

No warning displayed. Proceeding silently to the next step.

## Summary

Both version streams have a security matrix with a `Last-Updated` timestamp of 2026-06-28T10:00:00Z, which is 3 days old. This is well within the default 14-day staleness threshold. No staleness warning is presented to the user, and no user prompt or options are displayed. The triage continues to Step 0.5 (JIRA Access Initialization) without interruption from the staleness check.
