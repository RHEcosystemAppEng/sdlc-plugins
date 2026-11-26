# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

## 2.1 – Supportability Matrix

Both configured streams were loaded from security-matrix.md (the eval mock). The format check passed: Supportability Matrix, Ecosystem Mappings, Source Pinning Method, and Forward Pointer are all present, and the Ecosystem Mappings columns match the template.

- 2.1.x (`rhtpa-release.0.3.z`): 2.1.0 (`v0.3.8`), 2.1.1 (`v0.3.12`)
- 2.2.x (`rhtpa-release.0.4.z`): 2.2.0 (`v0.4.5`), 2.2.1 (`v0.4.8`), 2.2.2 (build 0.4.9, retag of 2.2.1 / `v0.4.8`), 2.2.3 (`v0.4.11`), 2.2.4 (`v0.4.12`)

Staleness warning (Step 0.3): the matrix was last updated 2026-06-28, 151 days ago. Releases after 2.2.4 may be missing.

## 2.2 – Development Stream

Finding the development stream needs `getJiraIssueTypeMetaWithFields` (unreleased `RHTPA` versions), and Jira was not called in this eval. 2.2.x is the latest configured stream (it has no forward pointer). No development-stream branch HEAD was inspected, so no dev-stream row is shown. **Development stream: not determined (Jira metadata unavailable).** The latest released 2.2.x build (2.2.4, `v0.4.12`) already ships the fixed version.

## 2.3 – Lock File Extraction (rpms.lock.yaml at pinned tags)

Command per tag (simulated output from the mock lock data): `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'`

Comparison uses RPM version ordering against the threshold `3.0.7-28.el9_4`. Every build has the same upstream version, 3.0.7, so the result depends on the release number (24/25/27 < 28).

## 2.4 – Version Impact Table

```
Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):
```

### Stream 2.2.x (in scope: issue suffix [rhtpa-2.2])

| Version | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|-------------------------------|-----------|-------|
| 2.2.0 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | |
| 2.2.1 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | |
| 2.2.2 | `v0.4.9` → `v0.4.8` | — | **YES** | same as 2.2.1 (retag of 2.2.1; lock check skipped, result carried forward) |
| 2.2.3 | `v0.4.11` | 3.0.7-28.el9_4 | NO | ships the fixed version |
| 2.2.4 | `v0.4.12` | 3.0.7-28.el9_4 | NO | ships the fixed version |

### Stream 2.1.x (out of scope: cross-stream impact)

| Version | Tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|---------|-----|-------------------------------|-----------|-------|
| 2.1.0 | `v0.3.8` | 3.0.7-24.el9 | **YES** | outside issue scope, so Case A cross-stream |
| 2.1.1 | `v0.3.12` | 3.0.7-24.el9 | **YES** | outside issue scope, so Case A cross-stream |

**Summary:** In scope (2.2.x), 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship openssl-libs 3.0.7-28.el9_4. Out of scope, every 2.1.x release (2.1.0 and 2.1.1) is affected.

## 2.3.5 – Dependency Chain Context

```
Dependency chain for openssl-libs (RPM), stream 2.2.x:
  rpms.lock.yaml: present at v0.4.5 (3.0.7-25.el9_3), v0.4.8 (3.0.7-27.el9_4),
                  v0.4.11 (3.0.7-28.el9_4), v0.4.12 (3.0.7-28.el9_4) → explicit install
  SBOM verification: ⚠️ skipped — cosign not available (cosign/`which cosign` not executed
                     in this eval; no external tools permitted) and the supportability matrix
                     has no Container Images section with image reference/digest needed for
                     `cosign download sbom <image-reference>@<image-digest>`.
                     Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs is resolved in rpms.lock.yaml / rpms.in.yaml of
          the Konflux release repo rhtpa-release.0.4.z)
  Introduction point: present in all 2.2.x releases; version moved 3.0.7-25.el9_3 (2.2.0)
          → 3.0.7-27.el9_4 (2.2.1) → 3.0.7-28.el9_4 (2.2.3, fixed). The fix first shipped in
          2.2.3 (v0.4.11).

Remediation: update the openssl-libs package spec in rpms.in.yaml / regenerate
rpms.lock.yaml in rhtpa-release.0.4.z so the build resolves openssl-libs >= 3.0.7-28.el9_4.
Note that the latest pinned release (v0.4.12) already resolves 3.0.7-28.el9_4. Confirm that
the Konflux repo main branch still pins >= 3.0.7-28.el9_4 and that no affected 2.2.x build
needs a respin.
```

```
Dependency chain for openssl-libs (RPM), stream 2.1.x (cross-stream context):
  rpms.lock.yaml: present at v0.3.8 and v0.3.12 (3.0.7-24.el9) → explicit install
  SBOM verification: ⚠️ skipped — cosign not available / no image reference+digest in matrix.
                     Using rpms.lock.yaml classification only.
  Origin: explicit install (rpms.lock.yaml in rhtpa-release.0.3.z)
  Fix not shipped in any 2.1.x release.
```

The Dockerfile `FROM` reference was not inspected because the origin is explicit install, not base image, and no `git show` calls are allowed in this eval.

## 2.5 – Upstream Fix Check

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (none configured) | n/a | n/a: fix is applied in the Konflux release repo. The latest released pin `v0.4.12` already ships 3.0.7-28.el9_4. |
| 2.1.x | RPM | — (none configured) | n/a | n/a: Konflux repo fix needed. Every 2.1.x pin ships 3.0.7-24.el9. |

RPM has no Upstream Branch configured, so no upstream source repo check applies. Remediation goes directly into the Konflux release repo (1 task per stream).
