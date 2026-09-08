# Step 0.3 -- Matrix Staleness Check

## Configuration

- Current date: 2026-09-08
- Staleness threshold: 14 days
- Version Streams checked:
  - **2.1.x** -- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z, Local Path: /home/dev/repos/rhtpa-release.0.3.z
  - **2.2.x** -- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z, Local Path: /home/dev/repos/rhtpa-release.0.4.z

## Staleness Results

### Stream 2.1.x

- **Matrix file**: security-matrix.md (at configured Security Matrix Path relative to project working directory)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 72 days
- **Result**: STALE (72 days exceeds the 14-day threshold)

**Warning**:

> Security matrix for stream **2.1.x** was last updated on 2026-06-28 (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

### Stream 2.2.x

- **Matrix file**: security-matrix.md (at configured Security Matrix Path relative to project working directory)
- **Last-Updated timestamp**: `2026-06-28T10:00:00Z`
- **Age**: 72 days
- **Result**: STALE (72 days exceeds the 14-day threshold)

**Warning**:

> Security matrix for stream **2.2.x** was last updated on 2026-06-28 (72 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Summary

| Stream | Last-Updated | Age (days) | Status |
|--------|-------------|------------|--------|
| 2.1.x  | 2026-06-28  | 72         | STALE  |
| 2.2.x  | 2026-06-28  | 72         | STALE  |

Both version streams have stale security matrices. The matrices were last updated 72 days ago, which significantly exceeds the 14-day staleness threshold. This means the matrices may not reflect recent releases or source commit changes. The user must choose whether to refresh the matrices, proceed with current data, or stop triage before continuing to Step 1.
