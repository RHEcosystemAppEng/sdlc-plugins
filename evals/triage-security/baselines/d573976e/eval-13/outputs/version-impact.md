# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from local security-matrix.md files for both streams.

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

## 2.3 -- Dependency Version Extraction

Using mock lock file data for `quinn-proto` at each pinned commit tag.
Fix threshold: **0.11.14** (from Step 1 data extraction).

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 |

### Dependency Chain Context (Step 2.3.5)

Dependency chain for quinn-proto (Cargo):
- The quinn-proto crate is a Cargo dependency found in `Cargo.lock`.
- Affected versions: 2.2.0 (0.11.9), 2.2.1 (0.11.12), 2.2.2 (retag of 2.2.1).
- Not affected: 2.2.3 (0.11.14), 2.2.4 (0.11.14).
- quinn-proto is part of the quinn QUIC transport stack, used for network communication.

## 2.5 -- Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

The upstream source branch `release/0.4.z` already ships quinn-proto 0.11.14, which meets the fix threshold. Remediation for the 2.2.x stream is a Konflux release repo change: bump the source reference to pick up the upstream fix.

## Cross-Stream Impact

The version impact analysis also shows that stream **2.1.x** is affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9). Since this issue is scoped to stream 2.2.x only, the cross-stream impact for 2.1.x will be handled in Step 8 Case B.
