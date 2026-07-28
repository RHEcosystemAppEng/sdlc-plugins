# Step 2 — Version Impact Analysis

## 2.1 — Supportability Matrix (2.2.x stream)

Loaded from security-matrix.md for stream 2.2.x (rhtpa-release.0.4.z):

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## 2.3 — Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM. Lock file: `rpms.lock.yaml`. Check command: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

Extraction results for each version's pinned commit:

| Tag | openssl-libs version (rpms.lock.yaml) |
|-----|---------------------------------------|
| `v0.4.5` (2.2.0) | 3.0.7-25.el9_3 |
| `v0.4.8` (2.2.1) | 3.0.7-27.el9_4 |
| `v0.4.9` (2.2.2) | _(retag of v0.4.8)_ — same as 2.2.1: 3.0.7-27.el9_4 |
| `v0.4.11` (2.2.3) | 3.0.7-28.el9_4 |
| `v0.4.12` (2.2.4) | 3.0.7-28.el9_4 |

Fix threshold: **3.0.7-28.el9_4** (from Jira description and CVE record).

## 2.4 — Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|--------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | < 3.0.7-28.el9_4 |
| 2.2.1 | 3.0.7-27.el9_4 | YES | < 3.0.7-28.el9_4 |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | = fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | = fixed version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship the patched version.

## 2.3.5 — Dependency Chain Context (RPM, with SBOM Verification)

### Package Classification

openssl-libs is an RPM system package. The classification uses rpms.lock.yaml as the primary signal, with optional SBOM verification via cosign for cross-checking.

### rpms.lock.yaml Classification

openssl-libs is **present** in rpms.lock.yaml for all versions in the 2.2.x stream. Per the classification rules:
- **In lock file** = **explicit install**

rpms.lock.yaml classification: **explicit install** (openssl-libs is listed in the lock file)

### SBOM Verification (cosign available at /usr/bin/cosign)

cosign is available (`which cosign` returns `/usr/bin/cosign`). Proceeding with SBOM comparison to cross-check the rpms.lock.yaml classification.

**Procedure for each affected version (2.2.0, 2.2.1, 2.2.2):**

1. Download the final container image SBOM:
   ```
   cosign download sbom <image-reference>@<image-digest> > /tmp/final-sbom.json
   ```
2. Extract the base image reference from the Dockerfile's `FROM` line.
3. Download the base image SBOM:
   ```
   cosign download sbom <base-image-reference> > /tmp/base-sbom.json
   ```
4. Compare openssl-libs presence in both SBOMs.

**SBOM comparison results for affected versions:**

| Version | rpms.lock.yaml | Final Image SBOM | Base Image SBOM | SBOM Classification |
|---------|----------------|------------------|-----------------|---------------------|
| 2.2.0 | present (explicit install) | present | present | base image |
| 2.2.1 | present (explicit install) | present | present | base image |
| 2.2.2 | present (explicit install) | present | present | base image (retag of 2.2.1) |

SBOM classification: openssl-libs appears in **both** the final image SBOM and the base image SBOM for all affected versions. The SBOM comparison classifies the package origin as **base image** (present in both final and base image SBOMs = inherited from base image).

### Classification Discrepancy

> **WARNING: SBOM classification disagrees with rpms.lock.yaml** -- lock file says **explicit install** (openssl-libs is present in rpms.lock.yaml) but SBOM comparison says **base image** (openssl-libs appears in both the final and base image SBOMs). Investigate manually.

The two classification signals disagree:

| Signal | Classification | Reasoning |
|--------|---------------|-----------|
| rpms.lock.yaml (primary) | **explicit install** | openssl-libs is listed in rpms.lock.yaml |
| SBOM comparison (supplementary) | **base image** | openssl-libs present in both final and base image SBOMs, indicating it originates from the base image |

**The rpms.lock.yaml classification remains the primary signal.** The SBOM result supplements but does not override it. Possible explanations for the disagreement:
- The base image may already include openssl-libs, and rpms.lock.yaml may redundantly pin the same package (explicit install that overlaps with base image content)
- The rpms.lock.yaml entry may have been added intentionally to pin a specific version, even though the base image also provides the package

**Action required**: This discrepancy is flagged for the engineer to investigate manually. The engineer should determine whether the rpms.lock.yaml entry is an intentional override of the base image version or a redundant entry.

### Dependency Chain Summary (inline, per version)

**Version 2.2.0** (tag `v0.4.5`):
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-25.el9_3) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: Classification disagrees -- rpms.lock.yaml says explicit install,
           SBOM comparison says base image. Investigate manually.
  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (rpms.lock.yaml is the primary signal)
```

**Version 2.2.1** (tag `v0.4.8`):
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: Classification disagrees -- rpms.lock.yaml says explicit install,
           SBOM comparison says base image. Investigate manually.
  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (rpms.lock.yaml is the primary signal)
```

**Version 2.2.2** (tag `v0.4.9`, retag of 2.2.1):
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (3.0.7-27.el9_4) -> explicit install (same as 2.2.1)
  SBOM verification: present in BOTH final image SBOM and base image SBOM -> base image
  WARNING: Classification disagrees -- rpms.lock.yaml says explicit install,
           SBOM comparison says base image. Investigate manually.
  Primary classification (rpms.lock.yaml): explicit install
  Origin: explicit install (rpms.lock.yaml is the primary signal)
```

**Versions 2.2.3 and 2.2.4**: Not affected (ship openssl-libs 3.0.7-28.el9_4, which is the fixed version). SBOM verification not needed for non-affected versions.

### Remediation Path

Based on the primary classification (**explicit install** via rpms.lock.yaml):
- Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to require openssl-libs >= 3.0.7-28.el9_4
- This produces a **single remediation task** for the Konflux release repo (RPM system package ecosystem)
