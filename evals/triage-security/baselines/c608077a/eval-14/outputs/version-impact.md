# Step 2 – Version Impact Analysis: TC-8005

CVE-2026-40215, openssl-libs (RPM), affected `< 3.0.7-28.el9_4`, fixed `3.0.7-28.el9_4`.
Scope: **2.2.x stream only** (`rhtpa-release.0.4.z`), from the `[rhtpa-2.2]` suffix.

Data sources (simulated – no real git/cosign/Jira calls were made):
- Supportability matrix: Stream 2 (`rhtpa-release.0.4.z`) in `security-matrix-mock.md`
- `rpms.lock.yaml` versions: "openssl-libs versions by tag" mock data
  (`git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`)
- SBOM comparison: mock results from the task prompt (`which cosign` → `/usr/bin/cosign`)

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | below fix threshold |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | below fix threshold |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | retag of 2.2.1 – same as 2.2.1 (3.0.7-27.el9_4) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |

**Summary**: 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and later already ship the fixed
openssl-libs (3.0.7-28.el9_4). The latest released 2.2.x version (2.2.4) is not affected.

Out of scope: the 2.1.x stream (`rhtpa-release.0.3.z`, openssl-libs 3.0.7-24.el9) is
not part of this issue's `[rhtpa-2.2]` scope and was not analyzed. Cross-stream impact
can be looked at separately in Step 7.5 Case A if needed.

Development stream (Step 2.2): there is no Jira unreleased-version data, and the matrix
says 2.2.x is the latest stream with no forward pointer, so no development-head row
could be added. In a live run, query unreleased RHTPA versions and check
`rpms.lock.yaml` at branch HEAD.

## Dependency chain context (Step 2.3.5) – with SBOM verification

### 2.2.0 (`v0.4.5`)

```
Dependency chain for openssl-libs (RPM) – 2.2.0:
  rpms.lock.yaml: present (openssl-libs-3.0.7-25.el9_3) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml (lock file is the primary classification);
          SBOM says the package is also in the base (FROM) image
  Dockerfile FROM: not resolved (no simulated Dockerfile data) – run
          `git show v0.4.5:Dockerfile | grep -i '^FROM'` to record the image ref and pinning
```

### 2.2.1 (`v0.4.8`)

```
Dependency chain for openssl-libs (RPM) – 2.2.1:
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml; SBOM says it is also in the base image
  Dockerfile FROM: not resolved (no simulated Dockerfile data)
```

### 2.2.2 (retag of 2.2.1, `v0.4.8`)

```
Dependency chain for openssl-libs (RPM) – 2.2.2 (same as 2.2.1):
  rpms.lock.yaml: present (openssl-libs-3.0.7-27.el9_4, carried forward from 2.2.1) → explicit install
  SBOM verification: present in BOTH final image SBOM and base image SBOM → base image
  ⚠️ SBOM classification disagrees with rpms.lock.yaml — lock file says explicit install
     but SBOM comparison says base image. Investigate manually.
  Origin: explicit install per rpms.lock.yaml; SBOM says it is also in the base image
```

### Summary of signals

| Version | rpms.lock.yaml signal | SBOM signal (final vs base) | Agreement |
|---------|-----------------------|-----------------------------|-----------|
| 2.2.0 | in lock file → explicit install | in both SBOMs → base image | ⚠️ DISAGREE |
| 2.2.1 | in lock file → explicit install | in both SBOMs → base image | ⚠️ DISAGREE |
| 2.2.2 | same as 2.2.1 → explicit install | in both SBOMs → base image | ⚠️ DISAGREE |
| 2.2.3 | not affected – chain not traced | — | — |
| 2.2.4 | not affected – chain not traced | — | — |

Introduction point: openssl-libs is in `rpms.lock.yaml` for every 2.2.x tag, and the
origin signals do not change across the affected versions. The package was bumped to
the fixed 3.0.7-28.el9_4 in `v0.4.11` (2.2.3).

### Interpretation and remediation implications

- The rpms.lock.yaml classification (explicit install) is the primary signal. SBOM
  verification only supplements it and does not replace it. This disagreement is
  flagged for the engineer to investigate manually.
- The likely explanation is that openssl-libs is both shipped in the base image and
  pinned again in `rpms.in.yaml`/`rpms.lock.yaml` (an explicit pin of a package the base
  image already has). If so, a full fix may need **both** changes: bump the
  `rpms.lock.yaml` entry to >= 3.0.7-28.el9_4 **and** make sure the base image layer
  does not keep a vulnerable copy (update the FROM tag/digest if needed).
- Ecosystem category: System package (RPM) → 1 remediation task per stream (Konflux
  release repo `rhtpa-release.0.4.z`). The 2.2.x stream already ships the fix from 2.2.3
  onward, so remediation for the affected versions is satisfied by the current release
  line. Handling of the older z-stream releases is decided in Steps 3–8.

## Upstream fix check (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | N/A | N/A – RPM fix lives in the Konflux release repo; latest released tag `v0.4.12` has 3.0.7-28.el9_4 (fixed) |

---
Waiting for the engineer to review and confirm this table before Step 3. Planned
Step 3 correction: Affects Versions `RHTPA 2.0.0` → `RHTPA 2.2.0`, `RHTPA 2.2.1`,
`RHTPA 2.2.2`.
