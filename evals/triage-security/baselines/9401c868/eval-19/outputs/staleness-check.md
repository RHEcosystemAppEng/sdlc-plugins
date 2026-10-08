# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Issue**: TC-8001
- **CVE**: CVE-2026-31812
- **Version Streams checked**:
  - 2.1.x (git.example.com/rhtpa/rhtpa-release.0.3.z)
  - 2.2.x (git.example.com/rhtpa/rhtpa-release.0.4.z)

## Staleness Detection

**Matrix file**: security-matrix-stale-mock.md
**Last-Updated timestamp**: `2026-05-01T10:00:00Z`
**Current date**: 2026-10-08
**Age**: 160 days
**Threshold**: 14 days
**Result**: **STALE**

## Warning

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (160 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (160 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Notes

Both version streams (2.1.x and 2.2.x) share the same matrix file with a single
`Last-Updated` timestamp of `2026-05-01T10:00:00Z`. At 160 days old, this
significantly exceeds the 14-day staleness threshold. The matrix may be missing
recently released product versions or using outdated source commit references,
which could cause triage to produce incorrect version impact results.

Awaiting user choice before proceeding to Step 1 (Data Extraction).
