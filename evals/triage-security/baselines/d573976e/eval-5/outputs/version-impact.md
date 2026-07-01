# Step 2 -- Version Impact Analysis

## 2.1 -- Load the Supportability Matrix

Issue is scoped to stream **2.2.x**. Loading the security-matrix.md for the 2.2.x stream (rhtpa-release.0.4.z).

Supportability Matrix for 2.2.x stream:

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.2 -- Development Stream Detection

> Note: In a real triage, `getJiraIssueTypeMetaWithFields` would be called to discover unreleased Jira versions. External tools are not called in this eval. Development stream analysis is deferred.

## 2.3 -- Extract Dependency Versions

Ecosystem: **RPM**. Lock file: `rpms.lock.yaml`. Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`.

Fix threshold: **3.0.7-28.el9_4** (from Step 1 data extraction).

RPM version comparison note: RPM versions follow the format `epoch:version-release.dist`. For openssl-libs in this analysis:
- 3.0.7-25.el9_3 < 3.0.7-28.el9_4 (release 25 < 28)
- 3.0.7-27.el9_4 < 3.0.7-28.el9_4 (release 27 < 28)
- 3.0.7-28.el9_4 = 3.0.7-28.el9_4 (equals fix version -- not affected)

Extracted versions from rpms.lock.yaml at each pinned commit:

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|---------------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | = fix version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | = fix version |

## 2.3.5 -- Dependency Chain Context

### Package Classification (RPM)

**Method**: rpms.lock.yaml inspection (lock file configured for RPM ecosystem in the 2.2.x stream Ecosystem Mappings table).

The check command `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` returns results for all tags in the 2.2.x stream, confirming that openssl-libs is **present in rpms.lock.yaml**.

- **rpms.lock.yaml**: openssl-libs is PRESENT -- **explicit install**
- **SBOM verification**: skipped -- cosign is not available in this eval environment (external tools are prohibited). In a real triage, `which cosign` would be run to check availability.

  > SBOM verification skipped -- cosign not available / external tools prohibited in eval. Using rpms.lock.yaml classification only.

- **Origin**: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT --> explicit install
  SBOM verification: skipped -- cosign not available (eval environment)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

  Affected versions: 2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4), 2.2.2 (retag of 2.2.1)
  Fixed versions: 2.2.3 (3.0.7-28.el9_4), 2.2.4 (3.0.7-28.el9_4)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to openssl-libs >= 3.0.7-28.el9_4.
```

## 2.4 -- Version Impact Table (Summary)

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | |
| 2.2.4 | 3.0.7-28.el9_4 | NO | |

Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: PRESENT -- explicit install
  SBOM verification: skipped -- cosign not available (eval environment)
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml / rpms.in.yaml)

Remediation path: update openssl-libs in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.

## 2.5 -- Upstream Fix Check

RPM ecosystem does not have an Upstream Branch configured in the Ecosystem Mappings table (Upstream Branch column is `--`). Upstream fix check is not applicable for system package ecosystems -- the fix source is the RPM vendor (Red Hat), not an upstream source repository branch.

The Red Hat Security Advisory RHSA-2026:4021 indicates the fix is available. Remediation involves updating the package reference in the Konflux release repo.

**Proposed action**: Present this version impact table to the engineer for confirmation before proceeding to Step 3.
