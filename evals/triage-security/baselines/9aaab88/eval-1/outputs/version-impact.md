# Step 2 -- Version Impact Analysis: CVE-2026-31812

## 2.1 -- Supportability Matrix

Loaded from two configured Version Streams:

- **2.1.x** stream: `security-matrix.md` at rhtpa-release.0.3.z (2 versions)
- **2.2.x** stream: `security-matrix.md` at rhtpa-release.0.4.z (5 versions)

## 2.3 -- Dependency Version Extraction

Lock file data extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` for each pinned source commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto version | Source |
|---------|-----------|---------------------|--------|
| 2.1.0 | v0.3.8 | 0.11.9 | Cargo.lock at v0.3.8 |
| 2.1.1 | v0.3.12 | 0.11.9 | Cargo.lock at v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto version | Source |
|---------|-----------|---------------------|--------|
| 2.2.0 | v0.4.5 | 0.11.9 | Cargo.lock at v0.4.5 |
| 2.2.1 | v0.4.8 | 0.11.12 | Cargo.lock at v0.4.8 |
| 2.2.2 | v0.4.9 | -- | retag of 2.2.1 (same source commit v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | Cargo.lock at v0.4.11 |
| 2.2.4 | v0.4.12 | 0.11.14 | Cargo.lock at v0.4.12 |

## 2.4 -- Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14. Comparing each extracted version against the affected range (< 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed version) |
| 2.2.4 | 2.2.x | 0.11.14 | NO | >= 0.11.14 (fixed version) |

### Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1)
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 NOT affected (ship fixed 0.11.14)

### Dependency Chain Context (Step 2.3.5)

Ecosystem: Cargo (source-level dependency). quinn-proto is a transitive dependency in the backend workspace, pulled in via the QUIC networking stack:

```
backend (workspace) -> quinn -> quinn-proto
```

The dependency is present across both 2.1.x and 2.2.x streams, indicating it was introduced before the 2.1.0 release. It is a production (non-dev) dependency used for QUIC transport in the backend server.

## 2.5 -- Upstream Fix Status

Checking whether the upstream source repo (rhtpa-backend) has the fix on the branches feeding each affected stream:

| Stream | Ecosystem | Upstream Branch | Repository | Assessment |
|--------|-----------|-----------------|------------|------------|
| 2.1.x | Cargo | release/0.3.z | backend | Needs verification -- latest released version (v0.3.12) ships 0.11.9, which is vulnerable. Upstream branch HEAD would need to be checked. |
| 2.2.x | Cargo | release/0.4.z | backend | Fixed in v0.4.11+ -- versions 2.2.3 and 2.2.4 already ship 0.11.14 (the fixed version). Upstream branch likely already has the fix. |

**Key finding**: The fix for quinn-proto was picked up in the 2.2.x stream starting with version 2.2.3 (build v0.4.11), but the 2.1.x stream has NOT received the fix in any released version.
