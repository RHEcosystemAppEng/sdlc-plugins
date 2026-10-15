# Step 2 -- Version Impact Analysis

## Supportability Matrix (Aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Source Pinning |
|---------|-------|------------|-------------|----------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | artifacts.lock.yaml |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | artifacts.lock.yaml |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

## Dependency Version Extraction (Step 2.3)

Lock file check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

| Version | Backend Tag | quinn-proto version | Method |
|---------|-------------|---------------------|--------|
| 2.1.0 | v0.3.8 | 0.11.9 | Cargo.lock at pinned commit |
| 2.1.1 | v0.3.12 | 0.11.9 | Cargo.lock at pinned commit |
| 2.2.0 | v0.4.5 | 0.11.9 | Cargo.lock at pinned commit |
| 2.2.1 | v0.4.8 | 0.11.12 | Cargo.lock at pinned commit |
| 2.2.2 | v0.4.9 | 0.11.12 | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | Cargo.lock at pinned commit |
| 2.2.4 | v0.4.12 | 0.11.14 | Cargo.lock at pinned commit |

## Version Impact Table (Step 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | **YES** | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | **YES** | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | **NO** | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | 0.11.14 | **NO** | >= 0.11.14 (fixed) |

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | -- | Unknown (no mock data for branch HEAD) |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | **YES** (v0.4.11+ ship 0.11.14) |

The 2.2.x upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fixed version). This means remediation for the 2.2.x stream uses the **dependency bump** variant (Step 2.5 confirms fix is available upstream) rather than the upstream backport variant.

## Affects Versions Correction (Step 3)

The issue is scoped to stream 2.2.x. PSIRT assigned `RHTPA 2.0.0`, which does not exist as a configured version. The correct Affects Versions for the 2.2.x stream scope are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

## Cross-Stream Impact Summary

The issue is scoped to 2.2.x, but stream 2.1.x is also affected (versions 2.1.0 and 2.1.1 ship quinn-proto 0.11.9). This triggers **Case A** (cross-stream impact) in Step 8:
- A cross-stream impact comment will be posted on TC-8001.
- Preemptive remediation tasks will be created for stream 2.1.x if no sibling CVE Jira exists for that stream.
