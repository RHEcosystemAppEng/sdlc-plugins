# Step 0.3 -- Matrix Staleness Check

## Triage Target

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812
- **Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

## Staleness Detection

**Matrix file timestamp**: `<!-- Last-Updated: 2026-05-01T10:00:00Z -->`
**Current date**: 2026-10-07
**Staleness threshold**: 14 days

### Stream: 2.1.x

- **Konflux Release Repo**: git.example.com/rhtpa/rhtpa-release.0.3.z
- **Last-Updated**: 2026-05-01T10:00:00Z
- **Age**: 159 days

> **WARNING**: Security matrix for stream **2.1.x** was last updated on 2026-05-01 (159 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

### Stream: 2.2.x

- **Konflux Release Repo**: git.example.com/rhtpa/rhtpa-release.0.4.z
- **Last-Updated**: 2026-05-01T10:00:00Z
- **Age**: 159 days

> **WARNING**: Security matrix for stream **2.2.x** was last updated on 2026-05-01 (159 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Result

Both version streams (2.1.x and 2.2.x) have stale security matrices. The matrices were last updated 159 days ago, which exceeds the 14-day staleness threshold by 145 days. Awaiting user choice before proceeding with triage.
