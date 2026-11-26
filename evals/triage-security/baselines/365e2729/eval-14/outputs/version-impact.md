# TC-8005 — Step 2: Version Impact Analysis

**Scope:** 2.2.x stream only (from summary suffix `[rhtpa-2.2]`).
**Matrix:** rhtpa-release.0.4.z `security-matrix.md` (mock).
**Ecosystem / lock file:** RPM / `rpms.lock.yaml` (`git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`; output simulated from mock data).
**Fix threshold:** 3.0.7-28.el9_4 (Jira description; Step 1.5 external enrichment not run).

Matrix notes:
- Step 0.3 staleness: the matrix has no `Last-Updated` timestamp. Consider running `/setup`
  to add one. This does not block triage.
- Step 2.1.1 format check: passed. Supportability Matrix, Ecosystem Mappings, Source
  Pinning Method and Forward Pointer are all present, and the Ecosystem Mappings columns
  match the template.

## Version impact table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | below fix threshold |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | below fix threshold |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | retag of 2.2.1, same as 2.2.1 (3.0.7-27.el9_4) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |
| dev (branch HEAD) | — | — | not determined | — | Step 2.2 needs Jira unreleased-version metadata, which was not available here. 2.2.x is the latest configured stream (no forward pointer). |

Out of scope (2.1.x stream, not part of this issue): 2.1.0 and 2.1.1 pin `v0.3.8` and
`v0.3.12`, both with openssl-libs 3.0.7-24.el9. Both would be affected. Per Step 4, this
should be handled through a sibling or cross-stream issue for 2.1.x, not on TC-8005.

**Summary:** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship the fixed
package (3.0.7-28.el9_4).

## Dependency chain context (Step 2.3.5), with SBOM verification inline

cosign check: `which cosign` returned `/usr/bin/cosign`, so SBOM verification ran (simulated).

### 2.2.0 (tag `v0.4.5`)
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install (rpms.lock.yaml is the primary classification) — DISPUTED by SBOM
```

### 2.2.1 (tag `v0.4.8`)
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install (rpms.lock.yaml is the primary classification) — DISPUTED by SBOM
```

### 2.2.2 (retag of 2.2.1, tag `v0.4.8`)
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: same as 2.2.1 (openssl-libs-3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install (rpms.lock.yaml is the primary classification) — DISPUTED by SBOM
```

### Side-by-side signal summary

| Version | rpms.lock.yaml signal | SBOM comparison signal | Agreement |
|---------|----------------------|------------------------|-----------|
| 2.2.0 | present → explicit install | in final + base SBOM → base image | ⚠️ DISAGREE |
| 2.2.1 | present → explicit install | in final + base SBOM → base image | ⚠️ DISAGREE |
| 2.2.2 | same as 2.2.1 → explicit install | in final + base SBOM → base image | ⚠️ DISAGREE |

### What the disagreement means and what to check

- Most likely the package is in **both** places: the base image (for example a
  ubi9/ubi-minimal `FROM` image) already ships openssl-libs, and `rpms.in.yaml` /
  `rpms.lock.yaml` also pins it explicitly. That would place it in the lock file and in
  the base SBOM at the same time.
- The SBOM step supplements the lock file classification. It does not replace it. Per
  the skill, the rpms.lock.yaml result ("explicit install") stays primary, and the
  engineer must resolve the discrepancy manually before Step 8 picks a remediation path.
- Things to check by hand:
  1. Look at `rpms.in.yaml` at `v0.4.5` and `v0.4.8` to confirm openssl-libs is
     explicitly requested.
  2. Run `git show <tag>:Dockerfile | grep -i '^FROM'` to get the base image reference
     and how it is pinned. This was not available in the mock, so the base image
     reference is unresolved.
  3. Compare the openssl-libs NVR in the base image SBOM with the NVR in the final image
     SBOM to see which layer supplies the installed copy.
- Possible remediation paths, to be settled by the engineer:
  - Explicit install (lock file view): update openssl-libs to >= 3.0.7-28.el9_4 in
    `rpms.in.yaml` / `rpms.lock.yaml` in rhtpa-release.0.4.z.
  - Base image (SBOM view): also bump the base image tag or digest to a build that
    includes RHSA-2026:4021.
  - If both are true, do both, so the base layer does not keep the vulnerable copy.
- Introduction point: openssl-libs is present in every 2.2.x version. Its origin
  classification is the same (and disputed the same way) across 2.2.0 to 2.2.2.

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | n/a | n/a |

RPM has no upstream source branch. Remediation is a Konflux release repo change in
rhtpa-release.0.4.z: 1 task for the stream. Note that the latest released 2.2.x builds
(2.2.3 and 2.2.4) already ship 3.0.7-28.el9_4, so the fix already exists in the stream.

## Proposed Affects Versions correction (input for Step 3)

- Current: RHTPA 2.0.0, which is outside the scoped stream.
- Proposed: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2. This needs engineer confirmation; it
  was not written to Jira.

Waiting for the engineer to review and confirm this table, including the SBOM
discrepancy, before moving to Step 3.
