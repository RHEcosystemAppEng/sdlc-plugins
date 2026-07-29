# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Version Streams checked**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Staleness threshold**: 14 days
- **Current date**: 2026-07-29

## Matrix File

- **File**: security-matrix-mock.md (covers both streams)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`

## Staleness Calculation

| Stream | Last Updated | Age (days) | Threshold (days) | Status |
|--------|-------------|------------|-------------------|--------|
| 2.1.x (rhtpa-release.0.3.z) | 2026-06-28 | 31 | 14 | STALE |
| 2.2.x (rhtpa-release.0.4.z) | 2026-06-28 | 31 | 14 | STALE |

The matrix file contains a single `Last-Updated` timestamp (`2026-06-28T10:00:00Z`) that
applies to both streams. The matrix is **31 days old**, which exceeds the 14-day
staleness threshold.

## Result: STALE

The security matrix for both streams was last updated on 2026-06-28 (31 days ago).
The matrix may not reflect recent releases.

Per the SKILL.md Step 0.3 procedure, the following options would be presented to the
engineer:

> Security matrix for streams **2.1.x** and **2.2.x** was last updated on 2026-06-28
> (31 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for these streams
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

The engineer must choose an option before triage proceeds past this step.
