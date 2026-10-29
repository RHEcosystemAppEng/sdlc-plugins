# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Vulnerability Reference

- **CVE**: CVE-2026-31812
- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Scope

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.8 | 0.11.12 | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Combined Impact Summary

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | 0.11.12 | **YES** | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (assumed based on Cargo.lock presence)
  Ecosystem: Cargo
  Profile: production (quinn-proto is a QUIC protocol runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | **NO** |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | **YES** |

### Upstream Fix Analysis

- **Stream 2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 at HEAD (tags v0.4.11 and v0.4.12). The fix is already incorporated into the latest releases (2.2.3 and 2.2.4). **No new remediation task is needed for the 2.2.x stream** -- the vulnerability was already resolved in versions 2.2.3+.

- **Stream 2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 at HEAD (tags v0.3.8 and v0.3.12). The fix has **not** been backported to this branch. Remediation requires an upstream backport to bump quinn-proto to >= 0.11.14 on the `release/0.3.z` branch, followed by a downstream propagation in the Konflux release repo.

## Affects Versions Correction (Step 3 Preview)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not correspond to any configured version stream. Based on lock file evidence:

- **Should be affected**: RHTPA 2.1.0, RHTPA 2.1.1, RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Should NOT be affected**: RHTPA 2.2.3, RHTPA 2.2.4
- **Should be removed**: RHTPA 2.0.0 (no such stream exists)

PROPOSAL: Remove RHTPA 2.0.0 and set Affects Versions to the correct list of affected versions discovered via Jira version metadata (dynamic discovery required).

## Cross-Stream Impact (Case A)

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`). The version impact analysis reveals that stream **2.1.x** is also affected:

- 2.1.0: quinn-proto 0.11.9 -- AFFECTED
- 2.1.1: quinn-proto 0.11.9 -- AFFECTED

Cross-stream impact comment would be posted to TC-8001:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.

Since the 2.1.x stream has no existing CVE Jira for CVE-2026-31812, preemptive remediation tasks should be created for the 2.1.x stream (see remediation.md).
