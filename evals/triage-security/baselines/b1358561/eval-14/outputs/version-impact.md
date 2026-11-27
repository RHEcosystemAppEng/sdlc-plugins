# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Issue: TC-8005 — scoped to stream **2.2.x** (summary suffix `[rhtpa-2.2]`).
Fix threshold: 3.0.7-28.el9_4 (Jira description; external enrichment unavailable).

## 2.1 – Supportability Matrix

- Stream: 2.2.x — Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z` (mock `security-matrix-mock.md`, Stream 2).
- Stream 2.1.x (`rhtpa-release.0.3.z`) is **out of scope** for this stream-scoped issue and was not analyzed.
- Staleness (Step 0.3): matrix `Last-Updated` 2026-06-28 — 152 days old; WARNING raised, proceeding with current matrix.

### 2.1.1 – Matrix format validation (2.2.x)

| Check | Result |
|-------|--------|
| `## Supportability Matrix` | Present |
| `## Ecosystem Mappings` | Present |
| `### Source Pinning Method` | Present |
| `## Forward Pointer` | Present ("This is the latest stream — no forward pointer.") |
| Ecosystem Mappings columns | `Ecosystem | Repository | Lock File | Check Command | Upstream Branch` — match |
| Table parsability | Both tables parsable |
| Result | **Pass** |

Observation: the matrix has no Container Images section (no image references / digests). This limits the cosign SBOM step (see 2.3.5) — image references/digests would need to be supplied for a real `cosign download sbom` call.

## 2.2 – Development Stream

Not determined: Jira unreleased-version lookup (`getJiraIssueTypeMetaWithFields`) was not performed (no Jira calls in this eval). 2.2.x is the latest configured stream (no forward pointer). No development-head row is included in the table below.

## 2.3 – Dependency Versions (rpms.lock.yaml)

Simulated output of `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` (Check Command from the 2.2.x RPM Ecosystem Mapping), using the mock lock data.

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | vs. 3.0.7-28.el9_4 |
|---------|-------|-----------|-------------------------------|--------------------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | older → vulnerable |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | older → vulnerable |
| 2.2.2 | 0.4.9 | `v0.4.8` (retag) | — (retag; carried forward from 2.2.1) | same as 2.2.1 |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | equal to fix → fixed |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | equal to fix → fixed |

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4), stream 2.2.x:

| Version | openssl-libs    | Affected? | Notes                                   |
|---------|-----------------|-----------|-----------------------------------------|
| 2.2.0   | 3.0.7-25.el9_3  | YES       |                                         |
| 2.2.1   | 3.0.7-27.el9_4  | YES       |                                         |
| 2.2.2   | —               | YES       | retag of 2.2.1 — same as 2.2.1          |
| 2.2.3   | 3.0.7-28.el9_4  | NO        | ships fixed version                     |
| 2.2.4   | 3.0.7-28.el9_4  | NO        | ships fixed version                     |
```

Out of scope (not analyzed): 2.1.0, 2.1.1 (stream 2.1.x).

**Summary:** affected versions in scope = **2.2.0, 2.2.1, 2.2.2**. Fixed since **2.2.3** (openssl-libs 3.0.7-28.el9_4 picked up). The PSIRT-assigned Affects Versions (RHTPA 2.0.0) is incorrect — proposed correction for Step 3: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (subject to Jira version availability and engineer confirmation).

## 2.3.5 – Dependency Chain Context (affected versions, with inline SBOM verification)

SBOM verification pre-check: `which cosign` → `/usr/bin/cosign` (available). SBOM comparison results below are the mock results supplied for this eval (final image SBOM vs base image SBOM).

### 2.2.0 (tag `v0.4.5`)

```
Dependency chain for openssl-libs (RPM) — 2.2.0:
  rpms.lock.yaml: present (openssl-libs-3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install but SBOM comparison says base image. Investigate manually.
  Dockerfile: FROM reference not available in eval inputs (would be read via git show v0.4.5:Dockerfile | grep -i '^FROM')
  Origin: UNRESOLVED — lock file = explicit install, SBOM = base image (conflict)
  Pinning: unknown (Dockerfile not inspected)
```

### 2.2.1 (tag `v0.4.8`)

```
Dependency chain for openssl-libs (RPM) — 2.2.1:
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install but SBOM comparison says base image. Investigate manually.
  Dockerfile: FROM reference not available in eval inputs (would be read via git show v0.4.8:Dockerfile | grep -i '^FROM')
  Origin: UNRESOLVED — lock file = explicit install, SBOM = base image (conflict)
  Pinning: unknown (Dockerfile not inspected)
```

### 2.2.2 (retag of 2.2.1 — same as 2.2.1)

```
Dependency chain for openssl-libs (RPM) — 2.2.2:
  rpms.lock.yaml: same as 2.2.1 (retag) — present (openssl-libs-3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install but SBOM comparison says base image. Investigate manually.
  Origin: UNRESOLVED — lock file = explicit install, SBOM = base image (conflict)
```

### Side-by-side classification signals

| Version | rpms.lock.yaml signal | SBOM signal (final vs base) | Agreement |
|---------|-----------------------|-----------------------------|-----------|
| 2.2.0 | present → explicit install | in both SBOMs → base image | ⚠️ DISAGREE |
| 2.2.1 | present → explicit install | in both SBOMs → base image | ⚠️ DISAGREE |
| 2.2.2 | same as 2.2.1 → explicit install | in both SBOMs → base image | ⚠️ DISAGREE |

**Interpretation / remediation context:** Per the skill, the rpms.lock.yaml classification is primary and SBOM verification supplements but does not replace it — so the working classification is **explicit install**, with the discrepancy flagged for manual investigation. A plausible explanation is that openssl-libs is both shipped in the base image and explicitly pinned in rpms.lock.yaml (e.g., to force an update over the base image version). Remediation therefore likely requires updating the openssl-libs spec in rpms.in.yaml / rpms.lock.yaml to >= 3.0.7-28.el9_4, and the engineer should also verify whether the base image (`FROM`) carries the vulnerable version, which may require a base image tag/digest bump as well. Note that 2.2.3+ already ship 3.0.7-28.el9_4 via rpms.lock.yaml, confirming the lock-file update path is effective.

Introduction point: openssl-libs is present in rpms.lock.yaml in every 2.2.x version; no origin change observed within the stream (lock file signal). Fix introduced at 2.2.3 (tag `v0.4.11`).

## 2.5 – Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | N/A | N/A — RPM fix is a Konflux release repo change |

RPM is a system-package ecosystem: remediation is 1 task per affected stream — a Konflux release repo (`rhtpa-release.0.4.z`) fix. The latest released 2.2.x version (2.2.4) already ships the fixed openssl-libs, so the next 2.2.x build from the current release repo state is expected to carry the fix; the remaining question for Step 8 is whether any further remediation is required for the affected released versions versus closing/marking as fixed in 2.2.3.

Awaiting engineer review and confirmation of this table (and resolution of the SBOM vs rpms.lock.yaml discrepancy) before proceeding to Step 3.
