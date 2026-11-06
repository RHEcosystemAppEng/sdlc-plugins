# Step 2 – Version Impact Analysis: TC-8005

**CVE:** CVE-2026-40215 | **Library:** openssl-libs (RPM) | **Affected range:** `< 3.0.7-28.el9_4` | **Fixed:** 3.0.7-28.el9_4
**Issue scope:** 2.2.x stream (`[rhtpa-2.2]`)

Lock file data comes from the simulated `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` output in `security-matrix-mock.md`. SBOM data comes from the mock cosign comparison results in the task prompt.

## 2.1 – Supportability Matrix Loaded

| Stream | Konflux Release Repo | Versions | Matrix format |
|--------|----------------------|----------|---------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | Pass. Required sections present (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | Pass |

Staleness warning (Step 0.3): the matrix was last updated on 2026-06-28, 131 days ago. Releases after 2.2.4 may be missing.

RPM Ecosystem Mapping for both streams: Lock File `rpms.lock.yaml`, Check Command `git show <tag>:rpms.lock.yaml`, Repository `—`, Upstream Branch `—`.

## 2.2 – Development Stream

The development stream could not be determined. That requires `getJiraIssueTypeMetaWithFields` to find unreleased `RHTPA` versions, and Jira was not called in this eval. 2.2.x is marked as the latest stream ("no forward pointer"). No dev-HEAD lock file data was supplied, so the table has no dev row. In a live run, the engineer would confirm the development version and the skill would check `HEAD:rpms.lock.yaml`.

## 2.3 / 2.4 – Version Impact Table (in-scope stream: 2.2.x)

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):
```

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | Below fix threshold |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | Below fix threshold |
| 2.2.2 | 0.4.9 | `v0.4.8` (backend) / `v0.4.9` | — (same as 2.2.1: 3.0.7-27.el9_4) | **YES** | Retag of 2.2.1, so the lock file check was skipped and the 2.2.1 result carried forward |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | Ships the fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | Ships the fixed version |
| dev | — | branch HEAD | not determined | — | Needs Jira unreleased-version lookup (see 2.2) |

### Cross-stream versions (outside this issue's scope)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | **YES** | Out of scope for TC-8005. Cross-stream impact (Case A) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | **YES** | Out of scope for TC-8005. Cross-stream impact (Case A) |

**Summary:** within the 2.2.x scope, versions **2.2.0, 2.2.1, and 2.2.2 are affected**. 2.2.3 and 2.2.4 are not affected because they already ship 3.0.7-28.el9_4. The 2.1.x stream (2.1.0 and 2.1.1) is also affected. That needs a cross-stream impact comment, and either a preemptive remediation task or a sibling CVE Jira for 2.1.x (Step 4 / Case A).

## 2.3.5 – Dependency Chain Context (affected versions, with inline SBOM verification)

SBOM verification: `which cosign` returns `/usr/bin/cosign`, so cosign is available. The final image SBOM and the base image SBOM were compared for each affected version, using the mock results.

### 2.2.0 (tag `v0.4.5`)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml (primary signal); DISPUTED by SBOM (base image)
  Version: 3.0.7-25.el9_3 (< 3.0.7-28.el9_4 → vulnerable)
```

### 2.2.1 (tag `v0.4.8`)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml (primary signal); DISPUTED by SBOM (base image)
  Version: 3.0.7-27.el9_4 (< 3.0.7-28.el9_4 → vulnerable)
```

### 2.2.2 (retag of 2.2.1, build 0.4.9)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4, same as 2.2.1) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml (primary signal); DISPUTED by SBOM (base image)
  Version: 3.0.7-27.el9_4 (< 3.0.7-28.el9_4 → vulnerable)
```

### Side-by-side classification summary

| Version | rpms.lock.yaml signal | SBOM comparison signal | Agreement | Classification used |
|---------|-----------------------|------------------------|-----------|---------------------|
| 2.2.0 | Listed → explicit install | In final + base SBOM → base image | **DISAGREE** ⚠️ | Explicit install (lock file is primary), flagged for manual investigation |
| 2.2.1 | Listed → explicit install | In final + base SBOM → base image | **DISAGREE** ⚠️ | Explicit install (lock file is primary), flagged for manual investigation |
| 2.2.2 | Listed → explicit install (same as 2.2.1) | In final + base SBOM → base image | **DISAGREE** ⚠️ | Explicit install (lock file is primary), flagged for manual investigation |
| 2.2.3 | 3.0.7-28.el9_4 (fixed) | n/a (not affected, no chain trace needed) | — | — |
| 2.2.4 | 3.0.7-28.el9_4 (fixed) | n/a (not affected, no chain trace needed) | — | — |

**Interpretation for the engineer:** the SBOM verification supplements the lock file classification and does not replace it. The likely explanation is that openssl-libs is both shipped in the base image (for example ubi9/ubi-minimal) and pinned explicitly in `rpms.lock.yaml`, which would upgrade or re-install it on top of the base layer. So remediation probably needs:
1. Bump openssl-libs to `>= 3.0.7-28.el9_4` in `rpms.in.yaml` / `rpms.lock.yaml`, which is the explicit-install path.
2. Check whether the base image (`FROM` reference) also needs a tag or digest update, so that an older copy from the base layer is not left in the final image.

**Not available in the eval inputs (not fabricated):**
- The Dockerfile `FROM` line, base image reference, and pinning method. These would come from `git show <tag>:Dockerfile | grep -i '^FROM'`.
- Image reference and digest. The matrix has no Container Images section.

The remediation task should leave these as items for the engineer to research.

**Introduction point:** openssl-libs is in `rpms.lock.yaml` in every inspected version of both streams, so the origin did not change across versions. 3.0.7-24.el9 (2.1.x) went to 3.0.7-25.el9_3 (2.2.0), then 3.0.7-27.el9_4 (2.2.1/2.2.2), then 3.0.7-28.el9_4 (2.2.3+, fixed).

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | n/a | n/a. Already fixed in released 2.2.3/2.2.4 (3.0.7-28.el9_4) |

The RPM ecosystem has no upstream source repository. The fix belongs in the Konflux release repo (`rhtpa-release.0.4.z`) and is already present from build 0.4.11 (2.2.3) onward.

## Implications for Later Steps (preview, nothing executed)

- **Step 3 – Affects Versions correction:** PSIRT set `RHTPA 2.0.0`, which is wrong for a 2.2.x-scoped issue. The proposed correction is **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**, with Jira version IDs discovered dynamically. Engineer confirmation is required.
- **Case A – Cross-stream:** 2.1.x (2.1.0, 2.1.1 ship 3.0.7-24.el9) is affected. Post a cross-stream impact comment, then check for a sibling `[rhtpa-2.1]` CVE Jira. If there isn't one, create a preemptive task (`security-preemptive` label, Related link).
- **Case B – 2.2.x remediation:** 1 task (RPM is a system package), a Konflux release repo fix in `rhtpa-release.0.4.z`. The latest 2.2.x release (2.2.4) already ships the fix, so the task may only need to confirm the fix and cover any further z-stream release. The SBOM/lock-file discrepancy must be in the task's Implementation Notes.
- **Engineer confirmation required:** review and confirm this table, the SBOM discrepancy, and the staleness warning before Step 3.
