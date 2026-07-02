# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8** is affected, **h2 >= 0.4.8** is not affected.

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Build | Backend Tag | h2 version | Affected? | Notes |
|--------|---------|-------|-------------|------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | 0.3.12 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | 0.4.5 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.x | 2.2.1 | 0.4.8 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed version) |
| 2.2.x | 2.2.2 | 0.4.9 | v0.4.9 | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | 0.4.12 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected | Stream Status |
|--------|-------------------|-----------------------|---------------|
| 2.1.x | 2.1.0, 2.1.1 | -- | AFFECTED |
| 2.2.x (issue scope) | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | NOT AFFECTED |

## Issue Stream Scope Analysis

This issue is scoped to stream **2.2.x** (from suffix `[rhtpa-2.2]`).

- **2.2.x stream**: No versions are affected. All versions ship h2 >= 0.4.8, which is at or above the fix threshold. This triggers **Case C** (close as Not a Bug).
- **2.1.x stream**: Both versions are affected (h2 0.4.5 < 0.4.8). This triggers **Case B** (cross-stream impact). The 2.1.x stream ships a vulnerable h2 version and may require preemptive remediation if no companion CVE Jira exists for that stream.

## Dependency Chain Context (Step 2.3.5)

For affected versions in stream 2.1.x:

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency)

Present in: 2.1.0 (v0.3.8), 2.1.1 (v0.3.12) at version 0.4.5
Fixed in: 2.2.0+ (v0.4.5+) at version 0.4.8
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 at Branch HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.4.9 | YES |

- **2.1.x (release/0.3.z)**: h2 is still at 0.4.5 on the upstream branch -- the fix has NOT been backported. Remediation requires an upstream PR to bump h2 to >= 0.4.8 on release/0.3.z, followed by a downstream propagation in the Konflux release repo.
- **2.2.x (release/0.4.z)**: h2 is at 0.4.9 -- already fixed. No action needed.
