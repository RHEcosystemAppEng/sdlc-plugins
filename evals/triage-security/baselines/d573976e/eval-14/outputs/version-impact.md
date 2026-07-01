# Step 2 -- Version Impact Analysis

## 2.1 -- Load the Supportability Matrix

The issue is scoped to the **2.2.x** stream. Loading the security-matrix.md for stream 2 (rhtpa-release.0.4.z).

### 2.2.x Stream Supportability Matrix

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem: **RPM**
Lock file: `rpms.lock.yaml`
Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

## 2.2 -- Detect the Development Stream

(Simulated -- would call getJiraIssueTypeMetaWithFields in a real triage to find unreleased versions with prefix RHTPA. For this eval, the 2.2.x stream versions in the matrix are all released.)

## 2.3 -- Extract Dependency Versions

Using rpms.lock.yaml data from the mock lock file data for the 2.2.x stream:

**CVE-2026-40215 fix threshold**: 3.0.7-28.el9_4 (versions before this are affected)

| Tag | Command (simulated) | openssl-libs version | Affected? |
|-----|---------------------|----------------------|-----------|
| `v0.4.5` (2.2.0) | `git show v0.4.5:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-25.el9_3 | **YES** -- 3.0.7-25.el9_3 < 3.0.7-28.el9_4 |
| `v0.4.8` (2.2.1) | `git show v0.4.8:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-27.el9_4 | **YES** -- 3.0.7-27.el9_4 < 3.0.7-28.el9_4 |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8 -- skip, carry forward)_ | -- | **YES** -- same as 2.2.1 |
| `v0.4.11` (2.2.3) | `git show v0.4.11:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-28.el9_4 | **NO** -- 3.0.7-28.el9_4 = fixed version |
| `v0.4.12` (2.2.4) | `git show v0.4.12:rpms.lock.yaml \| grep 'openssl-libs'` | 3.0.7-28.el9_4 | **NO** -- 3.0.7-28.el9_4 = fixed version |

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | ships fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed openssl-libs version.

## 2.3.5 -- Dependency Chain Context

The dependency chain for openssl-libs is documented in the SBOM verification output (see `outputs/sbom-verification.md`). A summary follows here for completeness:

For the affected versions (2.2.0 through 2.2.2):
- **rpms.lock.yaml**: openssl-libs IS present in the lock file, indicating explicit install
- **SBOM verification**: openssl-libs appears in BOTH the final container image SBOM and the base image SBOM, indicating base image origin
- **Classification disagreement**: rpms.lock.yaml says explicit install, SBOM comparison says base image. Discrepancy flagged for manual investigation.

See `outputs/sbom-verification.md` for the full SBOM verification analysis including the discrepancy warning.

## 2.5 -- Upstream Fix Check

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table. The RPM fix comes from the base image vendor (Red Hat) via errata updates, not from an upstream source branch. No upstream fix check is applicable for this ecosystem.
