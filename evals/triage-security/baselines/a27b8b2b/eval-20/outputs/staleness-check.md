# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Staleness threshold**: 14 days (default)
- **Current date**: 2026-07-27

## Stream: 2.1.x (rhtpa-release.0.3.z)

- **Matrix file**: security-matrix-mock.md (Stream 1 section)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z` (extracted from `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` HTML comment)
- **Result**: Within the 14-day threshold -- **PASS**

No staleness warning displayed. Proceeding silently to Step 0.5.

## Stream: 2.2.x (rhtpa-release.0.4.z)

- **Matrix file**: security-matrix-mock.md (Stream 2 section)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z` (extracted from `<!-- Last-Updated: 2026-06-28T10:00:00Z -->` HTML comment)
- **Result**: Within the 14-day threshold -- **PASS**

No staleness warning displayed. Proceeding silently to Step 0.5.

## Summary

Both version streams have matrix files with recent Last-Updated timestamps within the 14-day staleness threshold. No user prompt or options were presented. The staleness check completed silently and triage continues uninterrupted to Step 0.5 (JIRA Access Initialization) and subsequent steps.
