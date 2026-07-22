# Step 0.3 -- Matrix Staleness Check

## Vulnerability Issue

**Issue**: TC-8001
**CVE**: CVE-2026-31812
**Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

## Staleness Detection

### Stream: 2.1.x

**Security Matrix Path**: security-matrix.md (Konflux release repo: rhtpa-release.0.3.z)
**Last-Updated timestamp**: 2026-05-01T10:00:00Z
**Current date**: 2026-07-22
**Age**: 82 days (threshold: 14 days)
**Status**: STALE

> Security matrix for stream **2.1.x** was last updated on 2026-05-01
> (82 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

### Stream: 2.2.x

**Security Matrix Path**: security-matrix.md (Konflux release repo: rhtpa-release.0.4.z)
**Last-Updated timestamp**: 2026-05-01T10:00:00Z
**Current date**: 2026-07-22
**Age**: 82 days (threshold: 14 days)
**Status**: STALE

> Security matrix for stream **2.2.x** was last updated on 2026-05-01
> (82 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

## Summary

Both configured version streams (2.1.x and 2.2.x) have stale security matrices. The shared Last-Updated timestamp of 2026-05-01T10:00:00Z is 82 days old, which exceeds the 14-day staleness threshold. The matrix may not reflect recent releases -- new product versions or updated source commits could be missing.

Awaiting user choice before proceeding with triage. If the user chooses **Refresh now**, the matrix population logic from setup Step 10.6 will be invoked for the selected stream(s) to update the supportability matrix and write a new Last-Updated timestamp. If the user chooses **Proceed anyway**, triage will continue with the current (potentially outdated) matrix data.
