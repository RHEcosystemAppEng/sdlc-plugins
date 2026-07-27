# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (based on Cargo.lock presence)
  Ecosystem: Cargo
  Profile: production (quinn-proto is a runtime QUIC transport dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

- **2.2.x stream**: The upstream branch `release/0.4.z` already has the fix (quinn-proto 0.11.14 at v0.4.11+). Versions 2.2.3 and 2.2.4 already ship the fixed version. No new remediation tasks are required for this stream.
- **2.1.x stream**: The upstream branch `release/0.3.z` does NOT have the fix (quinn-proto 0.11.9). Remediation requires an upstream backport to bump quinn-proto to >= 0.11.14, followed by downstream propagation.

## Cross-Stream Impact Summary

The issue is scoped to **2.2.x** (`[rhtpa-2.2]`). Cross-stream analysis reveals:

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 both ship quinn-proto 0.11.9). Fix is NOT on the upstream branch. This triggers **Case A** (cross-stream impact) with preemptive remediation tasks for the 2.1.x stream.
- **2.2.x stream** (in-scope): Versions 2.2.0, 2.2.1, 2.2.2 are affected. Fix is already shipped in 2.2.3+ and is already on the upstream branch `release/0.4.z`. No new remediation tasks needed for this stream.

## Affects Versions Correction (Step 3)

Current Affects Versions: **RHTPA 2.0.0** (incorrect -- this version does not exist in any stream)

Corrected Affects Versions for the 2.2.x scoped issue:
- **RHTPA 2.2.0**
- **RHTPA 2.2.1**
- **RHTPA 2.2.2**

Action: Remove RHTPA 2.0.0 and add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
