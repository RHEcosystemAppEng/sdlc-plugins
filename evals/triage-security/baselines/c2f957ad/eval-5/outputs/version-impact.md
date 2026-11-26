# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

Source: `rpms.lock.yaml` at pinned tags from security-matrix.md (simulated
`git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` output from the mock data).
Comparison uses RPM EVR ordering against fix threshold `3.0.7-28.el9_4` (same upstream
version 3.0.7, so the release number decides: 24/25/27 < 28).

## Version Impact Table – stream 2.2.x (issue scope)

| Version | Build | Source tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 0.4.9 | `v0.4.8` | — | YES | same as 2.2.1 (backend retag of 2.2.1; lock check skipped) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | fixed version shipped |
| 2.2.4 | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | fixed version shipped |

## Cross-stream check – stream 2.1.x (outside issue scope)

All supported versions were checked (Important Rule 4):

| Version | Build | Source tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-------|------------|-------------------------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | YES | outside scope: cross-stream impact |
| 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | YES | outside scope: cross-stream impact |

## Development stream (Step 2.2)

The development stream is found from unreleased `RHTPA` Jira versions
(`getJiraIssueTypeMetaWithFields`). Jira is not called in this eval, and the mock data has no
unreleased version and no branch-HEAD rpms.lock.yaml data, so **the development stream was
not evaluated**. In a live run, check the dev stream's `rpms.lock.yaml` at branch HEAD
before finalizing. No dependency version is assumed.

## Dependency chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM) – stream 2.2.x:
  rpms.lock.yaml: present → explicit install
    v0.4.5  (2.2.0): openssl-libs-3.0.7-25.el9_3  (vulnerable)
    v0.4.8  (2.2.1, 2.2.2 retag): openssl-libs-3.0.7-27.el9_4  (vulnerable)
    v0.4.11 (2.2.3): openssl-libs-3.0.7-28.el9_4  (fixed)
    v0.4.12 (2.2.4): openssl-libs-3.0.7-28.el9_4  (fixed)
  SBOM verification: ⚠️ skipped — cosign not available (external tools such as
    `which cosign` / `cosign download sbom` are not permitted in this eval run, and
    the matrix has no Container Images section with image reference/digest to
    download an SBOM from). Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs pinned in rpms.lock.yaml / rpms.in.yaml)
  Introduction point: openssl-libs is in rpms.lock.yaml in every 2.1.x and 2.2.x tag,
    so its origin does not change between versions. The fix appears from v0.4.11 (2.2.3) on.

Remediation: update the openssl-libs package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4 in rhtpa-release.0.4.z. Current 2.2.x head (2.2.4, v0.4.12)
already ships 3.0.7-28.el9_4. Verify the main branch lock file and confirm
that no further 2.2.x z-stream build is planned from an older pinned lock.
```

Base image reference (Step 2.3.5 item 4): not applicable. The origin is explicit install,
not base image. The Dockerfile `FROM` line was not read (`git show` is not permitted in this eval).

## Upstream fix status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | n/a | n/a. Fix is in the Konflux release repo; latest released build 2.2.4 already ships 3.0.7-28.el9_4 |

RPM has no Upstream Branch configured, so no upstream source check applies. The remediation
path is a Konflux release repo change only.

## Summary

- In scope (2.2.x): **2.2.0, 2.2.1, 2.2.2 affected**; 2.2.3 and 2.2.4 not affected.
- Out of scope: 2.1.0 and 2.1.1 are affected (cross-stream impact, Step 8 Case A).
- Development stream: not determined (no Jira/branch-HEAD data available).
