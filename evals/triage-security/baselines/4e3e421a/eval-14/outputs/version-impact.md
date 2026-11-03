# Step 2 – Version Impact Analysis: TC-8005 (CVE-2026-40215, openssl-libs)

Scope: **2.2.x stream only** (from the `[rhtpa-2.2]` suffix).
Matrix: rhtpa-release.0.4.z `security-matrix.md` (mock). Required sections are present
and the Ecosystem Mappings columns match the template, so the matrix passes validation.
Fix threshold: `< 3.0.7-28.el9_4`, taken from the Jira description. Step 1.5 enrichment
was not run, so there is no external cross-validation.
Lock file data: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`. In this eval the
mock lock file data stands in for that output.

## 2.3 – Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | release 25 < 28 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | release 27 < 28 |
| 2.2.2 | 0.4.9 | `v0.4.8` | — (same as 2.2.1: 3.0.7-27.el9_4) | **YES** | retag of 2.2.1; check skipped and result carried forward |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | at the fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | at the fixed version |
| dev (2.2.x HEAD) | — | branch HEAD | not determined | — | Step 2.2 needs Jira unreleased-version metadata, which was not queried. 2.2.x is the latest stream (no forward pointer). |

**Result:** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and later already ship the fixed
openssl-libs 3.0.7-28.el9_4.

Out of scope (informational only, no action under this issue): the 2.1.x stream
(`v0.3.8`, `v0.3.12`) pins openssl-libs 3.0.7-24.el9, which is also below the threshold.
That stream should be tracked by its own `[rhtpa-2.1]` sibling issue (checked in Step 4).

## 2.3.5 – Dependency Chain Context (with inline SBOM verification)

`which cosign` returns `/usr/bin/cosign`, so cosign is available and SBOM verification
was performed. In this eval the SBOM comparison results come from the mock.

### 2.2.0 (`v0.4.5`)
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs 3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: UNRESOLVED (conflicting signals; rpms.lock.yaml is the primary classification → explicit install)
```

### 2.2.1 (`v0.4.8`)
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs 3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: UNRESOLVED (conflicting signals; rpms.lock.yaml is the primary classification → explicit install)
```

### 2.2.2 (build 0.4.9, retag of 2.2.1 / `v0.4.8`)
```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs 3.0.7-27.el9_4, same as 2.2.1) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: UNRESOLVED (conflicting signals; rpms.lock.yaml is the primary classification → explicit install)
```

### Side-by-side summary of signals

| Version | rpms.lock.yaml signal | rpms.lock.yaml classification | SBOM signal (final vs base) | SBOM classification | Agreement |
|---------|-----------------------|-------------------------------|-----------------------------|---------------------|-----------|
| 2.2.0 | listed (3.0.7-25.el9_3) | explicit install | in final AND in base | base image | ⚠️ DISAGREE |
| 2.2.1 | listed (3.0.7-27.el9_4) | explicit install | in final AND in base | base image | ⚠️ DISAGREE |
| 2.2.2 | listed (retag of 2.2.1) | explicit install | in final AND in base | base image | ⚠️ DISAGREE |

**Interpretation.** SBOM verification supplements the lock file but does not replace it.
The rpms.lock.yaml classification (explicit install) therefore stays primary, and the
disagreement is flagged for manual investigation. One plausible explanation is that
openssl-libs ships in the base image and is also pinned or upgraded explicitly in
`rpms.in.yaml` / `rpms.lock.yaml`. In that case the lock-file pin decides the version
that ends up in the final image. This has not been verified and needs engineer
confirmation.

**Base image reference:** not determined. No Dockerfile content was provided, and
`git show <commit>:Dockerfile` was not run, so the `FROM` reference and pinning method
are unknown. None has been made up here.

**Introduction point:** openssl-libs is in rpms.lock.yaml at every 2.2.x tag. Its version
moved 3.0.7-25.el9_3 → 3.0.7-27.el9_4 → 3.0.7-28.el9_4 (fixed at `v0.4.11`, 2.2.3).
SBOMs for 2.2.3 and 2.2.4 were not compared because those versions are not affected.

**Remediation implication (preview for Step 8):** this is a system package, so there is 1
Konflux release repo task for 2.2.x. Primary path (lock file): update openssl-libs to
>= 3.0.7-28.el9_4 in `rpms.in.yaml` / `rpms.lock.yaml`. Versions 2.2.3 and later already
carry this fix. Because the SBOM shows openssl-libs in the base image, the task should
also ask the engineer to check whether the base image's openssl-libs needs a base image
update. The SBOM/lock-file disagreement must be resolved before the task is finalised.

## 2.5 – Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | N/A | N/A. RPM is fixed in the Konflux release repo directly. The latest released lock file (`v0.4.12`) is already at 3.0.7-28.el9_4. |

Waiting for the engineer to review and confirm this table and the SBOM disagreement before Step 3.
Step 3 preview: replace Affects Versions `RHTPA 2.0.0` with `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`.
