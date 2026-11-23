# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

## 2.1 – Supportability matrix

Loaded both configured Version Streams (security-matrix mock). The format check passed: Supportability Matrix, Ecosystem Mappings, Source Pinning Method and Forward Pointer sections are all present, and the Ecosystem Mappings columns match the template.

- **2.1.x**: `rhtpa-release.0.3.z`, versions 2.1.0 and 2.1.1
- **2.2.x**: `rhtpa-release.0.4.z`, versions 2.2.0 to 2.2.4 (2.2.2 is a backend retag of 2.2.1)

Ecosystem used: **RPM**. Lock file `rpms.lock.yaml`, check command `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`. Because a lock file is configured, it is the source of truth and the SBOM fallback for presence is not needed.

## 2.2 – Development stream

Unreleased Jira versions could not be queried (no Jira calls in this eval). No unreleased-version data was supplied, and 2.2.x is the latest stream (no forward pointer). As a result, **no development-stream (branch HEAD) row is included**. In a live triage, `getJiraIssueTypeMetaWithFields` would identify the earliest unreleased `RHTPA` version, and `rpms.lock.yaml` would be checked at HEAD of its release repo.

## 2.3 – Extracted dependency versions (simulated `git show <tag>:rpms.lock.yaml` output)

Comparison uses RPM EVR ordering against the fix threshold `3.0.7-28.el9_4`. The version is the same (3.0.7), so the release field decides: 24 < 28, 25 < 28, 27 < 28, and 28 = 28 means fixed.

### Version impact table (issue scope: 2.2.x)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|-----------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | **YES** | same as 2.2.1 (retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | ships fixed version |

### Other streams (outside issue scope, used for Case A cross-stream check)

| Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|-----------|-------------------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | **YES** | out of scope (2.1.x) |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | **YES** | out of scope (2.1.x) |

**Summary:** within the 2.2.x scope, 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and later (the current latest, 2.2.4) already ship the fixed `openssl-libs-3.0.7-28.el9_4`. The fix entered the 2.2.x stream between `v0.4.8` and `v0.4.11`. Stream 2.1.x is also fully affected (3.0.7-24.el9) and is handled through Case A in Step 8.

## 2.3.5 – Dependency chain context

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present → explicit install
    2.2.0 (v0.4.5):  openssl-libs 3.0.7-25.el9_3
    2.2.1 (v0.4.8):  openssl-libs 3.0.7-27.el9_4
    2.2.2:           same as 2.2.1 (retag)
    2.2.3 (v0.4.11): openssl-libs 3.0.7-28.el9_4 (fixed)
    2.2.4 (v0.4.12): openssl-libs 3.0.7-28.el9_4 (fixed)
  SBOM verification: ⚠️ skipped — cosign not available / SBOM download failed.
    Using rpms.lock.yaml classification only.
    (Eval context: no external tools may run, so `which cosign` and
    `cosign download sbom` were not executed. The supportability matrix also
    has no Container Images section, so no image reference or digest exists
    to compare the final and base image SBOMs.)
  Origin: explicit install (openssl-libs is resolved in rpms.lock.yaml, from rpms.in.yaml)
  Introduction point: origin is the same (explicit install) in every 2.2.x and 2.1.x
    version checked. Only the pinned RPM release changes. The fixed build
    3.0.7-28.el9_4 first appears at v0.4.11 (2.2.3).

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml in the
Konflux release repo (rhtpa-release.0.4.z) so that openssl-libs >= 3.0.7-28.el9_4.
For 2.2.x this is already true from v0.4.11 onward. The remaining work is to
confirm that main/HEAD keeps >= 3.0.7-28.el9_4 and that any z-stream rebuild of
an affected version picks it up.
```

The Cargo-only dependency scope decision tree does not apply (RPM is a shipped runtime system package, not a dev or build dependency), so no `dev-dependency` label is needed.

## 2.5 – Upstream fix check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | n/a | n/a |

No Upstream Branch is configured for RPM, so there is no upstream source-repo fix check. RPM remediation is a Konflux release repo change only (1 task). The latest released pins (v0.4.11, v0.4.12) already contain the fixed RPM.

_Engineer confirmation of this table is required before Step 3 (simulated as confirmed for this eval)._
