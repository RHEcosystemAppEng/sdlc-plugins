# Step 2 -- Version Impact Analysis

## 2.1 -- Supportability Matrix (2.2.x stream)

Source: `security-matrix.md` for stream `rhtpa-release.0.4.z`
Last-Updated: 2026-06-28T10:00:00Z (25 days ago -- exceeds 14-day staleness threshold)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Ecosystem Mappings (2.2.x):

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

## 2.3 -- Dependency Version Extraction

Ecosystem: RPM
Lock file: `rpms.lock.yaml`
Package: `openssl-libs`
Fixed version: `3.0.7-28.el9_4`

### rpms.lock.yaml results

| Version | Tag | openssl-libs version (rpms.lock.yaml) | Vulnerable? |
|---------|-----|---------------------------------------|-------------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | YES -- before 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | YES -- before 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8)_ | YES -- same as 2.2.1 |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO -- matches fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO -- matches fixed version |

## 2.3.5 -- Dependency Chain Context

### RPM origin classification

**Classification method**: rpms.lock.yaml + SBOM verification (cosign available at `/usr/bin/cosign`)

#### Version 2.2.0 (tag v0.4.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  CLASSIFICATION DISAGREEMENT: rpms.lock.yaml says explicit install but SBOM comparison says base image
  Origin: DISPUTED -- investigate manually

  rpms.lock.yaml signal: explicit install (openssl-libs listed in rpms.lock.yaml)
  SBOM signal:           base image (openssl-libs found in both final and base image SBOMs)
```

> **Warning**: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

#### Version 2.2.1 (tag v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  CLASSIFICATION DISAGREEMENT: rpms.lock.yaml says explicit install but SBOM comparison says base image
  Origin: DISPUTED -- investigate manually

  rpms.lock.yaml signal: explicit install (openssl-libs listed in rpms.lock.yaml)
  SBOM signal:           base image (openssl-libs found in both final and base image SBOMs)
```

> **Warning**: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

#### Version 2.2.2 (tag v0.4.9 -- retag of v0.4.8)

```
Dependency chain for openssl-libs (RPM):
  Same as 2.2.1 (retag of v0.4.8)
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  CLASSIFICATION DISAGREEMENT: rpms.lock.yaml says explicit install but SBOM comparison says base image
  Origin: DISPUTED -- investigate manually

  rpms.lock.yaml signal: explicit install (openssl-libs listed in rpms.lock.yaml)
  SBOM signal:           base image (openssl-libs found in both final and base image SBOMs)
```

> **Warning**: SBOM classification disagrees with rpms.lock.yaml -- lock file says explicit install but SBOM comparison says base image. Investigate manually.

#### Versions 2.2.3 and 2.2.4 (not affected)

Not affected -- openssl-libs at 3.0.7-28.el9_4 (matches fixed version). Dependency chain not traced for unaffected versions.

## 2.4 -- Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | rpms.lock.yaml: explicit install; SBOM: base image (DISAGREE) |
| 2.2.1 | 3.0.7-27.el9_4 | YES | rpms.lock.yaml: explicit install; SBOM: base image (DISAGREE) |
| 2.2.2 | -- | YES | retag of 2.2.1; rpms.lock.yaml: explicit install; SBOM: base image (DISAGREE) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | matches fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | matches fixed version |

### Summary

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Ecosystem**: RPM (system package)
- **Origin classification**: DISPUTED for all affected versions -- rpms.lock.yaml indicates explicit install but SBOM comparison indicates base image origin. Manual investigation required to determine the correct remediation path (update rpms.lock.yaml/rpms.in.yaml vs. update base image).

### Cross-stream impact (scoped issue check)

This issue is scoped to stream 2.2.x via suffix `[rhtpa-2.2]`. The 2.1.x stream also has vulnerable openssl-libs versions (3.0.7-24.el9 at tags v0.3.8 and v0.3.12, both before the 3.0.7-28.el9_4 fix threshold), but is outside this issue's scope. Cross-stream impact would be noted in Step 8 Case B.
