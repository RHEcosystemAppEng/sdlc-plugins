# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Supportability Matrix Source

Matrix data loaded from security-matrix-mock.md covering two streams:
- Stream 2.1.x (rhtpa-release.0.3.z) -- Last-Updated: 2026-06-28T10:00:00Z (within 14-day freshness threshold)
- Stream 2.2.x (rhtpa-release.0.4.z) -- Last-Updated: 2026-06-28T10:00:00Z (within 14-day freshness threshold)

## Dependency Version Extraction (Step 2.3)

Fix threshold: quinn-proto >= 0.11.14 (versions before 0.11.14 are vulnerable)

Lock file check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

### Stream 2.1.x

| Version | Build Tag | quinn-proto version | Method |
|---------|-----------|---------------------|--------|
| 2.1.0 | v0.3.8 | 0.11.9 | Cargo.lock at pinned commit |
| 2.1.1 | v0.3.12 | 0.11.9 | Cargo.lock at pinned commit |

### Stream 2.2.x

| Version | Build Tag | quinn-proto version | Method |
|---------|-----------|---------------------|--------|
| 2.2.0 | v0.4.5 | 0.11.9 | Cargo.lock at pinned commit |
| 2.2.1 | v0.4.8 | 0.11.12 | Cargo.lock at pinned commit |
| 2.2.2 | v0.4.9 | -- | retag of v0.4.8 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | Cargo.lock at pinned commit |
| 2.2.4 | v0.4.12 | 0.11.14 | Cargo.lock at pinned commit |

## Version Impact Table (Step 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | quinn-proto | Affected? | Notes |
|--------|---------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo ecosystem)
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Check (Step 2.5)

Upstream fix status:

| Stream | Ecosystem | Upstream Branch | Fix Status | Notes |
|--------|-----------|-----------------|------------|-------|
| 2.1.x | Cargo | release/0.3.z | Check required | Upstream branch HEAD must be inspected |
| 2.2.x | Cargo | release/0.4.z | Fixed in v0.4.11+ | Versions 2.2.3 and 2.2.4 ship 0.11.14 |

Upstream fix PR: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048)

The fix has been picked up in the 2.2.x stream starting from build v0.4.11 (version 2.2.3). Versions 2.2.0, 2.2.1, and 2.2.2 remain affected.

All versions in the 2.1.x stream (2.1.0, 2.1.1) remain affected with quinn-proto 0.11.9.

## Cross-Stream Impact Summary

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

- **Within scope (2.2.x)**: versions 2.2.0, 2.2.1, 2.2.2 are affected -> Case A (create remediation tasks)
- **Outside scope (2.1.x)**: versions 2.1.0, 2.1.1 are also affected -> Case B (cross-stream impact notification and preemptive remediation tasks)

## Affects Versions Correction Preview

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect (no 2.0.x stream exists).

Based on lock file evidence, the correct Affects Versions for this scoped issue (2.2.x stream only) should be:
- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (they ship quinn-proto 0.11.14, which is the fixed version).
