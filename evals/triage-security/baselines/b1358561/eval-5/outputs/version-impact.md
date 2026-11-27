# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Evidence source: the simulated output of `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`, taken from the mock lock file data in `security-matrix-mock.md`. The lock file is `rpms.lock.yaml` (RPM row in the Ecosystem Mappings table of both streams), so the lock file is the source of truth and the SBOM fallback (2.3 item 3) does not apply.

Issue stream scope: **2.2.x** (from the `[rhtpa-2.2]` suffix). Per Important Rule 4, all supported versions were checked. 2.1.x is shown for cross-stream impact only.

## 2.1 – Matrix load and format validation

- Both stream matrices loaded. They contain Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer sections, and the Ecosystem Mappings columns match `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`. Result: **Pass**.
- Staleness: Last-Updated is 2026-06-28 (152 days old). The engineer chose to proceed anyway, so releases after 2.2.4 may be missing.

## 2.2 – Development stream

Not determinable: it needs `getJiraIssueTypeMetaWithFields` (unreleased RHTPA versions), and Jira was not called. 2.2.x is the latest configured stream (no forward pointer). Konflux repo branch HEAD was not checked. **Development stream: unknown, needs engineer confirmation.**

## 2.4 – Version impact table

### In scope: 2.2.x stream (rhtpa-release.0.4.z)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | release 25 < 28 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | release 27 < 28 |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (retag of 2.2.1; check skipped, result carried forward) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |
| dev | — | HEAD | not checked | unknown | Step 2.2 could not run without Jira |

### Out of scope (cross-stream impact): 2.1.x stream (rhtpa-release.0.3.z)

| Version | Build | Tag | openssl-libs | Affected? | Notes |
|---------|-------|-----|--------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | **YES** | release 24 < 28 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | **YES** | release 24 < 28 |

Summary: in the 2.2.x stream, **2.2.0, 2.2.1 and 2.2.2 are affected**. 2.2.3 and 2.2.4 already ship the fixed 3.0.7-28.el9_4. The 2.1.x stream (2.1.0, 2.1.1) is also affected, which triggers Case A cross-stream handling.

Retag caveat: the matrix marks 2.2.2 as a "backend retag of 2.2.1", and the mock data lists `v0.4.9` as a retag of `v0.4.8`. `rpms.lock.yaml` lives in the Konflux release repo, not the backend repo, so the engineer should confirm that build 0.4.9's `rpms.lock.yaml` was not changed independently. Until then, 2.2.2 carries forward YES.

## 2.3.5 – Dependency chain context

```
Dependency chain for openssl-libs (RPM), stream 2.2.x:
  rpms.lock.yaml: present at v0.4.5 (3.0.7-25.el9_3), v0.4.8 (3.0.7-27.el9_4),
                  v0.4.11 / v0.4.12 (3.0.7-28.el9_4) → explicit install
  SBOM verification: ⚠️ skipped (cosign not run / unavailable in this eval environment
                     (no external tools permitted), and the matrix has no image
                     reference@digest (no Container Images section) to download an SBOM from).
                     Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs pinned in rpms.lock.yaml / rpms.in.yaml of
          rhtpa-release.0.4.z)
  Dockerfile FROM / base image: not inspected (no git show permitted). Not needed for
          explicit-install origin
  Introduction point: present in every 2.2.x version. Fixed version first appears at
          2.2.3 (v0.4.11)

Dependency chain for openssl-libs (RPM), stream 2.1.x (cross-stream):
  rpms.lock.yaml: present at v0.3.8 / v0.3.12 (3.0.7-24.el9) → explicit install
  SBOM verification: ⚠️ skipped (cosign not available). Using rpms.lock.yaml classification only.
  Origin: explicit install (rhtpa-release.0.3.z)

Remediation: update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml
of the Konflux release repo to >= 3.0.7-28.el9_4 (already done on 2.2.x as of v0.4.11).
```

Direct vs transitive and dev-dependency scope do not apply to RPM. The package ships in the production image.

## 2.5 – Upstream fix check

The RPM Ecosystem Mappings row has no Upstream Branch (`—`) and no source repository. The fix lives directly in the Konflux release repo, so no upstream check applies. In 2.2.x, the Konflux repo already pins the fixed 3.0.7-28.el9_4 from v0.4.11 onward. Whether `main` HEAD still pins at least that version was not verified (no `git show`).

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (Konflux repo) | not checked; latest release v0.4.12 = 3.0.7-28.el9_4 | YES (as of 2.2.3) |
| 2.1.x | RPM | — (Konflux repo) | not checked; latest release v0.3.12 = 3.0.7-24.el9 | NO |
