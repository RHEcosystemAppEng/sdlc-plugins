# TC-8005 — Step 2: Version Impact Analysis

CVE-2026-40215 — openssl-libs `< 3.0.7-28.el9_4` (fixed in 3.0.7-28.el9_4)
Issue stream scope: **2.2.x** (from summary suffix `[rhtpa-2.2]`)
Ecosystem: **RPM** (system package). Lock file: `rpms.lock.yaml`. SBOM verification: cosign available (`which cosign` → `/usr/bin/cosign`).

All dependency versions below come from the mock `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`
output in security-matrix-mock.md. SBOM results come from the mock SBOM comparison
supplied with the eval task. No commands were actually run.

## 2.1 — Supportability matrix loaded

| Stream | Konflux release repo | Versions | Format check |
|--------|----------------------|----------|--------------|
| 2.1.x | rhtpa-release.0.3.z | 2.1.0, 2.1.1 | Pass (Supportability Matrix, Source Pinning Method, Ecosystem Mappings, Forward Pointer present) |
| 2.2.x | rhtpa-release.0.4.z | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | Pass |

Matrix is stale (148 days, see data-extraction.md Step 0.3). Proceeding with the
current matrix as the eval assumes.

## 2.2 — Development stream

Unreleased Jira versions could not be queried (no Jira calls in this eval). The 2.2.x
matrix says "This is the latest stream — no forward pointer", and no other stream is
configured, so **no development stream was identified**. This needs engineer
confirmation. If an unreleased RHTPA version exists, its `rpms.lock.yaml` at branch
HEAD must be checked before the table is final.

## 2.3 / 2.4 — Version impact table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Stream | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | In scope? | Notes |
|---------|--------|------------|-------------------------------|-----------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 3.0.7-24.el9 | YES | No (cross-stream) | below fix threshold |
| 2.1.1 | 2.1.x | `v0.3.12` | 3.0.7-24.el9 | YES | No (cross-stream) | below fix threshold |
| 2.2.0 | 2.2.x | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | Yes | below fix threshold |
| 2.2.1 | 2.2.x | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | Yes | below fix threshold |
| 2.2.2 | 2.2.x | `v0.4.8` (build 0.4.9) | — | **YES** | Yes | retag of 2.2.1; result carried forward ("same as 2.2.1"), no lock file check |
| 2.2.3 | 2.2.x | `v0.4.11` | 3.0.7-28.el9_4 | NO | Yes | equals fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 3.0.7-28.el9_4 | NO | Yes | equals fixed version |
| dev | — | — | — | UNKNOWN | — | no development stream identified (see 2.2) |

Summary:
- **In-scope (2.2.x) affected:** 2.2.0, 2.2.1, 2.2.2
- **In-scope (2.2.x) not affected:** 2.2.3, 2.2.4. The fix (3.0.7-28.el9_4) shipped starting with 2.2.3.
- **Cross-stream affected (outside scope):** 2.1.0, 2.1.1. These go to Case A (cross-stream comment, plus a preemptive task if no sibling 2.1.x CVE Jira exists).

## 2.3.5 — Dependency chain context (with inline SBOM verification)

Only affected versions are traced. rpms.lock.yaml and SBOM signals are shown side by side.

### 2.2.0 (tag `v0.4.5`)

```
Dependency chain for openssl-libs (RPM) — RHTPA 2.2.0:
  rpms.lock.yaml: present (openssl-libs 3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  SBOM vs lock file: ⚠️ DISAGREE
  Dockerfile FROM: not available in eval data (git show <tag>:Dockerfile not run)
  Origin: UNRESOLVED — explicit install (lock file) vs base image (SBOM)
```

### 2.2.1 (tag `v0.4.8`)

```
Dependency chain for openssl-libs (RPM) — RHTPA 2.2.1:
  rpms.lock.yaml: present (openssl-libs 3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  SBOM vs lock file: ⚠️ DISAGREE
  Dockerfile FROM: not available in eval data
  Origin: UNRESOLVED — explicit install (lock file) vs base image (SBOM)
```

### 2.2.2 (retag of 2.2.1)

```
Dependency chain for openssl-libs (RPM) — RHTPA 2.2.2:
  same as 2.2.1 (retag; rpms.lock.yaml result carried forward: 3.0.7-27.el9_4 → explicit install)
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  SBOM vs lock file: ⚠️ DISAGREE
  Origin: UNRESOLVED — explicit install (lock file) vs base image (SBOM)
```

### Side-by-side summary

| Version | rpms.lock.yaml signal | Lock file classification | SBOM signal (final / base) | SBOM classification | Agreement |
|---------|-----------------------|--------------------------|----------------------------|---------------------|-----------|
| 2.2.0 | listed (3.0.7-25.el9_3) | explicit install | present / present | base image | ⚠️ DISAGREE |
| 2.2.1 | listed (3.0.7-27.el9_4) | explicit install | present / present | base image | ⚠️ DISAGREE |
| 2.2.2 | same as 2.2.1 | explicit install | present / present | base image | ⚠️ DISAGREE |

> ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says **explicit install**
> but SBOM comparison says **base image**, for RHTPA 2.2.0, 2.2.1 and 2.2.2. Investigate manually.

Interpretation for the engineer. The SBOM check supplements the lock file classification;
it does not replace it. One likely explanation: openssl-libs ships in the base image
(for example ubi9-minimal) **and** is also pinned in rpms.lock.yaml. In that case the
lock file entry decides the installed version, but bumping only rpms.lock.yaml may not
be enough if the base image layer still has the old build. Before creating the
remediation task, confirm the following:
1. Check `git show v0.4.5:Dockerfile` / `v0.4.8:Dockerfile` for the `FROM` reference and its pinning (tag or digest).
2. Check whether the openssl-libs build in the final image comes from the lock file install or the base image layer.
3. Decide the remediation path. Lock file bump only (explicit install), base image tag/digest update (base image), or both.

Origin did not change within the affected versions (all three show the same disagreement).
The fixed versions 2.2.3/2.2.4 were not traced because they are not affected.

Cross-stream (2.1.x, outside scope): rpms.lock.yaml lists openssl-libs 3.0.7-24.el9
(explicit install per lock file). No SBOM comparison data was supplied for 2.1.x, so
SBOM verification for 2.1.x is "not performed — no mock SBOM data provided".

## 2.5 — Upstream fix check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | n/a | n/a. Fix already ships in released 2.2.3 / 2.2.4 (3.0.7-28.el9_4) |

RPM has no upstream source branch. Remediation is a Konflux release repo change only
(rhtpa-release.0.4.z).

## Notes for Steps 3–8 (not executed; for engineer review)

- **Step 3 (Affects Versions):** PSIRT set `RHTPA 2.0.0`, which is not in any configured
  stream. Proposed correction for this 2.2.x-scoped issue: RHTPA 2.2.0, RHTPA 2.2.1,
  RHTPA 2.2.2. This needs confirmation and dynamic Jira version discovery.
- **Step 8:** scoped issue with other streams affected → Case A (cross-stream comment for
  2.1.x) + Case B. System package → **1 Konflux release repo task** for 2.2.x. The
  task's remediation path depends on resolving the SBOM/lock file disagreement above.
- The engineer must review and confirm this table before Step 3.
