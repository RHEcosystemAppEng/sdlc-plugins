# Step 0.3 -- Matrix Staleness Check

## Configuration

- **Vulnerability issue**: TC-8001 (CVE-2026-31812 quinn-proto)
- **Version Streams checked**: 2.1.x, 2.2.x
- **Staleness threshold**: 14 days
- **Current date**: 2026-10-06

## Staleness Detection

**Matrix file**: `security-matrix-stale-mock.md`
**Last-Updated timestamp**: `2026-05-01T10:00:00Z`
**Days since last update**: 158 days
**Status**: STALE (exceeds 14-day threshold by 144 days)

## Stream: 2.1.x (rhtpa-release.0.3.z)

Security matrix for stream **2.1.x** was last updated on 2026-05-01 (158 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

## Stream: 2.2.x (rhtpa-release.0.4.z)

Security matrix for stream **2.2.x** was last updated on 2026-05-01 (158 days ago). The matrix may not reflect recent releases.

Options:
1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
2. **Proceed anyway** -- continue triage with the current matrix
3. **Stop** -- halt triage so I can investigate

Awaiting user choice before proceeding.

## Summary

Both version streams (2.1.x and 2.2.x) share the same security matrix file with a Last-Updated timestamp of 2026-05-01T10:00:00Z, which is 158 days old. This significantly exceeds the 14-day staleness threshold. The matrix may not reflect recent releases, meaning triage could miss newly released versions or use outdated source commit references.

Triage is blocked pending user selection for each stream. No steps beyond Step 0.3 will execute until the user responds.
