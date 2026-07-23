# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Current date**: 2026-07-23
- **Staleness threshold**: 14 days
- **Version Streams checked**: 2

## Results

### Stream 2.1.x (rhtpa-release.0.3.z)

| Field | Value |
|-------|-------|
| Matrix file | security-matrix-mock.md (Stream 1: rhtpa-release.0.3.z) |
| Last-Updated timestamp | 2026-06-28T10:00:00Z |
| Age | 25 days |
| Threshold | 14 days |
| Status | **STALE** |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Field | Value |
|-------|-------|
| Matrix file | security-matrix-mock.md (Stream 2: rhtpa-release.0.4.z) |
| Last-Updated timestamp | 2026-06-28T10:00:00Z |
| Age | 25 days |
| Threshold | 14 days |
| Status | **STALE** |

## Staleness Warning

Both version streams share the same matrix file with a single `Last-Updated` timestamp of 2026-06-28T10:00:00Z. The matrix is **25 days old**, which exceeds the 14-day staleness threshold by 11 days.

Per Step 0.3 of the triage-security skill, the following warning would be presented to the engineer:

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28 (25 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for these streams
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Conclusion

The staleness check detected that the security matrix is **stale** (25 days old, threshold is 14 days). Engineer confirmation is required before proceeding with triage. If the engineer chooses "Proceed anyway," triage continues with the current matrix data. If the engineer chooses "Refresh now," the matrix population logic from setup Step 10.6 would be invoked to update the matrix with current release data and a fresh `Last-Updated` timestamp.
