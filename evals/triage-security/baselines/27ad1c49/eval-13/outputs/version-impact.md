# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Matrix Staleness Check (Step 0.3)

The security matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z`.
Compared to current date (2026-10-13), the matrix is **107 days old** (exceeds the 14-day threshold).

In interactive mode, the engineer would be warned about staleness and asked whether to refresh, proceed, or stop. For this analysis, proceeding with the current matrix data.

## Supportability Matrix (Loaded from security-matrix-mock.md)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction (Step 2.3)

Lock file check command (Cargo ecosystem): `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

| Version | Stream | Tag | quinn-proto version | vs. fix threshold (0.11.14) | Affected? | Notes |
|---------|--------|-----|--------------------|-----------------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | 0.11.9 < 0.11.14 | **YES** | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | 0.11.9 < 0.11.14 | **YES** | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | 0.11.9 < 0.11.14 | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | 0.11.12 < 0.11.14 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | 0.11.14 = 0.11.14 | **NO** | at fix threshold |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | 0.11.14 = 0.11.14 | **NO** | at fix threshold |

## Dependency Chain Context (Step 2.3.5)

quinn-proto is a **Cargo** (source-level) dependency. Based on the component label `pscomponent:org/rhtpa-server` and the ecosystem mappings listing `backend` as the repository for the Cargo ecosystem:

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present directly in Cargo.lock)
  Profile: production (quinn-proto is a runtime QUIC transport dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|------------|----------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | `v0.3.12` | 0.11.9 | **NO** |
| 2.2.x | Cargo | `release/0.4.z` | `v0.4.12` | 0.11.14 | **YES** |

### Analysis

- **2.2.x stream**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fix). Additionally, released versions 2.2.3 and 2.2.4 already include the fix in their shipped container images. The vulnerability is **already remediated** for this stream starting from version 2.2.3.

- **2.1.x stream**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 (affected). The fix has **not** been applied to this stream. Remediation requires an upstream backport to bump quinn-proto on `release/0.3.z`, followed by downstream propagation to the Konflux release repo `rhtpa-release.0.3.z`.

## Summary

- **Scoped stream (2.2.x)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version. The fix is already present on the upstream branch and in the latest released versions. No new remediation task is required for this stream.
- **Cross-stream (2.1.x)**: Both versions (2.1.0, 2.1.1) are affected. The upstream branch does not have the fix. Preemptive remediation tasks are needed (Case A: cross-stream impact).
