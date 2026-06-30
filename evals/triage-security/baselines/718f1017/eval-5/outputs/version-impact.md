# Step 2 -- Version Impact Analysis for CVE-2026-40215

## 2.1 -- Supportability Matrix

Loaded from security-matrix.md files for both configured streams.

### Stream 2.2.x (rhtpa-release.0.4.z) -- in scope

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

### Stream 2.1.x (rhtpa-release.0.3.z) -- cross-stream (out of scope for this issue)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM. Lock file: `rpms.lock.yaml`. Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

Fix threshold: **3.0.7-28.el9_4** (from Jira description; external CVE APIs would be queried in a live triage for cross-validation via Step 1.5).

### 2.2.x stream (in scope)

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | = fix version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | = fix version |

### 2.1.x stream (cross-stream impact -- out of scope for this issue)

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |

## 2.3.5 -- Dependency Chain Context

Dependency chain for openssl-libs (RPM):

- rpms.lock.yaml: **present** -> explicit install
- Origin: explicit install (openssl-libs specified in rpms.in.yaml / rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.

Note: openssl-libs is present in rpms.lock.yaml for all versions in both streams. The package is directly managed in the Konflux release repo lock file, not inherited from a base image.

## 2.4 -- Version Impact Table (Summary)

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | |
| 2.2.4 | 3.0.7-28.el9_4 | NO | |
| 2.1.0 | 3.0.7-24.el9 | YES | cross-stream (2.1.x) |
| 2.1.1 | 3.0.7-24.el9 | YES | cross-stream (2.1.x) |

## 2.5 -- Upstream Fix Check

RPM ecosystem has no configured Upstream Branch (column is "—" in the Ecosystem Mappings table). No upstream fix check is applicable for system packages -- the fix is applied directly in the Konflux release repo by updating rpms.lock.yaml.

The fix is already present in versions 2.2.3+ (openssl-libs 3.0.7-28.el9_4), confirming the fix was picked up in the 0.4.11 build.

## Cross-Stream Impact

Stream 2.1.x is also affected (all versions: 2.1.0, 2.1.1 ship openssl-libs 3.0.7-24.el9, which is below the fix threshold). This will be reported as Case B cross-stream impact in Step 7.
