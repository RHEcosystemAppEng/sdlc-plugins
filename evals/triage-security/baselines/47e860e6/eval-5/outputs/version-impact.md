# Step 2 – Version Impact Analysis: CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

## 2.1 – Supportability Matrix

- Loaded both streams from the Version Streams table: 2.1.x (`rhtpa-release.0.3.z`) and 2.2.x (`rhtpa-release.0.4.z`). The data comes from `security-matrix-mock.md`.
- **2.1.1 Format validation: Pass.** Both streams have Supportability Matrix, Source Pinning Method, Ecosystem Mappings and Forward Pointer. The Ecosystem Mappings columns are `Ecosystem | Repository | Lock File | Check Command | Upstream Branch`.
- Staleness warning carried over from Step 0.3: the matrix is 129 days old (Last-Updated 2026-06-28). Releases after 2.2.4 may be missing.

## 2.2 – Development Stream

- To find the development stream, the skill needs `getJiraIssueTypeMetaWithFields` to list unreleased `RHTPA` versions. **No Jira call was made in this eval, so no development stream could be identified.** 2.2.x is the latest stream (no forward pointer).
- No branch-HEAD check was done. In a live run, if an unreleased version maps to a stream, the skill checks that stream's `rpms.lock.yaml` at HEAD of `main` in the Konflux release repo.

## 2.3 – Dependency Versions (rpms.lock.yaml at pinned tags)

Command per version: `git show <tag>:rpms.lock.yaml | grep 'openssl-libs'` (simulated output from the mock lock-file data).

How the RPM comparison works: version `3.0.7` is the same everywhere, so the release field decides. Releases `24`, `25` and `27` are below `28`, so those builds are affected. Release `28.el9_4` equals the fixed release, so it is not affected.

### Version Impact Table

| Stream | Version | Build | Pinned tag | openssl-libs (rpms.lock.yaml) | Affected? | Notes |
|--------|---------|-------|------------|-------------------------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 3.0.7-24.el9 | YES | Out of issue scope (cross-stream) |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 3.0.7-24.el9 | YES | Out of issue scope (cross-stream) |
| **2.2.x** | **2.2.0** | 0.4.5 | `v0.4.5` | 3.0.7-25.el9_3 | **YES** | In scope |
| **2.2.x** | **2.2.1** | 0.4.8 | `v0.4.8` | 3.0.7-27.el9_4 | **YES** | In scope |
| **2.2.x** | **2.2.2** | 0.4.9 | `v0.4.9` | — | **YES** | Retag: same as 2.2.1 (lock file check skipped, result carried forward) |
| **2.2.x** | **2.2.3** | 0.4.11 | `v0.4.11` | 3.0.7-28.el9_4 | NO | Ships fixed version |
| **2.2.x** | **2.2.4** | 0.4.12 | `v0.4.12` | 3.0.7-28.el9_4 | NO | Ships fixed version (latest released) |
| — | dev | — | HEAD | not checked | unknown | Dev stream not identified (no Jira access) |

**Summary (issue scope 2.2.x):** 2.2.0, 2.2.1 and 2.2.2 are affected. 2.2.3 and 2.2.4 already ship `openssl-libs-3.0.7-28.el9_4`. The fix entered the stream between builds 0.4.9 and 0.4.11.

**Cross-stream:** both 2.1.x versions (2.1.0 and 2.1.1) ship 3.0.7-24.el9 and are affected. That stream is outside TC-8005's scope, so Step 8 Case A applies.

## 2.3.5 – Dependency Chain Context

```
Dependency chain for openssl-libs (RPM), stream 2.2.x:
  rpms.lock.yaml: present at v0.4.5 (3.0.7-25.el9_3), v0.4.8 (3.0.7-27.el9_4),
                  v0.4.11 / v0.4.12 (3.0.7-28.el9_4) → explicit install
  SBOM verification: ⚠️ skipped — cosign not available (cosign/`which cosign` not
                  run in this eval and no external registry access permitted;
                  no image reference/digest in the matrix). Using rpms.lock.yaml
                  classification only.
  Origin: explicit install (openssl-libs pinned in rpms.lock.yaml / rpms.in.yaml
          of rhtpa-release.0.4.z)
  Introduction point: present in every 2.2.x build. Fixed release
          3.0.7-28.el9_4 first appears at v0.4.11 (2.2.3).

Dependency chain for openssl-libs (RPM), stream 2.1.x (cross-stream):
  rpms.lock.yaml: present at v0.3.8 / v0.3.12 (3.0.7-24.el9) → explicit install
  SBOM verification: ⚠️ skipped — cosign not available. Using rpms.lock.yaml
          classification only.
  Origin: explicit install

Remediation: update the openssl-libs package spec in rpms.in.yaml /
rpms.lock.yaml of the Konflux release repo to >= 3.0.7-28.el9_4.
```

Notes:
- Step 2.3.5 sub-step 3 (SBOM comparison) is optional, but its status line is mandatory. It was **skipped**, so classification relies only on the lock file. Being in the lock file means explicit install. The Dockerfile `FROM` line was not inspected. It is not needed for the explicit-install path.
- No dev/build-only scope applies to RPMs. The package is shipped in the runtime image, so production risk applies.

## 2.5 – Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | RPM | — (not configured) | n/a | n/a: the latest released build 2.2.4 (`v0.4.12`) already ships 3.0.7-28.el9_4 |
| 2.1.x | RPM | — (not configured) | n/a | n/a: latest released build 2.1.1 ships 3.0.7-24.el9 (vulnerable) |

RPM is a system package ecosystem with no upstream source branch. The fix happens directly in the Konflux release repo.

_The engineer would review and confirm this table before Step 3._
