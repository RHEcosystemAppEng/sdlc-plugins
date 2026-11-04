# Step 2 – Version Impact Analysis: TC-8005 (CVE-2026-40215, openssl-libs)

Scope: **2.2.x stream only** (from the summary suffix `[rhtpa-2.2]`). Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`.
All lock file and SBOM data is simulated from the eval inputs. No git show, cosign, or Jira calls were made.

## 2.1 – Supportability matrix (2.2.x)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

Matrix format check: Supportability Matrix, Ecosystem Mappings, Source Pinning Method, and Forward Pointer are all present. Ecosystem Mappings columns match the template. **Pass.**
Staleness check (Step 0.3): the mock matrix has no `Last-Updated` timestamp. Consider running `/setup` to add one. This does not block triage.

## 2.2 – Development stream

Not determined. Finding it requires `getJiraIssueTypeMetaWithFields` (unreleased RHTPA versions), and Jira was not called in this eval. 2.2.x is the latest configured stream (it has no forward pointer). No development-head row is included.

## 2.3 – Dependency version extraction

Method: RPM ecosystem with `rpms.lock.yaml` configured, so the lock file is the source of truth.
Command per version (simulated): `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
Fix threshold: 3.0.7-28.el9_4 (Jira description; Step 1.5 external sources unavailable).

## 2.4 – Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|--------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | `v0.4.9` | — | **YES** | same as 2.2.1 (retag of v0.4.8, check skipped, result carried forward) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals the fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals the fixed version |

Summary: **2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship the fix.**
Out of scope (2.1.x stream, not analyzed for this scoped issue): 2.1.0 and 2.1.1.

## 2.3.5 – Dependency chain context (affected versions, with SBOM verification)

cosign check: `which cosign` -> `/usr/bin/cosign` (available, simulated). Final-image and base-image SBOMs were compared (simulated results supplied by the eval).

```
Dependency chain for openssl-libs (RPM) — 2.2.0 (tag v0.4.5):
  rpms.lock.yaml: present (openssl-libs 3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Dockerfile FROM: not available in eval inputs (git show <tag>:Dockerfile not run)
  Origin: explicit install per rpms.lock.yaml (primary classification); DISPUTED by SBOM
```

```
Dependency chain for openssl-libs (RPM) — 2.2.1 (tag v0.4.8):
  rpms.lock.yaml: present (openssl-libs 3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Dockerfile FROM: not available in eval inputs
  Origin: explicit install per rpms.lock.yaml (primary classification); DISPUTED by SBOM
```

```
Dependency chain for openssl-libs (RPM) — 2.2.2 (tag v0.4.9, retag of v0.4.8):
  rpms.lock.yaml: same as 2.2.1 (openssl-libs 3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml (primary classification); DISPUTED by SBOM
```

Side-by-side classification signals:

| Version | rpms.lock.yaml signal | SBOM comparison signal | Agreement |
|---------|-----------------------|------------------------|-----------|
| 2.2.0 | listed (3.0.7-25.el9_3) → explicit install | in final + base SBOM → base image | ⚠️ DISAGREE |
| 2.2.1 | listed (3.0.7-27.el9_4) → explicit install | in final + base SBOM → base image | ⚠️ DISAGREE |
| 2.2.2 | listed (retag of 2.2.1) → explicit install | in final + base SBOM → base image | ⚠️ DISAGREE |

Interpretation: openssl-libs most likely ships in the UBI base image, and the build also pins it in `rpms.lock.yaml`. A package can be both base-provided and explicitly locked/reinstalled. Per the skill, SBOM verification supplements the lock file classification and does not replace it. The lock file classification (explicit install) stays primary, but the engineer must investigate manually before choosing the remediation path:
- If the lock-file pin controls the installed version: update the openssl-libs spec in `rpms.in.yaml` / `rpms.lock.yaml` to >= 3.0.7-28.el9_4.
- If the version actually comes from the base image: update the base image tag/digest to a build with patched openssl-libs. The `FROM` reference must be retrieved from the Dockerfile.

Introduction point: openssl-libs is listed in rpms.lock.yaml at every 2.2.x tag. The vulnerable range ends at v0.4.11 (2.2.3), where 3.0.7-28.el9_4 is pinned.

## 2.5 – Upstream fix status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | n/a | n/a. Fix is in the Konflux release repo; latest release 2.2.4 already ships 3.0.7-28.el9_4 |

RPM is a system-package ecosystem with no upstream branch, so remediation is a single Konflux release repo task for 2.2.x.

## Notes for downstream steps

- Step 3: the current Affects Versions value `RHTPA 2.0.0` is wrong for this 2.2.x-scoped issue. The proposed correction is `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`, pending engineer confirmation and Jira version availability.
- Step 8: Case B (affected). Create 1 RPM remediation task for the 2.2.x Konflux repo and include the SBOM/lock-file discrepancy warning in it.

Awaiting engineer review and confirmation of this table before Step 3.
