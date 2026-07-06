# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using enriched fix threshold from Step 1.5: **h2 < 0.4.8** is affected (versions >= 0.4.8 are fixed).

## Version Impact Table

Version impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.2.x (issue-scoped stream)

| Version | Build | h2 version | Affected? | Notes |
|---------|-------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.1 | 0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | 0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |
| 2.2.4 | 0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 (fixed) |

### Stream 2.1.x (cross-stream analysis)

| Version | Build | h2 version | Affected? | Notes |
|---------|-------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

## Summary

- **2.2.x stream (scoped):** Only version 2.2.0 is affected. Versions 2.2.1+ ship h2 >= 0.4.8 and are not affected.
- **2.1.x stream (cross-stream):** All versions (2.1.0, 2.1.1) are affected. Both ship h2 0.4.5 which is < 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Source repository: backend

  h2 is a direct or transitive dependency in the backend workspace.
  The vulnerability (HTTP/2 CONTINUATION flood) affects the h2 HTTP/2
  implementation used by the backend service.

  First fixed in stream 2.2.x at version 2.2.1 (build 0.4.8, h2 bumped to 0.4.8).
  Not fixed in stream 2.1.x (latest version 2.1.1 still ships h2 0.4.5).
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix available? | Notes |
|--------|-----------|-----------------|----------------|-------|
| 2.2.x | Cargo | release/0.4.z | YES | h2 was bumped to 0.4.8 starting at build 0.4.8 |
| 2.1.x | Cargo | release/0.3.z | Unknown | Latest build 0.3.12 still ships h2 0.4.5 |

## Triage Outcome

- **Case A (Affected):** Version 2.2.0 in the scoped 2.2.x stream is affected -- remediation tasks needed for 2.2.x.
- **Case B (Cross-stream impact):** Stream 2.1.x is also affected (all versions ship h2 0.4.5). Cross-stream notice required. Proactive remediation tasks may be needed for 2.1.x if no companion CVE Jira exists.
