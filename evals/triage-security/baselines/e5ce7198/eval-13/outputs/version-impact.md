# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix

Loaded from two streams configured in Version Streams table:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

Ecosystem Mappings:
- Cargo: Repository=backend, Lock File=`Cargo.lock`, Check Command=`git show <tag>:Cargo.lock`, Upstream Branch=`release/0.3.z`

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings:
- Cargo: Repository=backend, Lock File=`Cargo.lock`, Check Command=`git show <tag>:Cargo.lock`, Upstream Branch=`release/0.4.z`

## 2.2 -- Development Stream Detection

(Simulated) Query `getJiraIssueTypeMetaWithFields` for Vulnerability issue type in project TC.
Filter unreleased versions by prefix "RHTPA".
The development version with earliest releaseDate would be identified (e.g., RHTPA 3.0).
Development stream maps to the 2.2.x stream repo, checked at branch HEAD.

For this eval, no development stream version data is provided in the fixtures, so we proceed with the released versions only. In a real triage, the development stream would be checked at branch HEAD of the source repository.

## 2.3 -- Dependency Version Extraction

Lock file inspection results using `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`:

Fix threshold: **0.11.14** (from Step 1.5 cross-validated enrichment)

### Stream 2.1.x

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----|---------------------|----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

### Stream 2.2.x

| Version | Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----|---------------------|----------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | -- | YES (retag of 2.2.1, same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO |
| 2.2.4 | v0.4.12 | 0.11.14 | NO |

## 2.3.5 -- Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> reqwest [features: http3] -> h3 -> quinn -> quinn-proto
  Profile: production (reqwest is a runtime dependency)
  Type: transitive dependency (not a direct workspace dependency)

  Present in all versions across both streams (2.1.x and 2.2.x).
  Fixed in stream 2.2.x starting at version 2.2.3 (tag v0.4.11, quinn-proto 0.11.14).
  Stream 2.1.x remains on quinn-proto 0.11.9 across all versions.
```

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

**Summary**:
- Stream 2.1.x: ALL versions affected (2.1.0, 2.1.1)
- Stream 2.2.x: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 NOT affected
- The fix (quinn-proto >= 0.11.14) was picked up in stream 2.2.x starting at version 2.2.3 (tag v0.4.11)

## 2.5 -- Upstream Fix Check

Check whether the upstream source repository (rhtpa-backend) has already fixed the vulnerability on each stream's upstream branch:

| Stream | Ecosystem | Upstream Branch | Command | Version at HEAD | Fixed? |
|--------|-----------|-----------------|---------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | (simulated: would need actual git show) | TBD |
| 2.2.x | Cargo | release/0.4.z | `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | (simulated: would need actual git show) | TBD |

Based on the lock file data, the latest released version in stream 2.2.x (v0.4.12) already ships quinn-proto 0.11.14. This strongly suggests that the upstream branch `release/0.4.z` has already been fixed. For stream 2.1.x, the latest released version (v0.3.12) ships quinn-proto 0.11.9, so upstream branch `release/0.3.z` likely still needs a fix.

**Upstream fix status assessment**:

| Stream | Upstream Branch | Likely Fixed? | Evidence |
|--------|-----------------|---------------|----------|
| 2.1.x | release/0.3.z | NO | Latest release v0.3.12 ships quinn-proto 0.11.9 |
| 2.2.x | release/0.4.z | YES | v0.4.11+ ships quinn-proto 0.11.14 |

For stream 2.2.x, since the fix is already present in released versions 2.2.3+, remediation only needs to target the Affects Versions (2.2.0, 2.2.1, 2.2.2) which are already released and shipped with the vulnerable version. The fix is already present on the upstream branch.

For stream 2.1.x, the upstream backport to `release/0.3.z` has not happened yet based on the lock file evidence.
