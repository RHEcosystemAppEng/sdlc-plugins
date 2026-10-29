# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Supportability Matrix Sources

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Ecosystem Mappings Used

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| 2.2.x | Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Version Impact Table

CVE-2026-31812: quinn-proto < 0.11.14 (fixed in 0.11.14)

| Stream | Version | Build | Backend Tag | quinn-proto Version | Affected? | Notes |
|--------|---------|-------|-------------|---------------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | **YES** | < 0.11.14 |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | **YES** | < 0.11.14 |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | -- | **YES** | retag of 2.2.1 (same as 2.2.1: 0.11.12) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: assumed direct dependency (lock file confirms presence)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
```

quinn-proto is present in `Cargo.lock` across all versions inspected. It was introduced before version 2.1.0 (present at the earliest checked tag, v0.3.8).

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag on Branch | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|----------------------|---------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | `v0.3.12` | 0.11.9 | **NO** |
| 2.2.x | Cargo | `release/0.4.z` | `v0.4.12` | 0.11.14 | **YES** |

### Implications for Remediation

- **Stream 2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fixed version) at the latest tag `v0.4.12`. Remediation uses the **dependency bump** variant -- a `cargo update -p quinn-proto` is sufficient, followed by downstream propagation.
- **Stream 2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 at the latest tag `v0.3.12`. Remediation requires an **upstream backport** to bump quinn-proto on `release/0.3.z`, followed by downstream propagation.

## Affects Versions Correction (Step 3)

### Current vs Correct Affects Versions

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Issue scope**: 2.2.x stream only (from `[rhtpa-2.2]` suffix)
- **Correct Affects Versions** (based on lock file evidence, scoped to 2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

### PROPOSAL: Correct Affects Versions

Remove: RHTPA 2.0.0 (no such version stream exists; not supported)
Add: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact Summary

The issue is scoped to stream 2.2.x, but version impact analysis shows that stream 2.1.x is also affected (both 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This triggers **Case A** (cross-stream impact) in Step 8:

- Post a cross-stream impact comment on TC-8001
- Create preemptive remediation tasks for stream 2.1.x (if no sibling CVE Jira exists for 2.1.x)
