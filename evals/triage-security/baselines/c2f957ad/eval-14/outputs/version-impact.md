# Step 2 – Version Impact Analysis: TC-8005 (CVE-2026-40215)

Issue scope: **2.2.x** (from summary suffix `[rhtpa-2.2]`). All supported versions are enumerated per the skill's rule "Check ALL supported versions"; the 2.1.x rows are shown for cross-stream (Case A) context only.

Evidence source: simulated `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` output from `security-matrix-mock.md`, plus the eval-provided mock SBOM comparison results. No git, cosign, or Jira commands were actually run.

## 2.1 – Supportability matrix loaded

| Stream | Konflux Release Repo | Versions | Matrix format |
|--------|----------------------|----------|---------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | PASS (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer present) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | PASS |

Both streams: no `Last-Updated` timestamp (Step 0.3 warning, non-blocking).

## 2.2 – Development stream

Not determined: development-stream detection requires the Jira unreleased-versions lookup (`getJiraIssueTypeMetaWithFields`), which was not called in this eval. The 2.2.x matrix states it is the latest stream (no forward pointer). No branch-HEAD evidence is available, so no development row appears in the table below. It should be verified when Jira access is available.

## 2.3 – Extracted dependency versions (rpms.lock.yaml at pinned tags)

Fix threshold: `openssl-libs < 3.0.7-28.el9_4` (from the Jira description; external sources not queried).

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):
```

| Version | Stream | Tag | openssl-libs (rpms.lock.yaml) | Affected? | In issue scope? | Notes |
|---------|--------|-----|-------------------------------|-----------|-----------------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 3.0.7-24.el9 | YES | No (cross-stream) | |
| 2.1.1 | 2.1.x | `v0.3.12` | 3.0.7-24.el9 | YES | No (cross-stream) | |
| **2.2.0** | 2.2.x | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | Yes | |
| **2.2.1** | 2.2.x | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | Yes | |
| **2.2.2** | 2.2.x | `v0.4.9` | — (same as 2.2.1: 3.0.7-27.el9_4) | **YES** | Yes | retag of 2.2.1. Lock file check skipped, result carried forward |
| 2.2.3 | 2.2.x | `v0.4.11` | 3.0.7-28.el9_4 | NO | Yes | Ships the fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 3.0.7-28.el9_4 | NO | Yes | Ships the fixed version |

**Summary (2.2.x scope):** 2.2.0, 2.2.1, and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship `openssl-libs-3.0.7-28.el9_4` and are not affected.
**Cross-stream:** 2.1.0 and 2.1.1 (stream 2.1.x) are also affected. This feeds Case A in Step 8.
**PSIRT Affects Versions mismatch:** Jira field is `RHTPA 2.0.0`, which is not in any supported stream. Step 3 should propose replacing it with `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2` (scoped to 2.2.x).

## 2.3.5 – Dependency chain context (in-scope affected versions)

cosign availability check: `which cosign` -> `/usr/bin/cosign` (available). SBOM verification was performed using the eval-provided mock SBOM comparison results.

### 2.2.0 (tag `v0.4.5`)

```
Dependency chain for openssl-libs (RPM) — 2.2.0:
  rpms.lock.yaml: present (openssl-libs 3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install but SBOM comparison says base image. Investigate manually.
  Dockerfile FROM: not available (Dockerfile content not provided in eval data)
  Origin: UNRESOLVED (conflicting signals: lock file = explicit install, SBOM = base image)
```

### 2.2.1 (tag `v0.4.8`)

```
Dependency chain for openssl-libs (RPM) — 2.2.1:
  rpms.lock.yaml: present (openssl-libs 3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install but SBOM comparison says base image. Investigate manually.
  Dockerfile FROM: not available (Dockerfile content not provided in eval data)
  Origin: UNRESOLVED (conflicting signals: lock file = explicit install, SBOM = base image)
```

### 2.2.2 (tag `v0.4.9`, retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM) — 2.2.2 (same as 2.2.1):
  rpms.lock.yaml: present (openssl-libs 3.0.7-27.el9_4, carried forward from 2.2.1) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install but SBOM comparison says base image. Investigate manually.
  Dockerfile FROM: not available (Dockerfile content not provided in eval data)
  Origin: UNRESOLVED (conflicting signals: lock file = explicit install, SBOM = base image)
```

### Side-by-side classification summary

| Version | rpms.lock.yaml signal | rpms.lock.yaml classification | SBOM signal (final vs base) | SBOM classification | Agreement |
|---------|-----------------------|-------------------------------|-----------------------------|---------------------|-----------|
| 2.2.0 | listed (3.0.7-25.el9_3) | explicit install | in final AND base SBOM | base image | ⚠️ DISAGREE |
| 2.2.1 | listed (3.0.7-27.el9_4) | explicit install | in final AND base SBOM | base image | ⚠️ DISAGREE |
| 2.2.2 | listed (same as 2.2.1) | explicit install | in final AND base SBOM | base image | ⚠️ DISAGREE |

**Interpretation:** openssl-libs is pinned in `rpms.lock.yaml` and is also already present in the base image. The likely cause is that the Konflux build explicitly installs or upgrades a package the base image already provides. Per the skill, the SBOM check supplements the lock file classification but does not replace it, so the primary classification stays **explicit install**. Because the signals conflict, the engineer should confirm which layer determines the shipped openssl-libs version before the remediation task is finalized. A complete fix may need both of these:
- updating the `openssl-libs` spec in `rpms.in.yaml` / `rpms.lock.yaml` to `>= 3.0.7-28.el9_4`, and
- confirming that the base image (`FROM` reference, still to be extracted from the Dockerfile) does not keep shipping a vulnerable copy, and bumping its tag or digest if it does.

**Introduction point:** openssl-libs is in `rpms.lock.yaml` in every inspected version of both streams. Its origin does not change across versions according to the lock file. The fix (`3.0.7-28.el9_4`) first appears in 2.2.3 (`v0.4.11`).

**Cross-stream (2.1.x) chain:** not traced. The stream is outside this issue's scope, and no SBOM comparison data was supplied for 2.1.0/2.1.1. The lock file lists openssl-libs `3.0.7-24.el9` (explicit install per lock file). SBOM verification for 2.1.x: not performed (no mock SBOM data for these versions).

## 2.5 – Upstream fix check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | n/a | n/a |
| 2.1.x | RPM | — (not configured) | n/a | n/a |

The RPM ecosystem has no upstream source branch, so this check does not apply. Remediation is in the Konflux release repo. Within 2.2.x, the fixed RPM version is already shipped from 2.2.3 (`v0.4.11` lock file: `3.0.7-28.el9_4`).

## Implications for later steps (for engineer review)

- **Step 3:** Correct Affects Versions from `RHTPA 2.0.0` to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (requires confirmation).
- **Step 8:** Case A applies: the issue is scoped to 2.2.x and 2.1.x is also affected. Post a cross-stream impact comment, check for a sibling CVE Jira for 2.1.x, and create a preemptive task if none exists. Case B applies to 2.2.x: create **1** Konflux release repo fix task (system package ecosystem). The task should document the lock file vs SBOM classification discrepancy.
- Engineer confirmation of this version impact table is required before proceeding to Step 3.
