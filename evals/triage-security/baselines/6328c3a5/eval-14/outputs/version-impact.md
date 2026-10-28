# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix-mock.md` -- Stream 2: rhtpa-release.0.4.z (2.2.x stream)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

Vulnerable library: **openssl-libs**
Ecosystem: **RPM** (lock file: `rpms.lock.yaml`)
Fix threshold: **3.0.7-28.el9_4** (from Jira description)

| Version | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|-------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | before 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | before 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | **NO** | = fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | **NO** | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the fixed version.

## 2.3.5 -- Dependency Chain Context

### Affected versions: 2.2.0, 2.2.1, 2.2.2

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification (cosign available at /usr/bin/cosign):
    Final image SBOM: openssl-libs PRESENT
    Base image SBOM:  openssl-libs PRESENT
    SBOM comparison result: present in both final and base image SBOMs --> base image

  WARNING: SBOM classification DISAGREES with rpms.lock.yaml
    rpms.lock.yaml says: explicit install (package IS listed in lock file)
    SBOM comparison says: base image (package found in both final and base image SBOMs)
    Investigate manually.

  Origin: CONFLICTING SIGNALS
    rpms.lock.yaml classification: explicit install
    SBOM classification: base image (inherited from base image)

  Remediation (based on rpms.lock.yaml as source of truth):
    Update the package spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4.
    Note: SBOM cross-check indicates openssl-libs is also present in the base
    image. The rpms.lock.yaml entry may be redundant or may override the base
    image version. Investigate whether removing the explicit install and relying
    on a base image update is the correct remediation path.
```

**SBOM verification applied to all three affected versions (2.2.0, 2.2.1, 2.2.2):**

| Version | rpms.lock.yaml | SBOM (final image) | SBOM (base image) | rpms.lock.yaml Classification | SBOM Classification | Agreement? |
|---------|----------------|--------------------|--------------------|-------------------------------|----------------------|------------|
| 2.2.0 | openssl-libs present | openssl-libs present | openssl-libs present | explicit install | base image | **DISAGREE** |
| 2.2.1 | openssl-libs present | openssl-libs present | openssl-libs present | explicit install | base image | **DISAGREE** |
| 2.2.2 | (retag of 2.2.1) | (retag of 2.2.1) | (retag of 2.2.1) | explicit install | base image | **DISAGREE** |

### Non-affected versions: 2.2.3, 2.2.4

Versions 2.2.3 and 2.2.4 ship openssl-libs 3.0.7-28.el9_4 (the fixed version). No dependency chain analysis required for non-affected versions.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | -- | **YES** | retag of 2.2.1 |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

Affected versions: 2.2.0, 2.2.1, 2.2.2
Not affected: 2.2.3, 2.2.4

Ecosystem classification: System package (RPM) -- 1 remediation task for the 2.2.x stream.
