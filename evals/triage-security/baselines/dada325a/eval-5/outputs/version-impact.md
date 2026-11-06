# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Data source: `rpms.lock.yaml` at each pinned tag from the supportability matrix. The simulated output of `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` comes from `security-matrix-mock.md`. No real `git show` was run.

## 2.1 – Supportability Matrix (aggregated)

Both streams loaded from the mock matrix. Format check: the required sections (Supportability Matrix, Ecosystem Mappings, Source Pinning Method, Forward Pointer) are present and the tables parse. **Pass.**
Staleness warning (Step 0.3): matrix `Last-Updated` is 2026-06-28, which is 131 days old.

## 2.2 – Development Stream

No unreleased-version data is available, because the Jira `getJiraIssueTypeMetaWithFields` call is not permitted in this eval. 2.2.x is the latest stream (no forward pointer), and no mock lock data exists for a development branch HEAD. **The development stream state cannot be determined.** It is not reported as affected or unaffected, and needs engineer confirmation.

## 2.3 / 2.4 – Version Impact Table

Comparison is RPM EVR ordering against the fix `3.0.7-28.el9_4`.

### In scope: stream 2.2.x (issue scope `[rhtpa-2.2]`)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | release 25 < 28 |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | release 27 < 28 |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (backend retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | equals fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | equals fixed version |

### Out of scope: stream 2.1.x (reported for Case A cross-stream impact)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | **YES** | release 24 < 28 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | **YES** | release 24 < 28 |

### Summary

- **2.2.x:** 2.2.0, 2.2.1, and 2.2.2 are affected. The fix first shipped in **2.2.3** (build 0.4.11, 2026-03-23) and is still present in 2.2.4. The latest released 2.2.x version is not vulnerable.
- **2.1.x:** every released version (2.1.0 and 2.1.1) is affected, and no 2.1.x release ships the fix. This is outside TC-8005's scope and triggers Case A.
- **Development stream:** undetermined (see 2.2).

## 2.3.5 – Dependency Chain Context

```
Dependency chain for openssl-libs (RPM) — stream 2.2.x:
  rpms.lock.yaml: present → explicit install
    v0.4.5  (2.2.0): openssl-libs 3.0.7-25.el9_3
    v0.4.8  (2.2.1, 2.2.2): openssl-libs 3.0.7-27.el9_4
    v0.4.11 (2.2.3): openssl-libs 3.0.7-28.el9_4 (fixed)
    v0.4.12 (2.2.4): openssl-libs 3.0.7-28.el9_4 (fixed)
  SBOM verification: ⚠️ skipped — cosign not available (no external tools / registry access permitted in this run; `which cosign` and `cosign download sbom` were not executed). Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs pinned in rpms.lock.yaml / rpms.in.yaml of rhtpa-release.0.4.z)
  Introduction point: present in every 2.2.x release; origin unchanged across versions
                      (explicit install in all tags). Fix landed between v0.4.8 and v0.4.11.

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml to
openssl-libs >= 3.0.7-28.el9_4 (already done for 2.2.3+; verify current main).
```

```
Dependency chain for openssl-libs (RPM) — stream 2.1.x (cross-stream, out of scope):
  rpms.lock.yaml: present → explicit install
    v0.3.8  (2.1.0): openssl-libs 3.0.7-24.el9
    v0.3.12 (2.1.1): openssl-libs 3.0.7-24.el9
  SBOM verification: ⚠️ skipped — cosign not available. Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs pinned in rpms.lock.yaml of rhtpa-release.0.3.z)

Remediation: update rpms.in.yaml / rpms.lock.yaml to openssl-libs >= 3.0.7-28.el9_4
(or the equivalent el9 errata build for the 2.1.x base) in rhtpa-release.0.3.z.
```

The package is in the lock file in every tag, so it is classified as an explicit install and the base image `FROM` reference is not needed for remediation. The Dockerfile was not inspected because no `git show` is allowed.

## 2.5 – Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | n/a | n/a. RPM fixes happen in the Konflux release repo. The latest pinned release (`v0.4.12`) already ships 3.0.7-28.el9_4. |
| 2.1.x | RPM | — (not configured) | n/a | n/a. No 2.1.x release ships the fix. |

The RPM ecosystem has no Upstream Branch configured, so no upstream check applies. Remediation goes directly into the Konflux release repo.
